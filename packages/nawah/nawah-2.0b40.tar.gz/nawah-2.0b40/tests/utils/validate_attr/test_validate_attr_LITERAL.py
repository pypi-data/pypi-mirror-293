import pytest

from nawah.classes import Attr, Default
from nawah.exceptions import InvalidAttrException
from nawah.utils import validate_attr


def test_validate_attr_LITERAL_None():
    with pytest.raises(InvalidAttrException):
        validate_attr(
            attr_name="test_validate_attr_LITERAL",
            attr_type=Attr.LITERAL(literal=["str", 0, 1.1]),
            attr_val=None,
            mode="create",
        )


def test_validate_attr_LITERAL_str_invalid():
    with pytest.raises(InvalidAttrException):
        validate_attr(
            attr_name="test_validate_attr_LITERAL",
            attr_type=Attr.LITERAL(literal=["str", 0, 1.1]),
            attr_val="0",
            mode="create",
        )


def test_validate_attr_LITERAL_int_invalid():
    with pytest.raises(InvalidAttrException):
        validate_attr(
            attr_name="test_validate_attr_LITERAL",
            attr_type=Attr.LITERAL(literal=["str", 0, 1.1]),
            attr_val=1,
            mode="create",
        )


def test_validate_attr_LITERAL_str():
    attr_val = validate_attr(
        attr_name="test_validate_attr_LITERAL",
        attr_type=Attr.LITERAL(literal=["str", 0, 1.1]),
        attr_val="str",
        mode="create",
    )
    assert attr_val == "str"


def test_validate_attr_LITERAL_int():
    attr_val = validate_attr(
        attr_name="test_validate_attr_LITERAL",
        attr_type=Attr.LITERAL(literal=["str", 0, 1.1]),
        attr_val=0,
        mode="create",
    )
    assert attr_val == 0


def test_validate_attr_LITERAL_None_allow_none():
    attr_val = validate_attr(
        attr_name="test_validate_attr_LITERAL",
        attr_type=Attr.LITERAL(literal=["str", 0, 1.1]),
        attr_val=None,
        mode="update",
    )
    assert attr_val == None


def test_validate_attr_LITERAL_default_None():
    attr_type = Attr.LITERAL(literal=["str", 0, 1.1])
    attr_type.default = Default(value="test_validate_attr_LITERAL")
    attr_val = validate_attr(
        attr_name="test_validate_attr_LITERAL",
        attr_type=attr_type,
        attr_val=None,
        mode="create",
    )
    assert attr_val == "test_validate_attr_LITERAL"


def test_validate_attr_LITERAL_default_int():
    attr_type = Attr.LITERAL(literal=["str", 0, 1.1])
    attr_type.default = Default(value="test_validate_attr_LITERAL")
    attr_val = validate_attr(
        attr_name="test_validate_attr_LITERAL",
        attr_type=attr_type,
        attr_val=1,
        mode="create",
    )
    assert attr_val == "test_validate_attr_LITERAL"


def test_validate_attr_LITERAL_default_int_allow_none():
    attr_type = Attr.LITERAL(literal=["str", 0, 1.1])
    attr_type.default = Default(value="test_validate_attr_LITERAL")
    attr_val = validate_attr(
        attr_name="test_validate_attr_LITERAL",
        attr_type=attr_type,
        attr_val=1,
        mode="update",
    )
    assert attr_val == None
