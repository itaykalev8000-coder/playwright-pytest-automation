import pytest

pytestmark = pytest.mark.api


@pytest.mark.smoke
def test_verify_login_with_valid_details(api, new_user):
    body = api.verify_login(new_user["email"], new_user["password"])
    assert body["responseCode"] == 200
    assert body["message"] == "User exists!"


def test_verify_login_with_wrong_password(api, new_user):
    body = api.verify_login(new_user["email"], "not-the-password")
    assert body["responseCode"] == 404
    assert body["message"] == "User not found!"


def test_verify_login_without_email(api):
    body = api.verify_login(password="Test1234!")
    assert body["responseCode"] == 400
    assert body["message"] == (
        "Bad request, email or password parameter is missing in POST request."
    )


def test_get_user_details_by_email(api, new_user):
    body = api.get_user_by_email(new_user["email"])
    assert body["responseCode"] == 200
    user = body["user"]
    assert user["email"] == new_user["email"]
    assert user["name"] == new_user["name"]
    assert user["city"] == new_user["city"]


def test_deleted_user_cannot_log_in(api, user_factory):
    user = user_factory()

    body = api.delete_account(user["email"], user["password"])
    assert body["responseCode"] == 200
    user_factory.forget(user)  # it's gone, nothing left for teardown
    assert body["message"] == "Account deleted!"

    assert api.verify_login(user["email"], user["password"])["responseCode"] == 404
