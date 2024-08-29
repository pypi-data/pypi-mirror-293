from __future__ import annotations
from dataclasses import dataclass
from typing import Any
from ..fable_modules.fable_library.list import (map, choose, of_array)
from ..fable_modules.fable_library.option import (default_arg, map as map_1)
from ..fable_modules.fable_library.reflection import (TypeInfo, class_type, int32_type, string_type, record_type)
from ..fable_modules.fable_library.string_ import (join, to_text, printf)
from ..fable_modules.fable_library.system_text import (StringBuilder__ctor, StringBuilder__Append_Z721C83C5)
from ..fable_modules.fable_library.types import (to_string, Record)
from ..fable_modules.fable_library.util import (equals, ignore)
from .Helper.hash_codes import (box_hash_array, box_hash_option)

def _expr439() -> TypeInfo:
    return class_type("ARCtrl.Comment", None, Comment)


class Comment:
    def __init__(self, name: str | None=None, value: str | None=None) -> None:
        self._name: str | None = name
        self._value: str | None = value

    @property
    def Name(self, __unit: None=None) -> str | None:
        this: Comment = self
        return this._name

    @Name.setter
    def Name(self, name: str | None=None) -> None:
        this: Comment = self
        this._name = name

    @property
    def Value(self, __unit: None=None) -> str | None:
        this: Comment = self
        return this._value

    @Value.setter
    def Value(self, value: str | None=None) -> None:
        this: Comment = self
        this._value = value

    @staticmethod
    def make(name: str | None=None, value: str | None=None) -> Comment:
        return Comment(name, value)

    @staticmethod
    def create(name: str | None=None, value: str | None=None) -> Comment:
        return Comment.make(name, value)

    @staticmethod
    def to_string(comment: Comment) -> tuple[str, str]:
        return (default_arg(comment.Name, ""), default_arg(comment.Value, ""))

    def Copy(self, __unit: None=None) -> Comment:
        this: Comment = self
        name: str | None = this.Name
        value: str | None = this.Value
        return Comment.make(name, value)

    def __eq__(self, obj: Any=None) -> bool:
        this: Comment = self
        return (equals(obj.Value, this.Value) if equals(obj.Name, this.Name) else False) if isinstance(obj, Comment) else False

    def __hash__(self, __unit: None=None) -> Any:
        this: Comment = self
        return box_hash_array([box_hash_option(this.Name), box_hash_option(this.Value)])

    def __str__(self, __unit: None=None) -> str:
        this: Comment = self
        sb: Any = StringBuilder__ctor()
        ignore(StringBuilder__Append_Z721C83C5(sb, "Comment {"))
        def mapping_1(tupled_arg_1: tuple[str, str]) -> str:
            return to_text(printf("%s = %A"))(tupled_arg_1[0])(tupled_arg_1[1])

        def chooser(tupled_arg: tuple[str, str | None]) -> tuple[str, str] | None:
            def mapping(o: str, tupled_arg: Any=tupled_arg) -> tuple[str, str]:
                return (tupled_arg[0], o)

            return map_1(mapping, tupled_arg[1])

        ignore(StringBuilder__Append_Z721C83C5(sb, join(", ", map(mapping_1, choose(chooser, of_array([("Name", this.Name), ("Value", this.Value)]))))))
        ignore(StringBuilder__Append_Z721C83C5(sb, "}"))
        return to_string(sb)


Comment_reflection = _expr439

def Comment__ctor_40457300(name: str | None=None, value: str | None=None) -> Comment:
    return Comment(name, value)


def _expr440() -> TypeInfo:
    return record_type("ARCtrl.Remark", [], Remark, lambda: [("Line", int32_type), ("Value", string_type)])


@dataclass(eq = False, repr = False, slots = True)
class Remark(Record):
    Line: int
    Value: str
    @staticmethod
    def make(line: int, value: str) -> Remark:
        return Remark(line, value)

    @staticmethod
    def create(line: int, value: str) -> Remark:
        return Remark.make(line, value)

    @staticmethod
    def to_tuple(remark: Remark) -> tuple[int, str]:
        return (remark.Line, remark.Value)

    def Copy(self, __unit: None=None) -> Remark:
        this: Remark = self
        return Remark.make(this.Line, this.Value)


Remark_reflection = _expr440

__all__ = ["Comment_reflection", "Remark_reflection"]

