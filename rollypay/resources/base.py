from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from rollypay.client import RollyPayClient


class Resource:
    """Base class for all resources."""

    def __init__(self, client: RollyPayClient):
        self.client = client

    @staticmethod
    def _compact(params: dict[str, Any]) -> dict[str, Any]:
        return {key: value for key, value in params.items() if value is not None}

    def _get(self, path: str, params: dict[str, Any] | None = None) -> Any:
        return self.client.request("GET", path, params=params)

    def _post(
        self,
        path: str,
        json: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
    ) -> Any:
        return self.client.request("POST", path, json=json, params=params)

    def _put(
        self,
        path: str,
        json: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
    ) -> Any:
        return self.client.request("PUT", path, json=json, params=params)

    def _delete(self, path: str) -> Any:
        return self.client.request("DELETE", path)
