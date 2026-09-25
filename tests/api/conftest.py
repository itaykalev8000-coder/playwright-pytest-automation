import pytest

from api_client.automation_exercise import AutomationExerciseApi
from utils.helpers import unique_email
from utils.test_data import API_BASE_URL, NEW_USER


@pytest.fixture(scope="session")
def api(playwright):
    request_context = playwright.request.new_context(base_url=API_BASE_URL)
    yield AutomationExerciseApi(request_context)
    request_context.dispose()


@pytest.fixture
def new_user(api):
    """Registers a fresh user for the test and deletes it at the end."""
    user = {**NEW_USER, "email": unique_email()}
    body = api.create_account(user)
    assert body["responseCode"] == 201, body
    yield user
    api.delete_account(user["email"], user["password"])
