import logging
import time

import allure
from playwright.sync_api import Page

from UI.base.WebPage import WebPage
from UI.pages.main_page.news_page.news_locators import NewsPageLocators

logger = logging.getLogger(__name__)


class NewsPage(WebPage, NewsPageLocators):

    def __init__(self, page: Page, url: str = None):
        WebPage.__init__(self, page)  # Явный вызов инициализатора WebPage
        NewsPageLocators.__init__(self, page)  # Явный вызов инициализатора CanvasPageLocators
        self._page = page
        self.base_url = url if url else 'https://stage.prodboard.example.com/news/current'
        self.get_page(self.base_url)

    @allure.step("Удаляем тестовые новости")
    def check_work_news(self):

        while self.first_link.is_visible():
            self.first_link.click()
            self.first_delete.click()
            self.second_delete.click()
            time.sleep(0.5)

        while self.first_link.is_visible():
            self.first_link_edit.click()
            self.first_delete.click()
            self.second_delete.click()
            time.sleep(0.5)

    @allure.step("Добавляем новость")
    def add_news(self):
        with allure.step('Нажать кнопку "Добавить новость..."'):
            self.add_news_button.click()
        with allure.step('Написать валидный Заголовок'):
            self.header_input.fill('Заголовок На удаление')
        with allure.step('Написать валидный Текст новости'):
            self.description_input.fill('тест123')
        with allure.step("Проверяем, что изменения применились в блоке справа"):
            assert self.news_header_another.get_text() == 'Заголовок На удаление', f'Название новости справа: {self.news_header.get_text()}, ожидаемый: Заголовок На удаление'
            assert self.news_text.get_text() == 'тест123', f'Текст новости справа: {self.news_text.get_text()}, ожидаемый: тест123'

        with allure.step('Добавить валидную ссылку'):
            self.add_link_in_news.click()
        with allure.step('Нажать кнопку "Добавить новость"'):
            self.add_news_on_addpage.click()
        with allure.step('Проверить, что новость добавлена с нужным заголовком'):
            assert self.first_link.is_visible(), 'Созданная новость не отображена'

    @allure.step("Добавляем новость с невалидным названием")
    def add_news_invalid_name(self, header: str):
        with allure.step('Нажать кнопку "Добавить новость..."'):
            self.add_news_button.click()
        with allure.step('Написать невалидный заголовок'):
            self.header_input.fill(header)
        assert self.add_news_on_addpage.is_disabled(), 'Кнопка Добавить новость кликабельная'

    @allure.step("Добавляем новость с невалидным текстом")
    def add_news_invalid_description(self, header: str):
        with allure.step('Нажать кнопку "Добавить новость..."'):
            self.add_news_button.click()
        with allure.step('Написать невалидный заголовок'):
            self.description_input.fill(header)

        assert self.add_news_on_addpage.is_disabled(), 'Кнопка Добавить новость кликабельная'

    @allure.step("Удаляем новость")
    def delete_news(self):
        with allure.step('Кликаем на созданную новость'):
            self.first_link.click()
        with allure.step('Нажимаем кнопку Удалить'):
            self.first_delete.click()
        with allure.step('Подтверждаем удаление'):
            self.second_delete.click()
        with allure.step('Проверяем что новость удалена'):
            assert self.first_link.is_not_visible(), 'Удаленная новость отображена'

    @allure.step("Удаляем новость после редактирования")
    def delete_news_after_edit(self):
        with allure.step('Кликаем на созданную новость'):
            self.first_link_edit.click()
        with allure.step('Нажимаем кнопку Удалить'):
            self.first_delete.click()
        with allure.step('Подтверждаем удаление'):
            self.second_delete.click()
        with allure.step('Проверяем что новость удалена'):
            assert self.first_link.is_not_visible(), 'Удаленная новость отображена'

    @allure.step("Редактируем новость")
    def edit_news(self):
        with allure.step('Кликаем на созданную новость'):
            self.first_link.click()
            time.sleep(1)
        with allure.step('Изменить заголовок новости'):
            self.header_input.fill(' х2', clear=False)
        with allure.step('Изменить текст новости'):
            self.description_input.fill(' х2', clear=False)
        with allure.step("Проверяем, что изменения применились в блоке справа"):
            assert self.news_header_another.get_text() == 'Заголовок На удаление х2', f'Название новости справа: {self.news_header.get_text()}, ожидаемый: Заголовок На удаление х2'
            assert self.news_text.get_text() == 'тест123 привязать заголовок х2', f'Текст новости справа: {self.news_text.get_text()}, ожидаемый: тест123 х2'

        with allure.step('Добавить валидную ссылку'):
            self.add_link_in_news.click()
        with allure.step('Нажать на кнопку Изменить новость'):
            self.edit_news_button.click()
        with allure.step('Проверить, что новость отредактирована с нужным заголовком'):
            assert self.first_link_edit.is_visible(), 'Отредактированная новость не отображена'

    @allure.step("Меняем активность новости на странице новости")
    def change_news_activity_on_page(self):
        with allure.step('Кликаем на созданную новость'):
            self.first_link.click()
            time.sleep(1)
        with allure.step('Нажать на тогл активности'):
            self.change_active_on_news_page.click()
        with allure.step('Нажать на кнопку Изменить новость'):
            self.edit_news_button.click()
        with allure.step('Кликаем на созданную новость'):
            self.first_link.click()
            time.sleep(1)

    @allure.step("Поиск на странице новостей")
    def search_on_news_page(self, query: str):
        with allure.step("Ищем по названию"):
            self.search_line_news.fill(query)
