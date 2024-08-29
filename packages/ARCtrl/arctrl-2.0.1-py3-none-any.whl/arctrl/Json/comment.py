from __future__ import annotations
from collections.abc import Callable
from typing import Any
from ..fable_modules.fable_library.list import (choose, of_array)
from ..fable_modules.fable_library.option import value as value_6
from ..fable_modules.fable_library.result import FSharpResult_2
from ..fable_modules.fable_library.string_ import (replace, to_text, printf)
from ..fable_modules.fable_library.util import equals
from ..fable_modules.thoth_json_core.decode import (object, IOptionalGetter, string, IGetters, map)
from ..fable_modules.thoth_json_core.types import (Json, Decoder_1)
from ..fable_modules.thoth_json_python.decode import Decode_fromString
from ..fable_modules.thoth_json_python.encode import to_string
from ..Core.comment import Comment
from .context.rocrate.isa_comment_context import context_jsonvalue
from .encode import (try_include, default_spaces)
from .idtable import encode

def Comment_encoder(comment: Comment) -> Json:
    def chooser(tupled_arg: tuple[str, Json], comment: Any=comment) -> tuple[str, Json] | None:
        v: Json = tupled_arg[1]
        if equals(v, Json(3)):
            return None

        else: 
            return (tupled_arg[0], v)


    def _arrow1244(value: str, comment: Any=comment) -> Json:
        return Json(0, value)

    def _arrow1245(value_2: str, comment: Any=comment) -> Json:
        return Json(0, value_2)

    return Json(5, choose(chooser, of_array([try_include("name", _arrow1244, comment.Name), try_include("value", _arrow1245, comment.Value)])))


def _arrow1248(get: IGetters) -> Comment:
    def _arrow1246(__unit: None=None) -> str | None:
        object_arg: IOptionalGetter = get.Optional
        return object_arg.Field("name", string)

    def _arrow1247(__unit: None=None) -> str | None:
        object_arg_1: IOptionalGetter = get.Optional
        return object_arg_1.Field("value", string)

    return Comment(_arrow1246(), _arrow1247())


Comment_decoder: Decoder_1[Comment] = object(_arrow1248)

def Comment_ROCrate_genID(c: Comment) -> str:
    match_value: str | None = c.Name
    if match_value is None:
        return "#EmptyComment"

    else: 
        n: str = match_value
        v: str = ("_" + replace(value_6(c.Value), " ", "_")) if (c.Value is not None) else ""
        return ("#Comment_" + replace(n, " ", "_")) + v



def Comment_ROCrate_encoder(comment: Comment) -> Json:
    def chooser(tupled_arg: tuple[str, Json], comment: Any=comment) -> tuple[str, Json] | None:
        v: Json = tupled_arg[1]
        if equals(v, Json(3)):
            return None

        else: 
            return (tupled_arg[0], v)


    def _arrow1249(value_2: str, comment: Any=comment) -> Json:
        return Json(0, value_2)

    def _arrow1250(value_4: str, comment: Any=comment) -> Json:
        return Json(0, value_4)

    return Json(5, choose(chooser, of_array([("@id", Json(0, Comment_ROCrate_genID(comment))), ("@type", Json(0, "Comment")), try_include("name", _arrow1249, comment.Name), try_include("value", _arrow1250, comment.Value), ("@context", context_jsonvalue)])))


def _arrow1253(get: IGetters) -> Comment:
    def _arrow1251(__unit: None=None) -> str | None:
        object_arg: IOptionalGetter = get.Optional
        return object_arg.Field("name", string)

    def _arrow1252(__unit: None=None) -> str | None:
        object_arg_1: IOptionalGetter = get.Optional
        return object_arg_1.Field("value", string)

    return Comment(_arrow1251(), _arrow1252())


Comment_ROCrate_decoder: Decoder_1[Comment] = object(_arrow1253)

def Comment_ROCrate_encoderDisambiguatingDescription(comment: Comment) -> Json:
    return Json(0, to_string(0, Comment_ROCrate_encoder(comment)))


def ctor(s: str) -> Comment:
    match_value: FSharpResult_2[Comment, str] = Decode_fromString(Comment_ROCrate_decoder, s.strip())
    if match_value.tag == 1:
        raise Exception(to_text(printf("Error decoding string: %O"))(match_value.fields[0]))

    else: 
        return match_value.fields[0]



Comment_ROCrate_decoderDisambiguatingDescription: Decoder_1[Comment] = map(ctor, string)

def Comment_ISAJson_encoder(id_map: Any | None, comment: Comment) -> Json:
    def f(comment_1: Comment, id_map: Any=id_map, comment: Any=comment) -> Json:
        def chooser(tupled_arg: tuple[str, Json], comment_1: Any=comment_1) -> tuple[str, Json] | None:
            v: Json = tupled_arg[1]
            if equals(v, Json(3)):
                return None

            else: 
                return (tupled_arg[0], v)


        def _arrow1255(value: str, comment_1: Any=comment_1) -> Json:
            return Json(0, value)

        def _arrow1256(value_2: str, comment_1: Any=comment_1) -> Json:
            return Json(0, value_2)

        def _arrow1257(value_4: str, comment_1: Any=comment_1) -> Json:
            return Json(0, value_4)

        return Json(5, choose(chooser, of_array([try_include("@id", _arrow1255, Comment_ROCrate_genID(comment_1)), try_include("name", _arrow1256, comment_1.Name), try_include("value", _arrow1257, comment_1.Value)])))

    if id_map is None:
        return f(comment)

    else: 
        def _arrow1258(c: Comment, id_map: Any=id_map, comment: Any=comment) -> str:
            return Comment_ROCrate_genID(c)

        return encode(_arrow1258, f, comment, id_map)



Comment_ISAJson_decoder: Decoder_1[Comment] = Comment_decoder

def ARCtrl_Comment__Comment_fromJsonString_Static_Z721C83C5(s: str) -> Comment:
    match_value: FSharpResult_2[Comment, str] = Decode_fromString(Comment_decoder, s)
    if match_value.tag == 1:
        raise Exception(to_text(printf("Error decoding string: %O"))(match_value.fields[0]))

    else: 
        return match_value.fields[0]



def ARCtrl_Comment__Comment_toJsonString_Static_71136F3F(spaces: int | None=None) -> Callable[[Comment], str]:
    def _arrow1259(c: Comment, spaces: Any=spaces) -> str:
        value: Json = Comment_encoder(c)
        return to_string(default_spaces(spaces), value)

    return _arrow1259


def ARCtrl_Comment__Comment_toJsonString_71136F3F(this: Comment, spaces: int | None=None) -> str:
    return ARCtrl_Comment__Comment_toJsonString_Static_71136F3F(spaces)(this)


def ARCtrl_Comment__Comment_fromROCrateJsonString_Static_Z721C83C5(s: str) -> Comment:
    match_value: FSharpResult_2[Comment, str] = Decode_fromString(Comment_ROCrate_decoder, s)
    if match_value.tag == 1:
        raise Exception(to_text(printf("Error decoding string: %O"))(match_value.fields[0]))

    else: 
        return match_value.fields[0]



def ARCtrl_Comment__Comment_toROCrateJsonString_Static_71136F3F(spaces: int | None=None) -> Callable[[Comment], str]:
    def _arrow1260(c: Comment, spaces: Any=spaces) -> str:
        value: Json = Comment_ROCrate_encoder(c)
        return to_string(default_spaces(spaces), value)

    return _arrow1260


def ARCtrl_Comment__Comment_toROCrateJsonString_71136F3F(this: Comment, spaces: int | None=None) -> str:
    return ARCtrl_Comment__Comment_toROCrateJsonString_Static_71136F3F(spaces)(this)


def ARCtrl_Comment__Comment_fromISAJsonString_Static_Z721C83C5(s: str) -> Comment:
    match_value: FSharpResult_2[Comment, str] = Decode_fromString(Comment_ISAJson_decoder, s)
    if match_value.tag == 1:
        raise Exception(to_text(printf("Error decoding string: %O"))(match_value.fields[0]))

    else: 
        return match_value.fields[0]



def ARCtrl_Comment__Comment_toISAJsonString_Static_71136F3F(spaces: int | None=None) -> Callable[[Comment], str]:
    def _arrow1261(c: Comment, spaces: Any=spaces) -> str:
        value: Json = Comment_ISAJson_encoder(None, c)
        return to_string(default_spaces(spaces), value)

    return _arrow1261


def ARCtrl_Comment__Comment_toISAJsonString_71136F3F(this: Comment, spaces: int | None=None) -> str:
    return ARCtrl_Comment__Comment_toISAJsonString_Static_71136F3F(spaces)(this)


__all__ = ["Comment_encoder", "Comment_decoder", "Comment_ROCrate_genID", "Comment_ROCrate_encoder", "Comment_ROCrate_decoder", "Comment_ROCrate_encoderDisambiguatingDescription", "Comment_ROCrate_decoderDisambiguatingDescription", "Comment_ISAJson_encoder", "Comment_ISAJson_decoder", "ARCtrl_Comment__Comment_fromJsonString_Static_Z721C83C5", "ARCtrl_Comment__Comment_toJsonString_Static_71136F3F", "ARCtrl_Comment__Comment_toJsonString_71136F3F", "ARCtrl_Comment__Comment_fromROCrateJsonString_Static_Z721C83C5", "ARCtrl_Comment__Comment_toROCrateJsonString_Static_71136F3F", "ARCtrl_Comment__Comment_toROCrateJsonString_71136F3F", "ARCtrl_Comment__Comment_fromISAJsonString_Static_Z721C83C5", "ARCtrl_Comment__Comment_toISAJsonString_Static_71136F3F", "ARCtrl_Comment__Comment_toISAJsonString_71136F3F"]

