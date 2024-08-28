import pytest

from nawah.classes import Attr, Default
from nawah.exceptions import InvalidAttrException
from nawah.utils import validate_attr


def test_validate_attr_UNION_None():
    with pytest.raises(InvalidAttrException):
        validate_attr(
            attr_name="test_validate_attr_UNION",
            attr_type=Attr.UNION(union=[Attr.STR(), Attr.INT()]),
            attr_val=None,
            mode="create",
        )


def test_validate_attr_UNION_float():
    with pytest.raises(InvalidAttrException):
        validate_attr(
            attr_name="test_validate_attr_UNION",
            attr_type=Attr.UNION(union=[Attr.STR(), Attr.INT()]),
            attr_val=1.1,
            mode="create",
        )


def test_validate_attr_UNION_str():
    attr_val = validate_attr(
        attr_name="test_validate_attr_UNION",
        attr_type=Attr.UNION(union=[Attr.STR(), Attr.INT()]),
        attr_val="str",
        mode="create",
    )
    assert attr_val == "str"


def test_validate_attr_UNION_int():
    attr_val = validate_attr(
        attr_name="test_validate_attr_UNION",
        attr_type=Attr.UNION(union=[Attr.STR(), Attr.INT()]),
        attr_val=1,
        mode="create",
    )
    assert attr_val == 1


def test_validate_attr_UNION_None_allow_none():
    attr_val = validate_attr(
        attr_name="test_validate_attr_UNION",
        attr_type=Attr.UNION(union=[Attr.STR(), Attr.INT()]),
        attr_val=None,
        mode="update",
    )
    assert attr_val == None


def test_validate_attr_UNION_default_None():
    attr_type = Attr.UNION(union=[Attr.STR(), Attr.INT()])
    attr_type.default = Default(value="test_validate_attr_UNION")
    attr_val = validate_attr(
        attr_name="test_validate_attr_UNION",
        attr_type=attr_type,
        attr_val=None,
        mode="create",
    )
    assert attr_val == "test_validate_attr_UNION"


def test_validate_attr_UNION_default_float():
    attr_type = Attr.UNION(union=[Attr.STR(), Attr.INT()])
    attr_type.default = Default(value="test_validate_attr_UNION")
    attr_val = validate_attr(
        attr_name="test_validate_attr_UNION",
        attr_type=attr_type,
        attr_val=1.1,
        mode="create",
    )
    assert attr_val == "test_validate_attr_UNION"


def test_validate_attr_UNION_default_float_allow_none():
    attr_type = Attr.UNION(union=[Attr.STR(), Attr.INT()])
    attr_type.default = Default(value="test_validate_attr_UNION")
    attr_val = validate_attr(
        attr_name="test_validate_attr_UNION",
        attr_type=attr_type,
        attr_val=1.1,
        mode="update",
    )
    assert attr_val == None
