import re
import uuid


def parse_price(text):
    """'$29.99' or 'Item total: $39.98' -> float"""
    return float(re.search(r"\d+\.\d+", text).group())


def unique_email():
    return f"qa_{uuid.uuid4().hex[:10]}@example.com"
