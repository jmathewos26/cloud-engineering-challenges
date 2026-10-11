import pytest

import normalize

GOOD_ROW = {
    "order_id": "A-1",
    "order_date": "03/14/2026",
    "customer": "C001",
    "total": "$1,200.50",
    "state": "PAID",
}


def test_money_symbols_and_commas_are_removed():
    assert normalize.parse_money("$1,200.50") == 1200.50


def test_status_is_standardized():
    assert normalize.normalize_a(GOOD_ROW)["status"] == "completed"


def test_timestamp_is_iso_8601_utc():
    assert normalize.normalize_a(GOOD_ROW)["timestamp"] == "2026-03-14T00:00:00+00:00"


def test_unix_timestamp_and_text_amount_are_converted():
    item = {
        "id": "B-1",
        "created": 1773446400,
        "customer_id": "C001",
        "amount": "75.5",
        "status": "FAILED",
    }
    rec = normalize.normalize_b(item)
    assert rec["amount_usd"] == 75.5
    assert rec["status"] == "failed"
    assert rec["timestamp"].endswith("+00:00")


def test_negative_amount_is_rejected():
    rec = {"customer_id": "C001", "amount_usd": -10}
    assert "negative amount" in normalize.validate(rec)


def test_missing_customer_is_rejected():
    rec = {"customer_id": "", "amount_usd": 10}
    assert "missing customer_id" in normalize.validate(rec)


def test_unrecognized_date_format_raises_error():
    bad = dict(GOOD_ROW, order_date="15-03-2026")
    with pytest.raises(ValueError):
        normalize.normalize_a(bad)