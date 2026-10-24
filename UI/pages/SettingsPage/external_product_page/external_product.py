import logging

from playwright.sync_api import Page

from UI.base.WebPage import WebPage
from UI.pages.SettingsPage.external_product_page.external_product_locators import ExternalProductLocators

logger = logging.getLogger(__name__)


class ExternalProductPage(WebPage, ExternalProductLocators):

    def __init__(self, page: Page, url: str = None):
        WebPage.__init__(self, page)  # Явный вызов инициализатора WebPage
        ExternalProductLocators.__init__(self, page)  # Явный вызов инициализатора CanvasPageLocators
        self._page = page
        self.base_url = url if url else 'https://stage.prodboard.example.com/prefs/product_commercial'
        self.get_page(self.base_url)
