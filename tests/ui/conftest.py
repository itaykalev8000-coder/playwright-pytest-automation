import allure
import pytest
from playwright.sync_api import expect

from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage
from utils.test_data import PASSWORD, STANDARD_USER


@pytest.fixture
def login_page(page):
    login = LoginPage(page)
    login.open()
    return login


@pytest.fixture
def inventory_page(login_page):
    login_page.login(STANDARD_USER, PASSWORD)
    inventory = InventoryPage(login_page.page)
    expect(inventory.title).to_have_text("Products")
    return inventory


# save the result of each test phase on the item, so fixtures can tell if the test failed
@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    setattr(item, f"rep_{report.when}", report)


@pytest.fixture(autouse=True)
def screenshot_on_failure(request, page):
    yield
    report = getattr(request.node, "rep_call", None)
    if report and report.failed:
        allure.attach(
            page.screenshot(full_page=True),
            name="screenshot",
            attachment_type=allure.attachment_type.PNG,
        )
