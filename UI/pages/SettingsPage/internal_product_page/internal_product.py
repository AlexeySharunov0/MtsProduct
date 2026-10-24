import logging

from playwright.sync_api import Page

from UI.base.WebPage import WebPage
from UI.pages.SettingsPage.internal_product_page.internal_product_locators import InternalProductLocators

logger = logging.getLogger(__name__)


class InternalProductPage(WebPage, InternalProductLocators):

    def __init__(self, page: Page, url: str = None):
        WebPage.__init__(self, page)  # Явный вызов инициализатора WebPage
        InternalProductLocators.__init__(self, page)  # Явный вызов инициализатора CanvasPageLocators
        self._page = page
        self.base_url = url if url else 'https://stage.prodboard.example.com/prefs/product_internal'
        self.get_page(self.base_url)
