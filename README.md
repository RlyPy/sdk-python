# RollyPay Python SDK

[![PyPI version](https://badge.fury.io/py/rollypay.svg)](https://badge.fury.io/py/rollypay)
[![Python Versions](https://img.shields.io/pypi/pyversions/rollypay.svg)](https://pypi.org/project/rollypay/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Официальная Python библиотека для интеграции с платежной системой [RollyPay](https://rollypay.io).

**RollyPay** — это современная платежная система для приема платежей в интернете, предлагающая удобный интерфейс, высокую конверсию и простую интеграцию. Мы предоставляем гибкие инструменты для мерчантов.

Разработчики: [Rolly.pro](https://rolly.pro)

## Возможности

*   **Управление платежами**: Создание, получение информации, списки платежей.
*   **Управление кассами (терминалами)**: Просмотр списка касс, получение настроек, ротация API ключей.
*   **Статистика**: Получение финансовой сводки и аналитики.
*   **Курсы валют**: Актуальные курсы обмена.
*   **Баланс**: Проверка баланса кассы.

## Установка

Установите библиотеку через pip:

```bash
pip install rollypay
```

## Быстрый старт

### Инициализация клиента

Для начала работы вам потребуется API ключ, который можно получить в личном кабинете RollyPay.

```python
from rollypay import RollyPayClient, RollyPayError

# Инициализируйте клиент с вашим API ключом
client = RollyPayClient(api_key="ваш_api_ключ")
```

### Создание платежа

```python
try:
    payment = client.payments.create(
        amount="1500.00",
        order_id="order_12345",
        payment_method="sbp",  # Опционально: sbp, card, usdt и т.д.
        description="Оплата заказа #12345",
        customer_id="user@example.com",
        redirect_url="https://myshop.com/success"
    )
    
    print(f"ID платежа: {payment['payment_id']}")
    print(f"Ссылка на оплату: {payment['pay_url']}")
    
except RollyPayError as e:
    print(f"Произошла ошибка при создании платежа: {e}")
```

### Проверка статуса платежа

```python
payment_id = "payment_uuid"
payment = client.payments.get(payment_id)

if payment['status'] == 'succeeded':
    print("Платеж успешно оплачен!")
elif payment['status'] == 'pending':
    print("Платеж ожидает оплаты.")
else:
    print(f"Статус платежа: {payment['status']}")
```

### Работа с кассами (терминалами)

```python
# Получить список всех доступных касс
terminals = client.terminals.list()

for t in terminals:
    print(f"Касса: {t['name']} (ID: {t['id']})")

# Получить баланс конкретной кассы
balance = client.balance(terminal_id="terminal_uuid")
print(f"Доступно USDT: {balance['available_usdt']}")
```

### Получение текущего курса

```python
rate = client.rate(terminal_id="terminal_uuid")
print(f"Текущий курс: {rate['rate']} RUB/USDT")
```

## Обработка ошибок

Библиотека предоставляет несколько типов исключений для удобной обработки ошибок:

*   `RollyPayError`: Базовый класс для всех ошибок SDK.
*   `APIError`: Ошибка при выполнении запроса к API.
*   `AuthenticationError`: Ошибка аутентификации (неверный API ключ).
*   `NotFoundError`: Запрашиваемый ресурс не найден (404).
*   `ServerError`: Ошибка на стороне сервера RollyPay (5xx).

## Поддержка

При возникновении вопросов или проблем обращайтесь в поддержку:
*   Сайт: [rollypay.io](https://rollypay.io)
*   Разработчики: [rolly.pro](https://rolly.pro)
*   Email: support@rollypay.io
