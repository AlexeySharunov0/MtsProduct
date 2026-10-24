import allure
import pytest

from UI.tests.settingsPage.conftest import curators_page


@pytest.mark.ui
@allure.feature('Кураторы')
class TestCuratorPage:
    @allure.title('Кураторы / Проверка основных элементов / Заголовок')
    def test_curator_header(self, curators_page):
        with allure.step('Проверяем отображение хедера'):
            assert curators_page.header.is_visible(), 'Хедера нет'
            assert curators_page.header.get_text() == 'Кураторы по кластерам', 'Текст хедера не совпадает'

    @allure.title('Кураторы / Проверка основных элементов / Таблица кураторов и кластеров')
    def test_curator_table(self, curators_page):
        with allure.step('Проверяем отображение таблицы'):
            assert curators_page.table.is_visible(), 'Таблицы нет'
        with allure.step('Проверяем колонку кластеров'):
            assert curators_page.clusters.get_items(), 'Кластеров нет'
        with allure.step('Проверяем что кураторы отображаются'):
            assert curators_page.curators_list.is_visible(), 'Кураторов нет'
        with allure.step('Проверяем колонку сотрудников'):
            assert all(i.is_clickable() for i in curators_page.curators), 'На кураторов нельзя нажать'

    @allure.title('Кураторы / Проверка основных элементов / Кнопки управления')
    def test_curator_buttons(self, curators_page):
        with allure.step('Проверяем кнопку "Редактировать"'):
            assert curators_page.edit_button.is_visible(), 'Кнопки нет'
            assert curators_page.edit_button.is_clickable(), 'На кнопку нельзя нажать'
        with allure.step('Жмем кнопку "Редактировать"'):
            curators_page.edit_button.click()
        with allure.step('Проверяем, что появились кнопки "Принять" и "Отмена"'):
            assert curators_page.accept_button.is_visible(), 'Кнопки Принять нет'
            assert curators_page.undo_button.is_visible(), 'Кнопки Отмена нет'
            assert curators_page.undo_button.is_clickable(), 'На кнопку Отмена нельзя нажать'
        with allure.step("Жмем на кнопку Отмена"):
            curators_page.undo_button.click()
        with allure.step('Проверяем, что кнопки пропали'):
            assert curators_page.undo_button.is_not_visible(), 'Кнопки не пропали'

    @allure.title('Кураторы / Проверка основных элементов / Надпись при одном элементе')
    @pytest.mark.skip('Вроде как сказал что кураторы не могут быть единичными атрибутами, только множественными')
    def test_curator_single_record(self, curators_page):
        curators_page.find_curator()
        with allure.step('Проверяем, что есть надпись о том, что можно добавить только 1 сотрудника'):
            assert curators_page.single_info.is_visible(), 'Надписи нет'

        curators_page.find_curator(is_single=False)
        with allure.step('Проверяем, что нет надписи о том, что можно добавить только 1 сотрудника'):
            assert curators_page.single_info.is_not_visible(), 'Надпись есть '

    @allure.title('Кураторы / Юзер / Добавление куратора')
    def test_curator_add(self, curators_page):
        curators_page.find_curator()
        curators_page.delete_curators_in_one()
        with allure.step('Добавляем 1 сотрудника в первый кластер'):
            curators_page.add_curator_to_table()
        with allure.step('Проверяем, что куратор добавился'):
            assert len(curators_page.curators.get_items()) == 1, 'Добавилось больше кураторов, чем нужно'
            assert 'иванов' in curators_page.curators[0].get_text().lower(), 'Добавился не тот сотрудник'

    @allure.title('Кураторы / Мультиюзер / Добавление кураторов')
    def test_curator_add_multi(self, curators_page):
        curators_page.find_curator(is_single=False)
        curators_page.delete_curators()
        with allure.step('Добавляем 1 сотрудника в первый кластер'):
            curators_page.add_curator_to_table()
        with allure.step('Проверяем, что куратор добавился'):
            assert len(curators_page.curators.get_items()) == 1, 'Добавилось больше кураторов, чем нужно'
            assert 'иванов' in curators_page.curators[0].get_text().lower(), 'Добавился не тот сотрудник'

        with allure.step('Добавляем 2 сотрудника во второй кластер'):
            curators_page.add_curator_to_table(line_number=2, amount_to_choose=2)
        with allure.step('Проверяем, что куратор добавился'):
            assert len(curators_page.curators.get_items()) == 3, 'Добавилось больше кураторов, чем нужно'
            assert all('иванов' in i.get_text().lower() for i in curators_page.curators), 'Добавился не тот сотрудник'
