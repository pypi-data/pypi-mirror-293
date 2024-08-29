from __future__ import annotations

import inspect
from typing import Any, Callable, TypeVar, cast

from typing_extensions import ParamSpec

from .state import MorphFunctionMetaObject, MorphGlobalContext

Param = ParamSpec("Param")
RetType = TypeVar("RetType")
F = TypeVar("F", bound=Callable)


def _get_morph_function_id(func: Callable) -> str:
    if hasattr(func, "__morph_fid__"):
        return str(func.__morph_fid__)
    else:
        filename = inspect.getfile(func)
        function_name = func.__name__
        new_fid = f"{filename}:{function_name}"
        func.__morph_fid__ = new_fid  # type: ignore
        return new_fid


def _attribute_wrapper(func: F, fid: str) -> F:
    context = MorphGlobalContext.get_instance()
    func.__morph_fid__ = fid  # type: ignore
    context._update_meta_object(
        fid,
        {
            "function": func,
        },
    )
    return func


def config(
    name: str,
    description: str | None = None,
    **kwargs: dict[str, Any],
) -> Callable[[Callable[Param, RetType]], Callable[Param, RetType]]:
    context = MorphGlobalContext.get_instance()

    def decorator(func: Callable[Param, RetType]) -> Callable[Param, RetType]:
        fid = _get_morph_function_id(func)
        context._update_meta_object(
            fid,
            {
                "name": name,
                "description": description,
                **kwargs,  # type: ignore
            },
        )

        def wrapper(*args: Param.args, **kwargs: Param.kwargs) -> RetType:
            return func(*args, **kwargs)

        return _attribute_wrapper(wrapper, fid)

    return decorator


def argument(
    var_name: str,
) -> Callable[[Callable[Param, RetType]], Callable[Param, RetType]]:
    context = MorphGlobalContext.get_instance()

    def decorator(func: Callable[Param, RetType]) -> Callable[Param, RetType]:
        fid = _get_morph_function_id(func)
        meta = context._search_meta_object(fid)
        if meta is not None and "arguments" in meta:
            updated = {
                "arguments": meta["arguments"] + [var_name],
            }
        else:
            updated = {
                "arguments": [var_name],
            }
        context._update_meta_object(fid, cast(MorphFunctionMetaObject, updated))

        def wrapper(*args: Param.args, **kwargs: Param.kwargs) -> RetType:
            return func(*args, **kwargs)

        return _attribute_wrapper(wrapper, fid)

    return decorator


def load_data(
    name: str,
) -> Callable[[Callable[Param, RetType]], Callable[Param, RetType]]:
    context = MorphGlobalContext.get_instance()

    def decorator(func: Callable[Param, RetType]) -> Callable[Param, RetType]:
        fid = _get_morph_function_id(func)
        meta = context._search_meta_object(fid)
        if meta is not None and "data_requirements" in meta:
            updated = {
                "data_requirements": meta["data_requirements"] + [name],
            }
        else:
            updated = {
                "data_requirements": [name],
            }
        context._update_meta_object(fid, cast(MorphFunctionMetaObject, updated))

        def wrapper(*args: Param.args, **kwargs: Param.kwargs) -> RetType:
            return func(*args, **kwargs)

        return _attribute_wrapper(wrapper, fid)

    return decorator
