import allure
import pytest

from UI.data.assertions_data import ProductsAsserts as assertions
from UI.tests.productPage.conftest import eco_modules_page


@pytest.mark.ui
@allure.feature("Вкладка ЭкоМодули")
@pytest.mark.skip(reason="ЭкоМодули временно отключены")
class TestEcoModules:
    @allure.title("Проверка кликабельности и отображения таба Экосистемные модули у продуктов с экомодулями")
    def test_eco_tab_check(self, eco_modules_page):
        with allure.step("Проверяем, что таб есть в боковом меню"):
            assert eco_modules_page.eco_tab.is_visible(), 'Таба нет в меню'
        with allure.step('Проверяем, что таб Экосистемные модули кликабельный'):
            assert eco_modules_page.eco_tab.is_clickable(), 'Таб некликабельный'
        with allure.step("Проверяем, что таб отмечен как активный (черный)"):
            assert eco_modules_page.eco_tab.get_attribute('class') == 'content', 'Таб окрашен серым'

    @allure.title("Проверка кликабельности и отображения таба Экосистемные модули у продуктов без экомодулей")
    @pytest.mark.parametrize('eco_modules_page', ['https://stage.prodboard.mts.ru/product/BI_89/main'], indirect=True)
    def test_eco_tab_check_empty(self, eco_modules_page):
        with allure.step("Проверяем, что таб есть в боковом меню"):
            assert eco_modules_page.eco_tab.is_visible(), 'Таба нет в меню'
        with allure.step('Проверяем, что таб Экосистемные модули кликабельный'):
            assert eco_modules_page.eco_tab.is_clickable(), 'Таб некликабельный'
        with allure.step("Проверяем, что таб отмечен как неактивный (серый)"):
            assert eco_modules_page.eco_tab.get_attribute('class') == 'content empty', 'Таб окрашен черным'

    @allure.title("Проверка заголовков на странице Экосистемные модули")
    def test_check_eco_headers(self, eco_modules_page):
        with allure.step('Кликаем на таб "Экосистемные модули"'):
            eco_modules_page.eco_tab.click()
        with allure.step("Проверяем, что заголовок страницы отображается корректно"):
            assert eco_modules_page.eco_header.is_visible(), 'Заголовка нет'
            assert 'Экосистемные модули' in eco_modules_page.eco_header.get_text(), 'Текст заголовка не совпадает'
        with allure.step("Проверяем, что описание страницы отображается корректно"):
            assert eco_modules_page.tab_description.is_visible(), 'Описания нет'

    @allure.title("Проверка отображения таблицы Эко модулей")
    def test_check_eco_table(self, eco_modules_page):
        with allure.step("Проверяем, что таблица отображается"):
            assert eco_modules_page.eco_table.is_visible(), 'Таблицы нет'

    @allure.title("Проверка текста при отсутствии экомодулей")
    @pytest.mark.parametrize('eco_modules_page', ['https://stage.prodboard.mts.ru/product/BI_89/eco'], indirect=True)
    def test_check_text_eco_no_eco_modules(self, eco_modules_page):
        with allure.step("Проверяем, что текст при отсутствии экомодулей отображается корректно"):
            assert eco_modules_page.eco_error.is_visible(), 'Заголовка нет'

    @allure.title("Проверка отображения и кликабельности названия экосистемных модулей на странице продукта")
    def test_eco_prod_links(self, eco_modules_page):
        with allure.step("Проверяем элементы таблицы"):
            with allure.step("Проверяем, что у всех элементов есть название"):
                assert all(
                    i for i in eco_modules_page.eco_prod_links.get_texts()), 'У некоторых экомодулей нет названия'
            with allure.step("Проверяем, что все элементы кликабельны"):
                assert all(
                    i.is_clickable() for i in eco_modules_page.eco_prod_links), 'Некоторые элементы некликабельные'

    @allure.title("Проверка перехода на страницу экомодуля со страницы основного")
    def test_move_to_eco_module(self, eco_modules_page):
        with allure.step('Кликаем по первому элементу таблицы'):
            eco_modules_page.eco_prod_links.get_items()[0].click()
        with allure.step('Проверяем, что перешли на страницу нужного продукта'):
            assert eco_modules_page.url == 'https://stage.prodboard.mts.ru/product/BI_200/main', 'Ссылка не та'
        with allure.step("Проверяем, что табы изменились"):
            assert eco_modules_page.eco_tab.get_text() == 'Продукты с ЭПМ', 'Таб Экосистемные продукты не пропал'

    @allure.title("Проверка кликабельности ячеек интеграции на странице Экосистемных модулей")
    def test_integration_cells(self, eco_modules_page):
        with allure.step("Проверяем, что все элементы кликабельны"):
            assert all(i.is_clickable() for i in eco_modules_page.eco_cells), 'Некоторые элементы некликабельные'

    @allure.title("Проверка кликабельности и отображения таба продукты с ЭПМ")
    @pytest.mark.parametrize('eco_modules_page', ['https://stage.prodboard.mts.ru/product/BI_200/main'], indirect=True)
    def test_epm_tab_check(self, eco_modules_page):
        with allure.step('Проверяем, что таб Продукты с ЭПМ кликабельный'):
            assert eco_modules_page.eco_tab.is_clickable(), 'Таб некликабельный'
        with allure.step("Проверяем, что продукты таб не называется Экосистемные модули"):
            assert eco_modules_page.eco_tab.get_text() == 'Продукты с ЭПМ', 'Таб Экосистемные модули не пропал'
        with allure.step("Проверяем, что таб отмечен как активный (черный)"):
            assert eco_modules_page.eco_tab.get_attribute('class') == 'content', 'Таб окрашен серым'

    @allure.title("Проверка заголовков на странице Продукты с ЭПМ")
    @pytest.mark.parametrize('eco_modules_page', ['https://stage.prodboard.mts.ru/product/BI_200/eco'], indirect=True)
    def test_check_epm_headers(self, eco_modules_page):
        with allure.step("Проверяем, что заголовок страницы отображается корректно"):
            assert eco_modules_page.epm_header.is_visible(), 'Заголовка нет'
        with allure.step("Проверяем, что описание страницы отображается корректно"):
            assert eco_modules_page.epm_description.is_visible(), 'Описания нет'
            assert eco_modules_page.epm_description.get_text() == assertions.epm_description, 'Текст описания не совпадает'

    @allure.title("Проверка перехода на страницу основного продукта со страницы экомодуля")
    @pytest.mark.parametrize('eco_modules_page', ['https://stage.prodboard.mts.ru/product/BI_200/eco'], indirect=True)
    def test_move_to_main_from_eco(self, eco_modules_page):
        with allure.step('Кликаем по первому элементу таблицы'):
            eco_modules_page.eco_prod_links.get_items()[0].click()
        with allure.step('Проверяем, что перешли на страницу нужного продукта'):
            assert eco_modules_page.url == 'https://stage.prodboard.mts.ru/product/BI_22/main', 'Ссылка не та'
        with allure.step("Проверяем, что табы изменились"):
            assert eco_modules_page.eco_tab.get_text() == 'Экосистемные модули', 'Таб Продукты с ЭПМ не пропал'

    @allure.title(
        "Нажатие на название возвращает к основной информации о текущем продукте (с таба экосистемных модулей)")
    def test_name_returns_to_main_info_from_eco(self, product_page, eco_modules_page):
        with allure.step("Кликаем на название продукта"):
            product_page.product_name.click()
        with allure.step("Проверяем, что мы вернулись на главную страницу продукта"):
            assert eco_modules_page.eco_header.is_not_visible(), 'Заголовок с Экосистемные модули остался'

    @allure.title("Нажатие на лого возвращает к основной информации о текущем продукте (с таба экосистемных модулей)")
    def test_logo_returns_to_main_info_from_eco(self, product_page, eco_modules_page):
        with allure.step("Кликаем на лого продукта"):
            product_page.product_logo.click()
        with allure.step("Проверяем, что мы вернулись на главную страницу продукта"):
            assert eco_modules_page.eco_header.is_not_visible(), 'Заголовок с Экосистемные модули остался'
