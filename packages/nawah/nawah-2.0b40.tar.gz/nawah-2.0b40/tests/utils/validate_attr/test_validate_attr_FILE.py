import pytest
from bson import ObjectId

from nawah.classes import Attr, Default
from nawah.exceptions import InvalidAttrException
from nawah.utils import validate_attr


def test_validate_attr_FILE_None():
    with pytest.raises(InvalidAttrException):
        validate_attr(
            attr_name="test_validate_attr_FILE",
            attr_type=Attr.FILE(),
            attr_val=None,
            mode="create",
        )


def test_validate_attr_FILE_int():
    with pytest.raises(InvalidAttrException):
        validate_attr(
            attr_name="test_validate_attr_FILE",
            attr_type=Attr.FILE(),
            attr_val=1,
            mode="create",
        )


def test_validate_attr_FILE_dict_invalid():
    with pytest.raises(InvalidAttrException):
        validate_attr(
            attr_name="test_validate_attr_FILE",
            attr_type=Attr.FILE(),
            attr_val={"key": "value"},
            mode="create",
        )


def test_validate_attr_FILE_file():
    file_attr_val = {
        "name": "__filename",
        "type": "mime/type",
        "lastModified": 0,
        "size": 6,
        "ref": str(ObjectId()),
    }
    attr_val = validate_attr(
        attr_name="test_validate_attr_FILE",
        attr_type=Attr.FILE(),
        attr_val=file_attr_val,
        mode="create",
    )
    assert attr_val == file_attr_val


def test_validate_attr_FILE_file_list():
    file_attr_val = {
        "name": "__filename",
        "type": "mime/type",
        "lastModified": 0,
        "size": 6,
        "ref": str(ObjectId()),
    }
    attr_val = validate_attr(
        attr_name="test_validate_attr_FILE",
        attr_type=Attr.FILE(),
        attr_val=[file_attr_val],
        mode="create",
    )
    assert attr_val == file_attr_val


def test_validate_attr_FILE_None_allow_none():
    attr_val = validate_attr(
        attr_name="test_validate_attr_FILE",
        attr_type=Attr.FILE(),
        attr_val=None,
        mode="update",
    )
    assert attr_val == None


def test_validate_attr_FILE_default_None():
    attr_type = Attr.FILE()
    attr_type.default = Default(value="test_validate_attr_FILE")
    attr_val = validate_attr(
        attr_name="test_validate_attr_FILE",
        attr_type=attr_type,
        attr_val=None,
        mode="create",
    )
    assert attr_val == "test_validate_attr_FILE"


def test_validate_attr_FILE_default_int():
    attr_type = Attr.FILE()
    attr_type.default = Default(value="test_validate_attr_FILE")
    attr_val = validate_attr(
        attr_name="test_validate_attr_FILE",
        attr_type=attr_type,
        attr_val=1,
        mode="create",
    )
    assert attr_val == "test_validate_attr_FILE"


def test_validate_attr_FILE_default_int_allow_none():
    attr_type = Attr.FILE()
    attr_type.default = Default(value="test_validate_attr_FILE")
    attr_val = validate_attr(
        attr_name="test_validate_attr_FILE",
        attr_type=attr_type,
        attr_val=1,
        mode="update",
    )
    assert attr_val == None
