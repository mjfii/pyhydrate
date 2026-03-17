from pathlib import Path
from typing import Any, Union

from .notation import NotationArray, NotationObject, NotationPrimitive
from .notation.notation_base import NotationBase

class PyHydrate(NotationBase):
    _root_type: type
    _source_path: Path | None
    _structure: NotationObject | NotationArray | NotationPrimitive | None

    def __init__(
        self,
        source_value: Union[
            dict, list, str, float, bool, tuple, set, frozenset, range, None
        ] = ...,
        *,
        path: Union[str, Path, None] = ...,
        **kwargs: Any,
    ) -> None: ...
    def __int__(self) -> int: ...
    def __float__(self) -> float: ...
    def __bool__(self) -> bool: ...
    def __getattr__(self, key: str) -> Any: ...
    def __getitem__(
        self, index: int | None
    ) -> NotationArray | NotationObject | NotationPrimitive | None: ...
    def __setattr__(self, key: str, value: Any) -> None: ...
    def __setitem__(self, index: int, value: Any) -> None: ...
    def __delattr__(self, key: str) -> None: ...
    def __delitem__(self, index: int) -> None: ...
    def __call__(
        self, *args: Any
    ) -> dict | list | str | int | float | bool | type | None: ...
    def save(
        self,
        path: str | Path | None = ...,
        *,
        output_format: str | None = ...,
        original_keys: bool = ...,
    ) -> None: ...
