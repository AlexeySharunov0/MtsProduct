import logging

from playwright.sync_api import Page

from UI.base.WebPage import WebPage
from UI.pages.SettingsPage.roles_page.roles_locators import RolesLocators

logger = logging.getLogger(__name__)


class RolesPage(WebPage, RolesLocators):

    def __init__(self, page: Page, url: str = None):
        WebPage.__init__(self, page)  # Явный вызов инициализатора WebPage
        RolesLocators.__init__(self, page)  # Явный вызов инициализатора CanvasPageLocators
        self._page = page
        self.base_url = url if url else 'https://stage.prodboard.example.com/product/BI_60/atomic'
        self.get_page(self.base_url)
