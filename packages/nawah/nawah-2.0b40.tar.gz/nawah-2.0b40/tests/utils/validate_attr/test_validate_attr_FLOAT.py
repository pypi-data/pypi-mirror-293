import pytest

from nawah.classes import Attr, Default
from nawah.exceptions import InvalidAttrException
from nawah.utils import validate_attr


def test_validate_attr_FLOAT_None():
    with pytest.raises(InvalidAttrException):
        validate_attr(
            attr_name="test_validate_attr_FLOAT",
            attr_type=Attr.FLOAT(),
            attr_val=None,
            mode="create",
        )


def test_validate_attr_FLOAT_str():
    with pytest.raises(InvalidAttrException):
        validate_attr(
            attr_name="test_validate_attr_FLOAT",
            attr_type=Attr.FLOAT(),
            attr_val="str",
            mode="create",
        )


def test_validate_attr_FLOAT_float():
    attr_val = validate_attr(
        attr_name="test_validate_attr_FLOAT",
        attr_type=Attr.FLOAT(),
        attr_val=1.1,
        mode="create",
    )
    assert attr_val == 1.1


def test_validate_attr_FLOAT_int():
    attr_val = validate_attr(
        attr_name="test_validate_attr_FLOAT",
        attr_type=Attr.FLOAT(),
        attr_val=1,
        mode="create",
    )
    assert attr_val == 1


def test_validate_attr_FLOAT_float_as_str():
    attr_val = validate_attr(
        attr_name="test_validate_attr_FLOAT",
        attr_type=Attr.FLOAT(),
        attr_val="1.1",
        mode="create",
    )
    assert attr_val == 1.1


def test_validate_attr_FLOAT_int_as_str():
    attr_val = validate_attr(
        attr_name="test_validate_attr_FLOAT",
        attr_type=Attr.FLOAT(),
        attr_val="1",
        mode="create",
    )
    assert attr_val == 1


def test_validate_attr_FLOAT_range_float_invalid():
    with pytest.raises(InvalidAttrException):
        validate_attr(
            attr_name="test_validate_attr_FLOAT",
            attr_type=Attr.FLOAT(ranges=[[0.5, 9.5]]),
            attr_val=9.5,
            mode="create",
        )


def test_validate_attr_FLOAT_range_float():
    attr_val = validate_attr(
        attr_name="test_validate_attr_FLOAT",
        attr_type=Attr.FLOAT(ranges=[[0.5, 9.5]]),
        attr_val=0.5,
        mode="create",
    )
    assert attr_val == 0.5


def test_validate_attr_FLOAT_range_float_as_str():
    attr_val = validate_attr(
        attr_name="test_validate_attr_FLOAT",
        attr_type=Attr.FLOAT(ranges=[[0.5, 9.5]]),
        attr_val="0.5",
        mode="create",
    )
    assert attr_val == 0.5


def test_validate_attr_FLOAT_None_allow_none():
    attr_val = validate_attr(
        attr_name="test_validate_attr_FLOAT",
        attr_type=Attr.FLOAT(),
        attr_val=None,
        mode="update",
    )
    assert attr_val == None


def test_validate_attr_FLOAT_default_None():
    attr_type = Attr.FLOAT()
    attr_type.default = Default(value="test_validate_attr_FLOAT")
    attr_val = validate_attr(
        attr_name="test_validate_attr_FLOAT",
        attr_type=attr_type,
        attr_val=None,
        mode="create",
    )
    assert attr_val == "test_validate_attr_FLOAT"


def test_validate_attr_FLOAT_default_str():
    attr_type = Attr.FLOAT()
    attr_type.default = Default(value="test_validate_attr_FLOAT")
    attr_val = validate_attr(
        attr_name="test_validate_attr_FLOAT",
        attr_type=attr_type,
        attr_val="str",
        mode="create",
    )
    assert attr_val == "test_validate_attr_FLOAT"


def test_validate_attr_FLOAT_default_int_allow_none():
    attr_type = Attr.FLOAT()
    attr_type.default = Default(value="test_validate_attr_FLOAT")
    attr_val = validate_attr(
        attr_name="test_validate_attr_FLOAT",
        attr_type=attr_type,
        attr_val="str",
        mode="update",
    )
    assert attr_val == None
