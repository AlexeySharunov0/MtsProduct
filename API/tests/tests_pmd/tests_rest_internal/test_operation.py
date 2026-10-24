import os
import warnings

import allure
import pandas as pd
import pytest
from more_itertools import is_sorted

from API.models.pmd.rest_internal_modules.operations import Operations

warnings.filterwarnings('ignore', message='numpy.dtype size changed')


#### OPERATIONS
@pytest.mark.api
@allure.feature('Массовые операции')
@pytest.mark.last
class TestBulkOperationsApi(Operations):
    @allure.title('Получение файла массовых операций без выбора атрибутов')
    def test_operation_get_file(self, pmd_admin_rest_client):
        with open(self.filename, 'wb') as file:
            file.write(self.get_file_for_operation(pmd_admin_rest_client, {'attributes': ''}))

        df = pd.read_excel(self.filename)

        with allure.step('Проверяем что excel не пустой'):
            assert not df.empty, 'Файл excel массовых операций пустой'

        os.remove(self.filename)

    @allure.title('Получение файла массовых операций и проверка столбцов')
    def test_operation_get_file_check_cols(self, pmd_admin_rest_client):
        with open(self.filename, 'wb') as file:
            file.write(self.get_file_for_operation(pmd_admin_rest_client, {'attributes': ''}))

        df = pd.read_excel(self.filename)

        with allure.step('Проверяем наличие всех обязательных столбцов'):
            missed_cols = [col for col in self.required_cols if col not in df.columns]

            assert not missed_cols, f'Обязательных столбцов {missed_cols} не хватает'

        with allure.step('Проверяем, что все столбцы заполнены'):
            empty_cols = [column for column in df.columns if df[column].isnull().all()]

            assert not empty_cols, f'Столбцы {empty_cols} пустые'

        os.remove(self.filename)

    @allure.title('Получение файла массовых операций и проверка записей')
    def test_operation_get_file_check_rows(self, pmd_admin_rest_client):
        with open(self.filename, 'wb') as file:
            file.write(self.get_file_for_operation(pmd_admin_rest_client, {'attributes': ''}))

        df = pd.read_excel(self.filename)

        with allure.step('Проверяем, что записи отсортированы по коду'):
            assert is_sorted(df['Код']), 'Записи отсортированы не по коду'

        os.remove(self.filename)

    @allure.title('Получение файла массовых операций с выбором атрибутов')
    def test_operation_get_file_with_attr(self, pmd_admin_rest_client):
        params = self.get_default_attributes

        with open(self.filename, 'wb') as file:
            file.write(self.get_file_for_operation(pmd_admin_rest_client, params))

        df = pd.read_excel(self.filename)

        expected_columns = self.required_cols + self.get_default_attributes_names

        with allure.step('Проверяем наличие всех обязательных столбцов'):
            missed_cols = [col for col in expected_columns if col not in df.columns]

            assert not missed_cols, f'Обязательных столбцов {missed_cols} не хватает'

        with allure.step('Проверяем, что все столбцы заполнены'):
            empty_cols = [column for column in df.columns if df[column].isnull().all()]

            assert not empty_cols, f'Столбцы {empty_cols} пустые'

        os.remove(self.filename)

    @allure.title('Получение списка всех атрибутов в массовых операциях')
    def test_get_attributes_list(self, pmd_admin_rest_client):
        assert self.get_attributes_for_operation(pmd_admin_rest_client), 'Список атрибутов пустой'

    @allure.title('Получение файла массовых операций с выбором всех атрибутов')
    def test_operation_get_file_with_attr(self, pmd_admin_rest_client):
        with open(self.filename, 'wb') as file:
            file.write(self.get_file_for_operation(pmd_admin_rest_client))

        df = pd.read_excel(self.filename)

        expected_columns = self.required_cols + [i['name'] for i in
                                                 self.get_attributes_for_operation(pmd_admin_rest_client)]

        with allure.step('Проверяем наличие всех обязательных столбцов'):
            missed_cols = [col for col in expected_columns if col not in df.columns]

            assert not missed_cols, f'Обязательных столбцов {missed_cols} не хватает'

        os.remove(self.filename)

    #### Запись в массовых операциях

    @allure.title('Массовые операции / Запись файла / Стринга')
    @pytest.mark.parametrize('value', ['werwerq', '34514534'])
    def test_operation_save_file_string(self, pmd_admin_rest_client, value):
        response = self.save_file(pmd_admin_rest_client, self.validate_file(pmd_admin_rest_client,
                                                                            self.get_operation_file(
                                                                                pmd_admin_rest_client), value, 8))[
            'errors']

        with allure.step('Проверяем, что изменения успешно сохранились'):
            assert not response, f'Ошибка сохранения {response}'

        os.remove('filename_operation.xlsx')

    @allure.title('Массовые операции / Запись файла / Дата')
    @pytest.mark.parametrize('value', ['01.06.2020', '29.06.2024'])
    def test_operation_save_file_date(self, pmd_admin_rest_client, value):
        response = self.save_file(pmd_admin_rest_client, self.validate_file(pmd_admin_rest_client,
                                                                            self.get_operation_file(
                                                                                pmd_admin_rest_client), value, 9))[
            'errors']

        with allure.step('Проверяем, что изменения успешно сохранились'):
            assert not response, f'Ошибка сохранения {response}'

        os.remove('filename_operation.xlsx')

    @allure.title('Массовые операции / Запись файла / Юзер')
    @pytest.mark.parametrize('value', ['Воронцова Оксана Сергеевна (o.vorobyeva)',
                                       'Всезнаковый Пользователь (user-with.all_signs123)'])
    def test_operation_save_file_user(self, pmd_admin_rest_client, value):
        response = self.save_file(pmd_admin_rest_client, self.validate_file(pmd_admin_rest_client,
                                                                            self.get_operation_file(
                                                                                pmd_admin_rest_client), value, 7))[
            "errors"]

        with allure.step('Проверяем, что изменения успешно сохранились'):
            assert not response, f'Ошибка сохранения {response}'

        os.remove('filename_operation.xlsx')

    @allure.title('Массовые операции / Запись файла / Число')
    @pytest.mark.parametrize('value', [0, 9999999999, 123, -100])
    def test_operation_save_file_num(self, pmd_admin_rest_client, value):
        response = self.save_file(pmd_admin_rest_client, self.validate_file(pmd_admin_rest_client,
                                                                            self.get_operation_file(
                                                                                pmd_admin_rest_client), value, 10))[
            'errors']

        with allure.step('Проверяем, что изменения успешно сохранились'):
            assert not response, f'Ошибка сохранения {response}'

        os.remove('filename_operation.xlsx')

    @allure.title('Массовые операции / Запись файла / Один продукт')
    @pytest.mark.parametrize('value', ['BI_60', 'BI_42'])
    def test_operation_save_file_one_product(self, pmd_admin_rest_client, value):
        response = self.save_file(pmd_admin_rest_client, self.validate_file(pmd_admin_rest_client,
                                                                            self.get_operation_file(
                                                                                pmd_admin_rest_client), value, 11))[
            'errors']

        with allure.step('Проверяем, что изменения успешно сохранились'):
            assert not response, f'Ошибка сохранения {response}'

        os.remove('filename_operation.xlsx')

    @allure.title('Массовые операции / Запись файла / Описание')
    @allure.issue('https://jira.mts.ru/browse/PPI-2611', 'PPInfo - Изменение Описания в массовых операциях')
    @pytest.mark.parametrize('value', ['Такое вот описание \n 123', 'ОПИСАНИЕ \n\n\n 1234'])
    def test_operation_save_file_description(self, pmd_admin_rest_client, value):
        response = self.save_file(pmd_admin_rest_client, self.validate_file(pmd_admin_rest_client,
                                                                            self.get_operation_file(
                                                                                pmd_admin_rest_client), value, 12))[
            'errors']

        with allure.step('Проверяем, что изменения успешно сохранились'):
            assert not response, f'Ошибка сохранения {response}'

        os.remove('filename_operation.xlsx')

    @allure.title('Массовые операции / Запись файла / Многострочный текст')
    @pytest.mark.parametrize('value', ['привет всем!', 'люблю \n энтеры \n сильно'])
    def test_operation_save_file_multistring(self, pmd_admin_rest_client, value):
        response = self.save_file(pmd_admin_rest_client, self.validate_file(pmd_admin_rest_client,
                                                                            self.get_operation_file(
                                                                                pmd_admin_rest_client), value, 13))[
            'errors']

        with allure.step('Проверяем, что изменения успешно сохранились'):
            assert not response, f'Ошибка сохранения {response}'

        os.remove('filename_operation.xlsx')

    @allure.title('Массовые операции / Запись файла / Ссылка')
    @pytest.mark.parametrize('value', ['текст будет ссылкой', 'https://stage.prodboard.mts.ru/preset/external'])
    def test_operation_save_file_link(self, pmd_admin_rest_client, value):
        response = self.save_file(pmd_admin_rest_client, self.validate_file(pmd_admin_rest_client,
                                                                            self.get_operation_file(
                                                                                pmd_admin_rest_client), value, 15))[
            'errors']

        with allure.step('Проверяем, что изменения успешно сохранились'):
            assert not response, f'Ошибка сохранения {response}'

        os.remove('filename_operation.xlsx')

    @allure.title('Массовые операции / Запись файла / Мэниселект')
    @pytest.mark.parametrize('value', ["Основной", "Атомарный", ''])
    def test_operation_save_file_many_select(self, pmd_admin_rest_client, value):
        response = self.save_file(pmd_admin_rest_client, self.validate_file(pmd_admin_rest_client,
                                                                            self.get_operation_file(
                                                                                pmd_admin_rest_client), value, 16))[
            'errors']

        with allure.step('Проверяем, что изменения успешно сохранились'):
            assert not response, f'Ошибка сохранения {response}'

        os.remove('filename_operation.xlsx')

    @allure.title('Массовые операции / Запись файла / Множественный сотрудник')
    @allure.issue('https://jira.mts.ru/browse/PPI-2863',
                  'PPInfo - Массовые изменения: загрузка несколько логинов в атрибут')
    @pytest.mark.parametrize('value', ['Масленков Павел Юрьевич (pymaslenkov);Курочкин Сергей Викторович (svkurochkin)',
                                       'Молчанов Игорь Владимирович (ivmolchanov);Кондратьев Сергей Николаевич (snkondratyev)'])
    def test_operation_save_file_multy_user(self, pmd_admin_rest_client, value):
        response = self.save_file(pmd_admin_rest_client, self.validate_file(pmd_admin_rest_client,
                                                                            self.get_operation_file(
                                                                                pmd_admin_rest_client), value, 14))[
            'errors']

        with allure.step('Проверяем, что изменения успешно сохранились'):
            assert not response, f'Ошибка сохранения {response}'

        os.remove('filename_operation.xlsx')
