import allure
import pytest

from UI.data.assertions_data import ProductsAsserts as assertions
from UI.tests.productPage.conftest import metrics_page


@pytest.mark.ui
@allure.feature("Вкладка Метрики")
class TestMetrics:
    @allure.title("Проверка кликабельности и отображения таба Метрики")
    def test_metrics_check_tab(self, metrics_page):
        with allure.step("Проверяем, что таб есть в боковом меню"):
            assert metrics_page.metrics_tab.is_visible(), 'Таба нет в меню'
        with allure.step('Проверяем, что таб кликабельный'):
            assert metrics_page.metrics_tab.is_clickable(), 'Таб некликабельный'
        with allure.step("Проверяем, что таб отмечен как активный (черный)"):
            assert metrics_page.metrics_tab.get_attribute('class') == 'content', 'Таб окрашен серым'

    @allure.title("Проверка корректности заголовков на странице Метрики")
    @allure.issue('https://jira.mts.ru/browse/PPI-1886', 'PPInfo - Пояснения к разделам на странице продукта')
    def test_info_about_tab(self, metrics_page):
        with allure.step("Проверяем, что заголовок страницы отображается корректно"):
            assert metrics_page.metrics_header.is_visible(), 'Заголовка нет'
            assert metrics_page.metrics_header.get_text() == 'Метрики', 'Текст заголовка не совпадает'
        with allure.step("Проверяем, что описание страницы отображается корректно"):
            assert metrics_page.tab_description.is_visible(), 'Описания нет'
            assert metrics_page.tab_description.get_text() == assertions.metrics_description, 'Описание таба не совпадает'

    @allure.title("Проверка корректного отображения кнопки 'Запросить доступ' на странице Метрики")
    def test_metric_gain_access(self, metrics_page):
        with allure.step("Проверяем отображение кнопки"):
            assert metrics_page.get_access_button_metrics.is_visible(), 'Кнопка не отображается'
        with allure.step("Проверяем кликабельность кнопки"):
            assert metrics_page.get_access_button_metrics.is_clickable(), 'Кнопка некликабельна'
        with allure.step("Проверяем текст у кнопки"):
            assert metrics_page.get_access_button_metrics.get_text() == 'ЗАПРОСИТЬ ДОСТУП', 'Надпись у кнопки не совпадает'

    @allure.title("Корректное отображение iframe в метриках на странице продукта")
    def test_metrics_iframe(self, metrics_page):
        with allure.step("Проверяем, что айфрейм отображается"):
            assert metrics_page.metrics_iframe.is_visible(), 'Айфрейм не отображается'

    @allure.title("Отображение корректного текста при отсутствии iframe в метриках на странице продукта")
    @pytest.mark.parametrize('metrics_page', ['https://stage.prodboard.mts.ru/product/BI_202/metrics'], indirect=True)
    def test_metrics_iframe_none(self, metrics_page):
        with allure.step("Проверяем замещающий текст вместо айфрейма"):
            assert metrics_page.metrics_iframe_none.get_text() == assertions.metrics_error, 'Текст не совпадает'

    # TODO: придумать как закрыть окно авторизации

    # @allure.title("Нажатие на название возвращает к основной информации о текущем продукте (с таба метрик)")
    # def test_name_returns_to_main_info_from_metrics(self, metrics_page):
    #     page = ProductPage(self.driver)
    #     with allure.step('Кликаем на таб "Метрики и другие витрины"'):
    #         metrics_page.metrics_tab.click()
    #         metrics_page.wait_page_loaded()
    #     with allure.step("Кликаем на название продукта"):
    #         metrics_page.product_name.click()
    #     with allure.step("Проверяем, что мы вернулись на главную страницу продукта"):
    #         assert metrics_page.metrics_header.is_not_visible(), 'Заголовок с Метрики и другие витрины остался'
    #
    # @allure.title("Нажатие на лого возвращает к основной информации о текущем продукте (с таба метрик)")
    # def test_logo_returns_to_main_info_from_metrics(self, metrics_page):
    #     page = ProductPage(self.driver)
    #     with allure.step('Кликаем на таб "Метрики и другие витрины"'):
    #         metrics_page.metrics_tab.click()
    #         metrics_page.test1 = '123'
    #         metrics_page.wait_page_loaded()
    #         #metrics_page.press_key()
    #     with allure.step("Кликаем на лого продукта"):
    #         metrics_page.product_logo.click()
    #     with allure.step("Проверяем, что мы вернулись на главную страницу продукта"):
    #         assert metrics_page.metrics_header.is_not_visible(), 'Заголовок с Метрики и другие витрины остался'
