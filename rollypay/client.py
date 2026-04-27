from __future__ import annotations

import uuid
from typing import Any, Callable

import requests

from .exceptions import (
    APIError,
    AuthenticationError,
    ConflictError,
    ForbiddenError,
    NotFoundError,
    RateLimitError,
    ServerError,
    ServiceUnavailableError,
)
from .resources.misc import Misc
from .resources.payments import Payments
from .resources.payouts import Payouts
from .resources.stats import Stats
from .resources.terminals import Terminals

DEFAULT_BASE_URL = "https://rollypay.io/api/v1"
SDK_VERSION = "0.2.0"


class RollyPayClient:
    """
    Основной клиент для API RollyPay.
    RollyPay - современная платежная система для приема платежей.
    Разработчики: https://rolly.pro

    Args:
        api_key: API ключ для аутентификации.
        base_url: Базовый URL API RollyPay (по умолчанию https://rollypay.io/api/v1).
        timeout: Таймаут запроса в секундах (по умолчанию 30).
        nonce_factory: Функция генерации уникального X-Nonce для каждого запроса.
    """

    def __init__(
        self,
        api_key: str,
        base_url: str = DEFAULT_BASE_URL,
        timeout: int = 30,
        nonce_factory: Callable[[], str] | None = None,
    ):
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self._nonce_factory = nonce_factory or (lambda: str(uuid.uuid4()))
        self._session = requests.Session()
        self._session.headers.update(
            {
                "X-API-Key": self.api_key,
                "Content-Type": "application/json",
                "User-Agent": f"rollypay-python-sdk/{SDK_VERSION}",
            }
        )

        # Инициализация ресурсов
        self.terminals = Terminals(self)
        self.payments = Payments(self)
        self.payouts = Payouts(self)
        self.stats = Stats(self)
        self.misc = Misc(self)

    @property
    def me(self):
        """Прямой доступ к эндпоинту 'me'."""
        return self.misc.me

    @property
    def balance(self):
        """Прямой доступ к эндпоинту 'balance'."""
        return self.misc.balance

    @property
    def rate(self):
        """Прямой доступ к эндпоинту 'rate'."""
        return self.misc.rate

    def request(self, method: str, path: str, **kwargs) -> Any:
        """Выполнить запрос к API."""
        url = f"{self.base_url}/{path.lstrip('/')}"
        headers = dict(kwargs.pop("headers", {}) or {})
        if "X-Nonce" not in headers:
            headers["X-Nonce"] = self._nonce_factory()

        try:
            response = self._session.request(
                method,
                url,
                timeout=self.timeout,
                headers=headers,
                **kwargs,
            )
        except requests.RequestException as e:
            raise APIError(f"Ошибка запроса: {e}") from e

        if response.status_code >= 400:
            self._handle_error(response)

        try:
            return response.json()
        except ValueError:
            return response.content

    def _handle_error(self, response: requests.Response):
        """Обработка ошибок ответа."""
        try:
            data = response.json()
            message = data.get("error") or data.get("message") or "Неизвестная ошибка"
        except ValueError:
            message = response.text or "Неизвестная ошибка"

        if response.status_code == 401:
            raise AuthenticationError(message, response)
        elif response.status_code == 403:
            raise ForbiddenError(message, response)
        elif response.status_code == 404:
            raise NotFoundError(message, response)
        elif response.status_code == 409:
            raise ConflictError(message, response)
        elif response.status_code == 429:
            raise RateLimitError(message, response)
        elif response.status_code == 503:
            raise ServiceUnavailableError(message, response)
        elif response.status_code >= 500:
            raise ServerError(message, response)
        else:
            raise APIError(message, response)
