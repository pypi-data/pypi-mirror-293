import configparser
import json
import logging
import os
import time
from pathlib import Path
from typing import Any, List, Optional, Union, cast

import click
import matplotlib.figure
import pandas as pd
import plotly
from dotenv import dotenv_values, load_dotenv
from morphdb_utils.annotations import (
    _get_html_from_mpl_image,
    _get_html_from_plotly_image,
)

from morph.cli.flags import Flags
from morph.task.base import BaseTask
from morph.task.constant.project_config import ProjectConfig
from morph.task.utils.logging import get_morph_logger
from morph.task.utils.morph import Resource, find_project_root_dir
from morph.task.utils.run_backend.errors import logging_file_error_exception
from morph.task.utils.run_backend.execution import run_cell
from morph.task.utils.run_backend.state import (
    MorphFunctionMetaObject,
    MorphGlobalContext,
)
from morph.task.utils.sqlite import CliError, RunStatus, SqliteDBManager
from morph.task.utils.timer import TimeoutException
from morph.task.utils.timezone import TimezoneManager


class RunTask(BaseTask):
    def __init__(self, args: Flags):
        super().__init__(args)

        # validate credentials
        config_path = ProjectConfig.MORPH_CRED_PATH
        if not os.path.exists(config_path):
            click.echo(
                click.style(
                    f"Error: No credentials found in {config_path}.",
                    fg="red",
                )
            )
            raise FileNotFoundError(f"No credentials found in {config_path}.")

        # read credentials
        config = configparser.ConfigParser()
        config.read(config_path)
        if not config.sections():
            click.echo(
                click.style(
                    f"Error: No credentials entries found in {config_path}.",
                    fg="red",
                )
            )
            raise FileNotFoundError(f"No credentials entries found in {config_path}.")

        # NOTE: vm内ではセクションが必ず1つなので、'default' セクションを指定している
        self.team_slug: str = config.get("default", "team_slug")
        self.app_url: str = config.get("default", "app_url")
        self.database_id: str = config.get("default", "database_id")
        self.api_key: str = config.get("default", "api_key")

        # env variable configuration
        os.environ["MORPH_DATABASE_ID"] = self.database_id
        os.environ["MORPH_BASE_URL"] = self.app_url
        os.environ["MORPH_TEAM_SLUG"] = self.team_slug
        os.environ["MORPH_API_KEY"] = self.api_key

        # parse arguments
        # TODO: filenameを入力としているが、1ファイルに複数の関数を登録できるようになるので関数まで識別子を指定できるように改める必要がある
        filename_or_alias: str = os.path.normpath(args.FILENAME)
        self.run_id: str = self.args.RUN_ID or f"{int(time.time() * 1000)}"
        self.is_dag: bool = args.DAG or False
        self.is_dry_run: bool = args.DRY_RUN or False
        self.canvas = args.CANVAS
        self.connection = args.CONNECTION
        self.vars = args.DATA
        self.is_filepath = os.path.splitext(os.path.basename(filename_or_alias))[1]

        try:
            start_dir = filename_or_alias if os.path.isabs(filename_or_alias) else "./"
            self.project_root = find_project_root_dir(start_dir)
        except FileNotFoundError as e:
            click.echo(click.style(str(e), fg="red"))
            raise e

        # Initialize database
        self.db_manager = SqliteDBManager(self.project_root)
        self.db_manager.initialize_database()

        context = MorphGlobalContext.get_instance()
        if args.NO_CACHE:
            errors = context.load(self.project_root)
        else:
            errors = context.partial_load(
                self.project_root,
                (
                    str(Path(filename_or_alias).resolve())
                    if self.is_filepath
                    else filename_or_alias
                ),
            )

        if len(errors) > 0:
            click.echo(click.style("Error: Failed to load morph functions.", fg="red"))
            click.Abort()

        resource: Optional[MorphFunctionMetaObject] = None
        if self.is_filepath:
            self.filename = str(Path(filename_or_alias).resolve())
            if not os.path.isfile(self.filename):
                click.echo(
                    click.style(
                        f"Error: File {self.filename} not found.",
                        fg="red",
                    )
                )
                raise FileNotFoundError(f"Error: File {self.filename} not found.")
            resources = context._search_meta_objects_by_path(self.filename)
            if len(resources) > 0:
                resource = resources[0]
        else:
            resource = context._search_meta_object_by_name(filename_or_alias)
            if resource is not None:
                # id is formatted as {filename}:{function_name}
                self.filename = resource["id"].split(":")[0]

        if resource is None:
            click.echo(
                click.style(
                    f"Error: A resource with alias {self.filename} not found.",
                    fg="red",
                )
            )
            raise FileNotFoundError(f"A resource with alias {self.filename} not found.")

        self.resource = resource
        self.ext = os.path.splitext(os.path.basename(self.filename))[1]
        self.cell_alias = self.resource["name"]

        # Set up run directory
        self.runs_dir = os.path.normpath(
            os.path.join(
                ProjectConfig.RUNS_DIR,
                self.canvas if self.canvas else "",
                self.run_id,
            )
        )
        if not os.path.exists(self.runs_dir):
            os.makedirs(self.runs_dir)

        # Set up logger
        log_filename = f"{os.path.splitext(os.path.basename(self.cell_alias))[0]}.log"
        self.log_path = os.path.join(self.runs_dir, log_filename)
        self.logger = get_morph_logger(self.log_path)

        # load .env in project root and set timezone
        dotenv_path = os.path.join(self.project_root, ".env")
        load_dotenv(dotenv_path)
        env_vars = dotenv_values(dotenv_path)
        for e_key, e_val in env_vars.items():
            os.environ[e_key] = str(e_val)
        if self.canvas:
            os.environ["MORPH_CANVAS"] = str(self.canvas)
        desired_tz = os.getenv("TZ")
        if desired_tz is not None:
            tz_manager = TimezoneManager()
            if not tz_manager.is_valid_timezone(desired_tz):
                self.logger.error(f"Invalid TZ value in .env: {desired_tz}")
                raise ValueError(f"Invalid TZ value in .env: {desired_tz}")
            if desired_tz != tz_manager.get_current_timezone():
                tz_manager.change_timezone(desired_tz)

    def _finalize_run(
        self,
        cell_alias: str,
        final_state: str,
        output: Any,
        error: Optional[CliError],
    ) -> None:
        output_paths: Optional[List[str]] = self._save_output_to_file(
            output, self.logger
        )
        abs_output_paths: List[str] = []
        for output_path in output_paths if output_paths is not None else []:
            abs_path = Path(output_path).resolve()
            abs_output_paths.append(str(abs_path))

        self.db_manager.update_run_record(
            self.run_id,
            self.canvas,
            cell_alias,
            final_state,
            error,
            abs_output_paths,
        )

    def run(self) -> None:
        context = MorphGlobalContext.get_instance()
        log_path = os.path.join(self.runs_dir, f"{self.cell_alias}.log")
        logger = get_morph_logger(self.log_path)
        resource = context._search_meta_object_by_name(self.cell_alias)
        if not resource:
            click.echo(
                click.style(
                    f"Error: A resource with alias {self.cell_alias} not found.",
                    fg="red",
                )
            )
            raise FileNotFoundError(
                f"A resource with alias {self.cell_alias} not found."
            )

        self.db_manager.insert_run_record(
            self.run_id,
            self.canvas,
            self.cell_alias,
            self.is_dag,
            log_path,
        )

        # Execute cell
        if self.ext == ".sql":
            self._run_sql(
                resource,
                logger,
            )
        elif self.ext == ".py":
            self._run_python(resource, logger)
        else:
            text = "Invalid file type. Please specify a .sql or .py file."
            logger.error(text)
            self._finalize_run(
                self.cell_alias,
                RunStatus.FAILED,
                None,
                CliError(
                    type="general",
                    details=text,
                ),
            )

    def _run_sql(
        self, resource: MorphFunctionMetaObject, logger: logging.Logger
    ) -> None:
        cell = resource["name"]
        # id is formatted as {filename}:{function_name}
        filepath = resource["id"].split(":")[0]
        logger.info(f"Running sql file: {filepath}")

        try:
            vars = {resource["name"]: self.vars} if self.vars else {}
            use_cache = False if self.is_dag else True
            output = run_cell(
                resource, self.app_url, self.api_key, self.database_id, vars, use_cache
            )
        except Exception as e:
            text = f"An error occurred while running the SQL: {str(e)}"
            logger.error(text)
            self._finalize_run(
                cell,
                RunStatus.FAILED,
                None,
                CliError(
                    type="general",
                    details=text,
                ),
            )
            return
        self._finalize_run(
            cell,
            RunStatus.DONE,
            self._transform_output(output),
            None,
        )
        logger.info(f"Successfully ran sql file: {filepath}")

    def _run_python(
        self, resource: MorphFunctionMetaObject, logger: logging.Logger
    ) -> None:
        cell = resource["name"]
        # id is formatted as {filename}:{function_name}
        filepath = resource["id"].split(":")[0]
        logger.info(f"Running python file: {filepath}")

        try:
            # TODO: timeout, banned_functionなどの元々のevalベースの機構をどう復活させるかは後で検討する
            vars = {resource["name"]: self.vars} if self.vars else {}
            use_cache = False if self.is_dag else True
            output = run_cell(
                resource, self.app_url, self.api_key, self.database_id, vars, use_cache
            )
        except TimeoutException:
            text = f"Timeout error occurred while running the script: {filepath}"
            logger.error(text)
            self._finalize_run(
                cell,
                RunStatus.FAILED,
                None,
                CliError(
                    type="general",
                    details=text,
                ),
            )
            return
        except Exception as e:
            logging_file_error_exception(e, filepath, logger)
            text = f"Unexpected error occurred while executing python code: {str(e)}"
            logger.error(text)
            self._finalize_run(
                cell,
                RunStatus.FAILED,
                None,
                CliError(
                    type="general",
                    details=text,
                ),
            )
            return
        self._finalize_run(
            cell,
            RunStatus.DONE,
            self._transform_output(output),
            None,
        )
        logger.info(f"Successfully ran python file: {filepath}")

    def _transform_output(self, output: Any) -> Any:
        transformed_output: Any = output
        if isinstance(output, pd.DataFrame):
            transformed_output = output.to_csv(index=False).encode("utf-8")
        elif isinstance(output, dict):
            transformed_output = json.dumps(output, indent=4)
        elif isinstance(output, matplotlib.figure.Figure):
            transformed_output = [
                _get_html_from_mpl_image(output, "html"),
                _get_html_from_mpl_image(output, "png"),
            ]
        elif isinstance(output, plotly.graph_objs._figure.Figure):
            transformed_output = [
                _get_html_from_plotly_image(output, "html"),
                _get_html_from_plotly_image(output, "png"),
            ]
        output_type = (
            self.resource["output_type"] if "output_type" in self.resource else None
        )
        if output_type is not None:
            if output_type == "dataframe" and isinstance(output, pd.DataFrame):
                transformed_output = output.to_csv(index=False).encode("utf-8")
            elif output_type == "document" and isinstance(output, str):
                transformed_output = str(output)
            elif output_type == "json" and isinstance(output, dict):
                transformed_output = json.dumps(output, indent=4)
        return transformed_output

    def _infer_output_type(self, output: Any) -> Optional[str]:
        if isinstance(output, pd.DataFrame) or isinstance(output, bytes):
            return "dataframe"
        elif isinstance(output, dict):
            return "json"
        elif isinstance(output, list):
            return "visualization"
        else:
            return None

    def _get_output_paths(self) -> List[str]:
        output_paths: List[str] = (
            cast(list, self.resource["output_paths"])
            if "output_paths" in self.resource
            and len(self.resource["output_paths"]) > 0
            else []
        )
        output_type = (
            self.resource["output_type"] if "output_type" in self.resource else None
        )
        # output_typeが存在してoutput_pathsが指定されていない場合はデフォルトの出力先を設定
        if output_type is not None and len(output_paths) < 1:
            output_dir = os.path.join(
                self.project_root, ProjectConfig.PRIVATE_DIR, self.resource["name"]
            )
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            if self.resource["output_type"] == "dataframe":
                output_paths = [os.path.join(output_dir, "result.csv")]
            elif self.resource["output_type"] == "visualization":
                output_paths = [
                    os.path.join(output_dir, "result.html"),
                    os.path.join(output_dir, "result.png"),
                ]
            elif self.resource["output_type"] == "document":
                output_paths = [os.path.join(output_dir, "result.md")]
            elif self.resource["output_type"] == "json":
                output_paths = [os.path.join(output_dir, "result.json")]

        return output_paths

    def _save_output_to_file(
        self, output: Union[str, bytes, List[Union[str, bytes]]], logger: logging.Logger
    ) -> Optional[List[str]]:
        output_paths: List[str] = self._get_output_paths()
        output_type = (
            self.resource["output_type"]
            if "output_type" in self.resource
            else self._infer_output_type(output)
        )

        resource_ = Resource(
            alias=self.resource["name"],
            path=self.resource["id"].split(":")[0],
            connection=self.connection,
            output_paths=output_paths,
            output_type=output_type,
        )

        resource_ = resource_.save_output_to_file(output, logger)
        return resource_.output_paths
