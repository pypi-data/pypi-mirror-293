import pytest

from nawah import config
from nawah.classes import Attr, Default
from nawah.exceptions import InvalidAttrException
from nawah.enums import LocaleStrategy
from nawah.utils import validate_attr


def test_validate_attr_LOCALE_None(preserve_state):
    with preserve_state(config, "Config"):
        config.Config.locales = ["ar_AE", "en_GB", "de_DE"]
        config.Config.locale = "ar_AE"
        with pytest.raises(InvalidAttrException):
            validate_attr(
                attr_name="test_validate_attr_LOCALE",
                attr_type=Attr.LOCALE(),
                attr_val=None,
                mode="create",
            )


def test_validate_attr_LOCALE_dict_invalid(preserve_state):
    with preserve_state(config, "Config"):
        config.Config.locales = ["ar_AE", "en_GB", "de_DE"]
        config.Config.locale = "ar_AE"
        with pytest.raises(InvalidAttrException):
            validate_attr(
                attr_name="test_validate_attr_LOCALE",
                attr_type=Attr.LOCALE(),
                attr_val={
                    "ar": "str",
                },
                mode="create",
            )


def test_validate_attr_LOCALE_locale_all(preserve_state):
    with preserve_state(config, "Config"):
        config.Config.locales = ["ar_AE", "en_GB", "de_DE"]
        config.Config.locale = "ar_AE"
        locale_attr_val = {
            "ar_AE": "str",
            "en_GB": "str",
            "de_DE": "str",
        }
        attr_val = validate_attr(
            attr_name="test_validate_attr_LOCALE",
            attr_type=Attr.LOCALE(),
            attr_val=locale_attr_val,
            mode="create",
        )
        assert attr_val == locale_attr_val


def test_validate_attr_LOCALE_locale_min_strategy_duplicate(preserve_state):
    with preserve_state(config, "Config"):
        config.Config.locales = ["ar_AE", "en_GB", "de_DE"]
        config.Config.locale = "ar_AE"
        locale_attr_val = {
            "ar_AE": "str",
            "en_GB": "str",
            "de_DE": "str",
        }
        attr_val = validate_attr(
            attr_name="test_validate_attr_LOCALE",
            attr_type=Attr.LOCALE(),
            attr_val={
                "ar_AE": "str",
            },
            mode="create",
        )
        assert attr_val == locale_attr_val


def test_validate_attr_LOCALE_locale_min_strategy_none(preserve_state):
    with preserve_state(config, "Config"):
        config.Config.locales = ["ar_AE", "en_GB", "de_DE"]
        config.Config.locale = "ar_AE"
        config.Config.locale_strategy = LocaleStrategy.NONE_VALUE
        locale_attr_val = {
            "ar_AE": "str",
            "en_GB": None,
            "de_DE": None,
        }
        attr_val = validate_attr(
            attr_name="test_validate_attr_LOCALE",
            attr_type=Attr.LOCALE(),
            attr_val={
                "ar_AE": "str",
            },
            mode="create",
        )
        assert attr_val == locale_attr_val


def test_validate_attr_LOCALE_locale_min_strategy_callable(preserve_state):
    with preserve_state(config, "Config"):
        config.Config.locales = ["ar_AE", "en_GB", "de_DE"]
        config.Config.locale = "ar_AE"
        config.Config.locale_strategy = (
            lambda attr_val, locale: f"DEFAULT:{locale}:{attr_val[config.Config.locale]}"
        )
        locale_attr_val = {
            "ar_AE": "str",
            "en_GB": "DEFAULT:en_GB:str",
            "de_DE": "DEFAULT:de_DE:str",
        }
        attr_val = validate_attr(
            attr_name="test_validate_attr_LOCALE",
            attr_type=Attr.LOCALE(),
            attr_val={
                "ar_AE": "str",
            },
            mode="create",
        )
        assert attr_val == locale_attr_val


def test_validate_attr_LOCALE_locale_extra(preserve_state):
    with preserve_state(config, "Config"):
        config.Config.locales = ["ar_AE", "en_GB", "de_DE"]
        config.Config.locale = "ar_AE"
        with pytest.raises(InvalidAttrException):
            validate_attr(
                attr_name="test_validate_attr_LOCALE",
                attr_type=Attr.LOCALE(),
                attr_val={
                    "ar_AE": "str",
                    "invalid": "str",
                },
                mode="create",
            )


def test_validate_attr_LOCALE_None_allow_none(preserve_state):
    with preserve_state(config, "Config"):
        config.Config.locales = ["ar_AE", "en_GB", "de_DE"]
        config.Config.locale = "ar_AE"
        attr_val = validate_attr(
            attr_name="test_validate_attr_LOCALE",
            attr_type=Attr.LOCALE(),
            attr_val=None,
            mode="update",
        )
        assert attr_val == None


def test_validate_attr_LOCALE_default_None(preserve_state):
    with preserve_state(config, "Config"):
        config.Config.locales = ["ar_AE", "en_GB", "de_DE"]
        config.Config.locale = "ar_AE"
        attr_type = Attr.LOCALE()
        attr_type.default = Default(value="test_validate_attr_LOCALE")
        attr_val = validate_attr(
            attr_name="test_validate_attr_LOCALE",
            attr_type=attr_type,
            attr_val=None,
            mode="create",
        )
        assert attr_val == "test_validate_attr_LOCALE"


def test_validate_attr_LOCALE_default_int(preserve_state):
    with preserve_state(config, "Config"):
        config.Config.locales = ["ar_AE", "en_GB", "de_DE"]
        config.Config.locale = "ar_AE"
        attr_type = Attr.LOCALE()
        attr_type.default = Default(value="test_validate_attr_LOCALE")
        attr_val = validate_attr(
            attr_name="test_validate_attr_LOCALE",
            attr_type=attr_type,
            attr_val=1,
            mode="create",
        )
        assert attr_val == "test_validate_attr_LOCALE"


def test_validate_attr_LOCALE_default_int_allow_none(preserve_state):
    with preserve_state(config, "Config"):
        config.Config.locales = ["ar_AE", "en_GB", "de_DE"]
        config.Config.locale = "ar_AE"
        attr_type = Attr.LOCALE()
        attr_type.default = Default(value="test_validate_attr_LOCALE")
        attr_val = validate_attr(
            attr_name="test_validate_attr_LOCALE",
            attr_type=attr_type,
            attr_val=1,
            mode="update",
        )
        assert attr_val == None
