from playwright.sync_api import APIRequestContext, APIResponse


class AutomationExerciseApi:
    """Client for https://automationexercise.com/api_list

    Heads up: this API answers with HTTP 200 even for errors and puts the
    real status in the body ("responseCode"), so every method returns the
    JSON body and the tests check responseCode / message from there.
    """

    def __init__(self, request: APIRequestContext):
        self.request = request

    @staticmethod
    def _body(response: APIResponse):
        # if the HTTP status itself ever stops being 200 we want to know about it
        assert response.ok, f"Unexpected HTTP {response.status} for {response.url}"
        return response.json()

    def get_products(self):
        return self._body(self.request.get("/api/productsList"))

    def post_products(self):
        return self._body(self.request.post("/api/productsList"))

    def search_product(self, term=None):
        form = {"search_product": term} if term else None
        return self._body(self.request.post("/api/searchProduct", form=form))

    def verify_login(self, email=None, password=None):
        form = {}
        if email is not None:
            form["email"] = email
        if password is not None:
            form["password"] = password
        return self._body(self.request.post("/api/verifyLogin", form=form))

    def create_account(self, user):
        return self._body(self.request.post("/api/createAccount", form=user))

    def delete_account(self, email, password):
        form = {"email": email, "password": password}
        return self._body(self.request.delete("/api/deleteAccount", form=form))

    def get_user_by_email(self, email):
        return self._body(self.request.get("/api/getUserDetailByEmail", params={"email": email}))
