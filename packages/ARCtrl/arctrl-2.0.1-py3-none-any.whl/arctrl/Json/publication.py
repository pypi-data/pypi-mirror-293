from __future__ import annotations
from collections.abc import Callable
from typing import Any
from ..fable_modules.fable_library.list import (choose, of_array, FSharpList)
from ..fable_modules.fable_library.option import default_arg
from ..fable_modules.fable_library.result import FSharpResult_2
from ..fable_modules.fable_library.string_ import (replace, to_text, printf)
from ..fable_modules.fable_library.types import Array
from ..fable_modules.fable_library.util import equals
from ..fable_modules.thoth_json_core.decode import (object, IOptionalGetter, string, IGetters)
from ..fable_modules.thoth_json_core.types import (Json, Decoder_1)
from ..fable_modules.thoth_json_python.decode import Decode_fromString
from ..fable_modules.thoth_json_python.encode import to_string
from ..Core.comment import Comment
from ..Core.ontology_annotation import OntologyAnnotation
from ..Core.publication import Publication
from .comment import (Comment_encoder, Comment_decoder, Comment_ROCrate_encoderDisambiguatingDescription, Comment_ROCrate_decoderDisambiguatingDescription, Comment_ISAJson_encoder)
from .context.rocrate.isa_publication_context import context_jsonvalue
from .decode import (Decode_uri, Decode_resizeArray, Decode_noAdditionalProperties)
from .encode import (try_include, try_include_seq, default_spaces)
from .ontology_annotation import (OntologyAnnotation_encoder, OntologyAnnotation_decoder, OntologyAnnotation_ROCrate_encoderDefinedTerm, OntologyAnnotation_ROCrate_decoderDefinedTerm)
from .person import (Person_ROCrate_encodeAuthorListString, Person_ROCrate_decodeAuthorListString)

def Publication_encoder(oa: Publication) -> Json:
    def chooser(tupled_arg: tuple[str, Json], oa: Any=oa) -> tuple[str, Json] | None:
        v: Json = tupled_arg[1]
        if equals(v, Json(3)):
            return None

        else: 
            return (tupled_arg[0], v)


    def _arrow1413(value: str, oa: Any=oa) -> Json:
        return Json(0, value)

    def _arrow1414(value_2: str, oa: Any=oa) -> Json:
        return Json(0, value_2)

    def _arrow1415(value_4: str, oa: Any=oa) -> Json:
        return Json(0, value_4)

    def _arrow1416(value_6: str, oa: Any=oa) -> Json:
        return Json(0, value_6)

    def _arrow1417(oa_1: OntologyAnnotation, oa: Any=oa) -> Json:
        return OntologyAnnotation_encoder(oa_1)

    def _arrow1418(comment: Comment, oa: Any=oa) -> Json:
        return Comment_encoder(comment)

    return Json(5, choose(chooser, of_array([try_include("pubMedID", _arrow1413, oa.PubMedID), try_include("doi", _arrow1414, oa.DOI), try_include("authorList", _arrow1415, oa.Authors), try_include("title", _arrow1416, oa.Title), try_include("status", _arrow1417, oa.Status), try_include_seq("comments", _arrow1418, oa.Comments)])))


def _arrow1425(get: IGetters) -> Publication:
    def _arrow1419(__unit: None=None) -> str | None:
        object_arg: IOptionalGetter = get.Optional
        return object_arg.Field("pubMedID", Decode_uri)

    def _arrow1420(__unit: None=None) -> str | None:
        object_arg_1: IOptionalGetter = get.Optional
        return object_arg_1.Field("doi", string)

    def _arrow1421(__unit: None=None) -> str | None:
        object_arg_2: IOptionalGetter = get.Optional
        return object_arg_2.Field("authorList", string)

    def _arrow1422(__unit: None=None) -> str | None:
        object_arg_3: IOptionalGetter = get.Optional
        return object_arg_3.Field("title", string)

    def _arrow1423(__unit: None=None) -> OntologyAnnotation | None:
        object_arg_4: IOptionalGetter = get.Optional
        return object_arg_4.Field("status", OntologyAnnotation_decoder)

    def _arrow1424(__unit: None=None) -> Array[Comment] | None:
        arg_11: Decoder_1[Array[Comment]] = Decode_resizeArray(Comment_decoder)
        object_arg_5: IOptionalGetter = get.Optional
        return object_arg_5.Field("comments", arg_11)

    return Publication(_arrow1419(), _arrow1420(), _arrow1421(), _arrow1422(), _arrow1423(), _arrow1424())


Publication_decoder: Decoder_1[Publication] = object(_arrow1425)

def Publication_ROCrate_genID(p: Publication) -> str:
    match_value: str | None = p.DOI
    if match_value is None:
        match_value_1: str | None = p.PubMedID
        if match_value_1 is None:
            match_value_2: str | None = p.Title
            if match_value_2 is None:
                return "#EmptyPublication"

            else: 
                return "#Pub_" + replace(match_value_2, " ", "_")


        else: 
            return match_value_1


    else: 
        return match_value



def Publication_ROCrate_encoder(oa: Publication) -> Json:
    def chooser(tupled_arg: tuple[str, Json], oa: Any=oa) -> tuple[str, Json] | None:
        v: Json = tupled_arg[1]
        if equals(v, Json(3)):
            return None

        else: 
            return (tupled_arg[0], v)


    def _arrow1436(value_2: str, oa: Any=oa) -> Json:
        return Json(0, value_2)

    def _arrow1437(value_4: str, oa: Any=oa) -> Json:
        return Json(0, value_4)

    def _arrow1438(author_list: str, oa: Any=oa) -> Json:
        return Person_ROCrate_encodeAuthorListString(author_list)

    def _arrow1439(value_6: str, oa: Any=oa) -> Json:
        return Json(0, value_6)

    def _arrow1440(oa_1: OntologyAnnotation, oa: Any=oa) -> Json:
        return OntologyAnnotation_ROCrate_encoderDefinedTerm(oa_1)

    def _arrow1442(comment: Comment, oa: Any=oa) -> Json:
        return Comment_ROCrate_encoderDisambiguatingDescription(comment)

    return Json(5, choose(chooser, of_array([("@id", Json(0, Publication_ROCrate_genID(oa))), ("@type", Json(0, "Publication")), try_include("pubMedID", _arrow1436, oa.PubMedID), try_include("doi", _arrow1437, oa.DOI), try_include("authorList", _arrow1438, oa.Authors), try_include("title", _arrow1439, oa.Title), try_include("status", _arrow1440, oa.Status), try_include_seq("comments", _arrow1442, oa.Comments), ("@context", context_jsonvalue)])))


def _arrow1459(get: IGetters) -> Publication:
    def _arrow1446(__unit: None=None) -> str | None:
        object_arg: IOptionalGetter = get.Optional
        return object_arg.Field("pubMedID", Decode_uri)

    def _arrow1448(__unit: None=None) -> str | None:
        object_arg_1: IOptionalGetter = get.Optional
        return object_arg_1.Field("doi", string)

    def _arrow1450(__unit: None=None) -> str | None:
        object_arg_2: IOptionalGetter = get.Optional
        return object_arg_2.Field("authorList", Person_ROCrate_decodeAuthorListString)

    def _arrow1452(__unit: None=None) -> str | None:
        object_arg_3: IOptionalGetter = get.Optional
        return object_arg_3.Field("title", string)

    def _arrow1455(__unit: None=None) -> OntologyAnnotation | None:
        object_arg_4: IOptionalGetter = get.Optional
        return object_arg_4.Field("status", OntologyAnnotation_ROCrate_decoderDefinedTerm)

    def _arrow1458(__unit: None=None) -> Array[Comment] | None:
        arg_11: Decoder_1[Array[Comment]] = Decode_resizeArray(Comment_ROCrate_decoderDisambiguatingDescription)
        object_arg_5: IOptionalGetter = get.Optional
        return object_arg_5.Field("comments", arg_11)

    return Publication(_arrow1446(), _arrow1448(), _arrow1450(), _arrow1452(), _arrow1455(), _arrow1458())


Publication_ROCrate_decoder: Decoder_1[Publication] = object(_arrow1459)

def Publication_ISAJson_encoder(id_map: Any | None, oa: Publication) -> Json:
    def chooser(tupled_arg: tuple[str, Json], id_map: Any=id_map, oa: Any=oa) -> tuple[str, Json] | None:
        v: Json = tupled_arg[1]
        if equals(v, Json(3)):
            return None

        else: 
            return (tupled_arg[0], v)


    def _arrow1463(value: str, id_map: Any=id_map, oa: Any=oa) -> Json:
        return Json(0, value)

    def _arrow1464(value_2: str, id_map: Any=id_map, oa: Any=oa) -> Json:
        return Json(0, value_2)

    def _arrow1465(value_4: str, id_map: Any=id_map, oa: Any=oa) -> Json:
        return Json(0, value_4)

    def _arrow1466(value_6: str, id_map: Any=id_map, oa: Any=oa) -> Json:
        return Json(0, value_6)

    def _arrow1467(oa_1: OntologyAnnotation, id_map: Any=id_map, oa: Any=oa) -> Json:
        return OntologyAnnotation_encoder(oa_1)

    def _arrow1468(comment: Comment, id_map: Any=id_map, oa: Any=oa) -> Json:
        return Comment_ISAJson_encoder(id_map, comment)

    return Json(5, choose(chooser, of_array([try_include("pubMedID", _arrow1463, oa.PubMedID), try_include("doi", _arrow1464, oa.DOI), try_include("authorList", _arrow1465, oa.Authors), try_include("title", _arrow1466, oa.Title), try_include("status", _arrow1467, oa.Status), try_include_seq("comments", _arrow1468, oa.Comments)])))


Publication_ISAJson_allowedFields: FSharpList[str] = of_array(["pubMedID", "doi", "authorList", "title", "status", "comments"])

Publication_ISAJson_decoder: Decoder_1[Publication] = Decode_noAdditionalProperties(Publication_ISAJson_allowedFields, Publication_decoder)

def ARCtrl_Publication__Publication_fromJsonString_Static_Z721C83C5(s: str) -> Publication:
    match_value: FSharpResult_2[Publication, str] = Decode_fromString(Publication_decoder, s)
    if match_value.tag == 1:
        raise Exception(to_text(printf("Error decoding string: %O"))(match_value.fields[0]))

    else: 
        return match_value.fields[0]



def ARCtrl_Publication__Publication_toJsonString_Static_71136F3F(spaces: int | None=None) -> Callable[[Publication], str]:
    def _arrow1469(obj: Publication, spaces: Any=spaces) -> str:
        value: Json = Publication_encoder(obj)
        return to_string(default_spaces(spaces), value)

    return _arrow1469


def ARCtrl_Publication__Publication_ToJsonString_71136F3F(this: Publication, spaces: int | None=None) -> str:
    return ARCtrl_Publication__Publication_toJsonString_Static_71136F3F(spaces)(this)


def ARCtrl_Publication__Publication_fromROCrateJsonString_Static_Z721C83C5(s: str) -> Publication:
    match_value: FSharpResult_2[Publication, str] = Decode_fromString(Publication_ROCrate_decoder, s)
    if match_value.tag == 1:
        raise Exception(to_text(printf("Error decoding string: %O"))(match_value.fields[0]))

    else: 
        return match_value.fields[0]



def ARCtrl_Publication__Publication_toROCrateJsonString_Static_71136F3F(spaces: int | None=None) -> Callable[[Publication], str]:
    def _arrow1470(obj: Publication, spaces: Any=spaces) -> str:
        value: Json = Publication_ROCrate_encoder(obj)
        return to_string(default_spaces(spaces), value)

    return _arrow1470


def ARCtrl_Publication__Publication_ToROCrateJsonString_71136F3F(this: Publication, spaces: int | None=None) -> str:
    return ARCtrl_Publication__Publication_toROCrateJsonString_Static_71136F3F(spaces)(this)


def ARCtrl_Publication__Publication_fromISAJsonString_Static_Z721C83C5(s: str) -> Publication:
    match_value: FSharpResult_2[Publication, str] = Decode_fromString(Publication_ISAJson_decoder, s)
    if match_value.tag == 1:
        raise Exception(to_text(printf("Error decoding string: %O"))(match_value.fields[0]))

    else: 
        return match_value.fields[0]



def ARCtrl_Publication__Publication_toISAJsonString_Static_Z3B036AA(spaces: int | None=None, use_idreferencing: bool | None=None) -> Callable[[Publication], str]:
    id_map: Any | None = dict([]) if default_arg(use_idreferencing, False) else None
    def _arrow1480(obj: Publication, spaces: Any=spaces, use_idreferencing: Any=use_idreferencing) -> str:
        value: Json = Publication_ISAJson_encoder(id_map, obj)
        return to_string(default_spaces(spaces), value)

    return _arrow1480


def ARCtrl_Publication__Publication_ToISAJsonString_Z3B036AA(this: Publication, spaces: int | None=None, use_idreferencing: bool | None=None) -> str:
    return ARCtrl_Publication__Publication_toISAJsonString_Static_Z3B036AA(spaces, use_idreferencing)(this)


__all__ = ["Publication_encoder", "Publication_decoder", "Publication_ROCrate_genID", "Publication_ROCrate_encoder", "Publication_ROCrate_decoder", "Publication_ISAJson_encoder", "Publication_ISAJson_allowedFields", "Publication_ISAJson_decoder", "ARCtrl_Publication__Publication_fromJsonString_Static_Z721C83C5", "ARCtrl_Publication__Publication_toJsonString_Static_71136F3F", "ARCtrl_Publication__Publication_ToJsonString_71136F3F", "ARCtrl_Publication__Publication_fromROCrateJsonString_Static_Z721C83C5", "ARCtrl_Publication__Publication_toROCrateJsonString_Static_71136F3F", "ARCtrl_Publication__Publication_ToROCrateJsonString_71136F3F", "ARCtrl_Publication__Publication_fromISAJsonString_Static_Z721C83C5", "ARCtrl_Publication__Publication_toISAJsonString_Static_Z3B036AA", "ARCtrl_Publication__Publication_ToISAJsonString_Z3B036AA"]

