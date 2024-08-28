import pytest
from bson import ObjectId

from nawah.classes import Attr, Default
from nawah.exceptions import InvalidAttrException
from nawah.utils import validate_attr


def test_validate_attr_ID_None():
    with pytest.raises(InvalidAttrException):
        validate_attr(
            attr_name="test_validate_attr_ID",
            attr_type=Attr.ID(),
            attr_val=None,
            mode="create",
        )


def test_validate_attr_ID_int():
    with pytest.raises(InvalidAttrException):
        validate_attr(
            attr_name="test_validate_attr_ID",
            attr_type=Attr.ID(),
            attr_val=1,
            mode="create",
        )


def test_validate_attr_ID_str():
    attr_val = validate_attr(
        attr_name="test_validate_attr_ID",
        attr_type=Attr.ID(),
        attr_val="000000000000000000000000",
        mode="create",
    )
    assert attr_val == "000000000000000000000000"


def test_validate_attr_ID_objectid():
    attr_val = validate_attr(
        attr_name="test_validate_attr_ID",
        attr_type=Attr.ID(),
        attr_val=ObjectId("000000000000000000000000"),
        mode="create",
    )
    assert attr_val == "000000000000000000000000"


def test_validate_attr_ID_None_allow_none():
    attr_val = validate_attr(
        attr_name="test_validate_attr_ID",
        attr_type=Attr.ID(),
        attr_val=None,
        mode="update",
    )
    assert attr_val == None


def test_validate_attr_ID_default_None():
    attr_type = Attr.ID()
    attr_type.default = Default(value="test_validate_attr_ID")
    attr_val = validate_attr(
        attr_name="test_validate_attr_ID",
        attr_type=attr_type,
        attr_val=None,
        mode="create",
    )
    assert attr_val == "test_validate_attr_ID"


def test_validate_attr_ID_default_int():
    attr_type = Attr.ID()
    attr_type.default = Default(value="test_validate_attr_ID")
    attr_val = validate_attr(
        attr_name="test_validate_attr_ID",
        attr_type=attr_type,
        attr_val=1,
        mode="create",
    )
    assert attr_val == "test_validate_attr_ID"


def test_validate_attr_ID_default_int_allow_none():
    attr_type = Attr.ID()
    attr_type.default = Default(value="test_validate_attr_ID")
    attr_val = validate_attr(
        attr_name="test_validate_attr_ID",
        attr_type=attr_type,
        attr_val=1,
        mode="update",
    )
    assert attr_val == None
