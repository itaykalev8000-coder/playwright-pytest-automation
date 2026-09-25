import pytest
from playwright.sync_api import expect

from pages.inventory_page import InventoryPage
from utils.test_data import PASSWORD, PROBLEM_USER

pytestmark = pytest.mark.ui


def test_all_products_displayed(inventory_page):
    expect(inventory_page.items).to_have_count(6)


def test_sort_by_price_low_to_high(inventory_page):
    inventory_page.sort_by("lohi")
    prices = inventory_page.get_item_prices()
    assert prices == sorted(prices)


def test_sort_by_name_z_to_a(inventory_page):
    inventory_page.sort_by("za")
    names = inventory_page.get_item_names()
    assert names == sorted(names, reverse=True)


# problem_user comes with bugs on purpose, broken sorting is one of them
@pytest.mark.xfail(reason="known bug: sorting doesn't work for problem_user")
def test_sort_for_problem_user(login_page):
    login_page.login(PROBLEM_USER, PASSWORD)
    inventory = InventoryPage(login_page.page)
    inventory.sort_by("lohi")
    prices = inventory.get_item_prices()
    assert prices == sorted(prices)
