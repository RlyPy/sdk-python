from typing import Any, Dict, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from rollypay.client import RollyPayClient

class Resource:
    """Base class for all resources."""
    def __init__(self, client: "RollyPayClient"):
        self.client = client

    def _get(self, path: str, params: Optional[Dict[str, Any]] = None) -> Any:
        return self.client.request("GET", path, params=params)

    def _post(self, path: str, json: Optional[Dict[str, Any]] = None) -> Any:
        return self.client.request("POST", path, json=json)

    def _put(self, path: str, json: Optional[Dict[str, Any]] = None) -> Any:
        return self.client.request("PUT", path, json=json)

    def _delete(self, path: str) -> Any:
        return self.client.request("DELETE", path)
