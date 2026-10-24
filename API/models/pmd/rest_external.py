from datetime import datetime
from typing import Any

import allure

from API.data.pmd import ProductsExternal, ProductExternal, AttributesExternalRest, StoryForUI, PGExternal
from API.models.pmd.rest_internal_modules.internal_product import Story

HOST = 'https://stage.prodboard.example.com'



class RestApiExternalUrls:
    """
    https://stage.prodboard.example.com/pmd/swagger/rest/external/index.html#/
    """

    # Получение продуктов
    PRODUCTS = 'v1/product'

    # Получение определенного продукта по коду BI
    PRODUCT = 'v1/product/{}'

    # Получение логотипа продукта
    GET_PRODUCT_LOGO = 'v1/product/{}/logo'

    # Получение атрибутов
    ATTRIBUTE = 'v1/specification/attribute'

    # Получение историчности по продукту
    STORY = 'v1/product/{}/story'

    # Получение шагов ПГ по типу продукта
    GET_STEPS_BY_PRODUCT_TYPE = 'v1/actions/{}'

    # Получение файла из ПГ по id
    GET_FILE_PG_BY_ID = 'v1/file/{}'


class RestApiExternal(RestApiExternalUrls, Story):

    @allure.step('Получение параметров для get_products')
    def get_data_for_products_rest(self, new_params: dict[str, Any] = None) -> dict[str, Any]:
        params = {
            'limit': 20000,
            'offset': "0",
            'version': '',
            'filterResponse': ''
        }
        if new_params:
            params.update(new_params)

        return params

    @allure.step('Получение продуктов')
    def get_products_with_params(self, client, params: dict[str, Any]) -> list[dict]:
        response = client.get(self.PRODUCTS, params=params)

        ProductsExternal(products=response)

        return response

    @allure.step('Получение информации о продукте по коду BI')
    def get_product_by_code(self, client, product_code: str) -> dict:
        response = client.get(self.PRODUCT.format(product_code))

        ProductExternal(**response)

        return response

    @allure.step('Получение лого продукта по коду BI')
    def get_logo_by_code(self, client, code: str, image_size: str = None):
        data = {
            'size': image_size
        }
        response = client.get(self.GET_PRODUCT_LOGO.format(code), params=data, raw_format=True)

        return response.headers['Content-Type']

    @allure.step('Невалидное получение информации о продукте по коду BI')
    def get_product_by_code_404(self, client, product_code: str) -> None:
        client.get(self.PRODUCT.format(product_code), expected_status_code=404)

    @allure.step('Получение информации об атрибуте по коду')
    def get_attribute_by_code(self, client, params: dict[str, Any]) -> dict[str, Any]:
        response = client.get(self.ATTRIBUTE, params=params)

        AttributesExternalRest(attributes=response)

        return response

    @allure.step('Получение историчности по коду')
    def get_story_by_product_code(self, client, bi_code, attribute_codes: list[str] = 'all') -> list[dict]:
        params = {
            'dateFrom': '01.01.2020',
            'dateTo': datetime.today().strftime('%d.%m.%Y'),
            'attributeCodes': attribute_codes if isinstance(attribute_codes, list) else [attribute_codes]
        }
        response = client.get(self.STORY.format(bi_code), params=params)

        StoryForUI(story=response)

        return response


    @allure.step('Получение шагов ПГ по коду продукта')
    def get_pg_steps(self, client, product_code: str) -> list[dict[str, Any]]:
        response = client.get(self.GET_STEPS_BY_PRODUCT_TYPE.format(product_code))

        PGExternal(groups=response)

        return response
