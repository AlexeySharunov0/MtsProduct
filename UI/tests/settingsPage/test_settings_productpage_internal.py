import allure
import pytest

from UI.tests.settingsPage.conftest import internal_product_page


@pytest.mark.ui
@allure.feature("Настройки")
class TestProductPageSettingsInternal:

    @allure.title(f"Настройки страницы продукта")
    @allure.story(f"Я, как администратор, хочу управлять страницей продукта")
    def test_group_order_int(self, internal_product_page):
        """ Отображение таба "Порядок групп" в настройках продукта """

        internal_product_page.group_order_tab.click()
        assert 'activeItem' in internal_product_page.group_order_tab.get_attribute('class')

    @allure.title(f"Настройки страницы продукта")
    @allure.story(f"Я, как администратор, хочу управлять страницей продукта")
    def test_common_group_int(self, internal_product_page):
        """ Отображение таба "Общие" в настройках продукта """

        internal_product_page.common_tab.click()
        assert 'activeItem' in internal_product_page.common_tab.get_attribute('class')

    @allure.title(f"Настройки страницы продукта")
    @allure.story(f"Я, как администратор, хочу управлять страницей продукта")
    def test_common_match_checked_to_list_int(self, internal_product_page):
        """ Соответствие количества включенных и элементов в списке - Общие"""

        internal_product_page.common_tab.click()
        assert internal_product_page.is_checked.count() == internal_product_page.draggables.count()

    @allure.title(f"Настройки страницы продукта")
    @allure.story(f"Я, как администратор, хочу управлять страницей продукта")
    def test_actions_match_checked_to_list_int(self, internal_product_page):
        """ Соответствие количества включенных и элементов в списке действий внешних """

        internal_product_page.int_actions_tab.click()
        assert internal_product_page.is_checked.count() == internal_product_page.draggables.count()

    @allure.title(f"Настройки страницы продукта")
    @allure.story(f"Я, как администратор, хочу управлять страницей продукта")
    def test_key_prop_checked_to_list_int(self, internal_product_page):
        """ Соответствие количества включенных и элементов в списке "Ключевые свойства" внутренних """

        internal_product_page.int_key_prop_tab.click()
        assert internal_product_page.is_checked.count() == internal_product_page.draggables.count()

    @allure.title(f"Настройки страницы продукта")
    @allure.story(f"Я, как администратор, хочу управлять страницей продукта")
    def test_links_about_tab_checked_to_list_int(self, internal_product_page):
        """ Соответствие количества включенных и элементов в списке "Ссылки о продукте" внутренних """

        internal_product_page.int_links_about_tab.click()
        assert internal_product_page.is_checked.count() == internal_product_page.draggables.count()

    @allure.title(f"Настройки страницы продукта")
    @allure.story(f"Я, как администратор, хочу управлять страницей продукта")
    def test_links_tab_checked_to_list_int(self, internal_product_page):
        """ Соответствие количества включенных и элементов в списке "Ссылки" внутренних """

        internal_product_page.int_links_tab.click()
        assert internal_product_page.is_checked.count() == internal_product_page.draggables.count()

    @allure.title(f"Настройки страницы продукта")
    @allure.story(f"Я, как администратор, хочу управлять страницей продукта")
    def test_users_checked_to_list_int(self, internal_product_page):
        """ Соответствие количества включенных и элементов в списке Руководство внутренних """

        internal_product_page.int_owners_tab.click()
        assert internal_product_page.is_checked.count() == internal_product_page.draggables.count()
