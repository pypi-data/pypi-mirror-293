import pytest

from nawah.classes import Attr, Default
from nawah.exceptions import InvalidAttrException
from nawah.utils import validate_attr


def test_validate_attr_PHONE_None():
    with pytest.raises(InvalidAttrException):
        validate_attr(
            attr_name="test_validate_attr_PHONE",
            attr_type=Attr.PHONE(),
            attr_val=None,
            mode="create",
        )


def test_validate_attr_PHONE_int():
    with pytest.raises(InvalidAttrException):
        validate_attr(
            attr_name="test_validate_attr_PHONE",
            attr_type=Attr.PHONE(),
            attr_val=1,
            mode="create",
        )


def test_validate_attr_PHONE_str_invalid():
    with pytest.raises(InvalidAttrException):
        validate_attr(
            attr_name="test_validate_attr_PHONE",
            attr_type=Attr.PHONE(),
            attr_val="str",
            mode="create",
        )


def test_validate_attr_PHONE_phone():
    attr_val = validate_attr(
        attr_name="test_validate_attr_PHONE",
        attr_type=Attr.PHONE(),
        attr_val="+0",
        mode="create",
    )
    assert attr_val == "+0"


def test_validate_attr_PHONE_codes_phone_invalid():
    with pytest.raises(InvalidAttrException):
        validate_attr(
            attr_name="test_validate_attr_PHONE",
            attr_type=Attr.PHONE(codes=["971", "1"]),
            attr_val="+0",
            mode="create",
        )


def test_validate_attr_PHONE_codes_phone():
    attr_val = validate_attr(
        attr_name="test_validate_attr_PHONE",
        attr_type=Attr.PHONE(codes=["971", "1"]),
        attr_val="+9710",
        mode="create",
    )
    assert attr_val == "+9710"


def test_validate_attr_PHONE_None_allow_none():
    attr_val = validate_attr(
        attr_name="test_validate_attr_PHONE",
        attr_type=Attr.PHONE(),
        attr_val=None,
        mode="update",
    )
    assert attr_val == None


def test_validate_attr_PHONE_default_None():
    attr_type = Attr.PHONE()
    attr_type.default = Default(value="test_validate_attr_PHONE")
    attr_val = validate_attr(
        attr_name="test_validate_attr_PHONE",
        attr_type=attr_type,
        attr_val=None,
        mode="create",
    )
    assert attr_val == "test_validate_attr_PHONE"


def test_validate_attr_PHONE_default_int():
    attr_type = Attr.PHONE()
    attr_type.default = Default(value="test_validate_attr_PHONE")
    attr_val = validate_attr(
        attr_name="test_validate_attr_PHONE",
        attr_type=attr_type,
        attr_val=1,
        mode="create",
    )
    assert attr_val == "test_validate_attr_PHONE"


def test_validate_attr_PHONE_default_int_allow_none():
    attr_type = Attr.PHONE()
    attr_type.default = Default(value="test_validate_attr_PHONE")
    attr_val = validate_attr(
        attr_name="test_validate_attr_PHONE",
        attr_type=attr_type,
        attr_val=1,
        mode="update",
    )
    assert attr_val == None
