import logging

import allure
from playwright.sync_api import Page

from UI.base.WebPage import WebPage
from UI.pages.main_page.main_page.main_page_locators import MainPageLocators

logger = logging.getLogger(__name__)


class MainPage(WebPage, MainPageLocators):
    def __init__(self, page: Page, url: str = None):
        WebPage.__init__(self, page)  # Явный вызов инициализатора WebPage
        MainPageLocators.__init__(self, page)  # Явный вызов инициализатора CanvasPageLocators
        self._page = page
        self.base_url = url if url else 'https://stage.prodboard.example.com'
        self.get_page(self.base_url)

    def execute_search_main(self, word: str):
        """ Выполняет поиск переданной строки в строке поиска и закрывает её """

        with allure.step('Кликаем на строку поиска'):
            self.search_str_closed.click()
        with allure.step(f'Вводим слово по которому нужно осуществить поиск - {word}'):
            self.search_str.fill(word)
        with allure.step('Нажимаем ENTER'):
            self.search_str.press_key("Enter")
