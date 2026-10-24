import time
from typing import Dict, Any

import allure
import requests
from requests import RequestException

from API.data.mobile import MobilSearch, ProductMobil, FavProductsList, ManagedProductsList, ProductV2
from UI.pages.product_page.main.main_page import logger


class MobilUrls:
    """
    https://stage.prodboard.example.com/mobile/swagger/index.html#/
    """
    SEARCH = 'v1/product/search'

    PRODUCT_V1 = 'v1/product/{}'

    LOGO = 'v1/product/{}/logo'

    MANAGED = 'v1/product/managed'

    FAVORITE = 'v1/product/favorites'

    PRODUCT_V2 = 'v2/product/{}'


class Mobil(MobilUrls):

    @allure.step('Поиск')
    def search(self, client, pattern: str) -> list:
        params = {
            "pattern": f"{pattern}"
        }

        response = client.get(self.SEARCH, params=params)

        MobilSearch(Mobile=response)

        return response

    @allure.step('Получение продуктов в мобильной апи')
    def get_product_mobil(self, client, pattern: str) -> Dict[str, Any]:
        with allure.step('Делаем запрос на получение продуктов'):
            response = client.get(self.PRODUCT_V1.format(pattern))

        with allure.step('Проверяем модель ответа и статус код'):
            ProductMobil(**response)
            return response

    @allure.step('Получение логотипов по продуктам у которых нет логотипа')
    def get_logo(self, client, pattern: int) -> str:
        with allure.step('Получаем логотип по продукту'):
            response = client.get(self.LOGO.format(pattern), raw_format=True)

        with allure.step('Проверяем статус код и что в ответ пришел портфельчик вместо картинки'):
            return response.headers['Content-Type']

    @allure.step('Получение избранных')
    def get_favorite(self, client) -> Dict[str, Any]:
        response = client.get(self.FAVORITE)

        FavProductsList(products=response)

        return response

    @allure.step('Получение моих продуктов')
    def get_managed(self, client) -> Dict[str, Any]:
        response = client.get(self.MANAGED)

        ManagedProductsList(products=response)

        return response

    @allure.step('Добавление/удаление продукта из избранного')
    def add_delete_favorite(self, client):
        data = {
            "code": "60"
        }
        with allure.step('Добавляем или удаляем продукт в избранное'):
            client.post(self.FAVORITE, json=data, raw_format=True)

    @allure.step('Проверяем что продукт в избранных')
    def check_product_in_favorite(self, client):
        with allure.step('Проверяем что продукт удален/добавлен'):
            response = client.get(self.FAVORITE)

            assert any(product['code'] == 'BI_60' for product in
                       response), f'В списке продуктов {response.json()} нет продукта с кодом BI_60'

    @allure.step('Проверяем что продукт не в избранных')
    def check_product_not_in_favorite(self, client):
        with allure.step('Проверяем что продукт удален/добавлен'):
            response = client.get(self.FAVORITE)

            assert not any(product['code'] == 'BI_60' for product in
                           response), f'В списке продуктов {response.json()} есть продукт с кодом BI_60'

    @allure.step('Получение продукта в мобильной апи')
    def get_product_v2(self, client, product_code: str) -> Dict[str, Any]:
        with allure.step('Получаем продукт'):
            response = client.get(self.PRODUCT_V2.format(product_code))

        with allure.step('Проверяем статус код и что в ответ пришел портфельчик'):
            ProductV2(**response)
            return response
