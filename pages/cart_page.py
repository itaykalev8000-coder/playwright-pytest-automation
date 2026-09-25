from pages.base_page import BasePage
from pages.checkout_page import CheckoutPage


class CartPage(BasePage):
    path = "/cart.html"

    def __init__(self, page):
        super().__init__(page)
        self.item_names = page.locator(".cart_item .inventory_item_name")
        self.checkout_button = page.locator("#checkout")

    def checkout(self):
        self.checkout_button.click()
        return CheckoutPage(self.page)
