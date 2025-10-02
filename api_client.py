from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional

import requests
from requests import Response

from config import Config


class ApiError(Exception):
    """Error genérico para respuestas fallidas de la API."""

    def __init__(self, status_code: int, message: str, details: Optional[Any] = None):
        super().__init__(message)
        self.status_code = status_code
        self.details = details

    def __str__(self) -> str:
        base = f"[{self.status_code}] {self.args[0]}"
        if self.details:
            return f"{base}: {self.details}"
        return base


@dataclass
class ApiConfig:
    base_url: str = Config.API_BASE_URL.rstrip('/')
    timeout: float = Config.API_TIMEOUT


class ApiClient:
    """Cliente HTTP simple para consumir la API del taller."""

    def __init__(self, config: Optional[ApiConfig] = None):
        self.config = config or ApiConfig()
        self.session = requests.Session()
        self.session.headers.update({"Content-Type": "application/json", "Accept": "application/json"})

    def _request(
        self,
        method: str,
        path: str,
        *,
        json: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
    ) -> Any:
        url = f"{self.config.base_url}{path}" if path.startswith('/') else f"{self.config.base_url}/{path}"
        try:
            response = self.session.request(
                method,
                url,
                json=json,
                params=params,
                timeout=self.config.timeout,
            )
        except requests.RequestException as exc:
            raise ApiError(0, "No se pudo conectar con la API", str(exc)) from exc

        return self._handle_response(response)

    def _handle_response(self, response: Response) -> Any:
        if 200 <= response.status_code < 300:
            if response.status_code == 204:
                return None
            try:
                return response.json()
            except ValueError:
                return None

        message = "Error desconocido"
        details: Optional[Any] = None
        try:
            payload = response.json()
            if isinstance(payload, dict):
                message = payload.get("message") or payload.get("error") or message
                details = payload.get("details")
        except ValueError:
            message = response.text or message

        raise ApiError(response.status_code, message, details)

    def get(self, path: str, *, params: Optional[Dict[str, Any]] = None) -> Any:
        return self._request("GET", path, params=params)

    def post(self, path: str, *, json: Optional[Dict[str, Any]] = None) -> Any:
        return self._request("POST", path, json=json)

    def put(self, path: str, *, json: Optional[Dict[str, Any]] = None) -> Any:
        return self._request("PUT", path, json=json)

    def patch(self, path: str, *, json: Optional[Dict[str, Any]] = None) -> Any:
        return self._request("PATCH", path, json=json)

    def delete(self, path: str) -> Any:
        return self._request("DELETE", path)


shared_client = ApiClient()
