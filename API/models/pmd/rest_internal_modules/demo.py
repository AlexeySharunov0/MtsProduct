import os
import warnings
from typing import Any

import allure
import pandas as pd

from API.data.pmd import DemosInProduct, DemosCategories, Quarters, Demos
from API.utils.generate import Gen
from API.api_fixtures import rest_internal_client

warnings.filterwarnings("ignore", message="numpy.dtype size changed")

HOST = 'https://stage.prodboard.example.com'


class DemoUrls:
    """
    https://stage.prodboard.example.com/pmd/swagger/rest/internal/index.html#/
    """

    #### DEMO

    # Получение списка всех демо
    GET_DEMOS = 'v1/demo'

    # Получение категорий демо
    GET_CATEGORIES = 'v1/demo/category'

    # Добавление категории демо
    ADD_CATEGORY = 'v1/demo/category'

    # Получение категории демо по id
    GET_CATEGORY_BY_ID = 'v1/demo/category/{}'

    # Изменение категории демо по id
    PATCH_CATEGORY_BY_ID = 'v1/demo/category/{}'

    # Получение файла по id
    GET_FILE_BY_ID = 'v1/demo/file/{}'

    # Удаление файла по id
    DELETE_FILE_BY_ID = 'v1/demo/file/{}'

    # Добавление файла
    ADD_FILE = 'v1/demo/file'

    # Проверка уникальность демо
    GET_DEMO_BY_LINK = 'v1/demo/link'

    # Получение демо по коду продукта
    GET_DEMOS_BY_BI_CODE_V1 = 'v1/demo/product/{}'

    # Создание демо по коду продукта
    ADD_DEMO_BY_BI_CODE_V1 = 'v1/demo/product/{}'

    # Получение демо по id
    GET_DEMO_BY_ID = 'v2/demo/{}'

    # Удаление демо продукта по id
    DELETE_DEMO_BY_ID_V1 = 'v1/demo/{}'

    # Изменение демо продукта по id
    PATCH_DEMO_BY_ID_V1 = 'v1/demo/{}'

    # Создание нового демо
    ADD_DEMO = 'v2/demo'

    # Получение демо по коду продукта
    GET_DEMOS_BY_BI_CODE = 'v2/demo/product/{}'

    # Удаление демо продукта по id
    DELETE_DEMO_BY_ID = 'v2/demo/{}'

    # Изменение демо продукта по id
    PATCH_DEMO_BY_ID = 'v2/demo/{}'

    # Иксель демо
    DEMO_EXCEL = 'v2/demo/excel'

    # # Получение демо по коду продукта
    # GET_DEMOS_BY_BI_CODE = 'v1/demo/product/{}'


class Demo(DemoUrls):
    # DEMO

    @property
    def text(self):
        return Gen.generate_text(7) + 'test'


    @allure.step('Получение Демо по коду продукта')
    def get_demo_by_code(self, client, bi_code: str = 'BI_3266') -> dict:
        response = client.get(self.GET_DEMOS_BY_BI_CODE.format(bi_code))

        DemosInProduct(**response)

        return response

    @allure.step('Получение всех демо')
    def get_demos(self, client) -> dict:
        response = client.get(self.GET_DEMOS)

        Quarters(demos=response)

        return response

    @allure.step('Формирование тела для Демо')
    def get_demo_data(self, description: str = 'test_description', link: str = 'test_link', name: str = 'test_name',
                      other: dict[str, Any] = None, category_id: str = '0040360f-9ab3-63d0-b4c8-cfc6294438de') -> dict[str, Any]:
        data = {
            "name": name,
            "categoryID": category_id,
            "conductedAt": "2025-01-09T00:00:00Z",
            "description": description,
            "link": link + self.text,
            "linkedProducts": [],
            "files": [
            ]

        }

        if other:
            data.update(other)

        return data

    @allure.step('Формирование тела для категории Демо')
    def get_category_data(self, description: str = 'test_category_description', is_active: bool = True, name: str = 'test_category_name', color: str = "#33a9f2",
                          other: dict[str, Any] = None) -> dict[str, Any]:
        data = {
            "color": color,
            "description": description,
            "isActive": is_active,
            "name": name
        }
        if other:
            data.update(other)

        return data

    @allure.step('Получение Демо по коду продукта')
    def get_demo_by_product_code(self, client, bi_code: str = 'BI_3266') -> dict:
        response = client.get(self.GET_DEMOS_BY_BI_CODE.format(bi_code))

        Demos(**response)

        return response

    @allure.step('Получение всех демо')
    def get_demos(self, client) -> dict:
        response = client.get(self.GET_DEMOS)

        Quarters(quarters=response)

        return response

    @allure.step('Создание демо')
    def create_demo(self, client, data: dict[str, Any]) -> dict[str, Any]:
        response = client.post(self.ADD_DEMO, json=data)

        return response

    @allure.step('Создание демо')
    def create_demo_400(self, client, data: dict[str, Any]) -> None:
        client.post(self.ADD_DEMO, json=data, expected_status_code=400)

    @allure.step('Создание заявки на добавление Демо')
    def create_demo_user(self, client, data: dict[str, Any]) -> dict[str, Any]:
        response = client.post(self.ADD_DEMO, json=data)

        return response

    @allure.step('Удаление демо')
    def delete_demo(self, client, demo_id: str) -> None:
        client.delete(self.DELETE_DEMO_BY_ID.format(demo_id))

    @allure.step('Создание заявки на удаление демо')
    def delete_demo_user(self, client, demo_id: str) -> str:
        response = client.delete(self.DELETE_DEMO_BY_ID.format(demo_id))

        return response.text.strip('"')

    @allure.step('Изменение демо')
    def patch_demo(self, client, demo_id: str, data: dict[str, Any]) -> None:
        client.patch(self.PATCH_DEMO_BY_ID.format(demo_id), json=data, raw_format=True)

    @allure.step('Создание заявки на изменение демо')
    def patch_demo_user(self, client, demo_id: str, data: dict[str, Any]) -> str:
        response = client.patch(self.PATCH_DEMO_BY_ID.format(demo_id), json=data, raw_format=True)

        return response.text.strip('"')

    @allure.step('Получение всех категорий демо')
    def get_categories(self, client) -> dict:
        response = client.get(self.GET_CATEGORIES)
        DemosCategories(categories=response)
        return response

    @allure.step('Добавление новой категории демо')
    def add_category(self, client, data: dict[str, Any]) -> str:
        response = client.post(self.ADD_CATEGORY, json=data)
        return response

    @allure.step('Некорректное добавление новой категории демо')
    def add_category_400(self, client, data: dict[str, Any]) -> None:
        client.post(self.ADD_CATEGORY, json=data, expected_status_code=400)

    @allure.step('Получение категории демо по ID')
    def get_category_by_id(self, client, category_id: str) -> dict:
        response = client.get(self.GET_CATEGORY_BY_ID.format(category_id))
        return response

    @allure.step('Изменение категории демо по ID')
    def patch_category_by_id(self, client, category_id: str, data: dict[str, Any]) -> None:
        client.patch(self.PATCH_CATEGORY_BY_ID.format(category_id), json=data, raw_format=True)

    @allure.step('Добавление файла')
    def add_file(self, client, filename: str, file_format: str = '.xlsx') -> str:
        with open(filename + file_format, 'w'):
            with open(filename + file_format, 'rb') as f:
                file_dict = {'file': f}
                with allure.step('Добавляем документ'):
                    response = client.post(self.ADD_FILE, files=file_dict)

        os.remove(filename + file_format)

        return response

    @allure.step('Получение файла по ID')
    def get_file_by_id(self, client, file_id: str) -> dict:
        response = client.get(self.GET_FILE_BY_ID.format(file_id), raw_format=True)
        return response

    @allure.step('Получение файла по несуществующему ID')
    def get_file_by_id_404(self, client, file_id: str) -> None:
        client.get(self.GET_FILE_BY_ID.format(file_id), raw_format=True, expected_status_code=404)

    @allure.step('Удаление файла по ID')
    def delete_file_by_id(self, client, file_id: str) -> None:
        client.delete(self.DELETE_FILE_BY_ID.format(file_id))

    @allure.step('Проверка уникальности демо по ссылке')
    def check_uniqueness_link(self, client, link: str) -> None:
        params = {
            'link': link
        }
        client.get(self.GET_DEMO_BY_LINK, params=params, expected_status_code=404)

    @allure.step('Проверка уникальности демо по ссылке')
    def check_not_uniqueness_link(self, client, link: str) -> None:
        params = {
            'link': link
        }
        response = client.get(self.GET_DEMO_BY_LINK, params=params)

        return response

    @allure.step('Создание демо по коду продукта (версия 1)')
    def add_demo_by_bi_code_v1(self, client, bi_code: str, data: dict[str, Any]) -> dict:
        response = client.post(self.ADD_DEMO_BY_BI_CODE_V1.format(bi_code), json=data)
        return response

    @allure.step('Получение демо по ID')
    def get_demo_by_id(self, client, demo_id: str) -> dict:
        response = client.get(self.GET_DEMO_BY_ID.format(demo_id))
        return response

    @allure.step('Проверяем результаты поиска')
    def check_demo_in_search_result(self, pattern: str, search_result: list[dict[str, Any]]):
        demos = []
        for demo in search_result:
            if pattern.lower() not in demo["name"].lower():
                demos.append(demo["name"])

        assert not demos, f"{demos=} появились по паттерну {pattern}"

    @allure.step("Создание Excel")
    def get_excel_demos(self, client) -> pd.DataFrame:
        excel_content = client.get(self.DEMO_EXCEL, raw_format=True)

        with open("filename_excel.xlsx", 'wb') as f:
            f.write(excel_content.content)

        return pd.read_excel("filename_excel.xlsx")


