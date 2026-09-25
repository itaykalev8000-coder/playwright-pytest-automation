from pages.base_page import BasePage


class LoginPage(BasePage):
    path = "/"

    def __init__(self, page):
        super().__init__(page)
        self.username_input = page.get_by_placeholder("Username")
        self.password_input = page.get_by_placeholder("Password")
        self.login_button = page.locator("#login-button")
        self.error_message = page.locator("[data-test='error']")

    def login(self, username, password):
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()
