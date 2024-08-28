"""Provides 'session' Nawah Core Module"""

from nawah.classes import (Attr, Default, Extn, Func, Module, Perm, QueryMod,
                           Var)

from ._callables import _auth, _reauth, _signout
from ._exceptions import (AnonReauthException, AnonSignoutException,
                          ExpiredSessionException, InvalidCredentialsException,
                          InvalidSessionException, InvalidUserException)

session = Module(
    name="session",
    desc="'session' module provides data type and controller for sessions in Nawah eco-system. "
    "CRUD methods of the module are supposed to used for internal calls only, while methods "
    "'auth', 'reauth', and 'signout' are available for use by API as well as internal calls "
    "when needed",
    collection="session_docs",
    attrs={
        "user": Attr.ID(desc="'_id' of 'User' doc the doc belongs to"),
        "groups": Attr.LIST(
            desc="List of '_id' for every group the session is authenticated against. This attr "
            "is set by 'auth' method when called with 'groups' Doc Arg for Controller Auth "
            "Sequence",
            list=[
                Attr.ID(desc="'_id' of Group doc the session is authenticated against")
            ],
        ),
        "host_add": Attr.IP(desc="IP of the host the user used to authenticate"),
        "user_agent": Attr.STR(
            desc="User-agent of the app the user used to authenticate"
        ),
        "expiry": Attr.DATETIME(desc="Python 'datetime' ISO format of session expiry"),
        "token_hash": Attr.STR(desc="Hashed system-generated session token"),
        "create_time": Attr.DATETIME(
            desc="Python 'datetime' ISO format of the doc creation"
        ),
    },
    defaults={"groups": Default(value=[])},
    extns={"user": Extn(module="user", attrs=["*"], force=True)},
    funcs={
        "read": Func(
            permissions=[
                Perm(
                    privilege="read",
                    query_mod=QueryMod([{"user": {"$eq": Var.SESSION("user._id")}}]),
                )
            ],
        ),
        "create": Func(permissions=[Perm(privilege="__sys")]),
        "update": Func(permissions=[Perm(privilege="__sys")]),
        "delete": Func(permissions=[Perm(privilege="__sys")]),
        "auth": Func(
            permissions=[Perm(privilege="*")],
            call_args={"skip_status_check": Attr.BOOL()},
            doc_attrs=[],
            callable=_auth,
            exceptions={
                InvalidCredentialsException: False,
                InvalidUserException: False,
            },
        ),
        "reauth": Func(
            permissions=[Perm(privilege="*")],
            query_attrs=[
                {
                    "_id:$eq": Attr.ID(),
                    "token:$eq": Attr.STR(),
                    "groups:$eq": Attr.LIST(list=[Attr.ID()]),
                },
                {"_id:$eq": Attr.ID(), "token:$eq": Attr.STR()},
            ],
            callable=_reauth,
            exceptions={
                AnonReauthException: True,
                InvalidSessionException: True,
                ExpiredSessionException: False,
            },
            call_args={
                "skip_update_session": Attr.BOOL(),
            },
        ),
        "signout": Func(
            permissions=[Perm(privilege="*")],
            query_attrs={"_id:$eq": Attr.ID()},
            callable=_signout,
            exceptions={
                AnonSignoutException: True,
                InvalidSessionException: True,
            },
        ),
    },
)
