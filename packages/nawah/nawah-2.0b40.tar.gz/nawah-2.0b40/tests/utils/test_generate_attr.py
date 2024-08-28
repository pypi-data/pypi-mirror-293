# [TODO] Add docstrings to all tests

import datetime
import re
from math import inf

from bson import ObjectId

from nawah import config, utils
from nawah.classes import Attr


def test_generate_attr_ANY():
    utils.generate_attr_val(attr_type=Attr.ANY())


def test_generate_attr_BOOL():
    attr_val = utils.generate_attr_val(attr_type=Attr.BOOL())
    assert attr_val in [True, False]


def test_generate_attr_DATE_no_args():
    attr_val = utils.generate_attr_val(attr_type=Attr.DATE())
    assert attr_val == datetime.datetime.utcnow().isoformat().split("T")[0]


def test_generate_attr_DATE_ranges_datetime_end():
    attr_val = utils.generate_attr_val(
        attr_type=Attr.DATE(ranges=[["+1d", "2020-10-20"]])
    )
    assert attr_val == "2020-10-19"


def test_generate_attr_DATE_ranges_datetime_start():
    attr_val = utils.generate_attr_val(
        attr_type=Attr.DATE(ranges=[["2020-10-20", "+104w"]])
    )
    assert attr_val == "2020-10-20"


def test_generate_attr_DATE_ranges_dynamic_start_end():
    attr_val = utils.generate_attr_val(attr_type=Attr.DATE(ranges=[["+2d", "+52w"]]))
    assert (
        attr_val
        == (datetime.datetime.utcnow() + datetime.timedelta(days=2))
        .isoformat()
        .split("T")[0]
    )


def test_generate_attr_DATE_ranges_dynamic_start_end_negative():
    attr_val = utils.generate_attr_val(attr_type=Attr.DATE(ranges=[["-5d", "+52w"]]))
    assert (
        attr_val
        == (datetime.datetime.utcnow() + datetime.timedelta(days=-5))
        .isoformat()
        .split("T")[0]
    )


def test_generate_attr_DATETIME_no_args():
    attr_val = utils.generate_attr_val(attr_type=Attr.DATETIME())
    assert (
        attr_val.split(".")[0] == datetime.datetime.utcnow().isoformat().split(".")[0]
    )


def test_generate_attr_DATETIME_ranges_datetime_end():
    attr_val = utils.generate_attr_val(
        attr_type=Attr.DATETIME(ranges=[["+1d", "2020-10-20T00:00:00"]])
    )
    assert attr_val == "2020-10-19T00:00:00"


def test_generate_attr_DATETIME_ranges_datetime_start():
    attr_val = utils.generate_attr_val(
        attr_type=Attr.DATETIME(ranges=[["2020-10-20T00:00:00", "+104w"]])
    )
    assert attr_val == "2020-10-20T00:00:00"


def test_generate_attr_DATETIME_ranges_dynamic_start_end():
    attr_val = utils.generate_attr_val(
        attr_type=Attr.DATETIME(ranges=[["+2d", "+52w"]])
    )
    assert (
        attr_val.split(".")[0]
        == (datetime.datetime.utcnow() + datetime.timedelta(days=2))
        .isoformat()
        .split(".")[0]
    )


def test_generate_attr_DATETIME_ranges_dynamic_start_end_negative():
    attr_val = utils.generate_attr_val(
        attr_type=Attr.DATETIME(ranges=[["-5d", "+52w"]])
    )
    assert (
        attr_val.split(".")[0]
        == (datetime.datetime.utcnow() + datetime.timedelta(days=-5))
        .isoformat()
        .split(".")[0]
    )


def test_generate_attr_KV_DICT_no_args():
    attr_val = utils.generate_attr_val(
        attr_type=Attr.KV_DICT(key=Attr.STR(), val=Attr.INT())
    )
    assert len(attr_val.keys()) == 0


def test_generate_attr_KV_DICT_min():
    attr_val = utils.generate_attr_val(
        attr_type=Attr.KV_DICT(key=Attr.STR(), val=Attr.INT(), len_range=[2, inf])
    )
    assert len(attr_val.keys()) == 2
    assert set(type(k) for k in attr_val.keys()) == {str}
    assert set(type(v) for v in attr_val.values()) == {int}


def test_generate_attr_KV_DICT_key_LITERAL():
    attr_val = utils.generate_attr_val(
        attr_type=Attr.KV_DICT(
            key=Attr.LITERAL(literal=["foo", "bar"]), val=Attr.INT(), len_range=[2, inf]
        )
    )
    assert len(attr_val.keys()) == 2
    assert set(attr_val.keys()) == {"foo", "bar"}


def test_generate_attr_TYPED_DICT():
    attr_val = utils.generate_attr_val(
        attr_type=Attr.TYPED_DICT(
            dict={
                "foo": Attr.INT(),
                "bar": Attr.STR(),
            }
        )
    )
    assert len(attr_val.keys()) == 2
    assert set(attr_val.keys()) == {"foo", "bar"}
    assert isinstance(attr_val["foo"], int)
    assert isinstance(attr_val["bar"], str)


def test_generate_attr_EMAIL_no_args():
    attr_val = utils.generate_attr_val(attr_type=Attr.EMAIL())
    assert re.match(r"^[^@]+@[^@]+\.[^@]+$", attr_val) != None


def test_generate_attr_EMAIL_allowed_domains():
    attr_val = utils.generate_attr_val(
        attr_type=Attr.EMAIL(allowed_domains=["foo.com", "bar.net", "baz.ae"])
    )
    assert (
        attr_val.endswith("@mail.foo.com")
        or attr_val.endswith("@mail.bar.net")
        or attr_val.endswith("@mail.baz.ae")
    )


def test_generate_attr_EMAIL_allowed_domains_strict():
    attr_val = utils.generate_attr_val(
        attr_type=Attr.EMAIL(
            allowed_domains=["foo.com", "bar.net", "baz.ae"], strict_matching=True
        )
    )
    assert (
        attr_val.endswith("@foo.com")
        or attr_val.endswith("@bar.net")
        or attr_val.endswith("@baz.ae")
    )


def test_generate_attr_FILE_no_args():
    attr_val = utils.generate_attr_val(attr_type=Attr.FILE())
    assert type(attr_val) == dict
    assert set(k for k in attr_val.keys()) == {
        "name",
        "lastModified",
        "type",
        "size",
        "content",
    }
    assert attr_val["type"] == "text/plain"
    assert attr_val["name"].endswith(".txt")


def test_generate_attr_FILE_types():
    attr_val = utils.generate_attr_val(attr_type=Attr.FILE(types=["image/*"]))
    assert attr_val["type"] == "image/*"
    assert attr_val["name"].endswith(".txt")


def test_generate_attr_FILE_types_extension():
    attr_val = utils.generate_attr_val(attr_type=Attr.FILE(types=["image/*", "*.png"]))
    assert attr_val["type"] == "image/*"
    assert attr_val["name"].endswith(".png")


def test_generate_attr_FLOAT_no_args():
    attr_val = utils.generate_attr_val(attr_type=Attr.FLOAT())
    assert type(attr_val) == float


def test_generate_attr_FLOAT_ranges():
    attr_val = utils.generate_attr_val(attr_type=Attr.FLOAT(ranges=[[0.5, 10.3]]))
    assert type(attr_val) == float
    assert attr_val >= 0 and attr_val < 10


def test_generate_attr_GEO():
    attr_val = utils.generate_attr_val(attr_type=Attr.GEO_POINT())
    assert type(attr_val) == dict
    assert set(k for k in attr_val.keys()) == {"type", "coordinates"}


def test_generate_attr_ID():
    attr_val = utils.generate_attr_val(attr_type=Attr.ID())
    assert type(attr_val) == ObjectId


def test_generate_attr_INT_no_args():
    attr_val = utils.generate_attr_val(attr_type=Attr.INT())
    assert type(attr_val) == int


def test_generate_attr_INT_ranges():
    attr_val = utils.generate_attr_val(attr_type=Attr.INT(ranges=[[0, 10]]))
    assert type(attr_val) == int
    assert attr_val in range(0, 10)


def test_generate_attr_IP():
    attr_val = utils.generate_attr_val(attr_type=Attr.IP())
    assert (
        re.match(
            r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$",
            attr_val,
        )
        != None
    )


def test_generate_attr_LIST_no_args():
    attr_val = utils.generate_attr_val(attr_type=Attr.LIST(list=[Attr.STR()]))
    assert len(attr_val) == 0


def test_generate_attr_LIST_min():
    attr_val = utils.generate_attr_val(
        attr_type=Attr.LIST(list=[Attr.STR()], len_range=[2, inf])
    )
    assert len(attr_val) == 2
    assert set(type(j) for j in attr_val) == {str}


def test_generate_attr_LIST_multiple_types():
    attr_val = utils.generate_attr_val(
        attr_type=Attr.LIST(list=[Attr.STR(), Attr.INT()], len_range=[2, inf])
    )
    assert len(attr_val) == 2
    assert sum(1 for j in attr_val if type(j) in [int, str]) == 2


def test_generate_attr_LOCALE(preserve_state):
    with preserve_state(config, "Config"):
        config.Config.locales = ["ar_AE", "en_GB"]
        config.Config.locale = "ar_AE"
        attr_val = utils.generate_attr_val(attr_type=Attr.LOCALE())

        assert len(attr_val.keys()) == 2
        assert set(attr_val.keys()) == {"ar_AE", "en_GB"}


def test_generate_attr_LOCALES(preserve_state):
    with preserve_state(config, "Config"):
        config.Config.locales = ["ar_AE", "en_GB"]
        config.Config.locale = "ar_AE"
        attr_val = utils.generate_attr_val(attr_type=Attr.LOCALES())

        assert attr_val in ["ar_AE", "en_GB"]


def test_generate_attr_PHONE_no_args():
    attr_val = utils.generate_attr_val(attr_type=Attr.PHONE())
    assert re.match(r"^\+[0-9]+$", attr_val) != None


def test_generate_attr_PHONE_codes():
    attr_val = utils.generate_attr_val(attr_type=Attr.PHONE(codes=["123", "45", "6"]))
    assert re.match(r"^\+(123|45|6)[0-9]+$", attr_val) != None


def test_generate_attr_STR_no_args():
    attr_val = utils.generate_attr_val(attr_type=Attr.STR())
    assert type(attr_val) == str


def test_generate_attr_STR_pattern(caplog):
    utils.generate_attr_val(attr_type=Attr.STR(pattern="^[0-9]+$"))
    # [DOC] Assert warning was logged of existence of pattern Attr Type Arg
    assert caplog.records[0].levelname == "WARNING"


def test_generate_attr_TIME_no_args():
    attr_val = utils.generate_attr_val(attr_type=Attr.TIME())
    assert (
        attr_val.split(".")[0]
        == datetime.datetime.utcnow().isoformat().split("T")[1].split(".")[0]
    )


def test_generate_attr_TIME_ranges_datetime_end():
    attr_val = utils.generate_attr_val(
        attr_type=Attr.TIME(ranges=[["+1h", "22:00:00"]])
    )
    assert attr_val == "21:59:00"


def test_generate_attr_TIME_ranges_datetime_start():
    attr_val = utils.generate_attr_val(
        attr_type=Attr.TIME(ranges=[["18:00:00", "+2h"]])
    )
    assert attr_val == "18:00:00"


def test_generate_attr_TIME_ranges_dynamic_start_end():
    attr_val = utils.generate_attr_val(attr_type=Attr.TIME(ranges=[["+2h", "+5h"]]))
    assert (
        attr_val.split(".")[0]
        == (datetime.datetime.utcnow() + datetime.timedelta(hours=2))
        .isoformat()
        .split("T")[1]
        .split(".")[0]
    )


def test_generate_attr_TIME_ranges_dynamic_start_end_negative():
    attr_val = utils.generate_attr_val(attr_type=Attr.TIME(ranges=[["-2h", "+5h"]]))
    assert (
        attr_val.split(".")[0]
        == (datetime.datetime.utcnow() + datetime.timedelta(hours=-2))
        .isoformat()
        .split("T")[1]
        .split(".")[0]
    )


def test_generate_attr_URI_WEB_no_args():
    attr_val = utils.generate_attr_val(attr_type=Attr.URI_WEB())
    assert (
        re.match(r"^https?:\/\/(?:[\w\-\_]+\.)(?:\.?[\w]{2,})+([\?\/].*)?$", attr_val)
        != None
    )


def test_generate_attr_URI_WEB_allowed_domains():
    attr_val = utils.generate_attr_val(
        attr_type=Attr.URI_WEB(allowed_domains=["foo.com", "bar.net", "baz.ae"])
    )
    assert (
        attr_val.startswith("https://sub.foo.com/")
        or attr_val.startswith("https://sub.bar.net/")
        or attr_val.startswith("https://sub.baz.ae/")
    )


def test_generate_attr_URI_WEB_allowed_domains_strict():
    attr_val = utils.generate_attr_val(
        attr_type=Attr.URI_WEB(
            allowed_domains=["foo.com", "bar.net", "baz.ae"], strict_matching=True
        )
    )
    assert (
        attr_val.startswith("https://foo.com/")
        or attr_val.startswith("https://bar.net/")
        or attr_val.startswith("https://baz.ae/")
    )


def test_generate_attr_LITERAL():
    attr_val = utils.generate_attr_val(
        attr_type=Attr.LITERAL(literal=["abc", 321, False, 12.34, "foo", "bar", "baz"])
    )
    assert attr_val in ["abc", 321, False, 12.34, "foo", "bar", "baz"]


def test_generate_attr_UNION():
    attr_val1 = utils.generate_attr_val(
        attr_type=Attr.UNION(union=[Attr.STR(), Attr.INT()])
    )
    attr_val2 = utils.generate_attr_val(
        attr_type=Attr.UNION(
            union=[
                Attr.LIST(list=[Attr.STR()], len_range=[1, inf]),
                Attr.TYPED_DICT(dict={"foo": Attr.FLOAT()}),
            ]
        )
    )
    assert type(attr_val1) in [str, int]
    assert (type(attr_val2) == list and type(attr_val2[0]) == str) or (
        type(attr_val2) == dict and type(attr_val2["foo"]) == float
    )
