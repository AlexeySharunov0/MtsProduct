import allure
import pytest

from API.utils.generate import Gen
from UI.data.assertions_data import CatalogueAssertions
from UI.tests.StoragePage.conftest import attributes_page
from UI.utils.EnvProvider import EnvProvider


@pytest.mark.ui
@allure.feature("Атрибуты")
@pytest.mark.usefixtures("clear_db_attribute")
class TestCatalogueAttributePage:

    @allure.title("Проверка урла хранилища атрибутов")
    def test_main_page_opens(self, attributes_page):
        with allure.step('Получаем фактический урл с текущей страницы'):
            current_url = attributes_page.url
        with allure.step('Подготавливаем ожидаемый урл'):
            target_url = EnvProvider.getBaseUrl() + "/catalogue/attributes"
        with allure.step('Сравниваем ожидаемый урл с фактическим'):
            assert target_url == current_url, 'Урл на странице хранилища не корректный'

    @allure.title("Проверка урла хранилища атрибутов при входе в атрибут и нажатии отмена")
    def test_attr_edit_page_opens(self, attributes_page):
        with allure.step('Кликаем на первый атрибут в списке хранилища'):
            attributes_page.first_search_result.click()
        with allure.step('Нажимаем кнопку "отмена"'):
            attributes_page.cancel_attr_button.click()
        with allure.step('Получаем фактический урл с текущей страницы'):
            current_url = attributes_page.url
        with allure.step('Подготавливаем ожидаемый урл'):
            target_url = EnvProvider.getBaseUrl() + "/catalogue/attributes"
        with allure.step('Сравниваем ожидаемый урл с фактическим'):
            assert target_url == current_url, 'Урл на странице хранилища не корректный'

    @allure.title("Добавление атрибутов всех типов")
    @pytest.mark.parametrize("type_attr", [0, 1, 2, 3, 4, 5, 6, 7])
    def test_add_attribute(self, attributes_page, type_attr):
        attributes_page.create_attribute(type_attr)

    @allure.title("Удаление атрибутов всех типов")
    @pytest.mark.parametrize("type_attr", [0, 1, 2, 3, 4, 5, 6, 7, 8])
    def test_delete_attribute(self, attributes_page, type_attr):
        attributes_page.create_attribute(type_attr, name="attr_to_delete")

        attributes_page.search("attr_to_delete")
        attributes_page.first_search_result.click()
        with allure.step('Нажимаем на "Удалить"'):
            attributes_page.delete_attr_button[0].click()
        with allure.step('Подтверждаем удаление атрибута'):
            attributes_page.broken_delete.click()
        with allure.step('Проверяем, что появился аллерт "Атрибут успешно удален"'):
            assert attributes_page.allert_delete.is_visible(), 'Аллерт не появился'

    @allure.title("Редактирование атрибутов всех типов")
    @pytest.mark.parametrize("type_attr", [0, 1, 2, 3, 4, 5, 6, 7])
    def test_edit_attribute(self, attributes_page, type_attr):
        attributes_page.create_attribute(type_attr, name="attr")
        attributes_page.search("attr")
        attributes_page.first_search_result.click()
        attributes_page.edit_name("new test" + Gen.generate_text(5))
        with allure.step('Выполняем поиск атрибута с новым именем'):
            attributes_page.search("new test")
            result = attributes_page.first_search_result.get_text().strip(' ')
            assert "new" in result

        attributes_page.first_search_result.click()

        attributes_page.delete_attr_button[0].click()
        attributes_page.broken_delete.click()

    @allure.title("Проверка поиска по атрибутам ")
    @pytest.mark.parametrize("searchable", CatalogueAssertions.important_attributes_list)
    def test_attributes_search(self, attributes_page, searchable):
        attributes_page.search(searchable)
        result = attributes_page.first_search_result.get_text().strip(' ')
        assert result == searchable, 'Результат поиска не совпал с запросом'

    @allure.title("Кнопка Добавить в атрибуте активна")
    def test_add_button_in_attr(self, attributes_page):
        with allure.step('Заходим на страницу атрибута'):
            attributes_page.get_page(
                'https://stage.prodboard.mts.ru/catalogue/attributes/19697703-36ce-48d2-bc16-98633691fccb')
        with allure.step('Кнопка добавить присутствует на странице и кликабельна'):
            assert attributes_page.add_choosable.is_clickable(), "Кнопка добавить не кликабельна"
