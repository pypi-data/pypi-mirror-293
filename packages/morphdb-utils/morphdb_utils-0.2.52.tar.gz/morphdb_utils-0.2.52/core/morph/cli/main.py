# type: ignore
import functools
from typing import Callable, Dict, Tuple, Union

import click
from morph.cli import params, requires


def global_flags(
    func: Callable[..., Tuple[Union[Dict[str, Union[str, int, bool]], None], bool]]
) -> Callable[..., Tuple[Union[Dict[str, Union[str, int, bool]], None], bool]]:
    @params.log_format
    @functools.wraps(func)
    def wrapper(
        *args: Tuple[Union[Dict[str, Union[str, int, bool]], None], bool],
        **kwargs: Dict[str, Union[str, int, bool]],
    ) -> Tuple[Union[Dict[str, Union[str, int, bool]], None], bool]:
        return func(*args, **kwargs)

    return wrapper


@click.group(
    context_settings={"help_option_names": ["-h", "--help"]},
    invoke_without_command=True,
    no_args_is_help=True,
    epilog="Specify one of these sub-commands and you can find more help from there.",
)
@click.pass_context
@global_flags
def cli(ctx: click.Context, **kwargs: Dict[str, Union[str, int, bool]]) -> None:
    """An data analysis tool for SQL transformations, visualization, and reporting.
    For more information on these commands, visit: docs.morphdb.io
    """


@cli.command("init")
@click.pass_context
@global_flags
@requires.preflight
@requires.postflight
def init(
    ctx: click.Context, **kwargs: Dict[str, Union[str, int, bool]]
) -> Tuple[Union[Dict[str, Union[str, int, bool]], None], bool]:
    from morph.task.init import InitTask

    task = InitTask(ctx.obj["flags"])
    results = task.run()
    return results, True


@cli.command("new")
@click.argument("directory_name", required=True)
@click.pass_context
@global_flags
@requires.preflight
@requires.postflight
def new(
    ctx: click.Context, directory_name: str, **kwargs: Dict[str, Union[str, int, bool]]
) -> Tuple[Union[Dict[str, Union[str, int, bool]], None], bool]:
    from morph.task.new import NewTask

    task = NewTask(ctx.obj["flags"], directory_name)
    results = task.run()
    return results, True


@cli.command("run")
@click.argument("filename", required=True)
@click.pass_context
@global_flags
@params.data
@params.run_id
@params.canvas
@params.dag
@params.dry_run
@params.no_cache
@params.connection
@requires.preflight
@requires.postflight
def run(
    ctx: click.Context, **kwargs: Dict[str, Union[str, int, bool]]
) -> Tuple[Union[Dict[str, Union[str, int, bool]], None], bool]:
    """Run sql and python file and bring the results in output file."""
    from morph.task.run import RunTask

    task = RunTask(ctx.obj["flags"])
    results = task.run()
    return results, True


@cli.command("create-file")
@click.argument("filename", required=True, type=str)
@click.argument("content", required=False, type=str, default=None)
@click.pass_context
@global_flags
@params.dag
@requires.preflight
@requires.postflight
def create_file(
    ctx: click.Context, **kwargs: Dict[str, Union[str, int, bool]]
) -> Tuple[Union[Dict[str, Union[str, int, bool]], None], bool]:
    """Create a file with specified file type."""
    from morph.task.file import CreateFileTask

    task = CreateFileTask(ctx.obj["flags"])
    results = task.run()
    return results, True


@cli.command("update-file")
@click.argument("filename", required=True, type=str)
@click.argument("content", required=True, type=str)
@click.pass_context
@global_flags
@params.dag
@requires.preflight
@requires.postflight
def update_file(
    ctx: click.Context, **kwargs: Dict[str, Union[str, int, bool]]
) -> Tuple[Union[Dict[str, Union[str, int, bool]], None], bool]:
    """Update a file content."""
    from morph.task.file import UpdateFileTask

    task = UpdateFileTask(ctx.obj["flags"])
    results = task.run()
    return results, True


@cli.command("print")
@click.pass_context
@global_flags
@params.file
@params.alias
@params.all
@params.verbose
@requires.preflight
@requires.postflight
def print_resource(
    ctx: click.Context, **kwargs: Dict[str, Union[str, int, bool]]
) -> Tuple[Union[Dict[str, Union[str, int, bool]], None], bool]:
    """Print details for the specified resource by path or alias."""
    from morph.task.resource import PrintResourceTask

    task = PrintResourceTask(ctx.obj["flags"])
    results = task.run()
    return results, True


@cli.command("compile")
@click.pass_context
@global_flags
@params.verbose
@requires.preflight
@requires.postflight
def compile(
    cts: click.Context, **kwargs: Dict[str, Union[str, int, bool]]
) -> Tuple[None, bool]:
    """Analyse morph functions into indexable objects."""
    from morph.task.compile import CompileTask

    task = CompileTask(cts.obj["flags"])
    task.run()
    return None, True


################################################################################################
# [GROUP] CREATE
################################################################################################


@cli.group()
def create():
    pass


@create.command("resource")
@click.pass_context
@global_flags
@click.argument("target")
@params.alias
@params.connection
@params.output_paths
@requires.preflight
@requires.postflight
def create_resource(
    ctx: click.Context, **kwargs: Dict[str, Union[str, int, bool]]
) -> Tuple[Union[Dict[str, Union[str, int, bool]], None], bool]:
    from morph.task.resource import CreateResourceTask

    task = CreateResourceTask(ctx.obj["flags"])
    results = task.run()
    return results, True


if __name__ == "__main__":
    cli()
