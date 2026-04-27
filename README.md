# RollyPay Python SDK

[![PyPI version](https://badge.fury.io/py/rollypay.svg)](https://badge.fury.io/py/rollypay)
[![Python Versions](https://img.shields.io/pypi/pyversions/rollypay.svg)](https://pypi.org/project/rollypay/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Официальная Python библиотека для интеграции с платежной системой
[RollyPay](https://rollypay.io).

SDK работает с API RollyPay: создание и получение платежей, список платежей,
кассы, баланс, курс RUB/USDT, выводы USDT и проверка подписи вебхуков. Клиент
автоматически передает `X-API-Key` и генерирует уникальный `X-Nonce` для каждого
запроса.

## Установка

```bash
pip install rollypay
```

Требуется Python 3.9+.

## Быстрый старт

```python
from rollypay import RollyPayClient, RollyPayError

client = RollyPayClient(api_key="ваш_api_ключ")

try:
    payment = client.payments.create(
        amount="1500.00",
        order_id="order_12345",
        payment_method="sbp",
        description="Оплата заказа #12345",
        customer_id="user@example.com",
        success_redirect_url="https://myshop.com/payment/success",
        fail_redirect_url="https://myshop.com/payment/fail",
        metadata={"internal_ref": "INV-2026-0042"},
    )
except RollyPayError as exc:
    print(f"Ошибка RollyPay: {exc}")
else:
    print(payment["payment_id"])
    print(payment["pay_url"])
```

## Платежи

```python
payment = client.payments.get("payment_uuid")

if payment["status"] == "paid":
    print("Платеж успешно оплачен")
elif payment["status"] == "created":
    print("Платеж создан и ожидает оплаты")
else:
    print(f"Статус: {payment['status']}")
```

Статусы платежа из API: `created`, `processing`, `paid`, `expired`, `canceled`,
`chargeback`.

```python
payments = client.payments.list(status="paid", terminal_id="terminal_uuid")
stats = client.payments.stats(status="paid")
```

## Кассы, баланс и курс

```python
terminals = client.terminals.list()

balance = client.balance()
rate = client.rate()

terminal_balance = client.balance(terminal_id="terminal_uuid")
terminal_rate = client.rate(terminal_id="terminal_uuid")
```

При использовании API-ключа конкретной кассы `terminal_id` можно не передавать
там, где это допускает API.

## Выводы

```python
payout = client.payouts.create(
    amount_usdt="50.00",
    wallet_address="TJYkxBf0XG3P8nFHv1i9zNbeQ7oCF3qLzR",
    network="TRC-20",
    idempotency_key="payout_20260223_001",
)

payouts = client.payouts.list()
```

## Вебхуки

Для проверки подписи нужен сырой body запроса, до JSON-парсинга.

```python
from rollypay import verify_webhook_signature

is_valid = verify_webhook_signature(
    body=raw_body,
    timestamp=request.headers["X-Timestamp"],
    signature=request.headers["X-Signature"],
    signing_secret="signing_secret_кассы",
)

if not is_valid:
    raise PermissionError("Invalid RollyPay webhook signature")
```

## Обработка ошибок

Библиотека предоставляет исключения:

* `RollyPayError`: базовый класс для всех ошибок SDK.
* `APIError`: ошибка API или транспорта.
* `AuthenticationError`: ошибка аутентификации, включая неверный API-ключ или nonce.
* `ForbiddenError`: недостаточно прав.
* `NotFoundError`: ресурс не найден.
* `ConflictError`: конфликт состояния или дубликат.
* `RateLimitError`: превышен лимит запросов.
* `ServerError`: ошибка на стороне RollyPay.
* `ServiceUnavailableError`: сервис временно недоступен.

## Разработка

```bash
python3 -m venv .venv
.venv/bin/pip install -e ".[dev]"
.venv/bin/python -m unittest discover
```

Документация API: [docs.rollypay.io](https://docs.rollypay.io).
