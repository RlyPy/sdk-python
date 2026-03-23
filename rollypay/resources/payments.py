from typing import Any, Dict, List, Optional
from .base import Resource

class Payments(Resource):
    """Ресурс для управления платежами."""

    def create(self, 
               amount: str,
               order_id: str,
               payment_currency: str = "RUB",
               payment_method: Optional[str] = None,
               description: Optional[str] = None,
               customer_id: Optional[str] = None,
               redirect_url: Optional[str] = None,
               success_redirect_url: Optional[str] = None,
               fail_redirect_url: Optional[str] = None,
               metadata: Optional[Dict[str, Any]] = None,
               terminal_id: Optional[str] = None) -> Dict[str, Any]:
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
        data = {
            "amount": amount,
            "order_id": order_id,
            "payment_currency": payment_currency,
        }
        if payment_method:
            data["payment_method"] = payment_method
        if description:
            data["description"] = description
        if customer_id:
            data["customer_id"] = customer_id
        if redirect_url:
            data["redirect_url"] = redirect_url
        if success_redirect_url:
            data["success_redirect_url"] = success_redirect_url
        if fail_redirect_url:
            data["fail_redirect_url"] = fail_redirect_url
        if metadata:
            data["metadata"] = metadata
        if terminal_id:
            data["terminal_id"] = terminal_id
            
        return self._post("payments", json=data)

    def get(self, payment_id: str) -> Dict[str, Any]:
        """Получить детали платежа по ID."""
        return self._get(f"payments/{payment_id}")

    def list(self, 
             limit: int = 20,
             page: int = 1,
             account_id: Optional[str] = None,
             terminal_id: Optional[str] = None,
             order_id: Optional[str] = None,
             status: Optional[str] = None,
             date_from: Optional[str] = None,
             date_to: Optional[str] = None,
             amount_from: Optional[float] = None,
             amount_to: Optional[float] = None,
             search: Optional[str] = None) -> Dict[str, Any]:
        """Получить список платежей с фильтрацией.
        
        Args:
            limit: Количество записей на странице.
            page: Номер страницы.
            account_id: ID аккаунта (для админов).
            terminal_id: ID кассы.
            order_id: ID заказа.
            status: Статус платежа (например, "PAID", "CREATED").
            date_from: Дата начала (ISO 8601).
            date_to: Дата окончания (ISO 8601).
            amount_from: Минимальная сумма.
            amount_to: Максимальная сумма.
            search: Строка поиска.
        """
        params = {
            "limit": limit,
            "page": page,
        }
        if account_id: params["account_id"] = account_id
        if terminal_id: params["terminal_id"] = terminal_id
        if order_id: params["order_id"] = order_id
        if status: params["status"] = status
        if date_from: params["from"] = date_from
        if date_to: params["to"] = date_to
        if amount_from is not None: params["amount_from"] = amount_from
        if amount_to is not None: params["amount_to"] = amount_to
        if search: params["search"] = search
        
        return self._get("payments", params=params)

    def stats(self, 
              account_id: Optional[str] = None,
              terminal_id: Optional[str] = None,
              order_id: Optional[str] = None,
              status: Optional[str] = None,
              date_from: Optional[str] = None,
              date_to: Optional[str] = None,
              amount_from: Optional[float] = None,
              amount_to: Optional[float] = None,
              search: Optional[str] = None) -> Dict[str, Any]:
        """Получить статистику по платежам (суммы, количество и т.д.)."""
        params = {}
        if account_id: params["account_id"] = account_id
        if terminal_id: params["terminal_id"] = terminal_id
        if order_id: params["order_id"] = order_id
        if status: params["status"] = status
        if date_from: params["from"] = date_from
        if date_to: params["to"] = date_to
        if amount_from is not None: params["amount_from"] = amount_from
        if amount_to is not None: params["amount_to"] = amount_to
        if search: params["search"] = search
        
        return self._get("payments/stats", params=params)
