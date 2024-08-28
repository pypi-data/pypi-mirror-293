"""Tests 'validate_type' Utility against attr of type 'DATE' """

# pylint: disable=invalid-name
import pytest

from nawah.classes import Attr
from nawah.exceptions import InvalidAttrTypeException
from nawah.utils import validate_type


def test_validate_type_DATE_simple():
    """Tests simple Attr Type 'DATE' object"""

    validate_type(attr_type=Attr.DATE())


def test_validate_type_DATE_ranges_invalid():
    """Tests Attr Type 'DATE' object with invalid value for
    Attr Type Arg 'ranges' to raise 'InvalidAttrTypeException'"""

    with pytest.raises(InvalidAttrTypeException):
        validate_type(attr_type=Attr.DATE(ranges=[["t", "e"]]))


def test_validate_type_DATE_ranges_delta():
    """Tests Attr Type 'DATE' object with valid value for
    Attr Type Arg 'ranges'"""

    validate_type(attr_type=Attr.DATE(ranges=[["+1d", "+1w"]]))


def test_validate_type_DATE_ranges_date():
    """Tests Attr Type 'DATE' object with valid value for
    Attr Type Arg 'ranges'"""

    validate_type(attr_type=Attr.DATE(ranges=[["2021-09-01", "2022-03-31"]]))
