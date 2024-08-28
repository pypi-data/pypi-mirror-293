from math import inf

import pytest

from nawah.classes import Attr, Default
from nawah.exceptions import InvalidAttrException
from nawah.utils import validate_attr


def test_validate_attr_DICT_None():
    with pytest.raises(InvalidAttrException):
        validate_attr(
            attr_name="test_validate_attr_DICT",
            attr_type=Attr.KV_DICT(key=Attr.STR(), val=Attr.ANY()),
            attr_val=None,
            mode="create",
        )


def test_validate_attr_DICT_int():
    with pytest.raises(InvalidAttrException):
        validate_attr(
            attr_name="test_validate_attr_DICT",
            attr_type=Attr.KV_DICT(key=Attr.STR(), val=Attr.ANY()),
            attr_val=1,
            mode="create",
        )


def test_validate_attr_DICT_dict_invalid():
    with pytest.raises(InvalidAttrException):
        validate_attr(
            attr_name="test_validate_attr_DICT",
            attr_type=Attr.KV_DICT(key=Attr.STR(), val=Attr.INT()),
            attr_val={
                "key": "value",
                "key2": 2,
            },
            mode="create",
        )


def test_validate_attr_DICT_simple_dict():
    dict_attr_val = {
        "key1": 3,
        "key2": 2,
    }
    attr_val = validate_attr(
        attr_name="test_validate_attr_DICT",
        attr_type=Attr.KV_DICT(key=Attr.STR(), val=Attr.ANY()),
        attr_val=dict_attr_val,
        mode="create",
    )
    assert attr_val == dict_attr_val


def test_validate_attr_DICT_nested_dict_invalid():
    with pytest.raises(InvalidAttrException):
        validate_attr(
            attr_name="test_validate_attr_DICT",
            attr_type=Attr.KV_DICT(
                key=Attr.STR(), val=Attr.KV_DICT(key=Attr.STR(), val=Attr.INT())
            ),
            attr_val={
                "key1": "value",
                "key2": 2,
            },
            mode="create",
        )


def test_validate_attr_DICT_nested_dict():
    dict_attr_val = {
        "key1": {"child_key": 1},
        "key2": {"child_key": 2},
    }
    attr_val = validate_attr(
        attr_name="test_validate_attr_DICT",
        attr_type=Attr.KV_DICT(
            key=Attr.STR(), val=Attr.KV_DICT(key=Attr.STR(), val=Attr.INT())
        ),
        attr_val=dict_attr_val,
        mode="create",
    )
    assert attr_val == dict_attr_val


def test_validate_attr_DICT_nested_list_dict_invalid():
    with pytest.raises(InvalidAttrException):
        validate_attr(
            attr_name="test_validate_attr_DICT",
            attr_type=Attr.KV_DICT(key=Attr.STR(), val=Attr.LIST(list=[Attr.INT()])),
            attr_val={
                "key1": ["a"],
            },
            mode="create",
        )


def test_validate_attr_DICT_nested_list_dict():
    attr_val = validate_attr(
        attr_name="test_validate_attr_DICT",
        attr_type=Attr.KV_DICT(key=Attr.STR(), val=Attr.LIST(list=[Attr.INT()])),
        attr_val={"key1": ["4"], "key2": [1, "2", 3]},
        mode="create",
    )
    assert attr_val == {
        "key1": [4],
        "key2": [1, 2, 3],
    }


def test_validate_attr_DICT_req_dict():
    attr_val = validate_attr(
        attr_name="test_validate_attr_DICT",
        attr_type=Attr.KV_DICT(key=Attr.STR(), val=Attr.INT(), req=["key3"]),
        attr_val={"key1": "4", "key2": 1, "key3": 0},
        mode="create",
    )
    assert attr_val == {"key1": 4, "key2": 1, "key3": 0}


def test_validate_attr_DICT_min_req_dict_invalid():
    with pytest.raises(InvalidAttrException):
        validate_attr(
            attr_name="test_validate_attr_DICT",
            attr_type=Attr.KV_DICT(
                key=Attr.STR(), val=Attr.INT(), len_range=[3, inf], req=["key3"]
            ),
            attr_val={"key1": "4", "key3": 0},
            mode="create",
        )


def test_validate_attr_DICT_min_req_max_dict_invalid():
    with pytest.raises(InvalidAttrException):
        validate_attr(
            attr_name="test_validate_attr_DICT",
            attr_type=Attr.KV_DICT(
                key=Attr.STR(), val=Attr.INT(), len_range=[3, 5], req=["key3"]
            ),
            attr_val={"key1": "4", "key2": 3, "key3": 0, "key4": 5, "key5": 2},
            mode="create",
        )


def test_validate_attr_DICT_min_req_max_dict():
    attr_val = validate_attr(
        attr_name="test_validate_attr_DICT",
        attr_type=Attr.KV_DICT(
            key=Attr.STR(), val=Attr.INT(), len_range=[3, 5], req=["key3"]
        ),
        attr_val={"key1": "4", "key2": 3, "key3": 0, "key4": 5},
        mode="create",
    )
    assert attr_val == {"key1": 4, "key2": 3, "key3": 0, "key4": 5}


def test_validate_attr_DICT_None_allow_none():
    attr_val = validate_attr(
        attr_name="test_validate_attr_DICT",
        attr_type=Attr.KV_DICT(key=Attr.STR(), val=Attr.INT()),
        attr_val=None,
        mode="update",
    )
    assert attr_val == None


# [TODO] Add tests for nested default values


def test_validate_attr_DICT_default_None():
    attr_type = Attr.KV_DICT(key=Attr.STR(), val=Attr.INT())
    attr_type.default = Default(value="test_validate_attr_DICT")
    attr_val = validate_attr(
        attr_name="test_validate_attr_DICT",
        attr_type=attr_type,
        attr_val=None,
        mode="create",
    )
    assert attr_val == "test_validate_attr_DICT"


def test_validate_attr_DICT_default_int():
    attr_type = Attr.KV_DICT(key=Attr.STR(), val=Attr.INT())
    attr_type.default = Default(value="test_validate_attr_DICT")
    attr_val = validate_attr(
        attr_name="test_validate_attr_DICT",
        attr_type=attr_type,
        attr_val=1,
        mode="create",
    )
    assert attr_val == "test_validate_attr_DICT"


def test_validate_attr_DICT_default_int_allow_none():
    attr_type = Attr.KV_DICT(key=Attr.STR(), val=Attr.INT())
    attr_type.default = Default(value="test_validate_attr_DICT")
    attr_val = validate_attr(
        attr_name="test_validate_attr_DICT",
        attr_type=attr_type,
        attr_val=1,
        mode="update",
    )
    assert attr_val == None
