import pytest

from nawah.classes import Attr, Default
from nawah.exceptions import InvalidAttrException
from nawah.utils import validate_attr


def test_validate_attr_DICT_None():
    with pytest.raises(InvalidAttrException):
        validate_attr(
            attr_name="test_validate_attr_DICT",
            attr_type=Attr.TYPED_DICT(dict={"key": Attr.STR()}),
            attr_val=None,
            mode="create",
        )


def test_validate_attr_DICT_int():
    with pytest.raises(InvalidAttrException):
        validate_attr(
            attr_name="test_validate_attr_DICT",
            attr_type=Attr.TYPED_DICT(dict={"key": Attr.STR()}),
            attr_val=1,
            mode="create",
        )


def test_validate_attr_DICT_dict_invalid():
    with pytest.raises(InvalidAttrException):
        validate_attr(
            attr_name="test_validate_attr_DICT",
            attr_type=Attr.TYPED_DICT(dict={"key": Attr.STR()}),
            attr_val={
                "key": "value",
                "key2": "value",
            },
            mode="create",
        )


def test_validate_attr_DICT_simple_dict():
    dict_attr_val = {
        "key1": "value",
        "key2": 2,
    }
    attr_val = validate_attr(
        attr_name="test_validate_attr_DICT",
        attr_type=Attr.TYPED_DICT(dict={"key1": Attr.STR(), "key2": Attr.INT()}),
        attr_val=dict_attr_val,
        mode="create",
    )
    assert attr_val == dict_attr_val


def test_validate_attr_DICT_simple_dict_Any_None_value():
    with pytest.raises(InvalidAttrException):
        validate_attr(
            attr_name="test_validate_attr_DICT",
            attr_type=Attr.TYPED_DICT(dict={"key1": Attr.ANY(), "key2": Attr.ANY()}),
            attr_val={
                "key1": "",  # [DOC] This is accepted
                "key2": None,  # [DOC] This would fail, raising exception
            },
            mode="create",
        )


def test_validate_attr_DICT_simple_dict_Any_default_None_value():
    dict_attr_val = {
        "key1": None,
        "key2": "",
    }
    attr_type_any = Attr.ANY()
    attr_type_any.default = Default(value=None)
    attr_val = validate_attr(
        attr_name="test_validate_attr_DICT",
        attr_type=Attr.TYPED_DICT(dict={"key1": attr_type_any, "key2": attr_type_any}),
        attr_val=dict_attr_val,
        mode="create",
    )
    assert attr_val == dict_attr_val


def test_validate_attr_DICT_nested_dict_invalid():
    with pytest.raises(InvalidAttrException):
        validate_attr(
            attr_name="test_validate_attr_DICT",
            attr_type=Attr.TYPED_DICT(
                dict={
                    "key1": Attr.STR(),
                    "key2": Attr.TYPED_DICT(dict={"child_key": Attr.INT()}),
                }
            ),
            attr_val={
                "key1": "value",
                "key2": 2,
            },
            mode="create",
        )


def test_validate_attr_DICT_nested_dict():
    dict_attr_val = {
        "key1": "value",
        "key2": {"child_key": 2},
    }
    attr_val = validate_attr(
        attr_name="test_validate_attr_DICT",
        attr_type=Attr.TYPED_DICT(
            dict={
                "key1": Attr.STR(),
                "key2": Attr.TYPED_DICT(dict={"child_key": Attr.INT()}),
            }
        ),
        attr_val=dict_attr_val,
        mode="create",
    )
    assert attr_val == dict_attr_val


def test_validate_attr_DICT_nested_list_dict_invalid():
    with pytest.raises(InvalidAttrException):
        validate_attr(
            attr_name="test_validate_attr_DICT",
            attr_type=Attr.TYPED_DICT(
                dict={
                    "key1": Attr.STR(),
                    "key2": Attr.LIST(list=[Attr.INT()]),
                }
            ),
            attr_val={
                "key1": "value",
                "key2": ["a"],
            },
            mode="create",
        )


def test_validate_attr_DICT_nested_list_dict():
    attr_val = validate_attr(
        attr_name="test_validate_attr_DICT",
        attr_type=Attr.TYPED_DICT(
            dict={
                "key1": Attr.STR(),
                "key2": Attr.LIST(list=[Attr.INT()]),
            }
        ),
        attr_val={"key1": "value", "key2": [1, "2", 3]},
        mode="create",
    )
    assert attr_val == {
        "key1": "value",
        "key2": [1, 2, 3],
    }


def test_validate_attr_DICT_None_allow_none():
    attr_val = validate_attr(
        attr_name="test_validate_attr_DICT",
        attr_type=Attr.TYPED_DICT(dict={"key": Attr.STR()}),
        attr_val=None,
        mode="update",
    )
    assert attr_val == None


# [TODO] Add tests for nested default values


def test_validate_attr_DICT_default_None():
    attr_type = Attr.TYPED_DICT(dict={"key": Attr.STR()})
    attr_type.default = Default(value="test_validate_attr_DICT")
    attr_val = validate_attr(
        attr_name="test_validate_attr_DICT",
        attr_type=attr_type,
        attr_val=None,
        mode="create",
    )
    assert attr_val == "test_validate_attr_DICT"


def test_validate_attr_DICT_default_int():
    attr_type = Attr.TYPED_DICT(dict={"key": Attr.STR()})
    attr_type.default = Default(value="test_validate_attr_DICT")
    attr_val = validate_attr(
        attr_name="test_validate_attr_DICT",
        attr_type=attr_type,
        attr_val=1,
        mode="create",
    )
    assert attr_val == "test_validate_attr_DICT"


def test_validate_attr_DICT_default_int_allow_none():
    attr_type = Attr.TYPED_DICT(dict={"key": Attr.STR()})
    attr_type.default = Default(value="test_validate_attr_DICT")
    attr_val = validate_attr(
        attr_name="test_validate_attr_DICT",
        attr_type=attr_type,
        attr_val=1,
        mode="update",
    )
    assert attr_val == None
