"""__init__.pyi"""
from __future__ import annotations
from typing import TypeVar, Type

T = TypeVar("T")


class FNV1a:
    _seed: int
    _prime: int
    _mask: int

    def __init__(self) -> None:
        self.hash_list: list[int]
        self.hash_out: str | None
        self.text: str | None

    def __repr__(self) -> str:
        ...

    def hash(self, text: str | None) -> str | None:
        ...

    def _clear(self) -> None:
        ...

    def _type_check(self, value: T, value_type: Type[T]) -> None:
        ...

    def dehash(self, hash_list: list[int] | None = None) -> str | None:
        ...
