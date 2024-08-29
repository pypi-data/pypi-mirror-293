from __future__ import annotations
from dataclasses import dataclass
from ....fable_modules.fable_library.reflection import (TypeInfo, string_type, record_type)
from ....fable_modules.fable_library.types import Record
from ....fable_modules.fable_library.util import to_enumerable
from ....fable_modules.thoth_json_core.types import Json

def _expr1201() -> TypeInfo:
    return record_type("ARCtrl.Json.ROCrateContext.MaterialAttribute.IContext", [], IContext, lambda: [("sdo", string_type), ("arc", string_type), ("MaterialAttribute", string_type), ("ArcMaterialAttribute", string_type), ("characteristic_type", string_type)])


@dataclass(eq = False, repr = False, slots = True)
class IContext(Record):
    sdo: str
    arc: str
    MaterialAttribute: str
    ArcMaterialAttribute: str
    characteristic_type: str

IContext_reflection = _expr1201

context_jsonvalue: Json = Json(5, to_enumerable([("sdo", Json(0, "http://schema.org/")), ("arc", Json(0, "http://purl.org/nfdi4plants/ontology/")), ("MaterialAttribute", Json(0, "sdo:Property")), ("ArcMaterialAttribute", Json(0, "arc:ARC#ARC_00000050")), ("characteristicType", Json(0, "arc:ARC#ARC_00000098"))]))

context_str: str = "\r\n{\r\n  \"@context\": {\r\n    \"sdo\": \"http://schema.org/\",\r\n    \"arc\": \"http://purl.org/nfdi4plants/ontology/\",\r\n\r\n    \"MaterialAttribute\": \"sdo:Property\",\r\n    \"ArcMaterialAttribute\": \"arc:ARC#ARC_00000050\",\r\n\r\n    \"characteristicType\": \"arc:ARC#ARC_00000098\"\r\n  }\r\n}\r\n    "

__all__ = ["IContext_reflection", "context_jsonvalue", "context_str"]

