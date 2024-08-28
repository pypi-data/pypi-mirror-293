import pytest

from nawah.classes import Attr, Default
from nawah.exceptions import InvalidAttrException
from nawah.utils import validate_attr


def test_validate_attr_IP_None():
    with pytest.raises(InvalidAttrException):
        validate_attr(
            attr_name="test_validate_attr_IP",
            attr_type=Attr.IP(),
            attr_val=None,
            mode="create",
        )


def test_validate_attr_IP_int():
    with pytest.raises(InvalidAttrException):
        validate_attr(
            attr_name="test_validate_attr_IP",
            attr_type=Attr.IP(),
            attr_val=1,
            mode="create",
        )


def test_validate_attr_IP_str_invalid():
    with pytest.raises(InvalidAttrException):
        validate_attr(
            attr_name="test_validate_attr_IP",
            attr_type=Attr.IP(),
            attr_val="str",
            mode="create",
        )


def test_validate_attr_IP_ip():
    attr_val = validate_attr(
        attr_name="test_validate_attr_IP",
        attr_type=Attr.IP(),
        attr_val="127.0.0.1",
        mode="create",
    )
    assert attr_val == "127.0.0.1"


def test_validate_attr_IP_None_allow_none():
    attr_val = validate_attr(
        attr_name="test_validate_attr_IP",
        attr_type=Attr.IP(),
        attr_val=None,
        mode="update",
    )
    assert attr_val == None


def test_validate_attr_IP_default_None():
    attr_type = Attr.IP()
    attr_type.default = Default(value="test_validate_attr_IP")
    attr_val = validate_attr(
        attr_name="test_validate_attr_IP",
        attr_type=attr_type,
        attr_val=None,
        mode="create",
    )
    assert attr_val == "test_validate_attr_IP"


def test_validate_attr_IP_default_int():
    attr_type = Attr.IP()
    attr_type.default = Default(value="test_validate_attr_IP")
    attr_val = validate_attr(
        attr_name="test_validate_attr_IP",
        attr_type=attr_type,
        attr_val=1,
        mode="create",
    )
    assert attr_val == "test_validate_attr_IP"


def test_validate_attr_IP_default_int_allow_none():
    attr_type = Attr.IP()
    attr_type.default = Default(value="test_validate_attr_IP")
    attr_val = validate_attr(
        attr_name="test_validate_attr_IP",
        attr_type=attr_type,
        attr_val=1,
        mode="update",
    )
    assert attr_val == None
