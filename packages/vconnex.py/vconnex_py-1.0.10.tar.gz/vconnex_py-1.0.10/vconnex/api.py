"""Vconnex API."""

from __future__ import annotations

import hashlib
import hmac
import json
import logging
import time
from types import SimpleNamespace
from typing import Any
from urllib.parse import urljoin

import requests

from vconnex import __version__

_API_TOKEN = "auth/project-token"

_LOGGER = logging.getLogger(__name__)


class TokenInfo:
    """Token Info."""

    def __init__(self, token_resp: dict[str, Any]) -> None:
        """Create Token Info object."""
        self.token = token_resp.get("token")
        self.expire_time = token_resp.get("expireTime", 0)
        self.data = token_resp.get("data")


class ApiResponse(SimpleNamespace):
    """Api Response."""

    code: int
    msg: str
    data: Any


class ReturnCode:
    """Return Code."""

    SUCCESS = 1
    ERROR = 2
    NOT_FOUND = 15


class VconnexAPI:
    """VconnexAPI."""

    def __init__(
        self,
        endpoint: str,
        client_id: str,
        client_secret: str,
        project_code: str = None,
        lang: str = "vi",
    ) -> None:
        """Create VconnexAPI object."""
        self.session = requests.session()

        self.endpoint = endpoint + "/" if not endpoint.endswith("/") else endpoint
        self.client_id = client_id
        self.client_secret = client_secret
        self.lang = lang
        self.project_code = project_code

        self.token_info: TokenInfo = None

    def __sign(
        self,
        ts: int,
        algorithm: str,
        method: str,
        url: str,
        params: dict[str, Any] = None,
        body: dict[str, Any] = None,
    ) -> str:
        """Sign"""

        prep = requests.PreparedRequest()
        prep.prepare_method(method)
        prep.prepare_url(url, params)
        prep.prepare_headers(None)
        prep.prepare_body(data=None, files=None, json=body)
        raw_signs = [
            f"{prep.method} {prep.path_url}",
            str(ts),
            f"{hashlib.md5(prep.body).hexdigest() if prep.body is not None else ""}",
        ]

        digestmod = hashlib.sha256
        if not algorithm.endswith("SHA256"):
            algorithm = "SHA256"

        if algorithm.startswith("Hmac"):
            sign = hmac.new(
                self.client_secret.encode("utf8"),
                msg="\n".join(raw_signs).encode("utf8"),
                digestmod=digestmod,
            ).hexdigest()
        else:
            sign = digestmod("\n".join(raw_signs).encode("utf8")).hexdigest()

        return f"algorithm={algorithm}, signature={sign}, t={ts}"

    def __get_token_info(self) -> TokenInfo:
        """Get exist token or retrieve new one"""
        if self.token_info is None or self.token_info.expire_time < (
            (int(time.time()) - 120) * 1000
        ):
            self.token_info = None
            try:
                resp = self.post(
                    _API_TOKEN,
                    {
                        "clientId": self.client_id,
                        "clientSecret": self.client_secret,
                        "projectCode": self.project_code,
                    },
                )

                if resp is not None and resp.code == ReturnCode.SUCCESS:
                    self.token_info = TokenInfo(resp.data)
            except Exception:
                _LOGGER.exception("Error while request token.\n")

        return self.token_info

    def __request(
        self,
        method: str,
        path: str,
        params: dict[str, Any] = None,
        body: dict[str, Any] = None,
    ) -> ApiResponse:
        """Request base"""
        if path.startswith("/"):
            path = path[1:]
        token_info = None if path.startswith(_API_TOKEN) else self.__get_token_info()

        ts = int(time.time())
        headers = {
            "lang": self.lang,
            "v": __version__,
            "t": str(ts),
        }

        if self.token_info is not None:
            headers["X-Authorization"] = token_info.token
        elif not path.startswith(_API_TOKEN):
            _LOGGER.error("Unauthorized request")
            raise RuntimeError("Unauthorized")

        url = urljoin(self.endpoint, path)
        sign = self.__sign(
            ts=ts,
            algorithm="HmacSHA256",
            method=method,
            url=url,
            params=params,
            body=body,
        )
        headers["X-Signature"] = sign

        logging.debug(
            f"Request: method={method}, url={url}, params={params}, body={body}, t={ts}"
        )

        response = self.session.request(
            method=method,
            url=url,
            params=params,
            json=body,
            headers=headers,
        )

        if response.ok is False:
            _LOGGER.error(
                "Response error: code=%d, body=%s",
                response.status_code,
                response.content,
            )
            return None

        result = ApiResponse(**response.json())

        _LOGGER.debug(
            "Response: %s",
            json.dumps(
                result.__dict__ if hasattr(result, "__dict__") else result,
                ensure_ascii=False,
                indent=2,
            ),
        )

        return result

    def get_client_id(self) -> str:
        """Get client id."""
        return self.client_id

    def is_valid(self) -> bool:
        """Validate."""
        token_info = self.__get_token_info()
        return token_info is not None

    def get_token_data(self):
        """Get token data."""
        token_info = self.__get_token_info()
        return token_info.data if token_info is not None else None

    def get(self, path: str, params: dict[str, Any] = None) -> ApiResponse:
        """Get request."""
        return self.__request("GET", path, params, None)

    def post(self, path: str, body: dict[str, Any] = None) -> ApiResponse:
        """Post request."""
        return self.__request("POST", path, None, body)

    def put(self, path: str, body: dict[str, Any] = None) -> ApiResponse:
        """Put request."""
        return self.__request("PUT", path, None, body)

    def delete(self, path: str, params: dict[str, Any] = None) -> ApiResponse:
        """Delete request."""
        return self.__request("DELETE", path, params, None)
