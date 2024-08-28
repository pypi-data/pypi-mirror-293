"""Tests for 'Query' class"""

from types import MappingProxyType

import pytest

from nawah.classes import Query


def test_query_no_pipe_no_special():
    """Tests 'Query' instance with no values sets 'list' for 'pipe', 'dict' for 'special'"""

    query = Query()
    assert query.pipe == ()  # pylint: disable=use-implicit-booleaness-not-comparison
    assert query.special == {}


def test_raises_invalid_pipe():
    """Tests 'Query' instance with 'str' as value for 'pipe' raises Exceptiopn"""

    with pytest.raises(Exception):
        Query("Invalid value for 'pipe'")


def test_raises_invalid_special():
    """Tests 'Query' instance with 'str' as value for 'special' raises Exceptiopn"""

    with pytest.raises(Exception):
        Query(special="Invalid value for 'special'")


def test_query_no_pipe_no_index():
    """Tests 'Query' instance with no value for 'pipe' results in empty 'dict' for 'index'"""

    query = Query()
    assert query.index == MappingProxyType({})


def test_query_no_special_no_index():
    """Tests 'Query' instance with no value for 'special' results in empty 'dict' for 'index'"""

    query = Query()
    assert query.index == MappingProxyType({})


def test_query_limit_special_no_index():
    """Tests 'Query' instance with value for 'special' results in empty 'dict' for 'index'"""

    query = Query(special={"$limit": 10})
    assert query.index == MappingProxyType({})


def test_query_pipe_single_item_two_index():
    """Tests 'Query' instance with single-item-'pipe' value results in two-entry-'index', one for
    'attr:$eq', another for 'attr:*'"""

    query = Query([{"attr": {"$eq": "value"}}])
    assert len(query.pipe) == 1
    assert len(query.index) == 2
    assert set(query.index) == {"attr:*", "attr:$eq"}


def test_query_pipe_two_item_one_attr_two_index():
    """Tests 'Query' instance with two-item-'pipe' value for same attr results in two-entry-'index'
    , one for 'attr:$eq', another for 'attr:*', both with two values"""

    query = Query([{"attr": {"$eq": "value"}}, {"attr": {"$eq": "value2"}}])
    assert len(query.pipe) == 2
    assert len(query.index) == 2
    assert set(query.index) == {"attr:*", "attr:$eq"}


def test_query_pipe_two_item_one_attr_two_oper_three_index():
    """Tests 'Query' instance with two-item-'pipe' value for same attr, with different Query
    Operators results in three-entry-'index', 'attr:$eq', 'attr:$ne', 'attr:*'"""

    query = Query([{"attr": {"$eq": "value"}}, {"attr": {"$ne": "value2"}}])
    assert len(query.pipe) == 2
    assert len(query.index) == 3
    assert set(query.index) == {"attr:*", "attr:$eq", "attr:$ne"}
