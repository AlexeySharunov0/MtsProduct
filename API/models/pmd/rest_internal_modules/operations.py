import io
import warnings
from typing import Any

import allure
import openpyxl
import pandas as pd

from API.data.pmd import AttributeListExternal

warnings.filterwarnings("ignore", message="numpy.dtype size changed")

HOST = 'https://stage.prodboard.example.com'


class OperationsUrls:
    """
    https://stage.prodboard.example.com/pmd/swagger/rest/internal/index.html#/
    """

    #### OPERATIONS

    # Получение файла с атрибутами для массовых операций
    BULK_OPERATIONS = 'v1/operation'

    # Получение списка с атрибутами для массовых операций
    OPERATIONS_ATTRIBUTES = 'v1/operation/attributes'

    # Валидация файла с атрибутами для массовых операций
    VALIDATE = 'v1/operation/validate'

    # Сохранение файла с атрибутами для массовых операций
    SAVE = 'v1/operation/save'


class Operations(OperationsUrls):

    #### OPERATIONS
    @property
    def required_cols(self) -> list[str]:
        return ['Код', 'Название', 'Статус', 'Структурный тип продукта', 'Тип продукта', 'Инициировано закрытие']

    @property
    def filename(self) -> str:
        return 'filename_operation.xlsx'

    @property
    def get_default_attributes(self):
        return {
            'attributes': [
                'PPInfo_showcase',  # 8
                'PPinfo_resolution',  # 13
                'PPinfo_StructuralProductType1',  # 16
                'PPinfo_start_close_date',  # 9
                'Identifikator_SOL',  # 10
                'employee_business_owner',  # 7
                'Odin_produkt',  # 11
                'PPInfo_site_landing',  # 15
                'Rukovoditel_etogo_balagana',  # 14
                'EXTRA_ProductDescription'  # 12
                # номера столбцов
            ]
        }

    @property
    def get_default_attributes_names(self):
        return ['Витрина', 'Решение', 'Структурный тип продукта', 'Дата инициировано закрытия', 'Идентификатор SOL',
                'Business owner', 'Один продукт', 'Сайт', 'Описание продукта']

    @allure.step('Получение файла с атрибутами для массовых операций')
    def get_file_for_operation(self, client, attributes: dict[str, Any] | None = None) -> bytes:
        response = client.get(self.BULK_OPERATIONS, params=attributes, raw_format=True)

        return response.content

    @allure.step('Получение списка с атрибутами для массовых операций')
    def get_attributes_for_operation(self, client) -> list[dict[str, str]]:
        response = client.get(self.OPERATIONS_ATTRIBUTES)

        AttributeListExternal(attributes=response)

        return response

    @allure.step('Валидация файла')
    def validate_file(self, client, file_operation: io.BytesIO, value: Any, column: int, validate: bool = True):
        df = pd.read_excel('filename_operation.xlsx')
        row = list(df['Код']).index(20319) + 2

        wb = openpyxl.load_workbook(file_operation)
        sheet = wb['Продукты']

        with allure.step(f'Меняем значение в записи на {value}'):
            cell = sheet.cell(row=row, column=column)
            cell.value = value

            wb.save('filename_operation.xlsx')
            file = {'file': (self.filename, open('filename_operation.xlsx', 'rb'),
                             'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')}

        response = client.post(self.VALIDATE, files=file)
        with allure.step(f'Проверяем что файл валидный'):
            assert response['products'][0][
                       'isValid'] is validate, f"Файл невалидный, {response['products'][0]['isValid']}"

        return response

    @allure.step('Сохранение файла в массовых операциях')
    def save_file(self, client, data: dict[str, Any]) -> dict[str, Any]:
        response = client.post(self.SAVE, json=data)

        return response['products'][0]['attributes'][0]

    @allure.step('Получение и подготовка файла массовых операций')
    def get_operation_file(self, client, params: dict[str, Any] = None):
        if params is None:
            params = self.get_default_attributes

        with open('filename_operation.xlsx', 'wb') as f:
            f.write(self.get_file_for_operation(client, params))

        xls = 'filename_operation.xlsx'

        return xls
