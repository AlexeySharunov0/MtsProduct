import logging

import allure
from playwright.sync_api import Page

from UI.base.WebElement import WebElement
from UI.base.WebPage import WebPage
from UI.pages.SettingsPage.forms_page.forms_locators import FormsLocators

logger = logging.getLogger(__name__)


class FormsPage(WebPage, FormsLocators):
    def __init__(self, page: Page, url: str = None):
        WebPage.__init__(self, page)  # Явный вызов инициализатора WebPage
        FormsLocators.__init__(self, page)  # Явный вызов инициализатора CanvasPageLocators
        self._page = page
        self.base_url = url if url else 'https://stage.prodboard.example.com/prefs/form_create'
        self.get_page(self.base_url)

    @allure.step('Проверяем наличие пункта меню и тоглов в нем')
    def check_menu_item_and_togls(self, menu_item: WebElement) -> None:
        assert menu_item.is_visible(), 'Пункт меню не отображен на странице настроек'
        menu_item.click()
        assert self.columns_attributes.is_visible(), 'В пункте меню нет тоглов атрибутов'
