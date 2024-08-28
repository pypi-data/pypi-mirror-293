"""Tests 'validate_attr' Utility against attr of type 'ANY' """

# pylint: disable=invalid-name

import pytest

from nawah.classes import Attr, Default
from nawah.exceptions import InvalidAttrException
from nawah.utils import validate_attr


def test_validate_attr_ANY_None():
    """Tests invalid None-value to raise 'InvalidAttrException'"""

    with pytest.raises(InvalidAttrException):
        validate_attr(
            attr_name="test_validate_attr_ANY",
            attr_type=Attr.ANY(),
            attr_val=None,
            mode="create",
        )


def test_validate_attr_ANY_str():
    """Tests valid str-value to return value"""

    attr_val = validate_attr(
        attr_name="test_validate_attr_ANY",
        attr_type=Attr.ANY(),
        attr_val="test_validate_attr_ANY",
        mode="create",
    )
    assert attr_val == "test_validate_attr_ANY"


def test_validate_attr_ANY_default_None():
    """Tests None-value with default to return default"""

    attr_type = Attr.ANY()
    attr_type.default = Default(value="test_validate_attr_ANY")
    attr_val = validate_attr(
        attr_name="test_validate_attr_ANY",
        attr_type=attr_type,
        attr_val=None,
        mode="create",
    )
    assert attr_val == "test_validate_attr_ANY"
