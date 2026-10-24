import warnings
from typing import Any

import allure
import openpyxl

from API.data.pmd import RMS, \
    EDT

warnings.filterwarnings("ignore", message="numpy.dtype size changed")

HOST = 'https://stage.prodboard.example.com'


class SystemUrls:
    """
    https://stage.prodboard.example.com/pmd/swagger/rest/internal/index.html#/
    """

    #### SYSTEM

    # Отображение сервисов и капабилити
    EDT = 'v1/system/edt/{}'

    # Выгрузка сервисов и капабилити в Excel
    EDT_EXCEL = 'v1/system/edt/{}/excel'

    # Отображение RMS во вкладке Проекты
    RMS = 'v1/system/rms/{}'


class System(SystemUrls):
    #### SYSTEM

    @allure.step('Получение информации по Сервисам и Капабилити из EDT')
    @allure.issue('https://jira.example.com/browse/PPI-2963', 'PPInfo - Раздел "Сервисы и капабилити"')
    def get_edt(self, client, product_code: str) -> dict[str, Any]:
        """
        Получение информации по Сервисам и Капабилити из EDT
        Args:
            product_code: Код продукта
            client: API клиент для запросов
        Returns:
            json с информацией по Сервисам и Капабилити
        """
        response = client.get(self.EDT.format(product_code))

        EDT(**response)

        return response

    @allure.step('Получение Excel Капабилити и Сервисов')
    def get_edt_info_by_excel(self, client, product_code: str) -> openpyxl.Workbook:
        """
        Получение Excel Капабилити и Сервисов по коду продукта
        Args:
            product_code: Код продукта
            client: API клиент для запросов

        Returns:
            Excel Сервисов и капабилити по коду продукта

        """
        response = client.get(self.EDT_EXCEL.format(product_code), raw_format=True)

        with open('filename_excel.xlsx', 'wb') as f:
            f.write(response.content)

        xls = 'filename_excel.xlsx'

        wb = openpyxl.load_workbook(xls)

        return wb

    @allure.step('Получение информации проектам RMS')
    def get_rms(self, client, product_code: str) -> dict[str, Any]:
        response = client.get(self.RMS.format(product_code))

        RMS(rms=response)

        return response

    @allure.step('Невалидное получение информации проектам RMS')
    def get_rms_400(self, client, product_code: str) -> None:
        client.get(self.RMS.format(product_code), expected_status_code=400)
