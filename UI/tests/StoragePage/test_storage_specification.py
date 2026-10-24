import allure
import pytest

from UI.tests.StoragePage.conftest import specification_page
from UI.utils.EnvProvider import EnvProvider


@pytest.mark.ui
@allure.feature("Спецификации")
class TestCatalogueSpecificationsPage:

    @allure.title("Проверка урла хранилища спецификаций")
    def test_main_page_specs_opens(self, specification_page):
        current_url = specification_page.url
        target_url = EnvProvider.getBaseUrl() + "/catalogue/specs"
        assert target_url == current_url, 'Урл хранилища спецификаций не совпал с ожидаемым'

    @allure.title("Добавление спецификации")
    def test_add_spec(self, specification_page):
        name = "test_add_specification"

        created_spec = specification_page.create_spec(name)

        specs = specification_page.specs.get_texts()
        with allure.step('Проверяем, что созданная спецификация есть в списке спецификаций'):
            assert any([created_spec in spec_name for spec_name in specs]), 'Созданной спецификации нет в списке'

        specification_page.delete()

    @allure.title("Удаление спецификации")
    def test_delete_spec(self, specification_page):
        specification_page.delete()
        name = "0_0_test_delete_spec"
        created_name = specification_page.create_spec(name=name)
        with allure.step('Заходим в спецификацию'):
            specification_page.first_spec.click()

        specification_page.delete_spec()

        specs = specification_page.specs.get_texts()
        with allure.step('Проверяем, что удаленной спецификации нет в списке'):
            assert all([created_name not in spec_name for spec_name in specs]), 'Удаленная спецификация есть в списке'

    @allure.title("Проверка тоглов в спецификации")
    def test_toggles_on(self, specification_page):
        name = "0_0_test_edit_group_attributes"
        specification_page.create_spec(name=name)
        with allure.step('Кликаем на спецификацию'):
            specification_page.first_spec.click()
        with allure.step('Включаем 10 тоглов в спецификации'):
            [toggle.click() for toggle in specification_page.toggles[:10]]
        with allure.step('Кликаем на "Изменить спецификацию"'):
            specification_page.edit_spec_button.click()
        with allure.step('Кликаем на спецификацию'):
            specification_page.first_spec.click()
        with allure.step('Проверяем, что включенные ранее тоглы активны'):
            assert specification_page.toggles.are_checked(10), 'Включенные ранее тоглы не активны'
        specification_page.delete_spec()
