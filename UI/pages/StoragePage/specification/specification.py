import logging

import allure
from playwright.sync_api import Page

from API.utils.generate import Gen
from UI.base.WebPage import WebPage
from UI.pages.StoragePage.specification.specification_locators import SpecificationLocators

logger = logging.getLogger(__name__)


class SpecificationPage(WebPage, SpecificationLocators):
    def __init__(self, page: Page, url: str = None):
        WebPage.__init__(self, page)  # Явный вызов инициализатора WebPage
        SpecificationLocators.__init__(self, page)  # Явный вызов инициализатора CanvasPageLocators
        self._page = page
        self.base_url = url if url else 'https://stage.prodboard.example.com/catalogue/specs'
        self.get_page(self.base_url)

    def create_spec(self, name):
        with allure.step('Нажимаем "Добавить спецификацию..."'):
            self.add_spec_button.click()

        text = Gen.generate_title_with_datetime(name)
        with allure.step('Вводим название спецификации'):
            self.input_name.fill(text)
        with allure.step('Нажимаем "Добавить спецификацию"'):
            self.create_button.click()

        return text

    def delete_spec(self):
        with allure.step('Нажимаем "Удалить"'):
            self.delete_spec_button.click()
        with allure.step('Подтверждаем удаление'):
            self.delete_spec_button_second.click()

    def delete(self):
        if 'test' in self.first_spec.get_text():
            self.first_spec.click()
            self.delete_spec()
            self.delete()
