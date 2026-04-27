from __future__ import annotations

from typing import Any

from .base import Resource


class Misc(Resource):
    """Разные ресурсы."""

    def me(self) -> dict[str, Any]:
        """Получить информацию о текущем пользователе/ключе."""
        return self._get("me")

    def balance(self, terminal_id: str | None = None) -> dict[str, Any]:
        """Получить баланс кассы.

        Args:
            terminal_id: ID кассы. Необязателен при API-ключе конкретной кассы.
        """
        params = self._compact({"terminal_id": terminal_id})
        return self._get("balance", params=params)

    def rate(self, terminal_id: str | None = None) -> dict[str, Any]:
        """Получить текущий курс обмена.

        Args:
            terminal_id: Опциональный ID кассы для применения специфичной наценки.
        """
        params = self._compact({"terminal_id": terminal_id})
        return self._get("rate", params=params)
