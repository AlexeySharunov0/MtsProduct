import logging

from playwright.sync_api import Page

from UI.base.WebPage import WebPage
from UI.pages.SettingsPage.edit_page.edit_locators import EditLocators

logger = logging.getLogger(__name__)


class EditPage(WebPage, EditLocators):
    def __init__(self, page: Page, url: str = None):
        WebPage.__init__(self, page)  # Явный вызов инициализатора WebPage
        EditLocators.__init__(self, page)  # Явный вызов инициализатора CanvasPageLocators
        self._page = page
        self.base_url = url if url else 'https://stage.prodboard.example.com/prefs/edit_settings'
        self.get_page(self.base_url)
