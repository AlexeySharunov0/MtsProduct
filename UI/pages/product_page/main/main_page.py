import logging

import allure
from playwright.sync_api import Page

from UI.base.WebPage import WebPage
from UI.pages.product_page.main.main_page_locators import MainPageLocators

logger = logging.getLogger(__name__)


class MainPage(WebPage, MainPageLocators):
    def __init__(self, page: Page, url: str = None):
        WebPage.__init__(self, page)
        MainPageLocators.__init__(self, page)
        self._page = page
        self.base_url = url if url else 'https://stage.prodboard.example.com/product/BI_60/main'
        self.get_page(self.base_url)

    @allure.step("Опубликовать продукт, если он удален")
    def publish_product(self):
        if self.get_back_from_dead_button.is_visible():
            self.get_back_from_dead_button.click()

    @allure.step("Удаляем продукт")
    def delete_product(self):
        with allure.step("Вводим текст в инпут удаления"):
            self.reason_deleted_input.fill('тест123')
        with allure.step("Жмем на кнопку Удалить"):
            self.delete_in_modal_button.click()
