import base64
import logging
import os
import re
import time
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, DefaultDict, Dict, List, Optional, Union

import click
import yaml

from morph.task.constant.project_config import ProjectConfig
from morph.task.utils.decorator import DecoratorParser
from morph.task.utils.os import OsUtils
from morph.task.utils.sqlite import SqliteDBManager

YAML_IGNORE_DIRS = ["/private/tmp", "/tmp"]


def find_project_root_dir(abs_filepath: Optional[str] = None) -> str:
    current_dir = (
        abs_filepath if abs_filepath and os.path.isabs(abs_filepath) else os.getcwd()
    )

    # /tmp などの再起動によって失われるファイルでの実行は実行場所を起点とする
    for ignore_dir in YAML_IGNORE_DIRS:
        if ignore_dir in current_dir:
            current_dir = os.getcwd()

    while current_dir != os.path.dirname(current_dir):
        morph_project_db_path = os.path.join(
            current_dir, ProjectConfig.MORPH_PROJECT_DB
        )
        if os.path.isfile(morph_project_db_path):
            return os.path.abspath(os.path.dirname(morph_project_db_path))
        current_dir = os.path.dirname(current_dir)

    morph_project_db_path = os.path.join(Path.home(), ProjectConfig.MORPH_PROJECT_DB)
    if os.path.isfile(morph_project_db_path):
        return os.path.abspath(os.path.dirname(morph_project_db_path))
    raise FileNotFoundError(
        f"{ProjectConfig.MORPH_PROJECT_DB} not found in the current directory or any parent directories."
    )


@dataclass
class Resource:
    alias: str
    path: str
    connection: Optional[str]
    output_paths: Optional[List[str]]
    public: Optional[bool]
    output_type: Optional[str]

    def __init__(
        self,
        alias: str,
        path: str,
        connection: Optional[str] = None,
        output_paths: Optional[List[str]] = None,
        public: Optional[bool] = None,
        output_type: Optional[str] = None,
    ):
        self.alias = alias
        self.path = path
        self.public = public
        self.output_type = output_type

        # Add attributes for executable files
        add_executable_attrs = False
        ext = os.path.splitext(path)[1]
        if ext in ProjectConfig.EXECUTABLE_EXTENSIONS:
            add_executable_attrs = True

        if add_executable_attrs:
            self.connection = connection
            self.output_paths = output_paths
        else:
            self.connection = None
            self.output_paths = None

    def has_valid_output_paths(self) -> bool:
        return len(self.output_paths or []) > 0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "alias": self.alias,
            "path": self.path,
            "connection": self.connection,
            "output_paths": self.output_paths,
            "public": self.public,
        }

    def _replace_output_placeholders(
        self, output_file: str, logger: logging.Logger = logging.getLogger()
    ) -> List[str]:
        # Definition of placeholder functions that can be used in the output_path
        placeholder_map: Dict[str, str] = {
            "{name}": self.alias,
            "{now()}": datetime.now().strftime("%Y%m%d_%H%M%S"),
            "{unix()}": str(int(time.time() * 1000)),
        }

        # Replace placeholders in the output path
        for placeholder, expanded in placeholder_map.items():
            if placeholder in output_file:
                output_file = output_file.replace(placeholder, expanded)

        # Replace ext() placeholder; ext() can produce multiple output_paths
        output_files: List[str] = []
        if "{ext()}" in output_file:
            extensions = [".txt"]
            if self.output_type == "visualization":
                extensions = [".html", ".png"]
            elif self.output_type == "dataframe":
                extensions = [".csv"]
            elif self.output_type == "document":
                extensions = [".md"]
            elif self.output_type == "json":
                extensions = [".json"]
            output_files = [output_file.replace("{ext()}", ext) for ext in extensions]
        else:
            output_files = [output_file]

        # Validate the output paths
        validated_outputs = []
        for f in output_files:
            # Check for undefined placeholders
            if "{" in f and "}" in f:
                logger.warning(
                    f"Unrecognized placeholder found in the output_paths: {f}. Cell output not saved."
                )
                continue

            # Avoid output_file to have multiple extensions
            dirname = os.path.dirname(f)
            basename = os.path.splitext(os.path.basename(f))[0].replace(".", "")
            ext = os.path.splitext(os.path.basename(f))[1]
            validated_outputs.append(os.path.join(dirname, f"{basename}{ext}"))
        return validated_outputs

    @staticmethod
    def _write_output_file(
        output_file: str,
        output: Union[str, bytes],
    ) -> None:
        if not os.path.exists(os.path.dirname(output_file)):
            os.makedirs(os.path.dirname(output_file))

        mode = "wb" if isinstance(output, bytes) else "w"
        with open(output_file, mode) as f:
            f.write(output or "")

    def save_output_to_file(
        self,
        output: Union[str, bytes, List[Union[str, bytes]]],
        logger: logging.Logger = logging.getLogger(),
    ) -> "Resource":
        processed_output_paths = []

        for original_output_path in self.output_paths or []:
            output_files = self._replace_output_placeholders(
                original_output_path, logger
            )
            for output_file in output_files:
                if isinstance(output, list):
                    # For multiple outputs, HTML and PNG outputs are saved as files
                    for raw_output in output:
                        should_save_as_html = output_file.endswith(".html")
                        should_save_as_png = output_file.endswith(".png")

                        is_html_encoded = (
                            isinstance(raw_output, str)
                            and re.compile(r"<[^>]+>").search(raw_output) is not None
                        )
                        if should_save_as_html and not is_html_encoded:
                            continue

                        is_base64_encoded = (
                            isinstance(raw_output, str)
                            and re.match(r"^[A-Za-z0-9+/=]*$", raw_output) is not None
                        )
                        if should_save_as_png and not is_base64_encoded:
                            continue

                        if should_save_as_png:
                            base64.b64decode(raw_output, validate=True)
                            raw_output = base64.b64decode(raw_output)

                        self._write_output_file(output_file, raw_output)
                        processed_output_paths.append(output_file)
                        logger.info(
                            f"Cell output saved to: {str(Path(output_file).resolve())}"
                        )
                else:
                    self._write_output_file(output_file, output)
                    processed_output_paths.append(output_file)
                    logger.info(
                        f"Cell output saved to: {str(Path(output_file).resolve())}"
                    )

        self.output_paths = processed_output_paths
        return self


@dataclass
class MorphYaml:
    version: str

    # TODO: これらの属性はResourceなどのオブジェクトに移行したい
    resources: Dict[str, Dict[str, Any]]

    @staticmethod
    def load_yaml(project_root_path: str) -> "MorphYaml":
        morph_yaml_path = os.path.join(project_root_path, ProjectConfig.MORPH_YAML)
        if not os.path.isfile(morph_yaml_path):
            raise FileNotFoundError(f"morph.yaml not found in {project_root_path}")

        with open(morph_yaml_path, "r") as file:
            data = yaml.safe_load(file)

        return MorphYaml.from_dict(data)

    def save_yaml(self, project_root_path: str) -> None:
        morph_yaml_path = os.path.join(project_root_path, ProjectConfig.MORPH_YAML)

        yaml_content = yaml.dump(self.to_dict(), sort_keys=False)

        headers = {
            "ja": """\
# -------------------------------------------------------------------------------------
# このYAMLファイルはMorphプロジェクトの設定を定義します。
# リソース（例：PythonおよびSQLセル）やキャンバスの定義が含まれます。
# resources セクションでは、スクリプトのパスおよびその出力場所を指定します。
# -------------------------------------------------------------------------------------
#
# [output_paths]
# output_pathsフィールドの前提条件：
#   - output_pathsは文字列のリストでなければならず、少なくとも1つのパスを含む必要があります。
# output_pathsで使用できるプレースホルダー関数：
#   - {ext()}  : 結果の内容に基づいて出力拡張子を決定します
#   - {now()}  : YYYYMMDD_HHMMSS形式で現在の日付と時刻を出力します
#   - {unix()} : ミリ秒単位で13桁のUNIXタイムスタンプを出力します
# 例：
#   - output_paths: ["_private/outputs/example_python_cell/result_{unix()}{ext()}"]""",
            "en": """\
# -------------------------------------------------------------------------------------
# This YAML file defines the configuration for a Morph project.
# It includes definitions for resources (e.g., Python and SQL cells).
# The resources section specifies the paths to the scripts and their output locations.
# -------------------------------------------------------------------------------------
#
# [output_paths]
# Prerequisites for the output_paths field:
#   - The output_paths must be a list of strings, which contains at least one path.
# Placeholder functions that can be used in the output_paths:
#   - {ext()}  : Determines the output extension based on the result content
#   - {now()}  : Outputs the current date and time in the format YYYYMMDD_HHMMSS
#   - {unix()} : Outputs a 13-digit UNIX timestamp in milliseconds
# Example:
#   - output_paths: ["_private/outputs/example_python_cell/result_{unix()}{ext()}"]""",
        }

        # Insert comments
        yaml_content = f"{headers['en']}\n\n{yaml_content}"

        with open(morph_yaml_path, "w") as file:
            file.write(yaml_content)

    def to_dict(self) -> dict:
        return {
            "version": self.version,
            "resources": self.resources,
        }

    @staticmethod
    def from_dict(data: dict) -> "MorphYaml":
        resources = data.get("resources", {})
        return MorphYaml(version=data["version"], resources=resources)

    @staticmethod
    def find_abs_project_root_dir(abs_filepath: Optional[str] = None) -> str:
        current_dir = (
            abs_filepath
            if abs_filepath and os.path.isabs(abs_filepath)
            else os.getcwd()
        )

        # /tmp などの再起動によって失われるファイルでの実行は実行場所を起点とする
        for ignore_dir in YAML_IGNORE_DIRS:
            if ignore_dir in current_dir:
                current_dir = os.getcwd()

        while current_dir != os.path.dirname(current_dir):
            morph_yaml_path = os.path.join(current_dir, ProjectConfig.MORPH_YAML)
            if os.path.isfile(morph_yaml_path):
                return os.path.abspath(os.path.dirname(morph_yaml_path))
            current_dir = os.path.dirname(current_dir)

        morph_yaml_path = os.path.join(Path.home(), ProjectConfig.MORPH_YAML)
        if os.path.isfile(morph_yaml_path):
            return os.path.abspath(os.path.dirname(morph_yaml_path))
        raise FileNotFoundError(
            f"{ProjectConfig.MORPH_YAML} not found in the current directory or any parent directories."
        )

    @staticmethod
    def find_resource_by_alias(
        alias: str, project_root: str, db_manager: SqliteDBManager
    ) -> Optional[Resource]:
        resource: Optional[Resource] = None

        # First, search in the SQLite database
        res_dict = db_manager.get_resource_by_alias(alias)
        if res_dict:
            resource = Resource(
                alias=res_dict["alias"],
                path=OsUtils.get_abs_path(res_dict["path"], project_root),
                connection=res_dict.get("connection"),
                output_paths=[
                    OsUtils.get_abs_path(p, project_root)
                    for p in res_dict.get("output_paths", [])
                ],
                public=res_dict.get("public"),
            )

        # If not found, load and search in the YAML file
        morph_yaml = MorphYaml.load_yaml(project_root)
        res_dict = morph_yaml.resources.get(alias)
        if res_dict and res_dict.get("path"):
            # Sync to SQLite
            replaced = db_manager.replace_resource_record(
                alias, res_dict["path"], res_dict
            )
            resource = Resource(
                alias=replaced["alias"],
                path=OsUtils.get_abs_path(replaced["path"], project_root),
                connection=replaced.get("connection"),
                output_paths=[
                    OsUtils.get_abs_path(p, project_root)
                    for p in replaced.get("output_paths", [])
                ],
                public=replaced.get("public"),
            )

        if not resource:
            return None

        # If the output_path is not valid, update SQLite and morph.yaml
        if resource.has_valid_output_paths():
            return resource
        else:
            return MorphYaml._update_resource_by_alias(
                resource.alias, project_root, db_manager
            )

    @staticmethod
    def find_resource_by_path(
        path: str, project_root: str, db_manager: SqliteDBManager
    ) -> Optional[Resource]:
        base_path = project_root if OsUtils.is_at(project_root) else os.getcwd()
        abs_path = OsUtils.get_abs_path(path, base_path)

        # /tmp などの再起動によって失われるファイルでの実行はYAMLファイルに記録しない
        for ignore_dir in YAML_IGNORE_DIRS:
            if ignore_dir in abs_path:
                return None

        # First, search in the SQLite database
        res_dict = db_manager.get_resource_by_path(abs_path)
        if res_dict:
            if not res_dict.get("alias") or not res_dict.get("path"):
                return None

            resource = Resource(
                alias=res_dict["alias"],
                path=OsUtils.get_abs_path(res_dict["path"], project_root),
                connection=res_dict.get("connection"),
                output_paths=[
                    OsUtils.get_abs_path(p, project_root)
                    for p in res_dict.get("output_paths", [])
                ],
                public=res_dict.get("public"),
            )

            if resource.has_valid_output_paths():
                return resource
            else:
                return MorphYaml._update_resource_by_path(
                    abs_path, project_root, db_manager
                )

        # If not found, load and search in the YAML file
        morph_yaml = MorphYaml.load_yaml(project_root)
        for alias, res_dict in morph_yaml.resources.items():
            resource_path = OsUtils.get_abs_path(res_dict["path"], project_root)
            if resource_path == abs_path:
                # Sync to SQLite
                replaced = db_manager.replace_resource_record(alias, abs_path, res_dict)
                resource = Resource(
                    alias=replaced["alias"],
                    path=OsUtils.get_abs_path(replaced["path"], project_root),
                    connection=replaced.get("connection"),
                    output_paths=[
                        OsUtils.get_abs_path(p, project_root)
                        for p in replaced.get("output_paths", [])
                    ],
                    public=replaced.get("public"),
                )

                if resource.has_valid_output_paths():
                    return resource
                else:
                    return MorphYaml._update_resource_by_path(
                        abs_path, project_root, db_manager
                    )

        return None

    @staticmethod
    def analyze_output_extensions(abs_filename: str) -> List[str]:
        ext = os.path.splitext(os.path.basename(abs_filename))[1]
        if ext == ".sql":
            return [".csv"]
        else:
            # Analyze decorators to determine the output extension
            code = open(abs_filename, "r").read()
            decorators = DecoratorParser.get_decorators(code)
            decorator_name = None
            for decorator in decorators:
                if isinstance(decorator, dict):
                    decorator_name = decorator.get("name")
                else:
                    decorator_name = decorator
            if decorator_name == "visualize" or decorator_name == "morph.visualize":
                return [".html", ".png"]
            elif decorator_name == "transform" or decorator_name == "morph.csv":
                return [".csv"]
            elif decorator_name == "report" or decorator_name == "morph.markdown":
                return [".md"]
            elif decorator_name == "api" or decorator_name == "morph.json":
                return [".json"]
            else:
                return [".txt"]

    @staticmethod
    def _generate_default_output_path(
        alias: str,
        project_root: str,
        output_dir: Optional[str] = None,
    ) -> List[str]:
        output_dir = output_dir or OsUtils.get_abs_path(
            os.path.join(ProjectConfig.PRIVATE_DIR, alias), project_root
        )
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        return [os.path.join(output_dir, "result{ext()}")]

    @staticmethod
    def generate_new_alias(
        path: str,
        project_root: str,
        db_manager: SqliteDBManager,
        alias: Optional[str] = None,
        connection: Optional[str] = None,
        output_paths: Optional[List[str]] = None,
    ) -> "Resource":
        base_path = project_root if OsUtils.is_at(project_root) else os.getcwd()
        abs_path = OsUtils.get_abs_path(path, base_path)

        base_name = os.path.splitext(os.path.basename(abs_path))[0]
        new_alias = alias or base_name

        # /tmp などの再起動によって失われるファイルでの実行はYAMLファイルに記録しない
        for ignore_dir in YAML_IGNORE_DIRS:
            if ignore_dir in abs_path:
                output_dir = OsUtils.get_abs_path(
                    os.path.join(ProjectConfig.PRIVATE_DIR, new_alias), ignore_dir
                )
                output_paths = output_paths or MorphYaml._generate_default_output_path(
                    new_alias, project_root, output_dir
                )
                return Resource(
                    alias=abs_path,  # To avoid duplicate alias, fill with abs_path
                    path=abs_path,
                    connection=connection,
                    output_paths=output_paths,
                    public=None,
                )

        # Loading morph.yaml to avoid duplicate alias
        alias_count: DefaultDict[str, int] = defaultdict(int)
        morph_yaml = MorphYaml.load_yaml(project_root)
        for alias in morph_yaml.resources.keys():
            if alias.startswith(base_name):
                alias_count[alias] += 1

        if new_alias in morph_yaml.resources:
            new_alias = f"{base_name}_{alias_count[base_name]}"

        while new_alias in morph_yaml.resources:
            alias_count[base_name] += 1
            new_alias = f"{base_name}_{alias_count[base_name]}"

        # Add attributes for executable files
        add_executable_attrs = False
        ext = os.path.splitext(path)[1]
        if ext in ProjectConfig.EXECUTABLE_EXTENSIONS:
            add_executable_attrs = True

        if add_executable_attrs:
            morph_yaml.resources[new_alias] = {
                "path": abs_path,
                "connection": connection,
                "output_paths": output_paths
                or MorphYaml._generate_default_output_path(new_alias, project_root),
            }
        else:
            morph_yaml.resources[new_alias] = {"path": abs_path}

        # Sync new resource to SQLite
        db_manager.replace_resource_record(
            new_alias, abs_path, morph_yaml.resources[new_alias]
        )

        # Save morph.yaml
        morph_yaml.save_yaml(project_root)

        click.echo(
            click.style(f"Resource {abs_path} added with alias {new_alias}", fg="green")
        )

        return Resource(
            alias=new_alias,
            path=abs_path,
            connection=morph_yaml.resources[new_alias].get("connection"),
            output_paths=morph_yaml.resources[new_alias].get("output_paths"),
            public=morph_yaml.resources[new_alias].get("public"),
        )

    @staticmethod
    def _update_resource_by_alias(
        alias: str, project_root: str, db_manager: SqliteDBManager
    ) -> "Resource":
        morph_yaml = MorphYaml.load_yaml(project_root)
        for a, res_dict in morph_yaml.resources.items():
            if a == alias:
                abs_path = res_dict["path"]

                # Check if the resource is executable
                add_executable_attrs = False
                ext = os.path.splitext(abs_path)[1]
                if ext in ProjectConfig.EXECUTABLE_EXTENSIONS:
                    add_executable_attrs = True

                if add_executable_attrs:
                    morph_yaml.resources[a][
                        "output_paths"
                    ] = MorphYaml._generate_default_output_path(a, project_root)

                    # Sync new resource to SQLite
                    db_manager.replace_resource_record(
                        a, abs_path, morph_yaml.resources[a]
                    )

                    # Save morph.yaml
                    morph_yaml.save_yaml(project_root)

                    click.echo(
                        click.style(
                            f"Resource {abs_path} with alias {a} has been updated",
                            fg="green",
                        )
                    )

                return Resource(
                    alias=a,
                    path=abs_path,
                    connection=morph_yaml.resources[a].get("connection"),
                    output_paths=morph_yaml.resources[a].get("output_paths"),
                    public=morph_yaml.resources[a].get("public"),
                )

        raise FileNotFoundError(f"Alias {alias} not found.")

    @staticmethod
    def _update_resource_by_path(
        abs_path: str, project_root: str, db_manager: SqliteDBManager
    ) -> "Resource":
        morph_yaml = MorphYaml.load_yaml(project_root)
        for alias, res_dict in morph_yaml.resources.items():
            if res_dict["path"] == abs_path:

                # Check if the resource is executable
                add_executable_attrs = False
                ext = os.path.splitext(abs_path)[1]
                if ext in ProjectConfig.EXECUTABLE_EXTENSIONS:
                    add_executable_attrs = True

                if add_executable_attrs:
                    morph_yaml.resources[alias][
                        "output_paths"
                    ] = MorphYaml._generate_default_output_path(alias, project_root)

                    # Sync new resource to SQLite
                    db_manager.replace_resource_record(
                        alias, abs_path, morph_yaml.resources[alias]
                    )

                    # Save morph.yaml
                    morph_yaml.save_yaml(project_root)

                    click.echo(
                        click.style(
                            f"Resource {abs_path} with alias {alias} has been updated",
                            fg="green",
                        )
                    )

                return Resource(
                    alias=alias,
                    path=abs_path,
                    connection=morph_yaml.resources[alias].get("connection"),
                    output_paths=morph_yaml.resources[alias].get("output_paths"),
                    public=morph_yaml.resources[alias].get("public"),
                )

        raise FileNotFoundError(f"File {abs_path} not found.")

    @staticmethod
    def find_or_create_resource_by_path(
        path: str, project_root: str, db_manager: SqliteDBManager
    ) -> Resource:
        base_path = project_root if OsUtils.is_at(project_root) else os.getcwd()
        abs_path = OsUtils.get_abs_path(path, base_path)

        if not os.path.exists(abs_path):
            click.echo(
                click.style(
                    f"Error: File {path} not found.",
                    fg="red",
                )
            )
            raise FileNotFoundError(f"File {path} not found.")

        # Go find the resource in the SQLite database or morph.yaml
        resource = MorphYaml.find_resource_by_path(abs_path, project_root, db_manager)
        if resource:
            return resource

        # Generate new alias if the resource is not defined yet in the morph.yaml
        return MorphYaml.generate_new_alias(abs_path, project_root, db_manager)

    @staticmethod
    def preprocess_output_paths(
        alias: str, project_root: str, db_manager: SqliteDBManager
    ) -> None:
        """
        outputに異なる拡張子の値が出力される場合にoutput_pathを確認する
        visuzlizeの場合以外にパターンがある場合はロジックを追加する
        """
        # リソースを取得
        resource = MorphYaml.find_resource_by_alias(alias, project_root, db_manager)
        if not resource:
            raise FileNotFoundError(f"Alias {alias} not found.")
        if not resource.has_valid_output_paths():
            raise FileNotFoundError(f"Resource path not found for alias {alias}.")

        output_paths = resource.output_paths or []

        if len(output_paths) == 0 or (
            len(output_paths) == 1
            and (output_paths[0].endswith(".html") or output_paths[0].endswith(".png"))
        ):
            # デフォルトのoutput_pathを生成
            output_dir = os.path.join(
                project_root, "src", ProjectConfig.PRIVATE_DIR, alias
            )
            base_output_path = os.path.join(output_dir, "result")
            default_output_paths = [
                f"{base_output_path}.html",
                f"{base_output_path}.png",
            ]

            if len(output_paths) == 1:
                base_output_path = os.path.splitext(output_paths[0])[0]
                if output_paths[0].endswith(".html"):
                    output_paths = [output_paths[0], base_output_path + ".png"]
                elif output_paths[0].endswith(".png"):
                    output_paths = [base_output_path + ".html", output_paths[0]]
                else:
                    output_paths = default_output_paths
            else:
                output_paths = default_output_paths

        elif len(output_paths) == 2:
            # output_pathが2つ指定されている場合の処理
            ext_0 = os.path.splitext(output_paths[0])[1]
            ext_1 = os.path.splitext(output_paths[1])[1]

            if {ext_0, ext_1} == {".html", ".png"}:
                # 順番が逆の場合は入れ替える
                if ext_0 == ".png" and ext_1 == ".html":
                    output_paths = [output_paths[1], output_paths[0]]
            else:
                # 拡張子が完全に異なる場合はエラーを吐く
                raise ValueError(
                    "Output paths must include both .html and .png extensions."
                )

        # morph.yamlをロードしてoutput_pathを更新
        morph_yaml = MorphYaml.load_yaml(project_root)
        morph_yaml.resources[alias]["output_paths"] = output_paths

        # SQLiteに新しいリソースを同期
        abs_path = OsUtils.get_abs_path(resource.path, project_root)
        db_manager.replace_resource_record(alias, abs_path, morph_yaml.resources[alias])

        # morph.yamlを保存
        morph_yaml.save_yaml(project_root)

    @staticmethod
    def get_cell_type(path: str) -> str:
        if os.path.isdir(path):
            return "directory"
        elif os.path.isfile(path):
            extension_mapping = {
                "sql": "sql",
                "py": "python",
            }
            ext = os.path.splitext(path)[1][1:]
            return extension_mapping.get(ext, "file")
        else:
            raise FileNotFoundError(f"File not found: {path}")
