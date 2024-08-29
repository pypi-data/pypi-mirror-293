from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Any, Callable, Literal, TypedDict, cast

import pandas as pd
from typing_extensions import Self

from .errors import MorphFunctionLoadError, MorphFunctionLoadErrorCategory
from .inspection import (
    DirectoryScanResult,
    _import_python_file,
    _import_python_sql_files,
    _import_sql_file,
    get_checksum,
)


class MorphFunctionMetaObject(TypedDict, total=False):
    id: str
    name: str
    function: Callable[..., Any]
    description: str
    arguments: list[str]
    data_requirements: list[str]
    output_paths: list[str]
    output_type: Literal["dataframe", "visualization", "document", "json"]
    connection: str


class MorphFunctionMetaObjectCacheItem(TypedDict):
    spec: MorphFunctionMetaObject
    file_path: str
    checksum: str


class MorphFunctionMetaObjectCache(TypedDict):
    directory: str
    directory_checksum: str
    items: list[MorphFunctionMetaObjectCacheItem]
    errors: list[MorphFunctionLoadError]


def _cache_path(directory: str) -> str:
    return f"{directory}/.morph/meta.json"


def load_cache(project_root: str) -> MorphFunctionMetaObjectCache | None:
    cache_path = _cache_path(project_root)
    if not Path(cache_path).exists():
        return None

    with open(cache_path, "r") as f:
        data = json.load(f)

    return cast(MorphFunctionMetaObjectCache, data)


def dump_cache(cache: MorphFunctionMetaObjectCache) -> None:
    cache_path = _cache_path(cache["directory"])
    if not Path(cache_path).parent.exists():
        Path(cache_path).parent.mkdir(parents=True)

    with open(cache_path, "w") as f:
        json.dump(cache, f, indent=2)


class MorphGlobalContext:
    __data: dict[str, pd.DataFrame]
    __var: dict[str, Any]
    __meta_objects: list[MorphFunctionMetaObject]
    __scans: list[DirectoryScanResult]

    def __init__(self):
        self.__data = {}
        self.__var = {}
        self.__meta_objects = []
        self.__scans = []

    @classmethod
    def get_instance(cls) -> Self:
        if not hasattr(cls, "_instance"):
            cls._instance = cls()  # type: ignore
        return cls._instance  # type: ignore

    @property
    def data(self) -> dict[str, pd.DataFrame]:
        return self.__data

    @property
    def var(self) -> dict[str, Any]:
        return self.__var

    def load(self, directory: str) -> list[MorphFunctionLoadError]:
        result = _import_python_sql_files(directory)
        for key, value in result["sql_contexts"].items():
            self._update_meta_object(key, value)

        entirety_errors = self._check_entirety_errors()
        result["errors"] += entirety_errors
        self.__scans.append(result)
        return result["errors"]

    def partial_load(
        self, directory: str, target_name: str
    ) -> list[MorphFunctionLoadError]:
        """load required using cache.
        This function is meant to be used in runtime, where all the necessary analysis functions are already loaded
        except loading actual functions.
        """
        cache = load_cache(directory)
        if cache is None:
            errors = self.load(directory)
            if len(errors) == 0:
                self.dump()

            return errors

        directory_checksum = get_checksum(Path(directory))
        if cache["directory_checksum"] != directory_checksum:
            errors = self.load(directory)
            if len(errors) == 0:
                self.dump()

            return errors

        return self._partial_load(target_name, cache)

    def _partial_load(
        self, target_name: str, cache: MorphFunctionMetaObjectCache
    ) -> list[MorphFunctionLoadError]:
        target_item: MorphFunctionMetaObjectCacheItem | None = None
        for item in cache["items"]:
            if item["spec"]["name"] == target_name or item["spec"]["id"].startswith(
                target_name
            ):
                target_item = item
                break
        if target_item is None:
            return [
                {
                    "category": MorphFunctionLoadErrorCategory.IMPORT_ERROR,
                    "file_path": "",
                    "name": target_name,
                    "error": "Not found",
                }
            ]

        suffix = target_item["file_path"].split(".")[-1]
        if suffix == "py":
            _, error = _import_python_file(target_item["file_path"])
        elif suffix == "sql":
            _, context, error = _import_sql_file(target_item["file_path"])
            for key, value in context.items():
                self._update_meta_object(key, value)
        else:
            return [
                {
                    "category": MorphFunctionLoadErrorCategory.IMPORT_ERROR,
                    "file_path": target_item["file_path"],
                    "name": target_name,
                    "error": "Unknown file type",
                }
            ]

        errors = []
        if error is not None:
            errors.append(error)

        requirements = target_item["spec"].get("data_requirements", [])
        for requirement in requirements:
            errors += self._partial_load(requirement, cache)

        return errors

    def dump(self) -> MorphFunctionMetaObjectCache:
        if len(self.__scans) == 0:
            raise ValueError("No files are loaded.")

        scan = self.__scans[-1]
        cache_items: list[MorphFunctionMetaObjectCacheItem] = []
        for scan_item in scan["items"]:
            for obj in self.__meta_objects:
                # id is formatted as {filename}:{function_name}
                obj_filepath = obj["id"].split(":")[0]
                if scan_item["file_path"] == obj_filepath:
                    cache_obj = copy.deepcopy(obj)
                    if "function" in cache_obj:
                        del cache_obj["function"]
                    item: MorphFunctionMetaObjectCacheItem = {
                        "spec": cache_obj,
                        "file_path": scan_item["file_path"],
                        "checksum": scan_item["checksum"],
                    }
                    cache_items.append(item)

        cache: MorphFunctionMetaObjectCache = {
            "directory": scan["directory"],
            "directory_checksum": scan["directory_checksum"],
            "items": cache_items,
            "errors": scan["errors"],
        }
        dump_cache(cache)
        return cache

    def _add_data(self, key: str, value: pd.DataFrame) -> None:
        self.__data[key] = value

    def _clear_var(self) -> None:
        self.__var = {}

    def _add_var(self, key: str, value: Any) -> None:
        self.__var[key] = value

    def _update_meta_object(self, fid: str, obj: MorphFunctionMetaObject) -> None:
        current_obj = self._search_meta_object(fid)
        if current_obj is None:
            obj["id"] = fid
            self.__meta_objects.append(obj)
        else:
            current_obj.update(obj)

    def _search_meta_object(self, fid: str) -> MorphFunctionMetaObject | None:
        for obj in self.__meta_objects:
            if "id" in obj and obj["id"] == fid:
                return obj
        return None

    def _search_meta_object_by_name(self, name: str) -> MorphFunctionMetaObject | None:
        for obj in self.__meta_objects:
            if "name" in obj and obj["name"] == name:
                return obj
        return None

    def _search_meta_objects_by_path(
        self, file_path: str
    ) -> list[MorphFunctionMetaObject]:
        objects = []
        for obj in self.__meta_objects:
            if "id" in obj and obj["id"].startswith(file_path):
                objects.append(obj)
        return objects

    def _check_entirety_errors(self) -> list[MorphFunctionLoadError]:
        # check is there's any missing or cyclic alias
        errors: list[MorphFunctionLoadError] = []
        names: list[str] = []
        ids: list[str] = []
        for obj in self.__meta_objects:
            if obj["name"] in names:
                obj_filepath = obj["id"].split(":")[0]
                errors.append(
                    {
                        "category": MorphFunctionLoadErrorCategory.DUPLICATED_ALIAS,
                        "file_path": obj_filepath,
                        "name": obj["name"],
                        "error": f"Alias {obj['name']} is also defined in {ids[names.index(obj['name'])]}",
                    }
                )
                continue
            else:
                names.append(obj["name"])
                ids.append(obj["id"])

            requirements = obj.get("data_requirements", [])
            for requirement in requirements:
                dependency = self._search_meta_object_by_name(requirement)
                if dependency is None:
                    obj_filepath = obj["id"].split(":")[0]
                    errors.append(
                        {
                            "category": MorphFunctionLoadErrorCategory.MISSING_ALIAS,
                            "file_path": obj_filepath,
                            "name": requirement,
                            "error": f"Requirement {requirement} is not found",
                        }
                    )
                elif obj["name"] in dependency.get("data_requirements", []):
                    obj_filepath = obj["id"].split(":")[0]
                    errors.append(
                        {
                            "category": MorphFunctionLoadErrorCategory.CYCLIC_ALIAS,
                            "file_path": obj_filepath,
                            "name": requirement,
                            "error": f"Requirement {requirement} is cyclic",
                        }
                    )

        return errors
