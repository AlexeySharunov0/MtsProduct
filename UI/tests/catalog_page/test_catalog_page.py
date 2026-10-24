import allure
import pytest

import UI.data.assertions_data as assertions
from UI.tests.catalog_page.conftest import catalog_page


@pytest.mark.ui
@allure.feature("Главная страница")
class TestNavigationBar:

    @allure.title(f"Добавление продукта в избранное и удаление оттуда")
    def test_add_in_favorite(self, catalog_page):
        product_name = catalog_page.product_title.get_text()
        with allure.step('Переходим в карточку продукта'):
            catalog_page.product_title.click()
        with allure.step('Кликаем по закладке, чтобы добавить продукт в избранные'):
            if not catalog_page.add_favorite_in_header.is_clickable():
                catalog_page.delete_favorite_in_header.click()
            catalog_page.add_favorite_in_header.click()
        with allure.step('Кликаем по избранным продуктам'):
            catalog_page.favorites_button.click()
        all_product = catalog_page.all_product_title.get_texts()
        with allure.step('Проверяем, что отмеченный продукт есть в списке избранных'):
            assert product_name in all_product, 'Продукта нет в избранных'
        with allure.step('Переходим в карточку продукта'):
            catalog_page.get_page("https://stage.prodboard.mts.ru/product/BI_63/main")
        with allure.step('Кликаем по закладке, чтобы убрать продукт из избранных'):
            catalog_page.delete_favorite_in_header.click()
        with allure.step('Кликаем по избранным продуктам'):
            catalog_page.favorites_button.click()
        all_product = catalog_page.all_product_title.get_texts()
        with allure.step('Проверяем, что отмеченного продукта нет в списке избранных'):
            assert product_name not in all_product, 'Продукт есть в избранных'


@pytest.mark.ui
@allure.feature("Главная страница")
class TestProductListView:

    @allure.issue("https://jira.mts.ru/browse/CAKF-1591", "На витрине отображены атомарные продукты")
    @allure.title("Отсутствие атомарных на витрине")
    def test_no_atomic_on_main(self, catalog_page):
        with allure.step('Заходим на главную страницу'):
            all_titles = catalog_page.products_titles.get_texts()
        with allure.step('Проверяем, что атомарные продукты не отображаются на витрине'):
            assert all(i not in all_titles for i in
                       assertions.ProductsAsserts.atomicProducts), 'На витрине отображены атомарные продукты'

