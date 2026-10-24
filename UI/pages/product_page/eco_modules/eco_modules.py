import logging

from playwright.sync_api import Page

from UI.base.WebPage import WebPage
from UI.pages.product_page.eco_modules.eco_modules_locators import EcoModulesPageLocators

logger = logging.getLogger(__name__)


class EcoModulesPage(WebPage, EcoModulesPageLocators):
    def __init__(self, page: Page, url: str = None):
        WebPage.__init__(self, page)  # Явный вызов инициализатора WebPage
        EcoModulesPageLocators.__init__(self, page)  # Явный вызов инициализатора CanvasPageLocators
        self._page = page

        self.base_url = url if url else 'https://stage.prodboard.example.com/product/BI_60/eco'
        self.get_page(self.base_url)
