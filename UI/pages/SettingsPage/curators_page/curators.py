import logging

import allure
from playwright.sync_api import Page

from UI.base.WebPage import WebPage
from UI.pages.SettingsPage.curators_page.curators_locators import CuratorLocators

logger = logging.getLogger(__name__)


class CuratorPage(WebPage, CuratorLocators):

    def __init__(self, page: Page, url: str = None):
        WebPage.__init__(self, page)  # Явный вызов инициализатора WebPage
        CuratorLocators.__init__(self, page)  # Явный вызов инициализатора CanvasPageLocators
        self._page = page
        self.base_url = url if url else 'https://stage.prodboard.example.com/curators'
        self.get_page(self.base_url)

    @allure.step('Переходим к тестовому атрибуту в кураторах')
    def find_curator(self, is_single: bool = True):

        with allure.step('Выбираем нужного куратора'):
            self.curators_test_one.click() if is_single else self.curators_test_many.click()

    @allure.step('Удаляем всех кураторов')
    def delete_curators(self):
        if self.curators.get_items():
            with allure.step('Нажимаем кнопку Редактировать'):
                self.edit_button.click()
            with allure.step('Удаляем всех кураторов'):
                while len(self.curator_delete_button.get_items()) != 0:
                    self.curator_delete_button[0].click()
            with allure.step('Нажимаем кнопку Принять'):
                self.accept_button.click()

    @allure.step('Удаляем всех кураторов')
    def delete_curators_in_one(self):
        if self.curators.get_items():
            with allure.step('Нажимаем кнопку Редактировать'):
                self.edit_button.click()
            with allure.step('Удаляем всех кураторов'):
                self.curator_only_delete_button.click_all()
            with allure.step('Нажимаем кнопку Принять'):
                self.accept_button.click()

    @allure.step('Добавляем куратора в таблицу')
    def add_curator_to_table(self, line_number: int = 0, pattern: str = 'иванов', amount_to_choose: int = 1):
        with allure.step('Нажимаем кнопку Редактировать'):
            self.edit_button.click()
        with allure.step('Жмем на форму добавления куратора'):
            self.table_curator_choose[line_number].click()
        with allure.step(f'Ищем в строке поиска {pattern}'):
            self.search.fill(pattern)
            self.search.press_key('Enter')
        with allure.step(f'Выбираем {amount_to_choose} элементов'):
            for i in self.users_variants[:amount_to_choose]:
                i.click()
        with allure.step('Нажимаем кнопку Применить'):
            self.accept_button.click()
