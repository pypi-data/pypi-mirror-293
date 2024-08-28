import pytest

from nawah.classes import Attr, Default
from nawah.exceptions import InvalidAttrException
from nawah.utils import validate_attr


def test_validate_attr_EMAIL_None():
    with pytest.raises(InvalidAttrException):
        validate_attr(
            attr_name="test_validate_attr_EMAIL",
            attr_type=Attr.EMAIL(),
            attr_val=None,
            mode="create",
        )


def test_validate_attr_EMAIL_int():
    with pytest.raises(InvalidAttrException):
        validate_attr(
            attr_name="test_validate_attr_EMAIL",
            attr_type=Attr.EMAIL(),
            attr_val=1,
            mode="create",
        )


def test_validate_attr_EMAIL_str_invalid():
    with pytest.raises(InvalidAttrException):
        validate_attr(
            attr_name="test_validate_attr_EMAIL",
            attr_type=Attr.EMAIL(),
            attr_val="str",
            mode="create",
        )


def test_validate_attr_EMAIL_email():
    attr_val = validate_attr(
        attr_name="test_validate_attr_EMAIL",
        attr_type=Attr.EMAIL(),
        attr_val="info@nawah.foobar.baz",
        mode="create",
    )
    assert attr_val == "info@nawah.foobar.baz"


def test_validate_attr_EMAIL_allowed_domains_email_invalid():
    with pytest.raises(InvalidAttrException):
        validate_attr(
            attr_name="test_validate_attr_EMAIL",
            attr_type=Attr.EMAIL(allowed_domains=["foo.com", "bar.net"]),
            attr_val="info@nawah.foobar.baz",
            mode="create",
        )


def test_validate_attr_EMAIL_allowed_domains_strict_email_invalid():
    with pytest.raises(InvalidAttrException):
        validate_attr(
            attr_name="test_validate_attr_EMAIL",
            attr_type=Attr.EMAIL(
                allowed_domains=["foo.com", "bar.net"], strict_matching=True
            ),
            attr_val="info@sub.foo.com",
            mode="create",
        )


def test_validate_attr_EMAIL_allowed_domains_email():
    attr_val = validate_attr(
        attr_name="test_validate_attr_EMAIL",
        attr_type=Attr.EMAIL(allowed_domains=["foo.com", "bar.net"]),
        attr_val="info@sub.foo.com",
        mode="create",
    )
    assert attr_val == "info@sub.foo.com"


def test_validate_attr_EMAIL_allowed_domains_strict_email():
    attr_val = validate_attr(
        attr_name="test_validate_attr_EMAIL",
        attr_type=Attr.EMAIL(
            allowed_domains=["foo.com", "bar.net"], strict_matching=True
        ),
        attr_val="info@foo.com",
        mode="create",
    )
    assert attr_val == "info@foo.com"


def test_validate_attr_EMAIL_disallowed_domains_email_invalid():
    with pytest.raises(InvalidAttrException):
        validate_attr(
            attr_name="test_validate_attr_EMAIL",
            attr_type=Attr.EMAIL(disallowed_domains=["foo.com", "bar.net"]),
            attr_val="info@nawah.foo.com",
            mode="create",
        )


def test_validate_attr_EMAIL_disallowed_domains_strict_email_invalid():
    with pytest.raises(InvalidAttrException):
        validate_attr(
            attr_name="test_validate_attr_EMAIL",
            attr_type=Attr.EMAIL(
                disallowed_domains=["foo.com", "bar.net"], strict_matching=True
            ),
            attr_val="info@foo.com",
            mode="create",
        )


def test_validate_attr_EMAIL_disallowed_domains_email():
    attr_val = validate_attr(
        attr_name="test_validate_attr_EMAIL",
        attr_type=Attr.EMAIL(disallowed_domains=["foo.com", "bar.net"]),
        attr_val="info@sub.foobar.com",
        mode="create",
    )
    assert attr_val == "info@sub.foobar.com"


def test_validate_attr_EMAIL_disallowed_domains_strict_email():
    attr_val = validate_attr(
        attr_name="test_validate_attr_EMAIL",
        attr_type=Attr.EMAIL(
            disallowed_domains=["foo.com", "bar.net"], strict_matching=True
        ),
        attr_val="info@sub.foo.com",
        mode="create",
    )
    assert attr_val == "info@sub.foo.com"


def test_validate_attr_EMAIL_None_allow_none():
    attr_val = validate_attr(
        attr_name="test_validate_attr_EMAIL",
        attr_type=Attr.EMAIL(),
        attr_val=None,
        mode="update",
    )
    assert attr_val == None


def test_validate_attr_EMAIL_default_None():
    attr_type = Attr.EMAIL()
    attr_type.default = Default(value="test_validate_attr_EMAIL")
    attr_val = validate_attr(
        attr_name="test_validate_attr_EMAIL",
        attr_type=attr_type,
        attr_val=None,
        mode="create",
    )
    assert attr_val == "test_validate_attr_EMAIL"


def test_validate_attr_EMAIL_default_int():
    attr_type = Attr.EMAIL()
    attr_type.default = Default(value="test_validate_attr_EMAIL")
    attr_val = validate_attr(
        attr_name="test_validate_attr_EMAIL",
        attr_type=attr_type,
        attr_val=1,
        mode="create",
    )
    assert attr_val == "test_validate_attr_EMAIL"


def test_validate_attr_EMAIL_default_int_allow_none():
    attr_type = Attr.EMAIL()
    attr_type.default = Default(value="test_validate_attr_EMAIL")
    attr_val = validate_attr(
        attr_name="test_validate_attr_EMAIL",
        attr_type=attr_type,
        attr_val=1,
        mode="update",
    )
    assert attr_val == None
