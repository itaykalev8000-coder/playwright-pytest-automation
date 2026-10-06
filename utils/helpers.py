import re
import uuid

_PRICE = re.compile(r"\d+(?:\.\d+)?")


def parse_price(text):
    """'$29.99', '$10' or 'Item total: $39.98' -> float"""
    match = _PRICE.search(text)
    if match is None:
        raise ValueError(f"no price found in {text!r}")
    return float(match.group())


def unique_email():
    return f"qa_{uuid.uuid4().hex[:10]}@example.com"
