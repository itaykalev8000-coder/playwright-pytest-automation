import pytest

pytestmark = pytest.mark.api


@pytest.mark.smoke
def test_get_all_products(api):
    body = api.get_products()
    assert body["responseCode"] == 200
    assert len(body["products"]) > 0


def test_products_have_expected_fields(api):
    for product in api.get_products()["products"]:
        assert isinstance(product["id"], int)
        assert product["name"]
        assert product["price"].startswith("Rs.")
        assert product["category"]["category"]


def test_post_to_products_list_not_supported(api):
    body = api.post_products()
    assert body["responseCode"] == 405
    assert body["message"] == "This request method is not supported."


@pytest.mark.parametrize("term", ["top", "tshirt", "jean"])
def test_search_product(api, term):
    body = api.search_product(term)
    assert body["responseCode"] == 200
    assert body["products"], f"no results for '{term}'"
    for product in body["products"]:
        text = f"{product['name']} {product['category']['category']}".lower()
        assert term in text, f"'{product['name']}' doesn't match the search '{term}'"


def test_search_without_parameter(api):
    body = api.search_product()
    assert body["responseCode"] == 400
    assert body["message"] == "Bad request, search_product parameter is missing in POST request."
