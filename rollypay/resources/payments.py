from __future__ import annotations

from decimal import Decimal
from typing import Any, Union

from .base import Resource

AmountFilter = Union[str, Decimal, float, int]


class Payments(Resource):
    """Ресурс для управления платежами."""

    def create(
        self,
        amount: str,
        order_id: str,
        payment_currency: str = "RUB",
        payment_method: str | None = None,
        description: str | None = None,
        customer_id: str | None = None,
        redirect_url: str | None = None,
        success_redirect_url: str | None = None,
        fail_redirect_url: str | None = None,
        metadata: dict[str, Any] | None = None,
        terminal_id: str | None = None,
    ) -> dict[str, Any]:
        """Создать новый платеж.

        Args:
            amount: Сумма платежа (строка, например "100.00").
            order_id: Уникальный ID заказа в вашей системе.
            payment_currency: Валюта платежа (по умолчанию "RUB").
            payment_method: Метод оплаты (необязательно).
            description: Описание платежа.
            customer_id: Идентификатор покупателя (например, email или ID).
            redirect_url: URL для перенаправления пользователя после оплаты.
            success_redirect_url: URL перенаправления при успешной оплате.
            fail_redirect_url: URL перенаправления при неуспешной оплате (expired/canceled).
            metadata: Дополнительные метаданные платежа (словарь).
            terminal_id: ID кассы (необязательно, если используется API ключ конкретной кассы).
        """
        data = self._compact(
            {
                "amount": amount,
                "order_id": order_id,
                "payment_currency": payment_currency,
                "payment_method": payment_method,
                "description": description,
                "customer_id": customer_id,
                "redirect_url": redirect_url,
                "success_redirect_url": success_redirect_url,
                "fail_redirect_url": fail_redirect_url,
                "metadata": metadata,
                "terminal_id": terminal_id,
            }
        )

        return self._post("payments", json=data)

    def get(self, payment_id: str) -> dict[str, Any]:
        """Получить детали платежа по ID."""
        return self._get(f"payments/{payment_id}")

    def list(
        self,
        limit: int = 20,
        page: int = 1,
        account_id: str | None = None,
        terminal_id: str | None = None,
        order_id: str | None = None,
        status: str | None = None,
        date_from: str | None = None,
        date_to: str | None = None,
        amount_from: AmountFilter | None = None,
        amount_to: AmountFilter | None = None,
        search: str | None = None,
    ) -> dict[str, Any]:
        """Получить список платежей с фильтрацией.

        Args:
            limit: Количество записей на странице.
            page: Номер страницы.
            account_id: ID аккаунта (для админов).
            terminal_id: ID кассы.
            order_id: ID заказа.
            status: Статус платежа (например, "created", "paid", "expired").
            date_from: Дата начала (ISO 8601).
            date_to: Дата окончания (ISO 8601).
            amount_from: Минимальная сумма.
            amount_to: Максимальная сумма.
            search: Строка поиска.
        """
        params = self._compact(
            {
                "limit": limit,
                "page": page,
                "account_id": account_id,
                "terminal_id": terminal_id,
                "order_id": order_id,
                "status": status,
                "from": date_from,
                "to": date_to,
                "amount_from": amount_from,
                "amount_to": amount_to,
                "search": search,
            }
        )

        return self._get("payments", params=params)

    def stats(
        self,
        account_id: str | None = None,
        terminal_id: str | None = None,
        order_id: str | None = None,
        status: str | None = None,
        date_from: str | None = None,
        date_to: str | None = None,
        amount_from: AmountFilter | None = None,
        amount_to: AmountFilter | None = None,
        search: str | None = None,
    ) -> dict[str, Any]:
        """Получить статистику по платежам (суммы, количество и т.д.)."""
        params = self._compact(
            {
                "account_id": account_id,
                "terminal_id": terminal_id,
                "order_id": order_id,
                "status": status,
                "from": date_from,
                "to": date_to,
                "amount_from": amount_from,
                "amount_to": amount_to,
                "search": search,
            }
        )

        return self._get("payments/stats", params=params)
