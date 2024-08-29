import json
import os
import shutil
from pathlib import Path
from typing import Any, List, Literal, cast

import click
from morph.cli.flags import Flags
from morph.task.base import BaseTask
from morph.task.utils.morph import MorphYaml, Resource, find_project_root_dir
from morph.task.utils.os import OsUtils
from morph.task.utils.run_backend.inspection import get_checksum
from morph.task.utils.run_backend.state import MorphGlobalContext, load_cache
from morph.task.utils.sqlite import SqliteDBManager


class PrintResourceTask(BaseTask):
    def __init__(self, args: Flags):
        super().__init__(args)
        self.args = args

        target: str
        target_type: Literal["alias", "file", "all"]
        if args.ALL:
            target = ""
            target_type = "all"
        elif args.ALIAS:
            target = args.ALIAS
            target_type = "alias"
        elif args.FILE:
            target = args.FILE
            target_type = "file"
        else:
            click.echo("Either --alias, --file or --all must be provided.")
            raise click.Abort()

        self.target = target
        self.target_type = target_type

        try:
            self.project_root = find_project_root_dir()
        except FileNotFoundError as e:
            click.echo(click.style(str(e), fg="red"))
            raise e

        # Initialize SQLite database
        self.db_manager = SqliteDBManager(self.project_root)
        self.db_manager.initialize_database()

    def run(self):
        cache = load_cache(self.project_root)
        checksum = get_checksum(Path(self.project_root))
        output: dict[str, Any] = {}
        if cache is None or checksum != cache["directory_checksum"]:
            context = MorphGlobalContext.get_instance()
            errors = context.load(self.project_root)
            if len(errors) > 0:
                output["errors"] = errors

            cache = context.dump()
        elif len(cache["errors"]) > 0:
            output["errors"] = cache["errors"]

        if self.target_type == "all":
            resource_dicts: list[dict] = []
            for item in cache["items"]:
                # id is formatted as {filename}:{function_name}
                filepath = item["spec"]["id"].split(":")[0]
                resource_item = Resource(
                    alias=item["spec"]["name"],
                    path=filepath,
                    connection=(
                        item["spec"]["connection"]
                        if "connection" in item["spec"]
                        else None
                    ),
                    output_paths=(
                        cast(list, item["spec"]["output_paths"])
                        if "output_paths" in item["spec"]
                        else None
                    ),
                )
                resource_dicts.append(resource_item.to_dict())

            output["resources"] = resource_dicts
            click.echo(json.dumps(output, indent=2))
        elif self.target_type == "alias":
            # NOTE: use Resource entity to keep backward compatibility with old output format
            resource: Resource | None = None
            for item in cache["items"]:
                if item["spec"]["name"] == self.target:
                    # id is formatted as {filename}:{function_name}
                    filepath = item["spec"]["id"].split(":")[0]
                    resource = Resource(
                        alias=item["spec"]["name"],
                        path=filepath,
                        connection=(
                            item["spec"]["connection"]
                            if "connection" in item["spec"]
                            else None
                        ),
                        output_paths=(
                            cast(list, item["spec"]["output_paths"])
                            if "output_paths" in item["spec"]
                            else None
                        ),
                    )
                    break
            if resource:
                output["resources"] = [resource.to_dict()]
                click.echo(json.dumps(output, indent=2))
            else:
                click.echo(f"Alias {self.target} not found.")
        elif self.target_type == "file":
            abs_path = Path(self.target).as_posix()
            resource = None
            for item in cache["items"]:
                # id is formatted as {filename}:{function_name}
                filepath = item["spec"]["id"].split(":")[0]
                if filepath == abs_path:
                    resource = Resource(
                        alias=item["spec"]["name"],
                        path=filepath,
                        connection=(
                            item["spec"]["connection"]
                            if "connection" in item["spec"]
                            else None
                        ),
                        output_paths=(
                            cast(list, item["spec"]["output_paths"])
                            if "output_paths" in item["spec"]
                            else None
                        ),
                    )
                    break
            if resource:
                output["resources"] = [resource.to_dict()]
                click.echo(json.dumps(output, indent=2))
            else:
                click.echo(f"File {self.target} not found.")


class CreateResourceTask(BaseTask):
    def __init__(self, args: Flags):
        super().__init__(args)

        # Validate required arguments
        self.file = args.TARGET
        if not self.file or not os.path.isfile(self.file):
            raise click.BadArgumentUsage(f"TARGET path {self.file} does not exist.")

        # Initialize project root
        try:
            self.project_root = MorphYaml.find_abs_project_root_dir()
        except FileNotFoundError as e:
            click.echo(click.style(str(e), fg="red"))
            raise e

        # Initialize SQLite database
        self.db_manager = SqliteDBManager(self.project_root)
        self.db_manager.initialize_database()

        # Validate optional arguments
        self.alias = args.ALIAS
        resource = MorphYaml.find_resource_by_alias(
            self.alias, self.project_root, self.db_manager
        )
        if resource:
            raise click.BadParameter(f"Alias {self.alias} already exists.")

        self.connection = args.CONNECTION
        self.output_paths = list(args.OUTPUT_PATHS)

    def run(self):
        resource = MorphYaml.generate_new_alias(
            self.file,
            self.project_root,
            self.db_manager,
            self.alias,
            self.connection,
            self.output_paths,
        )
        click.echo(json.dumps(resource.to_dict(), indent=2))


class MoveResourceTask(BaseTask):
    def __init__(self, args: Flags):
        super().__init__(args)

        # Initialize project root
        try:
            self.project_root = MorphYaml.find_abs_project_root_dir()
        except FileNotFoundError as e:
            click.echo(click.style(str(e), fg="red"))
            raise e

        base_path = (
            self.project_root if OsUtils.is_at(self.project_root) else os.getcwd()
        )
        self.source = OsUtils.get_abs_path(args.SOURCE, base_path)
        self.target = OsUtils.get_abs_path(args.TARGET, base_path)

        # Validate required arguments
        if not os.path.exists(self.source):
            raise click.BadArgumentUsage(f"SOURCE path {self.source} does not exist.")
        if os.path.isdir(self.target) and not os.path.exists(self.target):
            raise click.BadArgumentUsage(f"TARGET path {self.target} does not exist.")

        # Source must be a valid file or directory
        self.source_type: Literal["file", "directory"]
        if os.path.isfile(self.source):
            self.source_type = "file"
        elif os.path.isdir(self.source):
            self.source_type = "directory"
        else:
            raise click.BadArgumentUsage(f"Unsupported SOURCE type {self.source}.")

        # Treat target as a file if it does not exist
        self.target_type: Literal["file", "directory"]
        if self.source_type == "directory":
            self.target_type = "directory"
        elif os.path.isdir(self.target):
            self.target_type = "directory"
        elif os.path.isfile(self.target):
            self.target_type = "file"
        else:
            # If target does not exit yet, treat it as a file
            self.target_type = "file"

        # Initialize SQLite database
        self.db_manager = SqliteDBManager(self.project_root)
        self.db_manager.initialize_database()

        # Load morph.yaml
        self.morph_yaml = MorphYaml.load_yaml(self.project_root)

    def run(self):
        if self.source_type == "file":
            # Determine the target file path
            target_file_path: str
            if self.target_type == "file":
                target_file_path = self.target
            if self.target_type == "directory":
                target_file_path = os.path.abspath(
                    os.path.normpath(
                        (os.path.join(self.target, os.path.basename(self.source)))
                    )
                )

            # Update morph.yaml
            for alias, res_dict in self.morph_yaml.resources.items():
                resource_path = OsUtils.get_abs_path(
                    res_dict["path"], self.project_root
                )
                if resource_path == self.source:
                    res_dict["path"] = target_file_path
            self.morph_yaml.save_yaml(self.project_root)

            # Move the file
            os.rename(self.source, target_file_path)
        elif self.source_type == "directory" and self.target_type == "directory":
            # Update morph.yaml
            for alias, res_dict in self.morph_yaml.resources.items():
                resource_path = OsUtils.get_abs_path(
                    res_dict["path"], self.project_root
                )
                if resource_path.startswith(self.source):
                    res_dict["path"] = os.path.abspath(
                        os.path.normpath(
                            os.path.join(
                                self.target,
                                os.path.relpath(resource_path, self.source),
                            )
                        )
                    )
            self.morph_yaml.save_yaml(self.project_root)

            # Move the directory
            os.rename(self.source, self.target)
        else:
            raise click.BadArgumentUsage("Unsupported move operation.")

        # Sync morph.yaml to SQLite
        self.db_manager.sync_resources_from_yaml()
        click.echo(click.style("Synced morph.yaml to SQLite database.", fg="green"))


class RemoveResourceTask(BaseTask):
    def __init__(self, args: Flags):
        super().__init__(args)

        # Initialize project root
        try:
            self.project_root = MorphYaml.find_abs_project_root_dir()
        except FileNotFoundError as e:
            click.echo(click.style(str(e), fg="red"))
            raise e

        base_path = (
            self.project_root if OsUtils.is_at(self.project_root) else os.getcwd()
        )
        self.target = OsUtils.get_abs_path(args.TARGET, base_path)

        # Validate required arguments
        if not os.path.exists(self.target):
            raise click.BadArgumentUsage(f"TARGET path {self.target} does not exist.")

        # Target must be a valid file or directory
        self.target_type: Literal["file", "directory"]
        if os.path.isfile(self.target):
            self.target_type = "file"
        elif os.path.isdir(self.target):
            self.target_type = "directory"
        else:
            raise click.BadArgumentUsage(f"Unsupported TARGET type {self.target}.")

        # Initialize SQLite database
        self.db_manager = SqliteDBManager(self.project_root)
        self.db_manager.initialize_database()

        # Load morph.yaml
        self.morph_yaml = MorphYaml.load_yaml(self.project_root)

    def run(self):
        # Collect aliases to be deleted
        aliases_to_delete: List[str] = []

        if self.target_type == "file":
            # Collect aliases for file
            for alias, res_dict in self.morph_yaml.resources.items():
                resource_path = OsUtils.get_abs_path(
                    res_dict["path"], self.project_root
                )
                if resource_path == self.target:
                    aliases_to_delete.append(alias)

            # Update morph.yaml
            for alias in aliases_to_delete:
                del self.morph_yaml.resources[alias]
            self.morph_yaml.save_yaml(self.project_root)

            # Remove the file
            os.remove(self.target)
        elif self.target_type == "directory":
            # Collect aliases for directory
            for alias, res_dict in self.morph_yaml.resources.items():
                resource_path = OsUtils.get_abs_path(
                    res_dict["path"], self.project_root
                )
                if resource_path.startswith(self.target):
                    aliases_to_delete.append(alias)

            # Update morph.yaml
            for alias in aliases_to_delete:
                del self.morph_yaml.resources[alias]
            self.morph_yaml.save_yaml(self.project_root)

            # Remove the directory
            shutil.rmtree(self.target)
        else:
            raise click.BadArgumentUsage("Unsupported remove operation.")

        # Sync morph.yaml to SQLite
        self.db_manager.sync_resources_from_yaml()
        click.echo(click.style("Synced morph.yaml to SQLite database.", fg="green"))
