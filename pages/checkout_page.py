from pages.base_page import BasePage
from utils.helpers import parse_price


class CheckoutPage(BasePage):
    """All 3 checkout steps: your information -> overview -> complete"""

    def __init__(self, page):
        super().__init__(page)
        # step 1 - your information
        self.first_name_input = page.locator("#first-name")
        self.last_name_input = page.locator("#last-name")
        self.postal_code_input = page.locator("#postal-code")
        self.continue_button = page.locator("#continue")
        self.error_message = page.locator("[data-test='error']")
        # step 2 - overview
        self.item_prices = page.locator(".cart_item .inventory_item_price")
        self.subtotal_label = page.locator(".summary_subtotal_label")
        self.finish_button = page.locator("#finish")
        # step 3 - complete
        self.complete_header = page.locator(".complete-header")

    def fill_information(self, first_name, last_name, postal_code):
        self.first_name_input.fill(first_name)
        self.last_name_input.fill(last_name)
        self.postal_code_input.fill(postal_code)
        self.continue_button.click()

    def get_subtotal(self):
        return parse_price(self.subtotal_label.inner_text())

    def get_item_prices(self):
        return [parse_price(price) for price in self.item_prices.all_inner_texts()]

    def finish(self):
        self.finish_button.click()
