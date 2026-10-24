from typing import Any

import allure

from API.data.product_bi_id import ProductBiId

HOST = 'https://stage.prodboard.example.com'


class ProductV2Urls:
    """
    https://stage.prodboard.example.com/ppinfo/swagger/v2/product/index.html
    """
    # Поиск продукта в атрибуте с типом Продукт
    SEARCH = 'v2/product/search'

    # Получение информации по продукту для отображения в карточке продукта
    GET_INFO_BY_PRODUCT_CODE = 'v2/product/{}'


class ProductV2(ProductV2Urls):

    @allure.step('Получаем дату для смены атрибута в продукте')
    def get_data_for_attr_change(self, attr_id: str, code: str = None, value: str = None) -> dict[str, Any]:
        data = {
            'id': 'BI_2769',
            'attributes': [
                {
                    'id': attr_id,
                    'values': [
                        {
                            'code': code,
                            'value': value
                        }
                    ] if code else []
                }
            ],
            'notification': False,
            'type': 'Vneshnii'
        }
        return data

    @allure.step('Получение информации по продукту по коду BI')
    def get_info_by_product_code(self, client, product_code) -> dict[str, Any]:
        with allure.step(f'Получение информации по продукту по коду {product_code}'):
            response = client.get(self.GET_INFO_BY_PRODUCT_CODE.format(product_code))

        ProductBiId(**response)

        return response

    @allure.step('Получение информации по продукту по коду BI как обычный юзер')
    def get_info_by_product_code_by_user(self, client, product_code) -> dict[str, Any]:
        with allure.step(f'Получение информации по продукту по коду {product_code}'):
            response = client.get(self.GET_INFO_BY_PRODUCT_CODE.format(product_code))

        ProductBiId(**response)

        return response

    @allure.step('Поиск продукта в атрибутах')
    def search_products_in_attribute(self, client, pattern: str) -> dict[str, Any]:
        data = {
            'pattern': pattern
        }
        response = client.get(self.SEARCH, params=data)

        return response
