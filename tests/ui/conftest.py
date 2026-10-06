import allure
import pytest
from playwright.sync_api import expect

from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage
from utils.test_data import PASSWORD, STANDARD_USER


@pytest.fixture(scope="session")
def base_url(pytestconfig):
    # pytest-base-url only reads base_url from pytest.ini on the main process,
    # so under pytest-xdist (-n) the workers would get None. Fall back to the ini value.
    return pytestconfig.getoption("base_url") or pytestconfig.getini("base_url")


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


# keep each phase's report on the item, so fixtures can tell if the test failed
@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    setattr(item, f"rep_{report.when}", report)


@pytest.fixture(autouse=True)
def screenshot_on_failure(request, page):
    yield
    # check setup too, otherwise a failure inside a fixture (e.g. login) has no screenshot
    reports = (getattr(request.node, f"rep_{when}", None) for when in ("setup", "call"))
    if any(report and report.failed for report in reports):
        allure.attach(
            page.screenshot(full_page=True),
            name="screenshot",
            attachment_type=allure.attachment_type.PNG,
        )
