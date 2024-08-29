from __future__ import annotations
from dataclasses import dataclass
from ....fable_modules.fable_library.reflection import (TypeInfo, string_type, record_type)
from ....fable_modules.fable_library.types import Record
from ....fable_modules.fable_library.util import to_enumerable
from ....fable_modules.thoth_json_core.types import Json

def _expr1199() -> TypeInfo:
    return record_type("ARCtrl.Json.ROCrateContext.FactorValue.IContext", [], IContext, lambda: [("sdo", string_type), ("arc", string_type), ("FactorValue", string_type), ("ArcFactorValue", string_type), ("category", string_type), ("value", string_type), ("unit", string_type)])


@dataclass(eq = False, repr = False, slots = True)
class IContext(Record):
    sdo: str
    arc: str
    FactorValue: str
    ArcFactorValue: str
    category: str
    value: str
    unit: str

IContext_reflection = _expr1199

context_jsonvalue: Json = Json(5, to_enumerable([("sdo", Json(0, "http://schema.org/")), ("FactorValue", Json(0, "sdo:PropertyValue")), ("additionalType", Json(0, "sdo:additionalType")), ("category", Json(0, "sdo:name")), ("categoryName", Json(0, "sdo:alternateName")), ("categoryCode", Json(0, "sdo:propertyID")), ("value", Json(0, "sdo:value")), ("valueCode", Json(0, "sdo:valueReference")), ("unit", Json(0, "sdo:unitText")), ("unitCode", Json(0, "sdo:unitCode"))]))

__all__ = ["IContext_reflection", "context_jsonvalue"]

