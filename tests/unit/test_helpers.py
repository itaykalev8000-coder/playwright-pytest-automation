"""Tests for the framework's own helpers. No browser or network needed."""

import pytest

from api_client.automation_exercise import ApiError, AutomationExerciseApi
from utils.helpers import parse_price, unique_email

pytestmark = pytest.mark.unit


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("$29.99", 29.99),
        ("$10", 10.0),
        ("Item total: $39.98", 39.98),
        ("Tax: $3.20", 3.2),
    ],
)
def test_parse_price(text, expected):
    assert parse_price(text) == pytest.approx(expected)


def test_parse_price_without_number_gives_clear_error():
    with pytest.raises(ValueError, match="no price found"):
        parse_price("Free")


def test_unique_email_is_unique():
    emails = {unique_email() for _ in range(100)}
    assert len(emails) == 100
    assert all(email.endswith("@example.com") for email in emails)


class FakeResponse:
    def __init__(self, status, body=None):
        self.status = status
        self.ok = 200 <= status < 300
        self.url = "https://example.test/api/x"
        self._body = body or {}

    def json(self):
        return self._body

    def text(self):
        return "Forbidden"


def test_api_body_returned_on_http_200():
    body = {"responseCode": 404, "message": "User not found!"}
    assert AutomationExerciseApi._body(FakeResponse(200, body)) == body


def test_api_raises_on_http_error():
    with pytest.raises(ApiError, match="Unexpected HTTP 403"):
        AutomationExerciseApi._body(FakeResponse(403))
