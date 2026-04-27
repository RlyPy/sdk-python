import hashlib
import hmac
import time
from typing import Optional, Union

WebhookBody = Union[bytes, str]


def _to_bytes(value: WebhookBody) -> bytes:
    if isinstance(value, bytes):
        return value
    return value.encode("utf-8")


def compute_webhook_signature(
    body: WebhookBody,
    timestamp: Union[str, int],
    signing_secret: str,
) -> str:
    """Вычислить HMAC-SHA256 подпись вебхука RollyPay."""
    signed_payload = str(timestamp).encode("utf-8") + b"." + _to_bytes(body)
    return hmac.new(
        signing_secret.encode("utf-8"),
        signed_payload,
        hashlib.sha256,
    ).hexdigest()


def verify_webhook_signature(
    body: WebhookBody,
    timestamp: Union[str, int],
    signature: str,
    signing_secret: str,
    tolerance: Optional[int] = 300,
) -> bool:
    """Проверить подпись вебхука RollyPay.

    Args:
        body: Сырой body запроса, до JSON-парсинга.
        timestamp: Значение заголовка X-Timestamp.
        signature: Значение заголовка X-Signature.
        signing_secret: Секрет подписи кассы.
        tolerance: Допустимое отклонение timestamp в секундах. Передайте None,
            чтобы отключить проверку свежести.
    """
    if not signature or not signing_secret:
        return False

    try:
        timestamp_int = int(timestamp)
    except (TypeError, ValueError):
        return False

    if tolerance is not None and abs(time.time() - timestamp_int) > tolerance:
        return False

    expected = compute_webhook_signature(body, timestamp_int, signing_secret)
    return hmac.compare_digest(expected, signature)
