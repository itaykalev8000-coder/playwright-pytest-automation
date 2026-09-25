import pytest
from playwright.sync_api import expect

from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage
from utils.test_data import LOCKED_OUT_USER, PASSWORD, STANDARD_USER

pytestmark = pytest.mark.ui


@pytest.mark.smoke
def test_login_with_valid_user(login_page):
    login_page.login(STANDARD_USER, PASSWORD)
    expect(InventoryPage(login_page.page).title).to_have_text("Products")


@pytest.mark.parametrize(
    "username, password, expected_error",
    [
        (LOCKED_OUT_USER, PASSWORD, "Sorry, this user has been locked out"),
        (STANDARD_USER, "wrong_password", "Username and password do not match any user in this service"),
        ("", PASSWORD, "Username is required"),
        (STANDARD_USER, "", "Password is required"),
    ],
    ids=["locked-out-user", "wrong-password", "empty-username", "empty-password"],
)
def test_login_errors(login_page, username, password, expected_error):
    login_page.login(username, password)
    expect(login_page.error_message).to_contain_text(expected_error)


def test_inventory_requires_login(page):
    page.goto(InventoryPage.path)
    expect(LoginPage(page).error_message).to_contain_text("when you are logged in")


def test_logout(inventory_page):
    inventory_page.logout()
    expect(LoginPage(inventory_page.page).login_button).to_be_visible()
