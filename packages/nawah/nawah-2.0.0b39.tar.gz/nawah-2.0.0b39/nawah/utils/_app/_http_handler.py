import copy
import datetime
import json
import logging
import re
from typing import TYPE_CHECKING, Any

import aiohttp.web
from multidict import MultiDict
from requests_toolbelt.multipart import decoder

from nawah.classes import Query, app_encoder
from nawah.config import Config
from nawah.enums import Event
from nawah.utils import camel_to_upper

from .._call import _convert_deprecated_query, call
from .._config import _compile_anon_session, _compile_anon_user

if TYPE_CHECKING:
    from nawah.types import NawahDoc, NawahQuerySpecial, NawahSession

logger = logging.getLogger("nawah")


async def _http_handler(request: aiohttp.web.Request):
    headers = MultiDict(
        [
            ("Server", "Nawah"),
            ("Powered-By", "Nawah, https://nawah.masaar.com"),
            ("Access-Control-Allow-Origin", "*"),
            ("Access-Control-Allow-Methods", "GET,POST,OPTIONS"),
            (
                "Access-Control-Allow-Headers",
                "Content-Type,X-Auth-Bearer,X-Auth-Token,X-Auth-App",
            ),
            ("Access-Control-Expose-Headers", "Content-Disposition"),
        ]
    )

    logger.debug("Received new %s request: %s", request.method, request.match_info)

    if request.method == "OPTIONS":
        return aiohttp.web.Response(
            status=200,
            headers=headers,
            body=app_encoder.encode(
                {
                    "status": 200,
                    "msg": "OPTIONS request is allowed",
                }
            ),
        )

    module_name = request.url.parts[1]
    func_name = request.url.parts[2]
    request_args = dict(request.match_info.items())

    session: "NawahSession" = {
        "conn": {
            "REMOTE_ADDR": request.remote or "localhost",
            "HTTP_USER_AGENT": "",
            "HTTP_ORIGIN": "",
            "client_app": "__public",
            "args": {},
        }
    }

    session["conn"]["HTTP_USER_AGENT"] = (
        request.headers["user-agent"] if "user-agent" in request.headers else ""
    )
    session["conn"]["HTTP_ORIGIN"] = (
        request.headers["origin"] if "origin" in request.headers else ""
    )

    if "X-Auth-App" in request.headers:
        session["conn"]["client_app"] = request.headers["X-Auth-App"]

    # [TODO] Add condition to now allow a connection from a client with client_app = __sys
    if request.method == "POST" and Config.client_apps:
        if request.headers["X-Auth-App"] not in Config.client_apps or (
            Config.client_apps[request.headers["X-Auth-App"]].type == "web"
            and session["conn"]["HTTP_ORIGIN"]
            not in Config.client_apps[request.headers["X-Auth-App"]].origin
        ):
            logger.debug("Denying request due to unauthorised client_app")
            headers["Content-Type"] = "application/json; charset=utf-8"
            return aiohttp.web.Response(
                status=403,
                headers=headers,
                body=app_encoder.encode(
                    {
                        "status": 403,
                        "msg": "X-Auth headers could not be verified",
                        "args": {"code": "CORE_SESSION_INVALID_XAUTH"},
                    }
                ).encode("utf-8"),
            )

    if " X-Auth-Bearer" in request.headers or "X-Auth-Token" in request.headers:
        logger.debug("Detected 'X-Auth' header[s]")
        if (
            "X-Auth-Bearer" not in request.headers
            or "X-Auth-Token" not in request.headers
            or "X-Auth-App" not in request.headers
        ):
            logger.debug("Denying request due to missing 'X-Auth' header")
            headers["Content-Type"] = "application/json; charset=utf-8"
            return aiohttp.web.Response(
                status=400,
                headers=headers,
                body=app_encoder.encode(
                    {
                        "status": 400,
                        "msg": "One 'X-Auth' headers was set but not the other",
                    }
                ).encode("utf-8"),
            )
        try:
            session_results = await call(
                "session/reauth",
                skip_events=[Event.PERM],
                session=session,
                query=Query(
                    [
                        {"_id": {"$eq": request.headers["X-Auth-Bearer"]}},
                        {"token": {"$eq": request.headers["X-Auth-Token"]}},
                        {"groups": {"$eq": []}},
                    ]
                ),
                args={"skip_update_session": True},
            )
        except Exception:
            logger.debug("Denying request due to fail to reauth")
            headers["Content-Type"] = "application/json; charset=utf-8"
            return aiohttp.web.Response(
                status=403,
                headers=headers,
                body=app_encoder.encode(
                    {
                        "status": 403,
                        "msg": "Failed to reauth",
                        "args": {"code": "FAILED_REAUTH"},
                    }
                ).encode("utf-8"),
            )

        user_session = session_results["args"]["session"]
    else:
        anon_user = _compile_anon_user()
        anon_session = _compile_anon_session()
        anon_session["user"] = anon_user
        user_session = anon_session

    for key in user_session:
        session[key] = copy.deepcopy(user_session[key])

    doc: "NawahDoc" = {}

    if request.content_length:
        doc_content = await request.content.read()
        # Check Content-Type to decide how to deserialise content
        if request.content_type.startswith("multipart/form-data"):
            multipart_content_type = request.headers["Content-Type"]
            doc = {}
            try:
                multipart_parts = decoder.MultipartDecoder(
                    doc_content, multipart_content_type
                ).parts

                for part in multipart_parts:
                    content_disposition = part.headers[b"Content-Disposition"].decode(
                        "UTF-8"
                    )
                    attr_name_match = re.findall('name="([^"]+)"', content_disposition)
                    if not attr_name_match:
                        continue
                    attr_name = attr_name_match[0]
                    doc[attr_name] = part.content
                    # For non-file values, decode unto str
                    if "filename" not in content_disposition:
                        doc[attr_name] = doc[attr_name].decode("UTF-8")
            except decoder.ImproperBodyPartContentException:
                logger.debug(
                    "Ignoring processing 'doc_content' due to 'decoder."
                    "ImproperBodyPartContentException' Exception"
                )

        elif request.content_type.startswith("application/json"):
            doc = json.loads(doc_content)

    # Attempt to generate value for query
    query = None
    # If request_args (from GET route path) has length, use it as query
    if len(request_args):
        query = Query([{k: {"$eq": v}} for k, v in request_args.items()])  # type: ignore
    # Otherwise, check if doc contains $query
    else:
        if "$query" in doc:
            logger.debug(
                "Detected '$query' attr in doc. Attempting to process it as Query"
            )
            logger.debug("Raw value of '$query' before processing: %s", doc["$query"])
            try:
                if isinstance(doc["$query"], list):
                    # [TODO] Change to Warning, then Error
                    logger.debug("Call is using deprecated query format: %s", query)
                    query_special: "NawahQuerySpecial" = {}
                    for step in doc["$query"]:
                        if not isinstance(step, dict):
                            continue
                        for attr_name, attr_val in step.items():
                            if isinstance(attr_name, str) and attr_name[0] == "$":
                                query_special[attr_name] = attr_val
                    query = Query(
                        _convert_deprecated_query(doc["$query"]), special=query_special
                    )
                else:
                    special: Any = {}
                    if "$special" in doc["$query"]:
                        special = doc["$query"]["$special"]
                    if "$pipe" in doc["$query"]:
                        query = Query(doc["$query"]["$pipe"], special=special)
                    else:
                        query = Query(special=special)
            except Exception as e:  # pylint: disable=broad-except
                logger.error("Failed to process '$query' doc attr. Exception: %s", e)

            logger.debug("Processed value of '$query' after processing: %s", query)

            del doc["$query"]

    try:
        results = await call(
            f"{module_name}/{func_name}",
            session=session,
            query=query,
            doc=doc,
        )
    except Exception as e:  # pylint: disable=broad-except
        status = getattr(e, "status", 500)
        msg = "Unexpected error has occurred"
        code = camel_to_upper(e.__class__.__name__).replace("_EXCEPTION", "")
        if status != 500 and e.args:
            msg = e.args[0]

        results = {
            "status": status,
            "msg": msg,
            "args": {"code": code},
        }

    if "return" not in results["args"] or results["args"]["return"] == "json":
        if "return" in results["args"]:
            del results["args"]["return"]
        headers["Content-Type"] = "application/json; charset=utf-8"
        if results["status"] == 404:
            return aiohttp.web.Response(
                status=results["status"],
                headers=headers,
                body=app_encoder.encode(
                    {"status": 404, "msg": "Requested content not found"}
                ).encode("utf-8"),
            )
        return aiohttp.web.Response(
            status=results["status"],
            headers=headers,
            body=app_encoder.encode(results),
        )

    if results["args"]["return"] == "file":
        del results["args"]["return"]
        status = results["status"]
        expiry_time = datetime.datetime.utcnow() + datetime.timedelta(days=30)
        headers["Last-Modified"] = str(results["args"]["docs"][0]["lastModified"])
        headers["Content-Type"] = results["args"]["docs"][0]["type"]
        headers["Cache-Control"] = "public, max-age=31536000"
        headers["Expires"] = expiry_time.strftime("%a, %d %b %Y %H:%M:%S GMT")
        content = results["args"]["docs"][0]["content"]
        if "If-Modified-Since" in request.headers:
            if request.headers["If-Modified-Since"] == headers["Last-Modified"]:
                status = 304
                content = b""
        return aiohttp.web.Response(
            status=status,
            headers=headers,
            body=content,
        )

    if results["args"]["return"] == "msg":
        del results["args"]["return"]
        headers["Content-Type"] = "application/json; charset=utf-8"
        return aiohttp.web.Response(
            status=results["status"], headers=headers, body=results["msg"]
        )

    headers["Content-Type"] = "application/json; charset=utf-8"
    return aiohttp.web.Response(
        status=405,
        headers=headers,
        body=app_encoder.encode({"status": 405, "msg": "405 NOT ALLOWED"}),
    )
