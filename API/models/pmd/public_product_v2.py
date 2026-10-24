from typing import Any

import allure

from API.data.pmd import SearchResult, Story

HOST = 'https://stage.prodboard.example.com'


class ProductV2Urls:
    """
    https://stage.prodboard.example.com/pmd/swagger/public/v2/product/index.html#/
    """

    # Поиск по имени продукта
    SEARCH_BY_NAME = 'v2/product/search-by-name'

    # Получение значения атрибута на определенную дату
    STORY = 'v2/product/story'


class ProductV2(ProductV2Urls):

    @allure.step('Получение данных для story')
    def get_data_for_story(self, date: str = '2024-01-16T21:00:00.000Z', attr_name: str = 'PPinfo_market'):
        return {
            'date': date,
            'attributes': [
                attr_name
            ]
        }

    @allure.step('Поиск по имени пост запросом')
    def search_by_name(self, client, data: dict[str, Any]) -> dict[str, Any]:
        response = client.post(self.SEARCH_BY_NAME, json=data)

        SearchResult(**response)

        return response

    @allure.step('Получение значения атрибута на дату')
    def get_attribute_story(self, client, data: dict[str, Any]) -> dict[str, Any]:
        response = client.post(self.STORY, json=data)

        Story(**response)

        return response
