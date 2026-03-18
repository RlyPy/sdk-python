from typing import Any, Dict, Optional
from .base import Resource

class Stats(Resource):
    """Ресурс для статистики и финансов продавца."""

    def overview(self, terminal_id: str) -> Dict[str, Any]:
        """Получить обзорную статистику по кассе."""
        return self._get("merchant/stats/overview", params={"terminal_id": terminal_id})

    def finance_summary(self, terminal_id: Optional[str] = None) -> Dict[str, Any]:
        """Получить финансовую сводку."""
        params = {}
        if terminal_id:
            params["terminal_id"] = terminal_id
        return self._get("merchant/finance/summary", params=params)

    def timeseries(self, 
                   metric: str, 
                   interval: str, 
                   terminal_id: Optional[str] = None) -> Dict[str, Any]:
        """Получить статистику во времени (графики).
        
        Args:
            metric: Метрика (например, "volume", "count").
            interval: Интервал (например, "day", "hour").
            terminal_id: ID кассы (необязательно).
        """
        params = {
            "metric": metric,
            "interval": interval,
        }
        if terminal_id:
            params["terminal_id"] = terminal_id
        return self._get("merchant/stats/timeseries", params=params)
