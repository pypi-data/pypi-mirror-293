import pytest

from nawah.classes import Attr, Default
from nawah.exceptions import InvalidAttrException
from nawah.utils import validate_attr


def test_validate_attr_LIST_None():
    with pytest.raises(InvalidAttrException):
        validate_attr(
            attr_name="test_validate_attr_LIST",
            attr_type=Attr.LIST(list=[Attr.STR()]),
            attr_val=None,
            mode="create",
        )


def test_validate_attr_LIST_int():
    with pytest.raises(InvalidAttrException):
        validate_attr(
            attr_name="test_validate_attr_LIST",
            attr_type=Attr.LIST(list=[Attr.STR()]),
            attr_val=1,
            mode="create",
        )


def test_validate_attr_LIST_dict_invalid():
    with pytest.raises(InvalidAttrException):
        validate_attr(
            attr_name="test_validate_attr_LIST",
            attr_type=Attr.LIST(list=[Attr.STR()]),
            attr_val={
                "key": "value",
                "key2": "value",
            },
            mode="create",
        )


def test_validate_attr_LIST_simple_list():
    list_attr_val = ["str", "str", "str"]
    attr_val = validate_attr(
        attr_name="test_validate_attr_LIST",
        attr_type=Attr.LIST(list=[Attr.STR()]),
        attr_val=list_attr_val,
        mode="create",
    )
    assert attr_val == list_attr_val


def test_validate_attr_LIST_nested_list_invalid():
    with pytest.raises(InvalidAttrException):
        validate_attr(
            attr_name="test_validate_attr_LIST",
            attr_type=Attr.LIST(list=[Attr.LIST(list=[Attr.STR()])]),
            attr_val=["str", "str", ["str"]],
            mode="create",
        )


def test_validate_attr_LIST_nested_list():
    list_attr_val = [["str"], ["str", "str"], ["str"]]
    attr_val = validate_attr(
        attr_name="test_validate_attr_LIST",
        attr_type=Attr.LIST(list=[Attr.LIST(list=[Attr.STR()])]),
        attr_val=list_attr_val,
        mode="create",
    )
    assert attr_val == list_attr_val


def test_validate_attr_LIST_nested_dict_invalid():
    with pytest.raises(InvalidAttrException):
        validate_attr(
            attr_name="test_validate_attr_LIST",
            attr_type=Attr.LIST(list=[Attr.KV_DICT(key=Attr.STR(), val=Attr.INT())]),
            attr_val=[{"key": 1}, {"key": "val"}],
            mode="create",
        )


def test_validate_attr_LIST_nested_dict():
    attr_val = validate_attr(
        attr_name="test_validate_attr_LIST",
        attr_type=Attr.LIST(list=[Attr.KV_DICT(key=Attr.STR(), val=Attr.INT())]),
        attr_val=[{"key": 1}, {"key": "2"}],
        mode="create",
    )
    assert attr_val == [{"key": 1}, {"key": 2}]


def test_validate_attr_LIST_muti_list_invalid():
    with pytest.raises(InvalidAttrException):
        validate_attr(
            attr_name="test_validate_attr_LIST",
            attr_type=Attr.LIST(list=[Attr.EMAIL(), Attr.URI_WEB()]),
            attr_val=["info@nawah.masaar.com", "http://sub.example.com", "1"],
            mode="create",
        )


def test_validate_attr_LIST_multi_list_invalid_count():
    with pytest.raises(InvalidAttrException):
        validate_attr(
            attr_name="test_validate_attr_LIST",
            attr_type=Attr.LIST(list=[Attr.EMAIL(), Attr.URI_WEB()], len_range=[1, 3]),
            attr_val=[
                "info@nawah.masaar.com",
                "http://sub.example.com",
                "https://sub.domain.com",
            ],
            mode="create",
        )


def test_validate_attr_LIST_typed_dict():
    list_attr_val = [
        "info@nawah.masaar.com",
        "http://sub.example.com",
        "https://sub.domain.com",
    ]
    attr_val = validate_attr(
        attr_name="test_validate_attr_LIST",
        attr_type=Attr.LIST(list=[Attr.EMAIL(), Attr.URI_WEB()], len_range=[3, 5]),
        attr_val=list_attr_val,
        mode="create",
    )
    assert attr_val == list_attr_val


def test_validate_attr_LIST_None_allow_none():
    attr_val = validate_attr(
        attr_name="test_validate_attr_LIST",
        attr_type=Attr.LIST(list=[Attr.STR()]),
        attr_val=None,
        mode="update",
    )
    assert attr_val == None


# [TODO] Add tests for nested default values


def test_validate_attr_LIST_default_None():
    attr_type = Attr.LIST(list=[Attr.STR()])
    attr_type.default = Default(value="test_validate_attr_LIST")
    attr_val = validate_attr(
        attr_name="test_validate_attr_LIST",
        attr_type=attr_type,
        attr_val=None,
        mode="create",
    )
    assert attr_val == "test_validate_attr_LIST"


def test_validate_attr_LIST_default_int():
    attr_type = Attr.LIST(list=[Attr.STR()])
    attr_type.default = Default(value="test_validate_attr_LIST")
    attr_val = validate_attr(
        attr_name="test_validate_attr_LIST",
        attr_type=attr_type,
        attr_val=[1],
        mode="create",
    )
    assert attr_val == "test_validate_attr_LIST"


def test_validate_attr_LIST_default_int_allow_none():
    attr_type = Attr.LIST(list=[Attr.STR()])
    attr_type.default = Default(value="test_validate_attr_LIST")
    attr_val = validate_attr(
        attr_name="test_validate_attr_LIST",
        attr_type=attr_type,
        attr_val=[1],
        mode="update",
    )
    assert attr_val == None


def test_validate_attr_LIST_nested_default_int():
    attr_type = Attr.LIST(list=[Attr.STR()])
    attr_type.args["list"][0].default = Default(value="test_validate_attr_LIST")
    attr_val = validate_attr(
        attr_name="test_validate_attr_LIST",
        attr_type=attr_type,
        attr_val=[1],
        mode="create",
    )
    assert attr_val == ["test_validate_attr_LIST"]


def test_validate_attr_LIST_nested_default_int_allow_none():
    attr_type = Attr.LIST(list=[Attr.STR()])
    attr_type.args["list"][0].default = Default(value="test_validate_attr_LIST")
    attr_val = validate_attr(
        attr_name="test_validate_attr_LIST",
        attr_type=attr_type,
        attr_val=[1],
        mode="update",
    )
    assert attr_val == ["test_validate_attr_LIST"]
