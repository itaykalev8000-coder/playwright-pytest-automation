from pages.base_page import BasePage
from pages.cart_page import CartPage
from utils.helpers import parse_price


class InventoryPage(BasePage):
    path = "/inventory.html"

    def __init__(self, page):
        super().__init__(page)
        self.title = page.locator(".title")
        self.items = page.locator(".inventory_item")
        self.item_names = page.locator(".inventory_item_name")
        self.item_prices = page.locator(".inventory_item_price")
        self.sort_dropdown = page.locator(".product_sort_container")
        self.cart_badge = page.locator(".shopping_cart_badge")
        self.cart_link = page.locator(".shopping_cart_link")

    def sort_by(self, option):
        # values in the dropdown: az, za, lohi, hilo
        self.sort_dropdown.select_option(option)

    def get_item_names(self):
        return self.item_names.all_inner_texts()

    def get_item_prices(self):
        return [parse_price(price) for price in self.item_prices.all_inner_texts()]

    def add_to_cart(self, product_name):
        product = self.items.filter(has_text=product_name)
        product.get_by_role("button", name="Add to cart").click()

    def remove_from_cart(self, product_name):
        product = self.items.filter(has_text=product_name)
        product.get_by_role("button", name="Remove").click()

    def open_cart(self):
        self.cart_link.click()
        return CartPage(self.page)

    def logout(self):
        self.page.locator("#react-burger-menu-btn").click()
        self.page.locator("#logout_sidebar_link").click()
