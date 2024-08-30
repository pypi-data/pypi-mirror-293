import logging
from http import HTTPStatus
from typing import Dict, Literal, Optional

import requests
from requests import Response

from ...retry import retry_request
from .auth import Auth
from .safe_request import RequestSafeMode, handle_response
from .utils import build_url

logger = logging.getLogger(__name__)

Headers = Optional[Dict[str, str]]

# https://requests.readthedocs.io/en/latest/api/#requests.request
HttpMethod = Literal["GET", "OPTIONS", "HEAD", "POST", "PUT", "PATCH", "DELETE"]

DEFAULT_TIMEOUT = 60
RETRY_ON_EXPIRED_TOKEN = 1


class APIClient:
    """
    Interface to easily query REST-API with GET and POST requests

    Args:
        auth: auth class to enable logging to the API
        host: base url of the API
        headers: common headers to all calls that will be made
        timeout: read timeout for each request
        safe_mode: ignore certain exceptions based on status codes

    Note:
        If the auth implements a refreshing mechanism (refresh_token)
        the token is automatically refreshed once upon receiving the
        401: UNAUTHORIZED status code
    """

    def __init__(
        self,
        auth: Auth,
        host: Optional[str] = None,
        headers: Headers = None,
        timeout: int = DEFAULT_TIMEOUT,
        safe_mode: RequestSafeMode = RequestSafeMode(),
    ):
        self.base_headers = headers or {}
        self._host = host
        self._timeout = timeout
        self._auth = auth
        self._safe_mode = safe_mode

    def _call(
        self,
        method: HttpMethod,
        endpoint: str,
        *,
        headers: Headers = None,
        params: Optional[dict] = None,
        pagination_params: Optional[dict] = None,
    ) -> Response:
        headers = headers or {}
        _pagination_params = pagination_params or {}
        params = params or {}

        url = build_url(self._host, endpoint)
        combined_params = {**params, **_pagination_params}

        return requests.request(
            method=method,
            url=url,
            auth=self._auth,
            headers={**self.base_headers, **headers},
            params=combined_params if method == "GET" else None,
            json=combined_params if method == "POST" else None,
            timeout=self._timeout,
        )

    @retry_request(
        status_codes=(HTTPStatus.UNAUTHORIZED,),
        max_retries=RETRY_ON_EXPIRED_TOKEN,
    )
    def _get(
        self,
        endpoint: str,
        *,
        headers: Headers = None,
        params: Optional[dict] = None,
        pagination_params: Optional[dict] = None,
    ):
        response = self._call(
            method="GET",
            endpoint=endpoint,
            params=params,
            pagination_params=pagination_params,
            headers=headers,
        )
        if response.status_code == HTTPStatus.UNAUTHORIZED:
            self._auth.refresh_token()

        return handle_response(response, safe_mode=self._safe_mode)

    @retry_request(
        status_codes=(HTTPStatus.UNAUTHORIZED,),
        max_retries=RETRY_ON_EXPIRED_TOKEN,
    )
    def _post(
        self,
        endpoint: str,
        *,
        headers: Headers = None,
        data: Optional[dict] = None,
        pagination_params: Optional[dict] = None,
    ):
        response = self._call(
            method="POST",
            endpoint=endpoint,
            params=data,
            pagination_params=pagination_params,
            headers=headers,
        )
        if response.status_code == HTTPStatus.UNAUTHORIZED:
            self._auth.refresh_token()

        return handle_response(response, safe_mode=self._safe_mode)
