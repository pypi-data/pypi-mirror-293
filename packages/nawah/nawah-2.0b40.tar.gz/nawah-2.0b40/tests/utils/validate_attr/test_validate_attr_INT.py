import pytest

from nawah.classes import Attr, Default
from nawah.exceptions import InvalidAttrException
from nawah.utils import validate_attr


def test_validate_attr_INT_None():
    with pytest.raises(InvalidAttrException):
        validate_attr(
            attr_name="test_validate_attr_INT",
            attr_type=Attr.INT(),
            attr_val=None,
            mode="create",
        )


def test_validate_attr_INT_str():
    with pytest.raises(InvalidAttrException):
        validate_attr(
            attr_name="test_validate_attr_INT",
            attr_type=Attr.INT(),
            attr_val="str",
            mode="create",
        )


def test_validate_attr_INT_float():
    with pytest.raises(InvalidAttrException):
        validate_attr(
            attr_name="test_validate_attr_INT",
            attr_type=Attr.INT(),
            attr_val=1.1,
            mode="create",
        )


def test_validate_attr_INT_int():
    attr_val = validate_attr(
        attr_name="test_validate_attr_INT",
        attr_type=Attr.INT(),
        attr_val=1,
        mode="create",
    )
    assert attr_val == 1


def test_validate_attr_INT_float_as_str():
    with pytest.raises(InvalidAttrException):
        validate_attr(
            attr_name="test_validate_attr_INT",
            attr_type=Attr.INT(),
            attr_val="1.1",
            mode="create",
        )


def test_validate_attr_INT_int_as_str():
    attr_val = validate_attr(
        attr_name="test_validate_attr_INT",
        attr_type=Attr.INT(),
        attr_val="1",
        mode="create",
    )
    assert attr_val == 1


def test_validate_attr_INT_range_int_invalid():
    with pytest.raises(InvalidAttrException):
        validate_attr(
            attr_name="test_validate_attr_INT",
            attr_type=Attr.INT(ranges=[[0, 10]]),
            attr_val=10,
            mode="create",
        )


def test_validate_attr_INT_range_int():
    attr_val = validate_attr(
        attr_name="test_validate_attr_INT",
        attr_type=Attr.INT(ranges=[[0, 10]]),
        attr_val=0,
        mode="create",
    )
    assert attr_val == 0


def test_validate_attr_INT_range_int_as_str():
    attr_val = validate_attr(
        attr_name="test_validate_attr_INT",
        attr_type=Attr.INT(ranges=[[0, 10]]),
        attr_val="0",
        mode="create",
    )
    assert attr_val == 0


def test_validate_attr_INT_None_allow_none():
    attr_val = validate_attr(
        attr_name="test_validate_attr_INT",
        attr_type=Attr.INT(),
        attr_val=None,
        mode="update",
    )
    assert attr_val == None


def test_validate_attr_INT_default_None():
    attr_type = Attr.INT()
    attr_type.default = Default(value="test_validate_attr_INT")
    attr_val = validate_attr(
        attr_name="test_validate_attr_INT",
        attr_type=attr_type,
        attr_val=None,
        mode="create",
    )
    assert attr_val == "test_validate_attr_INT"


def test_validate_attr_INT_default_str():
    attr_type = Attr.INT()
    attr_type.default = Default(value="test_validate_attr_INT")
    attr_val = validate_attr(
        attr_name="test_validate_attr_INT",
        attr_type=attr_type,
        attr_val="str",
        mode="create",
    )
    assert attr_val == "test_validate_attr_INT"


def test_validate_attr_INT_default_int_allow_none():
    attr_type = Attr.INT()
    attr_type.default = Default(value="test_validate_attr_INT")
    attr_val = validate_attr(
        attr_name="test_validate_attr_INT",
        attr_type=attr_type,
        attr_val="str",
        mode="update",
    )
    assert attr_val == None
