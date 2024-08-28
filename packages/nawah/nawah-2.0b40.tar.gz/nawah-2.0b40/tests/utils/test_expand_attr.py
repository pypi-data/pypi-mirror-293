"""Tests for 'expand_attr' Utility"""

from nawah.utils import expand_val


def test_expand_attr():
    """Tests basic functionality of 'expand_attr' Utility"""

    doc = {
        "key_1": {"child_key_1": "value"},
        "key_1.child_key_2": "value",
        "key_2.child_key_1": "value",
        "key_3.child_key_1.grand_child_key_1": "value",
    }
    expanded_doc = expand_val(doc=doc)
    assert expanded_doc == {
        "key_1": {"child_key_1": "value", "child_key_2": "value"},
        "key_2": {"child_key_1": "value"},
        "key_3": {"child_key_1": {"grand_child_key_1": "value"}},
    }


def test_expand_attr_overwrite_non_dict():
    """Tests behaviour of 'expand_attr' Utility, where it overwrites non-dict
    values as empty dict to satisfy provided path in an attr"""

    doc = {
        "key_1": {"child_key_1": "value"},
        "key_1.child_key_1.grand_child_key_1": "value",
        "key_2.child_key_1": "value",
        "key_3.child_key_1.grand_child_key_1": "value",
    }
    expanded_doc = expand_val(doc=doc)
    assert expanded_doc == {
        "key_1": {"child_key_1": {"grand_child_key_1": "value"}},
        "key_2": {"child_key_1": "value"},
        "key_3": {"child_key_1": {"grand_child_key_1": "value"}},
    }
