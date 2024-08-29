from __future__ import annotations

import logging
from io import BytesIO
from typing import Any, List, Optional

import duckdb
import pandas as pd
import requests
from jinja2 import BaseLoader, Environment
from morphdb_utils.type import SignedUrlResponse

from morph.task.utils.connections.connector import Connector
from morph.task.utils.network import Network
from morph.task.utils.profile import CONNECTION_TYPE, ProfileYaml

from .state import MorphFunctionMetaObject, MorphGlobalContext


def run_cell(
    cell: str | MorphFunctionMetaObject,
    app_url: str,
    api_key: str,
    dataase_id: str,
    vars: dict[str, dict[str, Any]] = {},
    use_cache: bool = False,
    dry_run: bool = False,
    logger: logging.Logger | None = None,
) -> Any:
    if dry_run and logger:
        cell_name = cell if isinstance(cell, str) else cell["name"]
        logger.info("Dry run mode enabled. Running cell: %s", cell_name)

    context = MorphGlobalContext.get_instance()
    if isinstance(cell, str):
        meta_obj = context._search_meta_object_by_name(cell)
        if meta_obj is None:
            raise ValueError("not registered as a morph function.")
    else:
        meta_obj = cell

    ext = meta_obj["id"].split(".")[-1]
    sql = ""
    if ext == "sql":
        sql = _regist_sql_data_requirements(meta_obj, vars)
        meta_obj = context._search_meta_object_by_name(meta_obj["name"])
        if meta_obj is None:
            raise ValueError("not registered as a morph function.")

    required_data = meta_obj.get("data_requirements", [])
    for data_name in required_data:
        required_meta_obj = context._search_meta_object_by_name(data_name)
        if required_meta_obj is None:
            raise ValueError(
                f"required data '{data_name}' is not registered as a morph function."
            )
        if use_cache:
            # TODO: 非DAG実行の場合、実行結果がどこかに保存されていることを前提にして実行している. cacheを用意し、過去の実行結果をロードする機構を実装する
            pass
        result = run_cell(
            required_meta_obj["name"], app_url, api_key, dataase_id, vars, use_cache
        )
        context._add_data(data_name, result)

    context._clear_var()
    vars_for_this = vars.get(meta_obj["name"], {})
    for var_name, var_value in vars_for_this.items():
        context._add_var(var_name, var_value)

    if "arguments" in meta_obj:
        for arg in meta_obj["arguments"]:
            if arg not in context.var:
                pass
                # TODO: add variable validation
                # raise ValueError(f"argument '{arg}' is not provided.")

    if not dry_run:
        if ext == "sql":
            return run_sql(meta_obj, sql, app_url, api_key, dataase_id)
        else:
            return meta_obj["function"](context)


def _regist_sql_data_requirements(
    resource: MorphFunctionMetaObject, vars: dict[str, dict[str, Any]] = {}
) -> str:
    context = MorphGlobalContext.get_instance()
    filepath = resource["id"]
    vars_for_this = vars.get(resource["name"], {})

    def _config(**kwargs):
        return ""

    def _argument(v: Optional[str] = None) -> str:
        return ""

    def _connection(v: Optional[str] = None) -> str:
        return ""

    load_data: List[str] = []

    def _load_data(v: Optional[str] = None) -> str:
        nonlocal load_data
        if v is not None and v != "":
            _resource = context._search_meta_object_by_name(v)
            if _resource is None:
                raise FileNotFoundError(f"A resource with alias {v} not found.")
            load_data.append(v)
            output_paths = (
                _resource["output_paths"][0] if "output_paths" in _resource else ""
            )
            return f"'{output_paths}'"
        return ""

    env = Environment(loader=BaseLoader())
    env.globals["config"] = _config
    env.globals["argument"] = _argument
    env.globals["connection"] = _connection
    env.globals["load_data"] = _load_data

    sql = open(filepath, "r").read()
    template = env.from_string(sql)
    sql = template.render(vars_for_this)
    if len(load_data) > 0:
        context._update_meta_object(resource["id"], {"data_requirements": load_data})

    return sql


def run_sql(
    resource: MorphFunctionMetaObject,
    sql: str,
    app_url: str,
    api_key: str,
    database_id: str,
) -> pd.DataFrame:
    load_data = resource["data_requirements"] if "data_requirements" in resource else []
    connection = resource["connection"] if "connection" in resource else None

    if len(load_data) > 0:
        return duckdb.sql(sql).to_df()  # type: ignore
    if Network().is_cloud():
        if connection is not None:
            cloud_connection = ProfileYaml.find_cloud_connection(connection)
            if (
                cloud_connection.type == CONNECTION_TYPE.bigquery
                or cloud_connection.type == CONNECTION_TYPE.snowflake
            ):
                connector = Connector(
                    (connection if connection is not None else ""),
                    cloud_connection,
                    is_cloud=True,
                )
                return connector.execute_sql(sql)
        else:
            cloud_connection = ProfileYaml.find_builtin_db_connection()
            connector = Connector(
                (connection if connection is not None else ""),
                cloud_connection,
                is_cloud=True,
            )
            return connector.execute_sql(sql)

    url = f"{app_url}/{database_id}/sql/csv"
    headers = {
        "x-api-key": api_key,
    }
    request = {"sql": sql}
    if connection is not None:
        request["connectionSlug"] = connection

    response = requests.post(url=url, headers=headers, json=request, verify=True)
    if response.status_code > 500:
        text = f"An error occurred while running the SQL: {response.text}"
        raise Exception(text)
    else:
        response_json = response.json()
        if (
            "error" in response_json
            and "subCode" in response_json
            and "message" in response_json
        ):
            error_message = response_json["message"]
            text = f"An error occurred while running the SQL: {error_message}"
            raise Exception(text)
        else:
            structured_response = SignedUrlResponse(url=response_json["url"])
            r = requests.get(structured_response.url)
            return pd.read_csv(BytesIO(r.content))
