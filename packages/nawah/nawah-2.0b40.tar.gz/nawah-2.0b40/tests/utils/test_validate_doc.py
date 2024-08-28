import pytest

from nawah import config, utils
from nawah.classes import Attr
from nawah.exceptions import InvalidAttrException, MissingAttrException


def test_validate_doc_valid():
    attrs = {
        "attr_str": Attr.STR(),
        "attr_int": Attr.INT(),
    }
    doc = {"attr_str": "str", "attr_int": "42"}
    utils.validate_doc(mode="create", doc=doc, attrs=attrs)
    assert doc == {"attr_str": "str", "attr_int": 42}


def test_validate_doc_invalid():
    attrs = {
        "attr_str": Attr.STR(),
        "attr_int": Attr.INT(),
    }
    doc = {"attr_str": "str", "attr_int": "abc"}
    with pytest.raises(InvalidAttrException):
        utils.validate_doc(mode="create", doc=doc, attrs=attrs)


def test_validate_doc_invalid_none():
    attrs = {
        "attr_str": Attr.STR(),
        "attr_int": Attr.INT(),
    }
    doc = {"attr_str": "str", "attr_int": None}
    with pytest.raises(MissingAttrException):
        utils.validate_doc(mode="create", doc=doc, attrs=attrs)


def test_validate_doc_allow_update_valid_none():
    attrs = {
        "attr_str": Attr.STR(),
        "attr_int": Attr.INT(),
    }
    doc = {"attr_str": "str", "attr_int": None}
    utils.validate_doc(doc=doc, attrs=attrs, mode="update")
    assert doc == {"attr_str": "str", "attr_int": None}


def test_validate_doc_allow_update_list_int_str(preserve_state):
    with preserve_state(config, "Config"):
        config.Config.locales = ["ar_AE", "en_GB"]
        config.Config.locale = "ar_AE"
        attrs = {
            "attr_list_int": Attr.LIST(list=[Attr.INT()]),
        }
        doc = {"attr_list_int": {"$append": "1"}}
        utils.validate_doc(doc=doc, attrs=attrs, mode="update")
        assert doc == {"attr_list_int": {"$append": 1, "$unique": False}}


def test_validate_doc_allow_update_locale_dict_dot_notated(preserve_state):
    with preserve_state(config, "Config"):
        config.Config.locales = ["ar_AE", "en_GB"]
        config.Config.locale = "ar_AE"
        attrs = {
            "attr_locale": Attr.LOCALE(),
        }
        doc = {"attr_locale.ar_AE": "ar_AE value"}
        utils.validate_doc(doc=doc, attrs=attrs, mode="update")
        assert doc == {"attr_locale.ar_AE": "ar_AE value"}


def test_validate_doc_allow_update_kv_dict_typed_dict_time_dict_dot_notated():
    attrs = {
        "shift": Attr.KV_DICT(
            key=Attr.STR(pattern=r"[0-9]{2}"),
            val=Attr.TYPED_DICT(dict={"start": Attr.TIME(), "end": Attr.TIME()}),
        )
    }
    doc = {"shift.01.start": "09:00"}
    utils.validate_doc(doc=doc, attrs=attrs, mode="update")
    assert doc == {"shift.01.start": "09:00"}


def test_validate_doc_allow_update_list_str_dict_dot_notated():
    attrs = {"tags": Attr.LIST(list=[Attr.INT(), Attr.STR()])}
    doc = {"tags.0": "new_tag_val"}
    utils.validate_doc(doc=doc, attrs=attrs, mode="update")
    assert doc == {"tags.0": "new_tag_val"}


def test_validate_doc_allow_update_list_typed_dict_locale_dot_notated(
    preserve_state,
):
    with preserve_state(config, "Config"):
        config.Config.locales = ["en_GB", "jp_JP"]
        config.Config.locale = "en_GB"
        attrs = {
            "val": Attr.LIST(
                list=[
                    Attr.TYPED_DICT(
                        dict={"address": Attr.LOCALE(), "coords": Attr.GEO_POINT()}
                    )
                ]
            )
        }
        doc = {"val.0.address.jp_JP": "new_address"}
        utils.validate_doc(doc=doc, attrs=attrs, mode="update")
        assert doc == {"val.0.address.jp_JP": "new_address"}


def test_validate_doc_allow_update_list_typed_dict_locale_dict_dot_notated(
    preserve_state,
):
    with preserve_state(config, "Config"):
        config.Config.locales = ["en_GB", "jp_JP"]
        config.Config.locale = "en_GB"
        attrs = {
            "val": Attr.LIST(
                list=[
                    Attr.TYPED_DICT(
                        dict={"address": Attr.LOCALE(), "coords": Attr.GEO_POINT()}
                    )
                ]
            )
        }
        doc = {"val.0.address": {"en_GB": "new_address"}}
        utils.validate_doc(doc=doc, attrs=attrs, mode="update")
        assert doc == {
            "val.0.address": {
                "jp_JP": "new_address",
                "en_GB": "new_address",
            }
        }


def test_validate_doc_allow_update_list_typed_dict_locale_str_dot_notated(
    preserve_state,
):
    with preserve_state(config, "Config"):
        config.Config.locales = ["en_GB", "jp_JP"]
        config.Config.locale = "en_GB"
        attrs = {
            "val": Attr.LIST(
                list=[
                    Attr.TYPED_DICT(
                        dict={"address": Attr.LOCALE(), "coords": Attr.GEO_POINT()}
                    )
                ]
            )
        }
        doc = {"val.0.address.jp_JP": "new_address"}
        utils.validate_doc(doc=doc, attrs=attrs, mode="update")
        assert doc == {"val.0.address.jp_JP": "new_address"}
