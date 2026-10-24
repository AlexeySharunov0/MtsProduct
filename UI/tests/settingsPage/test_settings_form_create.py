import allure
import pytest

from UI.tests.settingsPage.conftest import forms_page


@pytest.mark.ui
@allure.feature("Настройки")
class TestEditSettings:

    @allure.title('Отображение настройки Поля для администраторов. Внешние')
    @allure.issue('https://jira.mts.ru/browse/PPI-1072',
                  'PPInfo - Настройка формы добавления продукта для администратора')
    def test_field_external_admin(self, forms_page):
        forms_page.check_menu_item_and_togls(forms_page.external_admin)

    @allure.title('Отображение настройки Поля для администраторов. Внутренние')
    @allure.issue('https://jira.mts.ru/browse/PPI-1072',
                  'PPInfo - Настройка формы добавления продукта для администратора')
    def test_field_internal_admin(self, forms_page):
        forms_page.check_menu_item_and_togls(forms_page.internal_admin)

    @allure.title('Отображение настройки Обязательные поля для пользователя. Внешние')
    @allure.issue('https://jira.mts.ru/browse/PPI-2046',
                  'PPInfo - Необязательные поля в пользовательской форме добавления продукта')
    def test_required_field_external_user(self, forms_page):
        forms_page.check_menu_item_and_togls(forms_page.required_external_user)

    @allure.title('Отображение настройки Обязательные поля для пользователя. Внутренние')
    @allure.issue('https://jira.mts.ru/browse/PPI-2046',
                  'PPInfo - Необязательные поля в пользовательской форме добавления продукта')
    def test_required_field_internal_user(self, forms_page):
        forms_page.check_menu_item_and_togls(forms_page.required_internal_user)

    @allure.title('Отображение настройки Необязательные поля для пользователя. Внешние')
    @allure.issue('https://jira.mts.ru/browse/PPI-2046',
                  'PPInfo - Необязательные поля в пользовательской форме добавления продукта')
    def test_optional_field_external_user(self, forms_page):
        forms_page.check_menu_item_and_togls(forms_page.optional_external_user)

    @allure.title('Отображение настройки Необязательные поля для пользователя. Внутренние')
    @allure.issue('https://jira.mts.ru/browse/PPI-2046',
                  'PPInfo - Необязательные поля в пользовательской форме добавления продукта')
    def test_optional_field_internal_user(self, forms_page):
        forms_page.check_menu_item_and_togls(forms_page.optional_internal_user)
