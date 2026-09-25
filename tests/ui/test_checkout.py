import re

import pytest
from playwright.sync_api import expect

from utils.test_data import BACKPACK, BIKE_LIGHT, CUSTOMER

pytestmark = pytest.mark.ui


@pytest.mark.smoke
def test_complete_purchase(inventory_page):
    inventory_page.add_to_cart(BACKPACK)
    inventory_page.add_to_cart(BIKE_LIGHT)
    checkout = inventory_page.open_cart().checkout()
    checkout.fill_information(**CUSTOMER)

    # item total on the overview page should be the sum of the item prices
    subtotal = checkout.get_subtotal()
    assert subtotal == pytest.approx(sum(checkout.get_item_prices()))

    checkout.finish()
    expect(checkout.complete_header).to_have_text(re.compile("thank you for your order", re.IGNORECASE))


@pytest.mark.parametrize(
    "first_name, last_name, postal_code, expected_error",
    [
        ("", "Levi", "7403201", "First Name is required"),
        ("Dana", "", "7403201", "Last Name is required"),
        ("Dana", "Levi", "", "Postal Code is required"),
    ],
    ids=["missing-first-name", "missing-last-name", "missing-postal-code"],
)
def test_checkout_required_fields(inventory_page, first_name, last_name, postal_code, expected_error):
    inventory_page.add_to_cart(BACKPACK)
    checkout = inventory_page.open_cart().checkout()
    checkout.fill_information(first_name, last_name, postal_code)
    expect(checkout.error_message).to_contain_text(expected_error)
