class RollyPayError(Exception):
    """Базовое исключение для всех ошибок RollyPay."""

    def __init__(self, message=None, response=None):
        super().__init__(message)
        self.message = message or "Неизвестная ошибка"
        self.response = response

    def __str__(self):
        if self.response:
            return f"{self.message} (Статус: {self.response.status_code})"
        return str(self.message)


class APIError(RollyPayError):
    """Вызывается, когда API возвращает ошибку (например, 400)."""

    pass


class AuthenticationError(RollyPayError):
    """Вызывается при ошибке аутентификации (401)."""

    pass


class ForbiddenError(RollyPayError):
    """Вызывается при недостатке прав (403)."""

    pass


class NotFoundError(RollyPayError):
    """Вызывается, когда ресурс не найден (404)."""

    pass


class ConflictError(RollyPayError):
    """Вызывается при конфликте состояния или дубликате (409)."""

    pass


class RateLimitError(RollyPayError):
    """Вызывается при превышении лимита запросов (429)."""

    pass


class ServerError(RollyPayError):
    """Вызывается при внутренней ошибке сервера (500+)."""

    pass


class ServiceUnavailableError(ServerError):
    """Вызывается при временной недоступности сервиса (503)."""

    pass
