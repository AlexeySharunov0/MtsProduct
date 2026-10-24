import allure
import pytest

from UI.tests.settingsPage.conftest import main_page


@pytest.mark.ui
@allure.feature("Настройки")
class TestMainPageSettings:

    @allure.title(f"Настройки главной страницы")
    @allure.story(f"Я, как администратор, хочу управлять главной страницей сайта")
    def test_filters(self, main_page):
        """ Отображение фильтров в настройках  """
        main_page.vnutrennii_filters.click()
        assert 'activeItem' in main_page.vnutrennii_filters.get_attribute('class')

    @allure.title(f"Настройки главной страницы")
    @allure.story(f"Я, как администратор, хочу управлять главной страницей сайта")
    def test_ext_excel(self, main_page):
        """ Отображение всех столбцов excel в настройках  """
        main_page.excel_tab.click()
        assert 'activeItem' in main_page.excel_tab.get_attribute('class')

    @allure.title(f"Настройки главной страницы")
    @allure.story(f"Я, как администратор, хочу управлять главной страницей сайта")
    def test_int_excel(self, main_page):
        """ Отображение всех столбцов excel в настройках  """
        main_page.excel_tab_int.click()
        assert 'activeItem' in main_page.excel_tab_int.get_attribute('class')

    @allure.title(f"Настройки главной страницы")
    @allure.story(f"Я, как администратор, хочу управлять главной страницей сайта")
    def test_switches_match_to_drag_items_cards(self, main_page):
        """ Соответствие количества включенных параметров и элементов в списке drag'n'drop в настройках карт продукта"""
        assert main_page.is_checked.count() == main_page.draggables.count()

    @allure.title(f"Настройки главной страницы")
    @allure.story(f"Я, как администратор, хочу управлять главной страницей сайта")
    def test_switches_match_to_drag_items_external_filters(self, main_page):
        """ Соответствие количества включенных параметров и элементов в списке drag'n'drop в настройках фильтров продукта"""
        assert main_page.is_checked.count() == main_page.draggables.count()

    @allure.title(f"Настройки главной страницы")
    @allure.story(f"Я, как администратор, хочу управлять главной страницей сайта")
    def test_switches_match_to_drag_items_external_excel(self, main_page):
        """ Соответствие количества включенных параметров и элементов в списке drag'n'drop в настройках эксель продукта"""
        main_page.excel_tab.click()
        assert main_page.is_checked.count() == main_page.draggables.count()
