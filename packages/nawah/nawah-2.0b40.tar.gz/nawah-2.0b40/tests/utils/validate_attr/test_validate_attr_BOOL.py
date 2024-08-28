"""Tests 'validate_attr' Utility against attr of type 'BOOL' """

# pylint: disable=invalid-name

import pytest

from nawah.classes import Attr, Default
from nawah.exceptions import InvalidAttrException
from nawah.utils import validate_attr


def test_validate_attr_BOOL_None():
    """Tests invalid None-value to raise 'InvalidAttrException'"""

    with pytest.raises(InvalidAttrException):
        validate_attr(
            attr_name="test_validate_attr_BOOL",
            attr_type=Attr.BOOL(),
            attr_val=None,
            mode="create",
        )


def test_validate_attr_BOOL_int():
    """Tests invalid int-value to raise 'InvalidAttrException'"""

    with pytest.raises(InvalidAttrException):
        validate_attr(
            attr_name="test_validate_attr_BOOL",
            attr_type=Attr.BOOL(),
            attr_val=1,
            mode="create",
        )


def test_validate_attr_BOOL_bool():
    """Tests invalid bool-value to raise 'InvalidAttrException'"""

    attr_val = validate_attr(
        attr_name="test_validate_attr_BOOL",
        attr_type=Attr.BOOL(),
        attr_val=False,
        mode="create",
    )
    assert attr_val is False


def test_validate_attr_BOOL_None_allow_none():
    """Tests invalid None-value with allow_none to return None"""

    attr_val = validate_attr(
        attr_name="test_validate_attr_BOOL",
        attr_type=Attr.BOOL(),
        attr_val=None,
        mode="update",
    )
    assert attr_val is None


def test_validate_attr_BOOL_default_None():
    """Tests invalid None-value with default to return default"""

    attr_type = Attr.BOOL()
    attr_type.default = Default(value="test_validate_attr_BOOL")
    attr_val = validate_attr(
        attr_name="test_validate_attr_BOOL",
        attr_type=attr_type,
        attr_val=None,
        mode="create",
    )
    assert attr_val == "test_validate_attr_BOOL"


def test_validate_attr_BOOL_default_int():
    """Tests invalid int-value with default to return default"""

    attr_type = Attr.BOOL()
    attr_type.default = Default(value="test_validate_attr_BOOL")
    attr_val = validate_attr(
        attr_name="test_validate_attr_BOOL",
        attr_type=attr_type,
        attr_val=1,
        mode="create",
    )
    assert attr_val == "test_validate_attr_BOOL"


def test_validate_attr_BOOL_default_int_allow_none():
    """Tests invalid int-value with allow_none to return None"""

    attr_type = Attr.BOOL()
    attr_type.default = Default(value="test_validate_attr_BOOL")
    attr_val = validate_attr(
        attr_name="test_validate_attr_BOOL",
        attr_type=attr_type,
        attr_val=1,
        mode="update",
    )
    assert attr_val is None
