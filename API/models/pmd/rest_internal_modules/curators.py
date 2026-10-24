import warnings
from typing import Any

import allure
import openpyxl

from API.data.pmd import CuratorsModel, CuratorAttributes
from API.models.ppinfo.rest import Rest

warnings.filterwarnings("ignore", message="numpy.dtype size changed")

HOST = 'https://stage.prodboard.example.com'


class CuratorsUrls:
    """
    https://stage.prodboard.example.com/pmd/swagger/rest/internal/index.html#/
    """

    # CURATORS

    # Добавление, изменение куратора
    ADD_CURATOR = 'v1/curator'

    # Получение всех атрибутов типа вычисляемый сотрудник
    GET_ALL_CURATOR_ATTRIBUTES = 'v1/curator/spec'

    # Выгрузка Excel кураторы
    GET_CURATORS_EXCEL = 'v1/curator/excel'

    # Получение всех кураторов и кластеров по id атрибута
    GET_CURATORS_BY_ID = 'v1/curator/{}'


class Curators(CuratorsUrls):
    # CURATORS
    @allure.step('Изменение кураторов')
    def change_curators(self, client, logins: list[str] | str,
                        attribute_id: str = '83adfce2-5067-4196-b8ce-1f347a2fd1e9',
                        value_id: str = 'ac8cc879-4240-4108-ba0f-ebefb6190c6a') -> list[dict[str, Any]]:
        data = {
            'attributeID': attribute_id,
            'clusters': [
                {
                    'logins': [logins] if isinstance(logins, str) else logins,
                    'valueID': value_id
                }
            ]
        }

        response = client.put(self.ADD_CURATOR, json=data)

        CuratorsModel(curator_list=response)

        return response

    @allure.step('Невалидное изменение кураторов')
    def change_curators_invalid(self, client, logins: list[str] | str,
                                attribute_id: str = '83adfce2-5067-4196-b8ce-1f347a2fd1e9',
                                value_id: str = 'ac8cc879-4240-4108-ba0f-ebefb6190c6a') -> None:
        data = {
            'attributeID': attribute_id,
            'clusters': [
                {
                    'logins': [logins] if isinstance(logins, str) else logins,
                    'valueID': value_id
                }
            ]
        }

        client.put(self.ADD_CURATOR, json=data, expected_status_code=400)

    @allure.step('Получение всех атрибутов типа вычисляемый сотрудник')
    def get_all_curator_attributes(self, client) -> list[dict[str, Any]]:
        response = client.get(self.GET_ALL_CURATOR_ATTRIBUTES)

        CuratorAttributes(attributes=response)

        return response

    @allure.step('Получение всех кураторов и кластеров по id атрибута')
    def get_all_curators_by_id(self, client, attr_id: str) -> list[dict[str, Any]]:
        response = client.get(self.GET_CURATORS_BY_ID.format(attr_id))

        CuratorsModel(curator_list=response)

        return response

    @allure.step('Невалидное получение всех кураторов и кластеров по id атрибута')
    def get_all_curators_by_id_invalid(self, client, attr_id: str) -> None:
        client.get(self.GET_CURATORS_BY_ID.format(attr_id), expected_status_code=400, raw_format=True)

    @allure.step('Получение выгрузки excel по кураторам ')
    def get_curators_excel(self, client) -> openpyxl:
        response = client.get(self.GET_CURATORS_EXCEL, raw_format=True)

        with open('filename_excel.xlsx', 'wb') as f:
            f.write(response.content)

        xls = 'filename_excel.xlsx'

        wb = openpyxl.load_workbook(xls)
        sheet = wb.active

        return sheet
