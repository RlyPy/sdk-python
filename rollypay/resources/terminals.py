from typing import Any, Dict, List, Optional
from .base import Resource

class Terminals(Resource):
    """Ресурс для управления кассами (терминалами)."""

    def list(self) -> List[Dict[str, Any]]:
        """Получить список всех касс аккаунта."""
        return self._get("terminals")

    def get(self, terminal_id: str) -> Dict[str, Any]:
        """Получить информацию о конкретной кассе по ID."""
        return self._get(f"terminals/{terminal_id}")

    def update(self, terminal_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Обновить настройки кассы.
        
        Args:
            terminal_id: ID кассы для обновления.
            data: Словарь с обновляемыми полями:
                - callback_url: str (URL для уведомлений)
                - success_redirect_url: str (URL перенаправления при успехе)
                - fail_redirect_url: str (URL перенаправления при ошибке)
                - redirect_url: str (Общий URL перенаправления)
                - show_platform_branding: bool (Показывать брендинг платформы)
                - fee_payer: str ("client" - платит клиент, или "merchant" - платит магазин)
        """
        return self._put(f"terminals/{terminal_id}", json=data)

    def rotate_api_key(self, terminal_id: str) -> Dict[str, str]:
        """Сгенерировать новый API ключ для кассы. Возвращает новый ключ."""
        return self._post(f"terminals/{terminal_id}/rotate-api-key")

    def get_providers(self, terminal_id: str) -> List[Dict[str, Any]]:
        """Получить список провайдеров, включенных для кассы."""
        return self._get(f"terminals/{terminal_id}/providers")
