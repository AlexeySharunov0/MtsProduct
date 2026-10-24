import allure
import pytest

from UI.tests.settingsPage.conftest import external_product_page


@allure.issue('https://jira.mts.ru/browse/PPI-254', 'PPInfo - Разделение настроек страницы продукта')
@pytest.mark.ui
@allure.feature("Настройки")
class TestProductPageSettingsCommercial:

    @allure.title(f"Настройки страницы продукта")
    @allure.story(f"Я, как администратор, хочу управлять страницей продукта")
    def test_group_order_ext(self, external_product_page):
        """ Отображение таба "Порядок групп" в настройках продукта """
        external_product_page.group_order_tab.click()
        assert 'activeItem' in external_product_page.group_order_tab.get_attribute('class')

    @allure.title(f"Настройки страницы продукта")
    @allure.story(f"Я, как администратор, хочу управлять страницей продукта")
    def test_common_group_ext(self, external_product_page):
        """ Отображение таба "Общие" в настройках продукта """
        external_product_page.common_tab.click()
        assert 'activeItem' in external_product_page.common_tab.get_attribute('class')

    @allure.title(f"Настройки страницы продукта")
    @allure.story(f"Я, как администратор, хочу управлять страницей продукта")
    def test_common_match_checked_to_list_ext(self, external_product_page):
        """ Соответствие количества включенных и элементов в списке - Общие"""
        external_product_page.common_tab.click()
        assert external_product_page.is_checked.count() == external_product_page.draggables.count()

    @allure.title(f"Настройки страницы продукта")
    @allure.story(f"Я, как администратор, хочу управлять страницей продукта")
    def test_actions_match_checked_to_list_ext(self, external_product_page):
        """ Соответствие количества включенных и элементов в списке действий внешних """
        external_product_page.actions_tab.click()
        assert external_product_page.is_checked.count() == external_product_page.draggables.count()

    @allure.title(f"Настройки страницы продукта")
    @allure.story(f"Я, как администратор, хочу управлять страницей продукта")
    def test_key_match_checked_to_list_ext(self, external_product_page):
        """ Соответствие количества включенных и элементов в списке Ключевые свойства внешних """
        external_product_page.ext_key_prop_tab.click()
        assert external_product_page.is_checked.count() == external_product_page.draggables.count()

    @allure.title(f"Настройки страницы продукта")
    @allure.story(f"Я, как администратор, хочу управлять страницей продукта")
    def test_links_about_product_checked_to_list_ext(self, external_product_page):
        """ Соответствие количества включенных и элементов в списке Ссылки о продукте внешних """
        external_product_page.ext_links_about_tab.click()
        assert external_product_page.is_checked.count() == external_product_page.draggables.count()

    @allure.title(f"Настройки страницы продукта")
    @allure.story(f"Я, как администратор, хочу управлять страницей продукта")
    def test_links_checked_to_list_ext(self, external_product_page):
        """ Соответствие количества включенных и элементов в списке Ссылки внешних """
        external_product_page.ext_links_tab.click()
        assert external_product_page.is_checked.count() == external_product_page.draggables.count()
