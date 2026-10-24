import logging

import allure
from playwright.sync_api import Page

from API.utils.generate import Gen
from UI.base.WebPage import WebPage
from UI.pages.StoragePage.attributes.attributes_locators import AttributesLocators

logger = logging.getLogger(__name__)


class AttributesPage(WebPage, AttributesLocators):
    def __init__(self, page: Page, url: str = None):
        WebPage.__init__(self, page)  # Явный вызов инициализатора WebPage
        AttributesLocators.__init__(self, page)  # Явный вызов инициализатора CanvasPageLocators
        self._page = page
        self.base_url = url if url else 'https://stage.prodboard.example.com/catalogue/attributes'
        self.get_page(self.base_url)

    def create_attribute(self, type_attr, name="test_add_attribute"):
        self.wait_force(2)
        with allure.step('Нажимаем кнопку "Добавить атрибут"'):
            self.add_attribute_button.click(force=True)

        fullname = Gen.generate_title_with_datetime(name)
        self.wait()
        with allure.step('Вводим название и описание атрибута'):
            self.input_name.fill(fullname)
            self.input_description.fill("description")
        with allure.step('Выбираем тип атрибута'):
            self.type_selector.click()

            self.type_items_selector[type_attr].click()

        if type_attr == 7:
            with allure.step('Задаем первый вариант для набора значений'):
                self.add_choosable.click()
                self.input_choosable_fields[0].fill("first")
            with allure.step('Проверяем, что кнопка "Добавить атрибут" не кликабельна'):
                assert not self.create_button.is_clickable()
            with allure.step('Задаем первый вариант для набора значений'):
                self.add_choosable.click()
                assert not self.create_button.is_clickable()

                self.input_choosable_fields[1].fill("second")
            with allure.step('Проверяем, что кнопка "Добавить атрибут" кликабельна'):
                assert self.create_button.is_clickable()
        with allure.step('Нажимаем на "Добавить атрибут"'):
            self.create_button.click()

        return fullname

    def search(self, searchable):
        with allure.step('Выполняем поиск атрибута'):
            self.wait_force(2)
            self.search_str.click(force=True)
            self.search_str.fill(searchable)

    def edit_name(self, name):
        with allure.step('Редактируем имя атрибута и сохраняем его'):
            self.input_name.fill(name)
            self.create_button.click()
