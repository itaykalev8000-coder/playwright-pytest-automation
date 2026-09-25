import pytest
from playwright.sync_api import expect

from utils.test_data import BACKPACK, BIKE_LIGHT

pytestmark = pytest.mark.ui


@pytest.mark.smoke
def test_add_product_updates_cart_badge(inventory_page):
    inventory_page.add_to_cart(BACKPACK)
    expect(inventory_page.cart_badge).to_have_text("1")


def test_remove_product_clears_cart_badge(inventory_page):
    inventory_page.add_to_cart(BACKPACK)
    inventory_page.remove_from_cart(BACKPACK)
    expect(inventory_page.cart_badge).not_to_be_visible()


def test_cart_contains_added_products(inventory_page):
    inventory_page.add_to_cart(BACKPACK)
    inventory_page.add_to_cart(BIKE_LIGHT)
    cart = inventory_page.open_cart()
    expect(cart.item_names).to_have_text([BACKPACK, BIKE_LIGHT])
