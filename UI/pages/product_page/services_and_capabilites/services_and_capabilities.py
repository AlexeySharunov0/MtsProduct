import logging

from playwright.sync_api import Page

from UI.base.WebPage import WebPage
from UI.pages.product_page.services_and_capabilites.services_and_capabilites_locators import \
    ServiceAndCapabilitiesPageLocators

logger = logging.getLogger(__name__)


class ServiceAndCapabilitiesPage(WebPage, ServiceAndCapabilitiesPageLocators):
    def __init__(self, page: Page):
        WebPage.__init__(self, page)  # Явный вызов инициализатора WebPage
        ServiceAndCapabilitiesPageLocators.__init__(self, page)  # Явный вызов инициализатора CanvasPageLocators
        self._page = page

        self.base_url = 'https://stage.prodboard.example.com/product/BI_60/main'
        self.get_page(self.base_url)
