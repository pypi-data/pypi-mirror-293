"""Tests 'validate_attr' Utility against attr of type 'DATE' """

# pylint: disable=invalid-name
import pytest

from nawah.classes import Attr, Default
from nawah.exceptions import InvalidAttrException
from nawah.utils import validate_attr


def test_validate_attr_DATE_None():
    with pytest.raises(InvalidAttrException):
        validate_attr(
            attr_name="test_validate_attr_DATE",
            attr_type=Attr.DATE(),
            attr_val=None,
            mode="create",
        )


def test_validate_attr_DATE_int():
    with pytest.raises(InvalidAttrException):
        validate_attr(
            attr_name="test_validate_attr_DATE",
            attr_type=Attr.DATE(),
            attr_val=1,
            mode="create",
        )


def test_validate_attr_DATE_str_invalid():
    with pytest.raises(InvalidAttrException):
        validate_attr(
            attr_name="test_validate_attr_DATE",
            attr_type=Attr.DATE(),
            attr_val="20200202",
            mode="create",
        )


def test_validate_attr_DATE_date():
    attr_val = validate_attr(
        attr_name="test_validate_attr_DATE",
        attr_type=Attr.DATE(),
        attr_val="2020-02-02",
        mode="create",
    )
    assert attr_val == "2020-02-02"


def test_validate_attr_DATE_None_allow_none():
    attr_val = validate_attr(
        attr_name="test_validate_attr_DATE",
        attr_type=Attr.DATE(),
        attr_val=None,
        mode="update",
    )
    assert attr_val == None


def test_validate_attr_DATE_default_None():
    attr_type = Attr.DATE()
    attr_type.default = Default(value="test_validate_attr_DATE")
    attr_val = validate_attr(
        attr_name="test_validate_attr_DATE",
        attr_type=attr_type,
        attr_val=None,
        mode="create",
    )
    assert attr_val == "test_validate_attr_DATE"


def test_validate_attr_DATE_default_int():
    attr_type = Attr.DATE()
    attr_type.default = Default(value="test_validate_attr_DATE")
    attr_val = validate_attr(
        attr_name="test_validate_attr_DATE",
        attr_type=attr_type,
        attr_val=1,
        mode="create",
    )
    assert attr_val == "test_validate_attr_DATE"


def test_validate_attr_DATE_default_int_allow_none():
    attr_type = Attr.DATE()
    attr_type.default = Default(value="test_validate_attr_DATE")
    attr_val = validate_attr(
        attr_name="test_validate_attr_DATE",
        attr_type=attr_type,
        attr_val=1,
        mode="update",
    )
    assert attr_val == None
