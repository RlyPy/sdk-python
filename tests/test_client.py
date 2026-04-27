import unittest
from unittest.mock import Mock

import requests

from rollypay import (
    APIError,
    AuthenticationError,
    ConflictError,
    ForbiddenError,
    NotFoundError,
    RateLimitError,
    RollyPayClient,
    RollyPayError,
    ServerError,
    ServiceUnavailableError,
)


def make_response(status_code=200, body=b'{"ok": true}'):
    response = requests.Response()
    response.status_code = status_code
    response._content = body
    response.headers["Content-Type"] = "application/json"
    return response


class ClientTests(unittest.TestCase):
    def test_root_exports_quickstart_error(self):
        self.assertTrue(issubclass(RollyPayError, Exception))

    def test_request_sends_api_key_and_fresh_nonce(self):
        nonces = iter(["nonce-1", "nonce-2"])
        client = RollyPayClient(
            api_key="rpk_test",
            base_url="https://example.test/api/v1",
            nonce_factory=lambda: next(nonces),
        )
        client._session.request = Mock(return_value=make_response())

        client.request("GET", "balance")
        client.request("GET", "rate")

        self.assertEqual(client._session.headers["X-API-Key"], "rpk_test")
        first_call = client._session.request.call_args_list[0]
        second_call = client._session.request.call_args_list[1]
        self.assertEqual(first_call.kwargs["headers"]["X-Nonce"], "nonce-1")
        self.assertEqual(second_call.kwargs["headers"]["X-Nonce"], "nonce-2")

    def test_request_preserves_custom_headers(self):
        client = RollyPayClient(api_key="rpk_test", nonce_factory=lambda: "nonce")
        client._session.request = Mock(return_value=make_response())

        client.request("GET", "balance", headers={"X-Trace-ID": "trace-1"})

        headers = client._session.request.call_args.kwargs["headers"]
        self.assertEqual(headers["X-Trace-ID"], "trace-1")
        self.assertEqual(headers["X-Nonce"], "nonce")

    def test_request_preserves_custom_nonce(self):
        nonce_factory = Mock(return_value="generated")
        client = RollyPayClient(api_key="rpk_test", nonce_factory=nonce_factory)
        client._session.request = Mock(return_value=make_response())

        client.request("GET", "balance", headers={"X-Nonce": "provided"})

        nonce_factory.assert_not_called()
        headers = client._session.request.call_args.kwargs["headers"]
        self.assertEqual(headers["X-Nonce"], "provided")

    def test_error_mapping(self):
        cases = [
            (400, APIError),
            (401, AuthenticationError),
            (403, ForbiddenError),
            (404, NotFoundError),
            (409, ConflictError),
            (429, RateLimitError),
            (500, ServerError),
            (503, ServiceUnavailableError),
        ]

        for status_code, error_class in cases:
            with self.subTest(status_code=status_code):
                client = RollyPayClient(api_key="rpk_test")
                client._session.request = Mock(
                    return_value=make_response(status_code, b'{"error": "boom"}')
                )

                with self.assertRaises(error_class) as ctx:
                    client.request("GET", "payments")

                self.assertIn("boom", str(ctx.exception))

    def test_balance_terminal_id_is_optional(self):
        client = RollyPayClient(api_key="rpk_test")
        client.request = Mock(return_value={"available_usdt": "1.00"})

        client.balance()

        client.request.assert_called_once_with("GET", "balance", params={})

    def test_payouts_create_and_list(self):
        client = RollyPayClient(api_key="rpk_test")
        client.request = Mock(return_value={"id": "po_123"})

        client.payouts.create(
            amount_usdt="50.00",
            wallet_address="wallet",
            network="TRC-20",
            idempotency_key="idem-1",
            terminal_id="terminal-1",
        )
        client.payouts.list()

        create_call = client.request.call_args_list[0]
        list_call = client.request.call_args_list[1]

        self.assertEqual(create_call.args[:2], ("POST", "payouts"))
        self.assertEqual(
            create_call.kwargs["json"],
            {
                "amount_usdt": "50.00",
                "wallet_address": "wallet",
                "network": "TRC-20",
                "idempotency_key": "idem-1",
            },
        )
        self.assertEqual(create_call.kwargs["params"], {"terminal_id": "terminal-1"})
        self.assertEqual(list_call.args[:2], ("GET", "payouts"))
        self.assertEqual(list_call.kwargs["params"], {})


if __name__ == "__main__":
    unittest.main()
