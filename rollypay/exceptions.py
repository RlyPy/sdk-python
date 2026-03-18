class RollyPayError(Exception):
    """Базовое исключение для всех ошибок RollyPay."""
    def __init__(self, message=None, response=None):
        super().__init__(message)
        self.message = message
        self.response = response

    def __str__(self):
        if self.response:
            return f"{self.message} (Статус: {self.response.status_code})"
        return self.message


class APIError(RollyPayError):
    """Вызывается, когда API возвращает ошибку (например, 400)."""
    pass


class AuthenticationError(RollyPayError):
    """Вызывается при ошибке аутентификации (401)."""
    pass


class NotFoundError(RollyPayError):
    """Вызывается, когда ресурс не найден (404)."""
    pass


class ServerError(RollyPayError):
    """Вызывается при внутренней ошибке сервера (500+)."""
    pass
