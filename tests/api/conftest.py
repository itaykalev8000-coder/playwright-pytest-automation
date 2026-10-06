import warnings

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
def user_factory(api):
    """Registers fresh users for a test and deletes whatever is left at the end.

    A test that deletes the user itself calls `forget(user)` so teardown skips it.
    """
    created = []

    def create():
        user = {**NEW_USER, "email": unique_email()}
        body = api.create_account(user)
        assert body["responseCode"] == 201, body
        created.append(user)
        return user

    create.forget = created.remove
    yield create

    for user in created:
        body = api.delete_account(user["email"], user["password"])
        # a failed cleanup shouldn't fail the test, but it must not be silent either
        if body.get("responseCode") != 200:
            warnings.warn(f"could not delete test user {user['email']}: {body}", stacklevel=1)


@pytest.fixture
def new_user(user_factory):
    """A single registered user, deleted at the end of the test."""
    return user_factory()
