from typing import Any

import allure

from API.data.pmd import DeletedProducts, Products, Documents, ProductByCode, SearchPublicProduct

HOST = 'https://stage.prodboard.example.com'


class ProductV1Urls:
    """
    https://stage.prodboard.example.com/pmd/swagger/public/v1/product/index.html#/
    """

    # Получение продуктов
    GET_PRODUCT = 'v1/product'

    # Получение документов
    GET_DOCUMENTS = 'v1/product/documents'

    # Поиск продуктов
    POST_SEARCH = 'v1/product/search'

    # Получение определенного продукта по коду
    GET_PRODUCT_BY_CODE = 'v1/product/{}'


class ProductV1(ProductV1Urls):

    @allure.step('Данные для удаленных продуктов')
    def get_params_for_deleted(self, new_params: dict[str, Any] | None = None) -> dict[str, Any]:
        params = {
            'limit': 10,
            'offset': 0,
            'startDate': '2023-06-01',
            'endDate': '2023-12-30'
        }
        if new_params:
            params.update(new_params)
        return params

    @allure.step('Данные для поиска')
    def get_data_for_search(self, new_data: dict[str, Any] | None = None) -> dict[str, Any]:
        data = {
            'limit': 10,
            'offset': 0,
            'query': '',
            'sort': '',
            'requiredData': 'PPinfo_market'
        }
        if new_data:
            data.update(new_data)
        return data


    @allure.step('Получение продуктов')
    def get_products(self, client) -> dict[str, Any]:
        response = client.get(self.GET_PRODUCT)

        Products(**response)

        return response

    @allure.step('Получение документов')
    def get_documents(self, client) -> dict[str, Any]:
        response = client.get(self.GET_DOCUMENTS)

        Documents(**response)

        return response

    @allure.step('Получение выборки продуктов')
    def post_search(self, client, data: dict[str, Any]) -> dict[str, Any]:
        response = client.post(self.POST_SEARCH, json=data)

        SearchPublicProduct(**response)

        return response

    @allure.step('Получение информации о продукте по id')
    def get_product_by_code(self, client, product_id: str, required_data: str = None) -> dict[str, Any]:
        response = client.get(self.GET_PRODUCT_BY_CODE.format(product_id), params=required_data)

        ProductByCode(**response)

        return response

    @allure.step('Невалидное получение информации о продукте по id')
    def get_product_by_code_400(self, client, product_id: str, required_data: str = None) -> None:
        client.get(self.GET_PRODUCT_BY_CODE.format(product_id), params=required_data, expected_status_code=400)
