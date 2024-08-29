import json
from pathlib import Path

import click
from morph.cli.flags import Flags
from morph.task.base import BaseTask
from morph.task.utils.morph import find_project_root_dir
from morph.task.utils.run_backend.inspection import get_checksum
from morph.task.utils.run_backend.state import MorphGlobalContext, load_cache


class CompileTask(BaseTask):
    def __init__(self, args: Flags):
        super().__init__(args)
        self.args = args

    def run(self):
        try:
            project_root = find_project_root_dir()
        except FileNotFoundError as e:
            click.echo(click.style(str(e), fg="red"))
            raise e

        cache = load_cache(project_root)
        checksum = get_checksum(Path(project_root))
        needs_compile = True
        if cache is not None and checksum == cache["directory_checksum"]:
            needs_compile = False

        if needs_compile:
            context = MorphGlobalContext.get_instance()
            errors = context.load(project_root)
            context.dump()

        if self.args.VERBOSE:
            info: dict = {
                "needs_compile": needs_compile,
            }
            if needs_compile:
                info["errors"] = errors
            elif cache is not None:
                info["errors"] = cache["errors"]

            click.echo(json.dumps(info, indent=2))
