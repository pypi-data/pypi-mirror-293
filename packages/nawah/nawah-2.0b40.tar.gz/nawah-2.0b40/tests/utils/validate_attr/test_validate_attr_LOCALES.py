import pytest

from nawah import config
from nawah.classes import Attr, Default
from nawah.exceptions import InvalidAttrException
from nawah.utils import validate_attr


def test_validate_attr_LOCALES_None(preserve_state):
    with preserve_state(config, "Config"):
        config.Config.locales = ["ar_AE", "en_GB", "de_DE"]
        config.Config.locale = "ar_AE"
        with pytest.raises(InvalidAttrException):
            validate_attr(
                attr_name="test_validate_attr_LOCALES",
                attr_type=Attr.LOCALES(),
                attr_val=None,
                mode="create",
            )


def test_validate_attr_LOCALES_str_invalid(preserve_state):
    with preserve_state(config, "Config"):
        config.Config.locales = ["ar_AE", "en_GB", "de_DE"]
        config.Config.locale = "ar_AE"
        with pytest.raises(InvalidAttrException):
            validate_attr(
                attr_name="test_validate_attr_LOCALES",
                attr_type=Attr.LOCALES(),
                attr_val="ar",
                mode="create",
            )


def test_validate_attr_LOCALES_locale(preserve_state):
    with preserve_state(config, "Config"):
        config.Config.locales = ["ar_AE", "en_GB", "de_DE"]
        config.Config.locale = "ar_AE"
        attr_val = validate_attr(
            attr_name="test_validate_attr_LOCALES",
            attr_type=Attr.LOCALES(),
            attr_val="en_GB",
            mode="create",
        )
        assert attr_val == "en_GB"


def test_validate_attr_LOCALES_None_allow_none(preserve_state):
    with preserve_state(config, "Config"):
        config.Config.locales = ["ar_AE", "en_GB", "de_DE"]
        config.Config.locale = "ar_AE"
        attr_val = validate_attr(
            attr_name="test_validate_attr_LOCALES",
            attr_type=Attr.LOCALES(),
            attr_val=None,
            mode="update",
        )
        assert attr_val == None


def test_validate_attr_LOCALES_default_None(preserve_state):
    with preserve_state(config, "Config"):
        config.Config.locales = ["ar_AE", "en_GB", "de_DE"]
        config.Config.locale = "ar_AE"
        attr_type = Attr.LOCALES()
        attr_type.default = Default(value="test_validate_attr_LOCALES")
        attr_val = validate_attr(
            attr_name="test_validate_attr_LOCALES",
            attr_type=attr_type,
            attr_val=None,
            mode="create",
        )
        assert attr_val == "test_validate_attr_LOCALES"


def test_validate_attr_LOCALES_default_int(preserve_state):
    with preserve_state(config, "Config"):
        config.Config.locales = ["ar_AE", "en_GB", "de_DE"]
        config.Config.locale = "ar_AE"
        attr_type = Attr.LOCALES()
        attr_type.default = Default(value="test_validate_attr_LOCALES")
        attr_val = validate_attr(
            attr_name="test_validate_attr_LOCALES",
            attr_type=attr_type,
            attr_val=1,
            mode="create",
        )
        assert attr_val == "test_validate_attr_LOCALES"


def test_validate_attr_LOCALES_default_int_allow_none(preserve_state):
    with preserve_state(config, "Config"):
        config.Config.locales = ["ar_AE", "en_GB", "de_DE"]
        config.Config.locale = "ar_AE"
        attr_type = Attr.LOCALES()
        attr_type.default = Default(value="test_validate_attr_LOCALES")
        attr_val = validate_attr(
            attr_name="test_validate_attr_LOCALES",
            attr_type=attr_type,
            attr_val=1,
            mode="update",
        )
        assert attr_val == None
