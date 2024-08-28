import pytest

from nawah.classes import Attr, Default
from nawah.exceptions import InvalidAttrException
from nawah.utils import validate_attr


def test_validate_attr_TIME_None():
    with pytest.raises(InvalidAttrException):
        validate_attr(
            attr_name="test_validate_attr_TIME",
            attr_type=Attr.TIME(),
            attr_val=None,
            mode="create",
        )


def test_validate_attr_TIME_int():
    with pytest.raises(InvalidAttrException):
        validate_attr(
            attr_name="test_validate_attr_TIME",
            attr_type=Attr.TIME(),
            attr_val=1,
            mode="create",
        )


def test_validate_attr_TIME_str_invalid():
    with pytest.raises(InvalidAttrException):
        validate_attr(
            attr_name="test_validate_attr_TIME",
            attr_type=Attr.TIME(),
            attr_val="0000",
            mode="create",
        )


def test_validate_attr_TIME_datetime_short():
    attr_val = validate_attr(
        attr_name="test_validate_attr_TIME",
        attr_type=Attr.TIME(),
        attr_val="00:00",
        mode="create",
    )
    assert attr_val == "00:00"


def test_validate_attr_TIME_datetime_medium():
    attr_val = validate_attr(
        attr_name="test_validate_attr_TIME",
        attr_type=Attr.TIME(),
        attr_val="00:00:00",
        mode="create",
    )
    assert attr_val == "00:00:00"


def test_validate_attr_TIME_datetime_iso():
    attr_val = validate_attr(
        attr_name="test_validate_attr_TIME",
        attr_type=Attr.TIME(),
        attr_val="00:00:00.000000",
        mode="create",
    )
    assert attr_val == "00:00:00.000000"


def test_validate_attr_TIME_None_allow_none():
    attr_val = validate_attr(
        attr_name="test_validate_attr_TIME",
        attr_type=Attr.TIME(),
        attr_val=None,
        mode="update",
    )
    assert attr_val == None


def test_validate_attr_TIME_default_None():
    attr_type = Attr.TIME()
    attr_type.default = Default(value="test_validate_attr_TIME")
    attr_val = validate_attr(
        attr_name="test_validate_attr_TIME",
        attr_type=attr_type,
        attr_val=None,
        mode="create",
    )
    assert attr_val == "test_validate_attr_TIME"


def test_validate_attr_TIME_default_int():
    attr_type = Attr.TIME()
    attr_type.default = Default(value="test_validate_attr_TIME")
    attr_val = validate_attr(
        attr_name="test_validate_attr_TIME",
        attr_type=attr_type,
        attr_val=1,
        mode="create",
    )
    assert attr_val == "test_validate_attr_TIME"


def test_validate_attr_TIME_default_int_allow_none():
    attr_type = Attr.TIME()
    attr_type.default = Default(value="test_validate_attr_TIME")
    attr_val = validate_attr(
        attr_name="test_validate_attr_TIME",
        attr_type=attr_type,
        attr_val=1,
        mode="update",
    )
    assert attr_val == None
