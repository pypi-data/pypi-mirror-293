"""Tests for 'extract_attr' Utility"""

from nawah.utils import extract_val


def test_extract_attr_item(attr_obj):
    """Tests extracting top-level attr"""

    attr_val = extract_val(scope=attr_obj, path="item2")
    assert attr_val == "val2"


def test_extract_attr_list_item(attr_obj):
    """Tests extracting nested list item, with variable prefix"""

    attr_val = extract_val(scope=attr_obj, path="$__list_item1.1")
    assert attr_val == "list_child2"


def test_extract_attr_dict_item(attr_obj):
    """Tests extracting nested dict item"""

    attr_val = extract_val(scope=attr_obj, path="dict_item1.dict_child2")
    assert attr_val == "child_val2"


def test_extract_attr_nested_dict_item(attr_obj):
    """Tests extracting deep nested dict item, with variable prefix"""

    attr_val = extract_val(
        scope=attr_obj, path="$__nested_dict.child_dict.child_child_item1"
    )
    assert attr_val == "child_child_val1"


def test_extract_attr_nested_list_item(attr_obj):
    """Tests extracting item from nested list"""

    attr_val = extract_val(scope=attr_obj, path="nested_list.1.0")
    assert attr_val == "child_child_item21"


def test_extract_attr_nested_obj_list_item(attr_obj):
    """Tests extracting dict item from list nested in dict"""

    attr_val = extract_val(scope=attr_obj, path="nested_obj.list.1.item2")
    assert attr_val == "val2"


def test_extract_attr_nested_obj_dict_item(attr_obj):
    """Tests extracting list item from nested dict, with variable prefix"""

    attr_val = extract_val(scope=attr_obj, path="$__nested_obj.dict.list.0")
    assert attr_val == "item1"


def test_extract_attr_nested_dict_list_dict(attr_obj):
    """Tests extracting dict using JSONPath filters"""

    attr_val = extract_val(
        scope=attr_obj, path='$__nested_dict_list[?(@.item=="nested_1")]'
    )
    assert attr_val == {"item": "nested_1", "val": "nested_1_val"}


def test_extract_attr_nested_dict_list_item(attr_obj):
    """Tests extracting item using JSONPath filters"""

    attr_val = extract_val(
        scope=attr_obj, path='$__nested_dict_list[?(@.item=="nested_2")].val'
    )
    assert attr_val == "nested_2_val"
