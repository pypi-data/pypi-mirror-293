import pytest

from nawah.classes import Attr, Default
from nawah.exceptions import InvalidAttrException
from nawah.utils import validate_attr


def test_validate_attr_GEO_POINT_None():
    with pytest.raises(InvalidAttrException):
        validate_attr(
            attr_name="test_validate_attr_GEO_POINT",
            attr_type=Attr.GEO_POINT(),
            attr_val=None,
            mode="create",
        )


def test_validate_attr_GEO_POINT_int():
    with pytest.raises(InvalidAttrException):
        validate_attr(
            attr_name="test_validate_attr_GEO_POINT",
            attr_type=Attr.GEO_POINT(),
            attr_val=1,
            mode="create",
        )


def test_validate_attr_GEO_POINT_dict_invalid():
    with pytest.raises(InvalidAttrException):
        validate_attr(
            attr_name="test_validate_attr_GEO_POINT",
            attr_type=Attr.GEO_POINT(),
            attr_val={"key": "value"},
            mode="create",
        )


def test_validate_attr_GEO_POINT_geo():
    geo_attr_val = {"type": "Point", "coordinates": [21.422507, 39.826181]}
    attr_val = validate_attr(
        attr_name="test_validate_attr_GEO_POINT",
        attr_type=Attr.GEO_POINT(),
        attr_val=geo_attr_val,
        mode="create",
    )
    assert attr_val == geo_attr_val


def test_validate_attr_GEO_POINT_geo_as_str():
    with pytest.raises(InvalidAttrException):
        validate_attr(
            attr_name="test_validate_attr_GEO_POINT",
            attr_type=Attr.GEO_POINT(),
            attr_val={"type": "Point", "coordinates": ["21.422507", "39.826181"]},
            mode="create",
        )


def test_validate_attr_GEO_POINT_None_allow_none():
    attr_val = validate_attr(
        attr_name="test_validate_attr_GEO_POINT",
        attr_type=Attr.GEO_POINT(),
        attr_val=None,
        mode="update",
    )
    assert attr_val == None


def test_validate_attr_GEO_POINT_default_None():
    attr_type = Attr.GEO_POINT()
    attr_type.default = Default(value="test_validate_attr_GEO_POINT")
    attr_val = validate_attr(
        attr_name="test_validate_attr_GEO_POINT",
        attr_type=attr_type,
        attr_val=None,
        mode="create",
    )
    assert attr_val == "test_validate_attr_GEO_POINT"


def test_validate_attr_GEO_POINT_default_int():
    attr_type = Attr.GEO_POINT()
    attr_type.default = Default(value="test_validate_attr_GEO_POINT")
    attr_val = validate_attr(
        attr_name="test_validate_attr_GEO_POINT",
        attr_type=attr_type,
        attr_val=1,
        mode="create",
    )
    assert attr_val == "test_validate_attr_GEO_POINT"


def test_validate_attr_GEO_POINT_default_int_allow_none():
    attr_type = Attr.GEO_POINT()
    attr_type.default = Default(value="test_validate_attr_GEO_POINT")
    attr_val = validate_attr(
        attr_name="test_validate_attr_GEO_POINT",
        attr_type=attr_type,
        attr_val=1,
        mode="update",
    )
    assert attr_val == None
