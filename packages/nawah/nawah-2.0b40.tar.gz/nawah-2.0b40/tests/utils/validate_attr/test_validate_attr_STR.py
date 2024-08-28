import pytest

from nawah.classes import Attr, Default
from nawah.exceptions import InvalidAttrException
from nawah.utils import validate_attr


def test_validate_attr_STR_None():
    with pytest.raises(InvalidAttrException):
        validate_attr(
            attr_name="test_validate_attr_STR",
            attr_type=Attr.STR(),
            attr_val=None,
            mode="create",
        )


def test_validate_attr_STR_int():
    with pytest.raises(InvalidAttrException):
        validate_attr(
            attr_name="test_validate_attr_STR",
            attr_type=Attr.STR(),
            attr_val=1,
            mode="create",
        )


def test_validate_attr_STR_str():
    attr_val = validate_attr(
        attr_name="test_validate_attr_STR",
        attr_type=Attr.STR(),
        attr_val="test_validate_attr_STR",
        mode="create",
    )
    assert attr_val == "test_validate_attr_STR"


def test_validate_attr_STR_pattern_str_invalid():
    with pytest.raises(InvalidAttrException):
        validate_attr(
            attr_name="test_validate_attr_STR",
            attr_type=Attr.STR(pattern=r"[a-z_]+"),
            attr_val="test_validate_attr_STR",
            mode="create",
        )


def test_validate_attr_STR_pattern_str():
    attr_val = validate_attr(
        attr_name="test_validate_attr_STR",
        attr_type=Attr.STR(pattern=r"[a-zA-Z_]+"),
        attr_val="test_validate_attr_STR",
        mode="create",
    )
    assert attr_val == "test_validate_attr_STR"


def test_validate_attr_STR_None_allow_none():
    attr_val = validate_attr(
        attr_name="test_validate_attr_STR",
        attr_type=Attr.STR(),
        attr_val=None,
        mode="update",
    )
    assert attr_val == None


def test_validate_attr_STR_default_None():
    attr_type = Attr.STR()
    attr_type.default = Default(value="test_validate_attr_STR")
    attr_val = validate_attr(
        attr_name="test_validate_attr_STR",
        attr_type=attr_type,
        attr_val=None,
        mode="create",
    )
    assert attr_val == "test_validate_attr_STR"


def test_validate_attr_STR_default_int():
    attr_type = Attr.STR()
    attr_type.default = Default(value="test_validate_attr_STR")
    attr_val = validate_attr(
        attr_name="test_validate_attr_STR",
        attr_type=attr_type,
        attr_val=1,
        mode="create",
    )
    assert attr_val == "test_validate_attr_STR"


def test_validate_attr_STR_default_int_allow_none():
    attr_type = Attr.STR()
    attr_type.default = Default(value="test_validate_attr_STR")
    attr_val = validate_attr(
        attr_name="test_validate_attr_STR",
        attr_type=attr_type,
        attr_val=1,
        mode="update",
    )
    assert attr_val == None
