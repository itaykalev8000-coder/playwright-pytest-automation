import re

import pytest
from playwright.sync_api import expect

from utils.test_data import BACKPACK, BIKE_LIGHT, CUSTOMER

pytestmark = pytest.mark.ui

TAX_RATE = 0.08  # SauceDemo charges a flat 8% tax


@pytest.mark.smoke
def test_complete_purchase(inventory_page):
    products = [BACKPACK, BIKE_LIGHT]
    # prices as the customer saw them on the products page
    expected_prices = [inventory_page.get_price_of(name) for name in products]
    for name in products:
        inventory_page.add_to_cart(name)

    checkout = inventory_page.open_cart().checkout()
    checkout.fill_information(**CUSTOMER)

    # the overview must show the same prices, and add them up correctly
    assert checkout.get_item_prices() == pytest.approx(expected_prices)
    subtotal = checkout.get_subtotal()
    tax = checkout.get_tax()
    assert subtotal == pytest.approx(sum(expected_prices))
    assert tax == pytest.approx(subtotal * TAX_RATE, abs=0.01)
    assert checkout.get_total() == pytest.approx(subtotal + tax)

    checkout.finish()
    expect(checkout.complete_header).to_have_text(
        re.compile("thank you for your order", re.IGNORECASE)
    )


@pytest.mark.parametrize(
    ("first_name", "last_name", "postal_code", "expected_error"),
    [
        ("", "Levi", "7403201", "First Name is required"),
        ("Dana", "", "7403201", "Last Name is required"),
        ("Dana", "Levi", "", "Postal Code is required"),
    ],
    ids=["missing-first-name", "missing-last-name", "missing-postal-code"],
)
def test_checkout_required_fields(
    inventory_page, first_name, last_name, postal_code, expected_error
):
    inventory_page.add_to_cart(BACKPACK)
    checkout = inventory_page.open_cart().checkout()
    checkout.fill_information(first_name, last_name, postal_code)
    expect(checkout.error_message).to_contain_text(expected_error)
