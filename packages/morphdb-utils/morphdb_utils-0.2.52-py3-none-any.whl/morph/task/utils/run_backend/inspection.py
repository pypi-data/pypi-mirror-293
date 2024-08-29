from __future__ import annotations

import hashlib
import importlib.util
from pathlib import Path
from typing import Any, Dict, TypedDict

from jinja2 import Environment, nodes

from .errors import MorphFunctionLoadError, MorphFunctionLoadErrorCategory


class ScanResult(TypedDict):
    file_path: str
    checksum: str


class DirectoryScanResult(TypedDict):
    directory: str
    directory_checksum: str
    items: list[ScanResult]
    sql_contexts: dict[str, Any]
    errors: list[MorphFunctionLoadError]


def get_checksum(path: Path) -> str:
    """get checksum of file or directory."""
    hash_func = hashlib.sha256()

    if path.is_file():
        with open(str(path), "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_func.update(chunk)

        return hash_func.hexdigest()
    elif path.is_dir():
        for file in sorted(path.glob("**/*")):
            if file.is_file() and (file.suffix == ".py" or file.suffix == ".sql"):
                with open(str(file), "rb") as f:
                    for chunk in iter(lambda: f.read(4096), b""):
                        hash_func.update(chunk)

        return hash_func.hexdigest()
    else:
        raise ValueError(f"Path {path} is not a file or directory.")


def _import_python_file(
    file_path: str,
) -> tuple[ScanResult | None, MorphFunctionLoadError | None]:
    """try importing python file to evaluate morph functions.

    Returns:
        tuple[ScanResult | None, MorphFunctionLoadError | None]:
            - ScanResult: if the file is successfully imported.
            - MorphFunctionLoadError: if the file is not successfully imported.
    """
    file = Path(file_path)
    if file.suffix != ".py" or file.name == "__init__.py":
        # just skip files that are not python files or __init__.py
        # so it doesn't return neither ScanResult nor MorphFunctionLoadError
        return None, None

    module_name = file.stem
    module_path = file.as_posix()
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    if spec is None:
        return None, MorphFunctionLoadError(
            category=MorphFunctionLoadErrorCategory.IMPORT_ERROR,
            file_path=module_path,
            name=module_name,
            error="Failed to load module.",
        )

    module = importlib.util.module_from_spec(spec)
    if spec.loader is None:
        return None, MorphFunctionLoadError(
            category=MorphFunctionLoadErrorCategory.IMPORT_ERROR,
            file_path=module_path,
            name=module_name,
            error="Failed to load module.",
        )

    try:
        spec.loader.exec_module(module)
    except Exception as e:
        return None, MorphFunctionLoadError(
            category=MorphFunctionLoadErrorCategory.IMPORT_ERROR,
            file_path=module_path,
            name=module_name,
            error=f"Fail to evaluate module: {e}",
        )
    return {"file_path": module_path, "checksum": get_checksum(file)}, None


def _import_sql_file(
    file_path: str,
) -> tuple[ScanResult | None, dict[str, Any], MorphFunctionLoadError | None]:
    file = Path(file_path)
    if file.suffix != ".sql":
        # just skip files that are not sql files
        # so it doesn't return neither ScanResult nor MorphFunctionLoadError
        return None, {}, None

    module_path = file_path
    sql_contexts: dict[str, Any] = {}
    with open(file_path, "r") as f:
        calls = _parse_jinja_sql(f.read())
        config = calls["config"][0] if "config" in calls else None
        if config is None:
            return None, {}, None

        args = []
        for argument in calls["argument"] if "argument" in calls else []:
            args.append(argument["args"][0])

        sql_contexts.update(
            {
                module_path: {
                    "id": module_path,
                    "name": config["kwargs"]["name"],
                    "arguments": args,
                    **config["kwargs"],
                },
            }
        )
        result: ScanResult = {
            "file_path": file.as_posix(),
            "checksum": get_checksum(file),
        }
        return result, sql_contexts, None


def _import_python_sql_files(directory: str) -> DirectoryScanResult:
    p = Path(directory)
    results: list[ScanResult] = []
    errors: list[MorphFunctionLoadError] = []
    # NOTE: ユーザーが実装した以外のpythonファイルを読み込んでしまうと、予期せぬエラーやパフォーマンスの問題が発生する可能性がある
    #       現状無視するディレクトリを列挙し除外することで対処しているが、これでもglobの対象範囲が広すぎることによるパフォーマンスの問題が依然起こる
    # TODO: 今後は対象範囲を限定するための設定を追加することを検討する
    ignore_dirs = [".local", ".git", ".venv", "__pycache__"]

    for file in p.glob("**/*.py"):
        if any(ignore_dir in file.parts for ignore_dir in ignore_dirs):
            continue

        result, error = _import_python_file(file.as_posix())
        if result is not None:
            results.append(result)
        if error is not None:
            errors.append(error)

    sql_contexts: Dict[str, Any] = {}
    for file in p.glob("**/*.sql"):
        if any(ignore_dir in file.parts for ignore_dir in ignore_dirs):
            continue

        module_path = file.as_posix()
        result, context, error = _import_sql_file(module_path)
        if result is not None:
            results.append(result)
            sql_contexts.update(context)
        if error is not None:
            errors.append(error)

    return {
        "directory": directory,
        "directory_checksum": get_checksum(p),
        "items": results,
        "sql_contexts": sql_contexts,
        "errors": errors,
    }


def _parse_jinja_sql(template):
    env = Environment()
    parsed_content = env.parse(template)
    calls: Dict[str, Any] = {}

    def visit_node(node):
        if isinstance(node, nodes.Call):
            func_name = node.node.name

            args = {
                "args": [arg.as_const() for arg in node.args],
                "kwargs": {kw.key: kw.value.as_const() for kw in node.kwargs},
            }

            if func_name in calls:
                calls[func_name].append(args)
            else:
                calls[func_name] = [args]

        for child in node.iter_child_nodes():
            visit_node(child)

    visit_node(parsed_content)

    return calls
