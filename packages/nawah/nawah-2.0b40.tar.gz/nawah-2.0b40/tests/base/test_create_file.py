"""Provides tests for 'CreateFile' IOC class for 'create_func' Base Function"""

from typing import TYPE_CHECKING

import pytest
from bson import ObjectId

from nawah.base._create_file._classes import CreateFile
from nawah.base.exceptions import UtilityModuleDataCallException
from nawah.classes import Attr, Module
from nawah.exceptions import InvalidAttrTypeException

if TYPE_CHECKING:
    from pytest_mock import MockerFixture


@pytest.mark.asyncio
async def test_create_file_raise_utility_module():
    """Tests 'CreateFile' IOC raising 'UtilityModuleDataCallException' if injected module is a
    Utility Module"""

    module = Module(
        name="test",
        attrs=None,
        funcs=None,
    )

    create_file_implementation = CreateFile(
        modules={"test": module},
        data_create_callable=None,
        set_file_callable=None,
    )

    with pytest.raises(UtilityModuleDataCallException):
        await create_file_implementation(module_name="test", session=None, doc=None)


@pytest.mark.asyncio
async def test_create_file_raise_attr_not_defined():
    """Tests 'CreateFile' IOC raising 'ValueError' if value of doc attr 'attr' is not defined in
    module"""

    module = Module(
        name="test",
        collection="test_docs",
        attrs={},
        funcs=None,
    )

    create_file_implementation = CreateFile(
        modules={"test": module},
        data_create_callable=None,
        set_file_callable=None,
    )

    with pytest.raises(ValueError):
        await create_file_implementation(
            module_name="test", session=None, doc={"attr": "photo"}
        )


@pytest.mark.asyncio
async def test_create_file_raise_attr_not_file():
    """Tests 'CreateFile' IOC raising 'InvalidAttrTypeException' if value of doc attr 'attr' is not
    of type 'FILE'"""

    module = Module(
        name="test",
        collection="test_docs",
        attrs={"photo": Attr.STR()},
        funcs=None,
    )

    create_file_implementation = CreateFile(
        modules={"test": module},
        data_create_callable=None,
        set_file_callable=None,
    )

    with pytest.raises(InvalidAttrTypeException):
        await create_file_implementation(
            module_name="test", session=None, doc={"attr": "photo"}
        )


@pytest.mark.asyncio
async def test_create_file_raise_attr_list_not_file():
    """Tests 'CreateFile' IOC raising 'InvalidAttrTypeException' if value of doc attr 'attr' is of
    type 'LIST' but first value for 'list' Attr Type Arg is not 'FILE'"""

    module = Module(
        name="test",
        collection="test_docs",
        attrs={"photo": Attr.LIST(list=[Attr.STR()])},
        funcs=None,
    )

    create_file_implementation = CreateFile(
        modules={"test": module},
        data_create_callable=None,
        set_file_callable=None,
    )

    with pytest.raises(InvalidAttrTypeException):
        await create_file_implementation(
            module_name="test", session=None, doc={"attr": "photo"}
        )


@pytest.mark.asyncio
async def test_create_file_type_file_success(mocker: "MockerFixture"):
    """Tests 'CreateFile' IOC calls injected 'DataCreateCallable' if all checks are passed"""

    module = Module(
        name="test",
        collection="test_docs",
        attrs={"photo": Attr.FILE()},
        # Ignore wrong value for Module.funcs
        funcs=None,  # type: ignore
    )

    data_create_stub = mocker.AsyncMock()

    create_file_implementation = CreateFile(
        modules={"test": module},
        data_create_callable=data_create_stub,
        # Ignore wrong value for CreateFile.set_file_callable
        set_file_callable=None,  # type: ignore
    )

    await create_file_implementation(
        module_name="test",
        # Ignore missing keys for NawahSession TypedDict
        session={"user": {"_id": ObjectId()}},  # type: ignore
        doc={
            "attr": "photo",
            "name": "file",
            "lastModified": 0,
            "type": "text/plain",
            "size": 0,
            "content": b"",
        },
    )

    data_create_stub.assert_called_once()


@pytest.mark.asyncio
async def test_create_file_type_union_str_file_success(mocker: "MockerFixture"):
    """Tests 'CreateFile' IOC calls injected 'DataCreateCallable' if all checks are passed"""

    module = Module(
        name="test",
        collection="test_docs",
        attrs={"photo": Attr.UNION(union=[Attr.STR(), Attr.FILE()])},
        # Ignore wrong value for Module.funcs
        funcs=None,  # type: ignore
    )

    data_create_stub = mocker.AsyncMock()

    create_file_implementation = CreateFile(
        modules={"test": module},
        data_create_callable=data_create_stub,
        # Ignore wrong value for CreateFile.set_file_callable
        set_file_callable=None,  # type: ignore
    )

    await create_file_implementation(
        module_name="test",
        # Ignore missing keys for NawahSession TypedDict
        session={"user": {"_id": ObjectId()}},  # type: ignore
        doc={
            "attr": "photo.1",
            "name": "file",
            "lastModified": 0,
            "type": "text/plain",
            "size": 0,
            "content": b"",
        },
    )

    data_create_stub.assert_called_once()


@pytest.mark.asyncio
async def test_create_file_type_union_str_dict_file_success(mocker: "MockerFixture"):
    """Tests 'CreateFile' IOC calls injected 'DataCreateCallable' if all checks are passed"""

    module = Module(
        name="test",
        collection="test_docs",
        attrs={
            "photo": Attr.UNION(
                union=[
                    Attr.STR(),
                    Attr.TYPED_DICT(dict={"tag": Attr.STR(), "file": Attr.FILE()}),
                ]
            )
        },
        # Ignore wrong value for Module.funcs
        funcs=None,  # type: ignore
    )

    data_create_stub = mocker.AsyncMock()

    create_file_implementation = CreateFile(
        modules={"test": module},
        data_create_callable=data_create_stub,
        # Ignore wrong value for CreateFile.set_file_callable
        set_file_callable=None,  # type: ignore
    )

    await create_file_implementation(
        module_name="test",
        # Ignore missing keys for NawahSession TypedDict
        session={"user": {"_id": ObjectId()}},  # type: ignore
        doc={
            "attr": "photo.1.file",
            "name": "file",
            "lastModified": 0,
            "type": "text/plain",
            "size": 0,
            "content": b"",
        },
    )

    data_create_stub.assert_called_once()
