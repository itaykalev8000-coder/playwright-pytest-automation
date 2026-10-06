import pytest
from playwright.sync_api import expect

from pages.inventory_page import InventoryPage
from utils.test_data import PASSWORD, PROBLEM_USER

pytestmark = pytest.mark.ui

PRODUCT_COUNT = 6


def test_all_products_displayed(inventory_page):
    expect(inventory_page.items).to_have_count(PRODUCT_COUNT)


@pytest.mark.parametrize(
    ("option", "read", "descending"),
    [
        ("az", InventoryPage.get_item_names, False),
        ("za", InventoryPage.get_item_names, True),
        ("lohi", InventoryPage.get_item_prices, False),
        ("hilo", InventoryPage.get_item_prices, True),
    ],
    ids=["name-a-to-z", "name-z-to-a", "price-low-to-high", "price-high-to-low"],
)
def test_sort(inventory_page, option, read, descending):
    before = read(inventory_page)
    inventory_page.sort_by(option)
    after = read(inventory_page)

    assert after == sorted(after, reverse=descending)
    # sorting must reorder the products, not drop or duplicate any
    assert sorted(after) == sorted(before)
    assert len(after) == PRODUCT_COUNT


# problem_user comes with bugs on purpose, broken sorting is one of them.
# strict: if the bug ever gets fixed the test turns red, so we notice and drop the xfail
@pytest.mark.xfail(reason="known bug: sorting doesn't work for problem_user", strict=True)
def test_sort_for_problem_user(login_page):
    login_page.login(PROBLEM_USER, PASSWORD)
    inventory = InventoryPage(login_page.page)
    inventory.sort_by("lohi")
    prices = inventory.get_item_prices()
    assert prices == sorted(prices)
