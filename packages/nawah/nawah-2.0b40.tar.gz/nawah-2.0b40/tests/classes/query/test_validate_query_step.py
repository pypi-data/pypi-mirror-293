"""Tests for 'validate_query_step' Utility"""

import pytest
from bson import ObjectId

from nawah.classes._query import _validate_query_step
from nawah.exceptions import (InvalidQueryOperTypeException,
                              InvalidQueryStepAttrLenException,
                              InvalidQueryStepAttrTypeException,
                              InvalidQueryStepLenException,
                              InvalidQueryStepTypeException,
                              UnknownQueryOperException)


def test_validate_query_step_str():
    """Tests '_validate_query_step' raises 'InvalidQueryStepTypeException' if passed step not of
    type dict"""

    with pytest.raises(InvalidQueryStepTypeException):
        _validate_query_step("Invalid Query step", allow_var=False)


def test_validate_query_step_two_items():
    """Tests '_validate_query_step' raises 'InvalidQueryStepLenException' if passed step with
    two items"""

    with pytest.raises(InvalidQueryStepLenException):
        _validate_query_step({"two": "items", "invalid": "step"}, allow_var=False)


def test_validate_query_step_attr_str():
    """Tests '_validate_query_step' raises 'InvalidQueryStepAttrTypeException' if passed step attr
    not of type dict"""

    with pytest.raises(InvalidQueryStepAttrTypeException):
        _validate_query_step({"invalid": "Query step attr"}, allow_var=False)


def test_validate_query_step_attr_two_items():
    """Tests '_validate_query_step' raises 'InvalidQueryStepAttrLenException' if passed step with
    two items"""

    with pytest.raises(InvalidQueryStepAttrLenException):
        _validate_query_step(
            {"two": {"items": "invalid", "Query": "step attr"}}, allow_var=False
        )


def test_validate_query_step_unknown_oper():
    """Tests '_validate_query_step' raises 'UnknownQueryOperException' if passed step with unknown
    Query Operator"""

    with pytest.raises(UnknownQueryOperException):
        _validate_query_step({"two": {"$invalid": "oper"}}, allow_var=False)


def test_validate_query_step_valid_oper_eq():
    """Tests '_validate_query_step' validates step attr with Query Operator '$eq' against types
    'str', 'int', 'float', 'list', 'dict', 'ObjectId'"""

    object_id = ObjectId()

    step = {"attr": {"$eq": "Valid"}}
    _validate_query_step(step, allow_var=False)
    assert step == {"attr": {"$eq": "Valid"}}

    step = {"attr": {"$eq": -1}}
    _validate_query_step(step, allow_var=False)
    assert step == {"attr": {"$eq": -1}}

    step = {"attr": {"$eq": -1.1}}
    _validate_query_step(step, allow_var=False)
    assert step == {"attr": {"$eq": -1.1}}

    step = {"attr": {"$eq": ["Valid", -1, 0.1, [], {}, object_id]}}
    _validate_query_step(step, allow_var=False)
    assert step == {"attr": {"$eq": ["Valid", -1, 0.1, [], {}, object_id]}}

    step = {"attr": {"$eq": {"valid": ["Valid", 0, 0.1, [], {}, object_id]}}}
    _validate_query_step(step, allow_var=False)
    assert step == {"attr": {"$eq": {"valid": ["Valid", 0, 0.1, [], {}, object_id]}}}

    step = {"attr": {"$eq": object_id}}
    _validate_query_step(step, allow_var=False)
    assert step == {"attr": {"$eq": object_id}}


def test_validate_query_step_invalid_oper_eq():
    """Tests '_validate_query_step' validates step attr with Query Operator '$eq' against types
    invalid types"""

    # Test type bytes
    with pytest.raises(InvalidQueryOperTypeException):
        _validate_query_step({"attr": {"$eq": b""}}, allow_var=False)

    # Test type tuple
    with pytest.raises(InvalidQueryOperTypeException):
        _validate_query_step({"attr": {"$eq": tuple("Invalid")}}, allow_var=False)

    # Test type set
    with pytest.raises(InvalidQueryOperTypeException):
        _validate_query_step({"attr": {"$eq": set("Invalid")}}, allow_var=False)

    # Test type object
    with pytest.raises(InvalidQueryOperTypeException):
        _validate_query_step({"attr": {"$eq": object()}}, allow_var=False)

    # Test type object
    with pytest.raises(InvalidQueryOperTypeException):
        _validate_query_step({"attr": {"$eq": object()}}, allow_var=False)


def test_valid_query_step_valid_oper_eq_key_id():
    """Tests '_validate_query_step' validates step attr with Query Operator '$eq' with key '_id'
    to convert value to 'ObjectId' type"""

    object_id = ObjectId()
    step_object_id = {"_id": {"$eq": object_id}}
    step_str = {"_id": {"$eq": str(object_id)}}
    step_list_object_id = {"_id": {"$eq": [object_id, object_id]}}
    step_list_str = {"_id": {"$eq": [str(object_id), str(object_id)]}}

    _validate_query_step(step_object_id, allow_var=False)
    assert step_object_id == {"_id": {"$eq": object_id}}

    _validate_query_step(step_str, allow_var=False)
    assert step_str == {"_id": {"$eq": object_id}}

    _validate_query_step(step_list_object_id, allow_var=False)
    assert step_list_object_id == {"_id": {"$eq": [object_id, object_id]}}

    _validate_query_step(step_list_str, allow_var=False)
    assert step_list_str == {"_id": {"$eq": [object_id, object_id]}}


def test_valid_query_step_valid_oper_in_key_id():
    """Tests '_validate_query_step' validates step attr with Query Operator '$in' with key '_id'
    to convert value to 'ObjectId' type"""

    object_id = ObjectId()
    step_list_object_id = {"_id": {"$in": [object_id, object_id]}}
    step_list_str = {"_id": {"$in": [str(object_id), str(object_id)]}}

    _validate_query_step(step_list_object_id, allow_var=False)
    assert step_list_object_id == {"_id": {"$in": [object_id, object_id]}}

    _validate_query_step(step_list_str, allow_var=False)
    assert step_list_str == {"_id": {"$in": [object_id, object_id]}}


def test_valid_query_step_valid_oper_nin_key_id():
    """Tests '_validate_query_step' validates step attr with Query Operator '$nin' with key '_id'
    to convert value to 'ObjectId' type"""

    object_id = ObjectId()
    step_list_object_id = {"_id": {"$nin": [object_id, object_id]}}
    step_list_str = {"_id": {"$nin": [str(object_id), str(object_id)]}}

    _validate_query_step(step_list_object_id, allow_var=False)
    assert step_list_object_id == {"_id": {"$nin": [object_id, object_id]}}

    _validate_query_step(step_list_str, allow_var=False)
    assert step_list_str == {"_id": {"$nin": [object_id, object_id]}}


def test_valid_query_step_valid_oper_all_key_id():
    """Tests '_validate_query_step' validates step attr with Query Operator '$all' with key '_id'
    to convert value to 'ObjectId' type"""

    object_id = ObjectId()
    step_list_object_id = {"_id": {"$all": [object_id, object_id]}}
    step_list_str = {"_id": {"$all": [str(object_id), str(object_id)]}}

    _validate_query_step(step_list_object_id, allow_var=False)
    assert step_list_object_id == {"_id": {"$all": [object_id, object_id]}}

    _validate_query_step(step_list_str, allow_var=False)
    assert step_list_str == {"_id": {"$all": [object_id, object_id]}}
