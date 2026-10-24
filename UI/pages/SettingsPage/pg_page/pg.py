import logging
import time

import allure
from playwright.sync_api import Page

from UI.base.WebPage import WebPage
from UI.pages.SettingsPage.pg_page.pg_locators import PGLocators
from paths import ROOT

logger = logging.getLogger(__name__)


class PGPage(WebPage, PGLocators):

    def __init__(self, page: Page, url: str = None):
        WebPage.__init__(self, page)  # Явный вызов инициализатора WebPage
        PGLocators.__init__(self, page)  # Явный вызов инициализатора CanvasPageLocators
        self._page = page
        self.base_url = url if url else 'https://stage.prodboard.example.com/lifecycleadmin/current'
        self.get_page(self.base_url)

    @allure.step('Создаем обычный шаг')
    def create_step(self, is_active: bool = False, name: str = 'test_name', description: str = None):
        with allure.step("Жмем кнопку Добавить шаг"):
            self.add_step_button.click()
        if is_active:
            with allure.step('Делаем шаг активным'):
                self.activity_toggle.click()
        with allure.step("Вводим название шага"):
            self.step_name.fill(name)
        with allure.step('Вводим описание'):
            self.step_description.fill(str(time.time()) if description is None else description)
        with allure.step('Жмем на кнопку Добавить'):
            self.add_button_inside.click()

    @allure.step('Создаем вложенный шаг')
    def create_sub_action(self, is_active: bool = False, name: str = 'test_name', description: str = None):
        with allure.step("Жмем кнопку Добавить шаг"):
            self.add_sub_action_button.click()
        if is_active:
            with allure.step('Делаем шаг активным'):
                self.activity_toggle.click()
        with allure.step("Вводим название шага"):
            self.step_name.fill(name)
        with allure.step('Вводим описание'):
            self.step_description.fill(str(time.time()) if description is None else description)
        with allure.step('Жмем на кнопку Добавить'):
            self.add_button_inside.click()

    @allure.step('Удаляем все тестовые шаги')
    def delete_test_steps(self):
        count = 0
        while 'test_name' in self.steps.get_texts() and count < 5:
            count += 1
            if self.test_step.is_visible():
                self.test_step.click()
                self.edit_step_button.click()
                self.delete_step_button.click()
                self.delete_step_approval.click()

    @allure.step("Удаляем все шаги")
    def delete_all_steps(self):
        while steps := self.steps.get_items():
            if steps[0].is_visible():
                steps[0].click()
                self.edit_step_button.click()
                self.delete_step_button.click()
                self.delete_step_approval.click()

    @allure.step("Удаляем текущий шаг")
    def delete_current_step(self):
        self.edit_step_button.click()
        self.delete_step_button.click()
        self.delete_step_approval.click()

    @allure.step("Добавить имя в шаг")
    def add_name_to_step(self, name: str = 'test_name'):
        self.step_name.fill(name)

    @allure.step("Добавить описание в шаг")
    def add_description_to_step(self, description: str = None):
        self.step_description = description if description else str(time.time())

    @allure.step("Сменить активность шага")
    def change_activity_step(self, make_active: bool = True):
        if make_active:
            if self.activity_toggle.is_not_checked():
                self.activity_toggle.click()
        else:
            if self.activity_toggle.is_checked():
                self.activity_toggle.click()

    @allure.step("Сменить обязательность шага")
    def change_required_step(self, make_required: bool = True):
        if make_required:
            self.step_required_radio_button[1].click()
        else:
            self.step_required_radio_button[0].click()

    @allure.step("Сменить повторяемость шага")
    def change_repeatable_step(self, make_repeatable: bool = True):
        if make_repeatable:
            self.step_repeatable_radio_button[3].click()
        else:
            self.step_repeatable_radio_button[2].click()

    @allure.step("Добавить сотрудников")
    def add_users_to_step(self, pattern: str = 'иванов', amount: int = 1):
        self.step_users.click()
        self.step_users_find_line.fill(pattern)
        self.step_find_button.click()
        for user in self.found_users[:amount]:
            user.click()
        self.step_users.click()

    @allure.step("Добавить последнюю ссылку")
    def add_links_to_step(self, link: list[str] = None):
        if link is None:
            link = ['тестовая ссылка', 'https://portal.example.com/Pages/MainPage.aspx']
        self.add_link_button.click()
        self.link_name_input.fill(link[0])
        self.link_input.fill(link[1])

    @allure.step("Добавить файлы")
    def add_files_to_step(self, amount: int = 1):
        doc_name = '/UI/data/test_file.docx'
        doc_full_name = ROOT + doc_name
        self.scroll_page_down(1000)

        while len(self.chosen_files.get_items()) != amount:
            self.add_file_form.input_file(doc_full_name)

    @allure.step("Убираем выбранные параметры у условия")
    def clear_values(self, index_of_condition: int):
        condition = self.conditions.get_items()[index_of_condition]
        condition.click()
        values = self.conditions_values.get_items()
        for value in values:
            if 'isSelected' in value.get_attribute('class'):
                value.click()

    @allure.step("Изменить условие")
    def change_condition(self, value_list: list[str], index_of_condition: int):
        self.clear_values(index_of_condition)
        values = self.conditions_values.get_items()
        for value in values:
            if value.get_text() in value_list:
                value.click()
