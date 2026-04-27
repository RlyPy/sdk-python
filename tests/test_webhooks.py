import time
import unittest

from rollypay import compute_webhook_signature, verify_webhook_signature


class WebhookTests(unittest.TestCase):
    def test_compute_and_verify_signature(self):
        body = b'{"event_type":"payment.paid","payment_id":"pay_123"}'
        timestamp = int(time.time())
        secret = "secret"
        signature = compute_webhook_signature(body, timestamp, secret)

        self.assertTrue(
            verify_webhook_signature(
                body=body,
                timestamp=str(timestamp),
                signature=signature,
                signing_secret=secret,
            )
        )

    def test_verify_rejects_invalid_signature(self):
        body = b'{"event_type":"payment.paid"}'
        timestamp = int(time.time())

        self.assertFalse(
            verify_webhook_signature(
                body=body,
                timestamp=timestamp,
                signature="bad",
                signing_secret="secret",
            )
        )

    def test_verify_rejects_stale_timestamp(self):
        body = "{}"
        timestamp = int(time.time()) - 1000
        signature = compute_webhook_signature(body, timestamp, "secret")

        self.assertFalse(
            verify_webhook_signature(
                body=body,
                timestamp=timestamp,
                signature=signature,
                signing_secret="secret",
                tolerance=300,
            )
        )


if __name__ == "__main__":
    unittest.main()
