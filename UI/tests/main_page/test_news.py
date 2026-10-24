import allure
import pytest

from UI.data.assertions_data import NewsAssertions
from UI.tests.main_page.conftest import news_page


@pytest.mark.ui
@allure.feature("Новости")
@pytest.mark.last
class TestNewsUI:

    @allure.title('Корректное создание и удаление новости')
    def test_create_correct_news_ui(self, news_page):
        news_page.check_work_news()
        news_page.add_news()
        news_page.delete_news()

    @allure.title("Проверяем, что кнопка «Добавить новость» гаснет при некорректном названии")
    @pytest.mark.parametrize("name", NewsAssertions.invalid_names)
    def test_check_add_news_invalid_name_button(self, name, news_page):
        news_page.add_news_invalid_name(name)

    @allure.title("Проверяем, что кнопка «Добавить новость» гаснет при некорректном описании")
    @pytest.mark.parametrize("description", NewsAssertions.invalid_descriptions)
    def test_check_add_news_invalid_description_button(self, description, news_page):
        news_page.add_news_invalid_description(description)

    @allure.title('Корректное редактирование заголовка и текста новости')
    def test_edit_correct_news_tittle_and_text(self, news_page):
        news_page.check_work_news()
        news_page.add_news()
        news_page.edit_news()
        news_page.delete_news_after_edit()

    @allure.title("Проверяем смену активности новости через тогл на странице новости")
    def test_change_news_activity_on_page(self, news_page):
        news_page.check_work_news()
        news_page.add_news()
        news_page.change_news_activity_on_page()
        with allure.step("Проверяем, что активность изменилась"):
            news_page.change_active_on_news_page.is_checked()
        news_page.delete_news()

    @allure.title("Проверяем работу поиска на странице новостей")
    def test_search_on_news_page(self, news_page):
        news_page.check_work_news()
        news_page.add_news()
        news_page.search_on_news_page('Заголовок')
        with allure.step("Проверяем, что нужная новость найдена"):
            assert news_page.first_link.is_visible(), 'Нужная новость не найдена'
        news_page.delete_news()

    @allure.title("Проверяем работу крестика в строке поиска")
    def test_search_on_news_page_cancel(self, news_page):
        news_page.check_work_news()
        news_page.add_news()
        news_page.search_on_news_page('белиберда')
        with allure.step("Жмем на крестик"):
            news_page.search_line_cross.click()
        with allure.step("Проверяем, что новости вернулись"):
            assert news_page.first_link.is_visible(), 'Нужная новость не найдена'
        news_page.delete_news()

    @allure.title("Проверяем текстовку, когда поиск ничего не нашел")
    def test_search_on_news_page_empty_result(self, news_page):
        news_page.search_on_news_page('белиберда')
        with allure.step("Проверяем, что текстовка появилась"):
            assert news_page.no_result_message.is_visible(), 'Текстовки нет'

    @allure.title('Новости отображаются только на главной странице')
    def test_show_news_only_on_main(self, news_page):
        news_page.get_page('https://stage.prodboard.mts.ru/')
        with allure.step('Проверить, что блок новостей отображается корректно'):
            assert news_page.news_block.is_visible(), 'Блок новостей не отображается'
        with allure.step('Перейти на таб внутренних и проверить что новости не отображаются'):
            news_page.get_page('https://stage.prodboard.mts.ru/preset2/products/all')
            assert news_page.news_block.is_not_visible(), 'Блок новостей отображается'


    @allure.title("Проверка работы стрелочек при клике вправо в блоке новостей на главной")
    def test_check_arrows_on_main_page_right(self, news_page):
        news_page.get_page('https://stage.prodboard.mts.ru/')
        current_header = news_page.news_header.get_text()
        current_text = news_page.news_text.get_text()
        current_counter = news_page.news_counter.get_text()
        with allure.step("Кликаем 1 раз вправо"):
            news_page.right_arrow.click()
        with allure.step("Проверяем, что каунтер увеличился на 1"):
            assert news_page.news_counter.get_text() == '2' + current_counter[
                                                              1:], f'Каунтер в новости после клика {news_page.news_counter.get_text()}'
        with allure.step("Проверяем, что новость изменилась"):
            assert news_page.news_header.get_text() != current_header, f'Заголовок новости не изменился'
            assert news_page.news_text.get_text() != current_text, f'Текст новости не изменился'

    @allure.title("Проверка работы стрелочек при клике влево в блоке новостей на главной")
    def test_check_arrows_on_main_page_left(self, news_page):
        news_page.get_page('https://stage.prodboard.mts.ru/')
        current_header = news_page.news_header.get_text()
        current_text = news_page.news_text.get_text()
        current_counter = news_page.news_counter.get_text()
        with allure.step("Кликаем 2 раза влево"):
            news_page.left_arrow.click()
        with allure.step("Проверяем, что каунтер стал максимальным"):
            max_number = str(current_counter[current_counter.find('/') + 2:])
            assert news_page.news_counter.get_text() == max_number + ' / ' + max_number, f'Каунтер в новости после клика {news_page.news_counter.get_text()}'
        with allure.step("Проверяем, что новость изменилась"):
            assert news_page.news_header.get_text() != current_header, f'Заголовок новости не изменился'
            assert news_page.news_text.get_text() != current_text, f'Текст новости не изменился'
