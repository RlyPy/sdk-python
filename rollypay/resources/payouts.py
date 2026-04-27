from __future__ import annotations

from typing import Any

from .base import Resource


class Payouts(Resource):
    """Ресурс для вывода USDT на внешний кошелек."""

    def create(
        self,
        amount_usdt: str,
        wallet_address: str,
        network: str,
        idempotency_key: str | None = None,
        terminal_id: str | None = None,
    ) -> dict[str, Any]:
        """Создать заявку на вывод.

        Args:
            amount_usdt: Сумма вывода в USDT.
            wallet_address: Адрес кошелька получателя.
            network: Сеть вывода, например "TRC-20".
            idempotency_key: Ключ идемпотентности для защиты от дублей.
            terminal_id: ID кассы. Необязателен при API-ключе конкретной кассы.
        """
        data = self._compact(
            {
                "amount_usdt": amount_usdt,
                "wallet_address": wallet_address,
                "network": network,
                "idempotency_key": idempotency_key,
            }
        )
        params = self._compact({"terminal_id": terminal_id})
        return self._post("payouts", json=data, params=params)

    def list(self, terminal_id: str | None = None) -> list[dict[str, Any]]:
        """Получить список выводов по кассе."""
        params = self._compact({"terminal_id": terminal_id})
        return self._get("payouts", params=params)
