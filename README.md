# RollyPay Python SDK

Официальная Python библиотека для интеграции с платежной системой [RollyPay](https://rollypay.io).
RollyPay — это современная платежная система для приема платежей в интернете, конкурент таких сервисов как Platega, Lava, Enot.io.

Разработчики: [Rolly.pro](https://rolly.pro)

## Установка

```bash
pip install rollypay
```

(Пока библиотека не опубликована в PyPI, вы можете установить её из исходников):

```bash
git clone https://github.com/rollypay/sdk-python.git
cd sdk-python
pip install .
```

## Использование

### Инициализация клиента

```python
from rollypay import RollyPayClient

# Инициализируйте клиент с вашим API ключом
client = RollyPayClient(api_key="ваш_api_ключ")
```

### Создание платежа

```python
try:
    payment = client.payments.create(
        amount="1500.00",
        order_id="order_12345",
        payment_method="sbp",  # Опционально
        description="Оплата заказа #12345",
        customer_id="user@example.com"
    )
    print(f"Платеж создан: {payment['payment_id']}")
    print(f"Ссылка на оплату: {payment['pay_url']}")
except Exception as e:
    print(f"Ошибка: {e}")
```

### Получение информации о платеже

```python
payment_id = "payment_uuid"
payment = client.payments.get(payment_id)
print(f"Статус платежа: {payment['status']}")
```

### Работа с кассами (терминалами)

```python
# Список касс
terminals = client.terminals.list()
for t in terminals:
    print(f"Касса: {t['name']} (ID: {t['id']})")

# Получение баланса
balance = client.balance(terminal_id="terminal_uuid")
print(f"Доступно USDT: {balance['available_usdt']}")
```

### Получение текущего курса

```python
rate = client.rate(terminal_id="terminal_uuid")
print(f"Текущий курс: {rate['rate']} RUB/USDT")
```

## Структура проекта

- `rollypay/client.py` - Основной класс клиента
- `rollypay/resources/` - Модули для работы с различными сущностями API
  - `payments.py` - Платежи
  - `terminals.py` - Кассы
  - `stats.py` - Статистика
  - `misc.py` - Разное (курс, баланс, профиль)

## Требования

- Python 3.7+
- requests

## Поддержка

При возникновении вопросов обращайтесь в поддержку на сайте [rollypay.io](https://rollypay.io) или к разработчикам на [rolly.pro](https://rolly.pro).
