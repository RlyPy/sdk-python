from typing import Any, Dict, Optional
from .base import Resource

class Misc(Resource):
    """Разные ресурсы."""

    def me(self) -> Dict[str, Any]:
        """Получить информацию о текущем пользователе/ключе."""
        return self._get("me")

    def balance(self, terminal_id: str) -> Dict[str, Any]:
        """Получить баланс кассы."""
        return self._get("balance", params={"terminal_id": terminal_id})

    def rate(self, terminal_id: Optional[str] = None) -> Dict[str, Any]:
        """Получить текущий курс обмена.
        
        Args:
            terminal_id: Опциональный ID кассы для применения специфичной наценки.
        """
        params = {}
        if terminal_id:
            params["terminal_id"] = terminal_id
        return self._get("rate", params=params)
