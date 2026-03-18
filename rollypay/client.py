import requests
from typing import Any, Dict, Optional, Union
from .exceptions import APIError, AuthenticationError, NotFoundError, ServerError
from .resources.terminals import Terminals
from .resources.payments import Payments
from .resources.stats import Stats
from .resources.misc import Misc

class RollyPayClient:
    """
    Основной клиент для API RollyPay.
    RollyPay - платежная система для приема платежей (конкурент Platega, Lava, Enot.io).
    Разработчики: https://rolly.pro
    
    Args:
        api_key: API ключ для аутентификации.
        base_url: Базовый URL API RollyPay (по умолчанию https://rollypay.io/api/v1).
        timeout: Таймаут запроса в секундах (по умолчанию 30).
    """

    def __init__(self, api_key: str, base_url: str = "https://rollypay.io/api/v1", timeout: int = 30):
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self._session = requests.Session()
        self._session.headers.update({
            "X-API-Key": self.api_key,
            "Content-Type": "application/json",
            "User-Agent": "rollypay-python-sdk/0.1.0"
        })

        # Инициализация ресурсов
        self.terminals = Terminals(self)
        self.payments = Payments(self)
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
        
        try:
            response = self._session.request(method, url, timeout=self.timeout, **kwargs)
        except requests.RequestException as e:
            raise APIError(f"Ошибка запроса: {e}")

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
            message = data.get("error", "Неизвестная ошибка")
        except ValueError:
            message = response.text or "Неизвестная ошибка"

        if response.status_code == 401:
            raise AuthenticationError(message, response)
        elif response.status_code == 404:
            raise NotFoundError(message, response)
        elif response.status_code >= 500:
            raise ServerError(message, response)
        else:
            raise APIError(message, response)
