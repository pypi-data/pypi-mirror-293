import base64
import json
import os
from dataclasses import asdict, dataclass
from typing import Dict, List, Optional

from morph.task.utils.morph import MorphYaml, Resource
from morph.task.utils.sqlite import SqliteDBManager


@dataclass
class CellCoordinates:
    x: int
    y: int
    w: int
    h: int


@dataclass
class CanvasCell:
    coordinates: CellCoordinates
    parents: List[str]


@dataclass
class CanvasPreviewResourceOutput:
    paths: List[str]  # 出力ファイルのパスのリスト
    content: str  # 出力ファイルの中身, 画像の場合はbase64


@dataclass
class CanvasPreviewResource(Resource):
    output: Optional[CanvasPreviewResourceOutput]


@dataclass
class CanvasPreview:
    version: str
    resources: Dict[str, CanvasPreviewResource]
    cells: Dict[str, CanvasCell]

    @classmethod
    def from_yaml(
        cls, morph_yaml: MorphYaml, canvas_name: str, db_manager: SqliteDBManager
    ) -> "CanvasPreview":
        # Load version
        version = morph_yaml.version

        # Load cells for the specified canvas
        cells = {}
        canvas_data = morph_yaml.canvases.get(canvas_name, {})
        if canvas_data is not None:
            for cell_alias, cell_info in canvas_data.items():
                coordinates = CellCoordinates(
                    x=cell_info["coordinates"]["x"],
                    y=cell_info["coordinates"]["y"],
                    w=cell_info["coordinates"]["w"],
                    h=cell_info["coordinates"]["h"],
                )
                cell = CanvasCell(
                    coordinates=coordinates, parents=cell_info.get("parents", [])
                )
                cells[cell_alias] = cell

        # Load only the resources that are used in the specified canvas
        resources = {}
        for cell_alias in cells.keys():
            resource_data = morph_yaml.resources.get(cell_alias)
            if resource_data:
                abs_path = resource_data["path"]
                output_extensions = MorphYaml.analyze_output_extensions(abs_path)

                image_extensions = [".png", ".jpg"]
                has_image_output = any(
                    [ext in output_extensions for ext in image_extensions]
                )

                # Retrieve the latest run record from the SQLite database
                latest_run = db_manager.find_latest_run_record(cell_alias)
                output_content: Optional[str] = None
                if latest_run and "outputs" in latest_run:
                    output_paths: List[str] = json.loads(latest_run["outputs"])
                    output_path = output_paths[0]

                    # Search for binary output if the output is an image
                    if has_image_output:
                        for output in output_paths:
                            if output.endswith(tuple(image_extensions)):
                                output_path = output
                                break

                    # Read the output file content
                    try:
                        with open(output_path, "rb") as f:
                            file_content = f.read()
                            if has_image_output:
                                output_content = base64.b64encode(file_content).decode()
                            else:
                                output_content = file_content.decode()
                    except Exception as e:
                        print(f"Error reading output file {output_path}: {e}")

                resource_output: Optional[CanvasPreviewResourceOutput] = None
                if output_content:
                    resource_output = CanvasPreviewResourceOutput(
                        paths=output_paths, content=output_content
                    )

                resource_obj = CanvasPreviewResource(
                    alias=cell_alias,
                    path=abs_path,
                    connection=resource_data.get("connection"),
                    output_paths=resource_data.get("output_paths"),
                    public=resource_data.get("public"),
                    output=resource_output,
                )
                resources[cell_alias] = resource_obj

        return cls(version=version, resources=resources, cells=cells)

    def save_to_json(
        self, project_root: str, canvas_name: Optional[str] = None
    ) -> None:
        output_dir = os.path.join(project_root, "canvases")
        os.makedirs(output_dir, exist_ok=True)

        output_file_name = (
            f"{canvas_name}.canvas-preview.json"
            if canvas_name
            else "canvas-preview.json"
        )
        output_path = os.path.join(output_dir, output_file_name)

        with open(output_path, "w") as f:
            json.dump(asdict(self), f, indent=4)
