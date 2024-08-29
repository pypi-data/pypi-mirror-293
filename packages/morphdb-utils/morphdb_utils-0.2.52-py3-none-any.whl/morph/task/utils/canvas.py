import glob
import json
import os
from dataclasses import dataclass
from typing import Any, Dict

from morph.task.constant.project_config import ProjectConfig


@dataclass
class Canvas:
    cells: Dict[str, Dict[str, Any]]

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "Canvas":
        return Canvas(cells=data.get("cells", {}))

    def to_dict(self) -> Dict[str, Any]:
        return {"cells": self.cells}


@dataclass
class CanvasJson:
    canvases: Dict[str, Canvas]

    @staticmethod
    def load_json(project_root_path: str) -> "CanvasJson":
        canvas_json_dir_path = os.path.join(project_root_path, ProjectConfig.CANVAS_DIR)
        if not os.path.exists(canvas_json_dir_path):
            os.makedirs(canvas_json_dir_path)

        canvases: Dict[str, Canvas] = {}
        files = glob.glob(f"{canvas_json_dir_path}/**/*", recursive=True)
        for file in files:
            filename = os.path.basename(file)
            if len(filename.split(".")) != 3:
                raise AttributeError(f"{file} is not a valid canvas file")
            if filename.split(".")[-1] != "json":
                raise FileNotFoundError(f"{file} is not a valid json file")
            with open(file, "r") as f:
                try:
                    canvas_json: Dict[str, Any] = json.load(f)
                    canvas_name = os.path.basename(file).split(".")[0]
                    canvases[canvas_name] = Canvas.from_dict(canvas_json)
                except Exception as e:
                    raise AttributeError(f"{file} is not a valid json file {e}")

        return CanvasJson(canvases=canvases)
