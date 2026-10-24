import os
import warnings
from datetime import datetime
from urllib.parse import unquote

import allure
import pandas as pd
import pytest

from API.models.pmd.rest_internal_modules.internal_product import InternalProduct, Story

warnings.filterwarnings('ignore', message='numpy.dtype size changed')


#### INTERNAL PRODUCT

@pytest.mark.api
@allure.label('priority', 'Высокий')
@allure.feature('Excel Кластер, добавление доков/лого, атомарные продукты')
class TestInternalProducts(InternalProduct):

    @allure.title('Получение икселя Кластер')
    @allure.issue('https://jira.mts.ru/browse/PPI-1459', 'PPInfo - Проверка актуальности Кластера')
    def test_get_cluster(self, rest_internal_client):
        with open('cluster.xlsx', 'wb') as f:
            f.write(self.get_excel_cluster(rest_internal_client))

        df = pd.read_excel('cluster.xlsx')

        with allure.step('Проверяем что excel не пустой'):
            assert not df.empty, 'Файл excel Кластер пустой'

        os.remove('cluster.xlsx')

    @allure.title('Получение икселя Кластер и проверка столбцов')
    @allure.issue('https://jira.mts.ru/browse/PPI-1459', 'PPInfo - Проверка актуальности Кластера')
    def test_get_cluster_check_cols(self, rest_internal_client):
        with open('cluster.xlsx', 'wb') as f:
            f.write(self.get_excel_cluster(rest_internal_client))

        df = pd.read_excel('cluster.xlsx')

        required_cols = ['Код BI_', 'Название продукта', 'Статус', 'Кластер', 'Chief Technology Officer',
                         'Кластер в HRGate', 'Соответствует тек. справочнику']

        with allure.step('Проверяем наличие всех cтолбцов'):
            missed_cols = [col for col in required_cols if col not in df.columns]

            assert not missed_cols, f'Cтолбцов {missed_cols} не хватает'

        with allure.step('Проверяем, что все столбцы заполнены'):
            empty_cols = [column for column in df.columns if
                          df[column].isnull().all() and column != "Соответствует тек. справочнику"]

            assert not empty_cols, f'Столбцы {empty_cols} пустые'

        os.remove('cluster.xlsx')

    @allure.title('Получение икселя Кластер и проверка наличия продукта при незаполненном CTO, кластере и HRGate')
    @allure.issue('https://jira.mts.ru/browse/PPI-1692', 'PPInfo - Доработать отчет "Проверка кластера"')
    def test_get_cluster_check_exist(self, rest_internal_client):
        with open('cluster.xlsx', 'wb') as f:
            f.write(self.get_excel_cluster(rest_internal_client))

        df = pd.read_excel('cluster.xlsx')

        with allure.step('Проверяем, что если не заполнены столбцы CTO, кластер и HRGate продукт есть в excel'):
            empty_values = [df['Код BI_'][ind] for ind in range(len(df['Код BI_'])) if
                            pd.isna(df['Кластер'][ind]) and pd.isna(df['Chief Technology Officer'][ind]) and pd.isna(
                                df['Кластер в HRGate'][ind])]
            assert empty_values, f'В Excel Проверка кластера нет строк с 3 пустыми атрибутами'

        os.remove('cluster.xlsx')

    @allure.title('Получение икселя Кластер и проверка условия на наличие продуктов')
    @allure.issue('https://jira.mts.ru/browse/PPI-1692', 'PPInfo - Доработать отчет "Проверка кластера"')
    def test_get_cluster_check_products(self, rest_internal_client):
        with open('cluster.xlsx', 'wb') as f:
            f.write(self.get_excel_cluster(rest_internal_client))

        df = pd.read_excel('cluster.xlsx')

        with allure.step('Проверяем, что в excel нет удаленных продуктов'):
            assert 'BI_2072' not in df['Код BI_'].values, 'Удаленный продукт BI_2072 появился в excel'

        with allure.step('Проверяем, что в excel есть атомарные продукты'):
            assert 'BI_1884' in df['Код BI_'].values, 'В excel не попадают атомарные продукты BI_1884'

        with allure.step('Проверяем, что в excel есть внешние продукты'):
            assert 'BI_60' in df['Код BI_'].values, 'В excel не попадают внешние продукты BI_60'

        with allure.step('Проверяем, что в excel есть внутренние продукты'):
            assert 'BI_1561' in df['Код BI_'].values, 'В excel не попадают атомарные продукты BI_1561'

        os.remove('cluster.xlsx')

    @allure.title('Добавление и удаление публичного/закрытого документа')
    @allure.issue('https://jira.mts.ru/browse/PPI-2034', 'PPInfo - Убрать ограничения по форматам файлов')
    @pytest.mark.parametrize('access_type', ['public', 'chanelDepended'])
    @pytest.mark.parametrize('file_format',
                             ['.xlsx', '.xls', '.doc', '.docx', '.ppt', '.pptx', '.txt', '.pdf', '.3gp', '.avi', '.mov',
                              '.mp4',
                              '.mp3', '.mkv', '.wav', '.jpg', '.jpeg', '.svg', '.png', '.zip', '.rar', '.gif', '.msg',
                              '.exe', '.rtf'])
    def test_add_and_delete_doc(self, rest_internal_client, access_type, file_format):
        data = {
            'name': 'filename_test_' + file_format[1:] + f"{access_type}",
            'description': file_format,
            'type': 'document',
            'accessType': access_type
        }
        self.delete_doc(rest_internal_client, self.add_doc(rest_internal_client, data, file_format))

    @allure.title('Добавление и удаление публичной/закрытой ссылки')
    @pytest.mark.parametrize('access_type', ['public', 'chanelDepended'])
    def test_add_and_delete_link(self, rest_internal_client, access_type):
        data = {
            'name': 'linkname_test_' + f'_{access_type}',
            'description': "linktest",
            'type': 'link',
            'link': 'https://stage.prodboard.mts.ru/product/BI_2687/docs',
            'accessType': access_type
        }
        self.delete_doc(rest_internal_client, self.add_link(rest_internal_client, data))

    @allure.title('Добавление и удаление логотипа')
    def test_add_and_delete_logo(self, ppinfo_client, rest_internal_client):
        data = {
            'name': 'logotest',
            'description': 'logotest',
            'type': 'logo',
            'accessType': 'public'
        }
        self.add_logo(rest_internal_client, data)

        self.delete_logo(ppinfo_client)  # из ProductV1, через удаление доков не работает

    @allure.title('Документы отсортированы по дате')
    @allure.issue('https://jira.mts.ru/browse/PPI-3159', 'PPInfo - Порядок расположения документов в разделе Документы')
    def test_docs_sorted(self, rest_internal_client):
        docs = self.get_docs_by_bi_code(rest_internal_client, 'BI_60')
        dates = [doc['createdAt'] for doc in docs['documents']]

        assert dates == sorted(dates, key=lambda x: datetime.strptime(x, '%Y-%m-%dT%H:%M:%SZ'),
                               reverse=True), 'Документы отсортированы не по дате'

    @allure.title('Получение атомарных продуктов')
    def test_get_atomic(self, rest_internal_client):
        with allure.step('Проверяем, что список атомарных продуктов не пустой'):
            assert self.get_atomic_by_code(rest_internal_client, 'BI_60'), 'У продукта не найдено атомарных'

    @allure.title('Получение атомарных продуктов у продукта без атомарных')
    def test_get_atomic_no(self, rest_internal_client):
        with allure.step('Проверяем, что список атомарных продуктов пустой'):
            assert not self.get_atomic_by_code(rest_internal_client, 'BI_42')[
                'categories'], f"Атомарные продукты: {self.get_atomic_by_code(rest_internal_client, 'BI_42')}"

    @allure.title('Кол-во Моих продуктов')
    @allure.issue('https://jira.mts.ru/browse/PPI-4050', 'PPInfo - Отображение на странице "Мои продукты"')
    def test_get_owned_count(self, rest_internal_client):

        owned_count = len(self.get_owned_products(rest_internal_client)['ownedProducts'])

        assert owned_count >= 50, f"Кол-во Моих продуктов меньше 50, фактическое кол-во Моих продуктов равно {owned_count}"

    @allure.title('Кол-во Моих продуктов')
    @allure.issue('https://jira.mts.ru/browse/PPI-4050', 'PPInfo - Отображение на странице "Мои продукты"')
    @pytest.mark.parametrize('employee',
                             ['employee_sponsor', 'employee_business_owner', 'employee_chief_PO', 'employee_tech_lead'])
    def test_get_owned_add_product(self, rest_internal_client, ppinfo_client, employee):

        owned_count = len(self.get_owned_products(rest_internal_client)['ownedProducts'])
        data = self.get_data_for_product_creation(product_type='Vneshnii')
        data['attributes'].append({
            'id': employee,
            'values': [
                {
                    'code': "ddsvetov1",
                    'value': "Светов Даниил Дмитриевич (ddsvetov1)"
                }
            ]
        })
        self.create_product(ppinfo_client, data)
        new_owned_count = len(self.get_owned_products(rest_internal_client)['ownedProducts'])

        assert new_owned_count == owned_count + 1, f"Кол-во Моих продуктов не изменилось после создания продукта. Фактическое кол-во Моих продуктов равно {new_owned_count}"

    @allure.title('Сортировка в Моих продуктах')
    @allure.issue('https://jira.mts.ru/browse/PPI-4204', 'PPInfo - "Мои продукты" в Архиве')
    def test_get_owned_sorted(self, rest_internal_client):

        owned = self.get_owned_products(rest_internal_client)['ownedProducts']
        products = []

        for product in owned:
            name = product["name"]
            status = product["properties"]['PPinfo_status'].get("code", "None")
            isInitClose = product["properties"].get("isInitClose", False)
            isDeleted = product["properties"].get("isDeleted", False)
            products.append((name, status, isInitClose, isDeleted))

        sorted_products = sorted(
            products,
            key=lambda x: (
                x[3],  # Сначала не удаленные (False), потом удаленные (True)
                x[1] == "Arkhiv" if not x[3] else 0,  # Для не удаленных: сначала не архив
                x[2] if not x[3] and x[1] != "Arkhiv" else 0,  # Для не удаленных и не архивных: isInitClose
                x[0]  # Сортировка по имени
            )
        )

        assert products == sorted_products, "Сортировка на странице Моих продуктов некорректная"


    @allure.title(
        'У продукта отображен корректный PQI')  # Так как нет возможности дебажить запрос к QWEB не из корп сети пока используем костыль в виде захардкоженых данных
    def test_health_pqi(self, rest_internal_client):

        health = self.get_product_health(rest_internal_client, 'BI_60')

        for i in health:
            if i['code'] == 'pqi':
                assert i['name'] == 'PQI - показатель качества', 'Некорректный заголовок'
                assert i['link'] == 'https://qweb.mts.ru/product_dashboard/products/?product=BI_60&agg=quarter'
                assert i['cells'][0]['name'] == '2Q 2025'
                assert i['cells'][0]['value'] == '96%'
                assert i['cells'][0]['color'] == 'green'
                assert i['cells'][0][
                           'valueHint'] == "Значение соответствует целевому уровню.<br><a class=\"tooltipHealthLink\" target=\"_blank\" href=\"https://confluence.mts.ru/x/NVJTQ\">Согласно утверждённой методологии</a> целевое значение для всех проудктов 95%."
                assert i['cells'][1]['name'] == '3Q 2025'
                assert i['cells'][1]['value'] == '98%'
                assert i['cells'][1]['color'] == 'green'
                assert i['cells'][1][
                           'valueHint'] == "Значение соответствует целевому уровню.<br><a class=\"tooltipHealthLink\" target=\"_blank\" href=\"https://confluence.mts.ru/x/NVJTQ\">Согласно утверждённой методологии</a> целевое значение для всех проудктов 95%."


#### Историчность
@pytest.mark.last
@pytest.mark.api
@allure.label('priority', 'Высокий')
@allure.feature('Историчность продуктов')
@allure.link('https://jira.mts.ru/browse/PPI-3338', 'task', 'PPInfo - Выгрузка истории изменений атрибутов в Excel')
@pytest.mark.usefixtures('clear_excel')
class TestStory(Story):

    @allure.title('Проверка корректности столбцов в икселе историчности')
    def test_story_correct_columns(self, rest_internal_client):
        excel = self.get_story_excel_by_product(rest_internal_client, 'BI_60')
        column_names = [cell.value for cell in excel[1]]

        assert column_names == ['Код', 'Дата и время изменения', 'Название атрибута', 'Предыдущее значение',
                                'Текущие значение', 'ФИО (логин) Инициатора изменения', 'E-mail Инициатора изменения',
                                'ФИО (логин) Модератора',
                                'E-mail Модератора'], f'Столбцы в икселе не соответствуют ожидаемым, фактический набор столбцов - {column_names}'

    @allure.title('Получение историчности для отображения в UI')
    def test_story_get_for_ui(self, rest_internal_client):
        self.get_story_for_ui_by_product(rest_internal_client, 'BI_60')

    @allure.title('Изменение строки в продукте и проверка отображения записей в историчности')
    @pytest.mark.parametrize('role', ['admin', 'user'])
    def test_story_string(self, ppinfo_client, ppinfo_user_client, rest_internal_client, role):
        if role == 'admin':
            excel = self.create_and_replace_product_admin(rest_internal_client, ppinfo_client, self.get_moves['string'])
        else:
            excel = self.create_and_replace_product_user(rest_internal_client, ppinfo_client, ppinfo_user_client,
                                                         self.get_moves['string'])

        assert excel.cell(row=4, column=4).value == '' and excel.cell(row=4,
                                                                      column=5).value == 'test', 'Запись на добавление строку не записалось'
        assert excel.cell(row=3, column=4).value == 'test' and excel.cell(row=3,
                                                                          column=5).value == 'test2', 'Запись на добавление строку не записалось'
        assert excel.cell(row=2, column=4).value == 'test2' and excel.cell(row=2,
                                                                           column=5).value == '', 'Запись на добавление строку не записалось'

    @allure.title('Изменение строки в продукте и проверка отображения записей в историчности для отображения на фронте')
    @pytest.mark.parametrize('role', ['admin', 'user'])
    def test_story_for_ui_string(self, rest_internal_client, ppinfo_client, ppinfo_user_client, role):
        if role == 'admin':
            story = self.create_and_replace_product_admin(rest_internal_client, ppinfo_client, self.get_moves['string'],
                                                          for_ui=True)
        else:
            story = self.create_and_replace_product_user(rest_internal_client, ppinfo_client, ppinfo_user_client,
                                                         self.get_moves['string'],
                                                         for_ui=True)

        assert story[0]['currentValues'] == [], 'Запись на очистку строки не произошла'

        assert story[1]['currentValues'] == ['test2'], 'Запись на изменение строки не произошла'

        assert story[2]['currentValues'] == ['test'], 'Запись на добавление строки не произошла'

    @allure.title('Изменение мэниселекта в продукте и проверка отображения записей в историчности')
    @pytest.mark.parametrize('role', ['admin', 'user'])
    def test_story_manyselect(self, rest_internal_client, ppinfo_client, ppinfo_user_client, role):
        if role == 'admin':
            excel = self.create_and_replace_product_admin(rest_internal_client, ppinfo_client,
                                                          self.get_moves['many_select'])
        else:
            excel = self.create_and_replace_product_user(rest_internal_client, ppinfo_client, ppinfo_user_client,
                                                         self.get_moves['many_select'])

        assert excel.cell(row=4, column=4).value == '' and excel.cell(row=4,
                                                                      column=5).value == 'Основной', 'Запись на добавление мэниселекта не записалось'
        assert excel.cell(row=3, column=4).value == 'Основной' and excel.cell(row=3,
                                                                              column=5).value == 'Атомарный', 'Запись на изменение мэниселекта не записалось'
        assert excel.cell(row=2, column=4).value == 'Атомарный' and excel.cell(row=2,
                                                                               column=5).value == '', 'Запись на очищение мэниселекта не записалось'

    @allure.title('Изменение мэниселекта в продукте и проверка отображения записей в историчности на фронте')
    @pytest.mark.parametrize('role', ['admin', 'user'])
    def test_story_for_ui_manyselect(self, rest_internal_client, ppinfo_client, ppinfo_user_client, role):
        if role == 'admin':
            story = self.create_and_replace_product_admin(rest_internal_client, ppinfo_client,
                                                          self.get_moves['many_select'],
                                                          for_ui=True)
        else:
            story = self.create_and_replace_product_user(rest_internal_client, ppinfo_client, ppinfo_user_client,
                                                         self.get_moves['many_select'],
                                                         for_ui=True)

        assert story[0]['currentValues'] == [], 'Запись на очищение мэниселекта не записалось'

        assert story[1]['currentValues'] == ['Атомарный'], 'Запись на изменение мэниселекта не записалось'

        assert story[2]['currentValues'] == ['Основной'], 'Запись на добавление мэниселекта не записалось'

    @allure.title('Изменение даты в продукте и проверка отображения записей в историчности')
    @pytest.mark.parametrize('role', ['admin', 'user'])
    def test_story_date(self, rest_internal_client, ppinfo_client, ppinfo_user_client, role):
        if role == 'admin':
            excel = self.create_and_replace_product_admin(rest_internal_client, ppinfo_client, self.get_moves['date'])
        else:
            excel = self.create_and_replace_product_user(rest_internal_client, ppinfo_client, ppinfo_user_client,
                                                         self.get_moves['date'])

        assert excel.cell(row=4, column=4).value == '' and excel.cell(row=4,
                                                                      column=5).value == '23.01.2024 03:00', 'Запись на добавление даты не записалось'
        assert excel.cell(row=3, column=4).value == '23.01.2024 03:00' and excel.cell(row=3,
                                                                                      column=5).value == '24.01.2024 03:00', 'Запись на изменение даты не записалось'
        assert excel.cell(row=2, column=4).value == '24.01.2024 03:00' and excel.cell(row=2,
                                                                                      column=5).value == '', 'Запись на очищение даты не записалось'

    @allure.title('Изменение даты в продукте и проверка отображения записей в историчности на фронте')
    @pytest.mark.parametrize('role', ['admin', 'user'])
    def test_story_for_ui_date(self, rest_internal_client, ppinfo_client, ppinfo_user_client, role):
        if role == 'admin':
            story = self.create_and_replace_product_admin(rest_internal_client, ppinfo_client, self.get_moves['date'],
                                                          for_ui=True)
        else:
            story = self.create_and_replace_product_user(rest_internal_client, ppinfo_client, ppinfo_user_client,
                                                         self.get_moves['date'],
                                                         for_ui=True)

        assert story[0]['currentValues'] == [], 'Запись на очищение даты не записалось'

        assert story[1]['currentValues'] == ['2024-01-24T03:00:00Z'], 'Запись на изменение даты не записалось'

        assert story[2]['currentValues'] == ['2024-01-23T03:00:00Z'], 'Запись на добавление даты не записалось'

    @allure.title('Изменение числа в продукте и проверка отображения записей в историчности')
    @pytest.mark.parametrize('role', ['admin', 'user'])
    def test_story_num(self, rest_internal_client, ppinfo_client, ppinfo_user_client, role):
        if role == 'admin':
            excel = self.create_and_replace_product_admin(rest_internal_client, ppinfo_client, self.get_moves['num'])
        else:
            excel = self.create_and_replace_product_user(rest_internal_client, ppinfo_client, ppinfo_user_client,
                                                         self.get_moves['num'])

        assert excel.cell(row=4, column=4).value == '' and excel.cell(row=4,
                                                                      column=5).value == '666', 'Запись на добавление числа не записалось'
        assert excel.cell(row=3, column=4).value == '666' and excel.cell(row=3,
                                                                         column=5).value == '777', 'Запись на изменение числа не записалось'
        assert excel.cell(row=2, column=4).value == '777' and excel.cell(row=2,
                                                                         column=5).value == '', 'Запись на очищение числа не записалось'

    @allure.title('Изменение числа в продукте и проверка отображения записей в историчности на фронте')
    @pytest.mark.parametrize('role', ['admin', 'user'])
    def test_story_for_ui_num(self, rest_internal_client, ppinfo_client, ppinfo_user_client, role):
        if role == 'admin':
            story = self.create_and_replace_product_admin(rest_internal_client, ppinfo_client, self.get_moves['num'],
                                                          for_ui=True)
        else:
            story = self.create_and_replace_product_user(rest_internal_client, ppinfo_client, ppinfo_user_client,
                                                         self.get_moves['num'],
                                                         for_ui=True)

        assert story[0]['currentValues'] == [], 'Запись на очищение числа не записалось'

        assert story[1]['currentValues'] == ['777'], 'Запись на изменение числа не записалось'

        assert story[2]['currentValues'] == ['666'], 'Запись на добавление числа не записалось'

    @allure.title('Изменение юзера в продукте и проверка отображения записей в историчности')
    @pytest.mark.parametrize('role', ['admin', 'user'])
    def test_story_user(self, rest_internal_client, ppinfo_client, ppinfo_user_client, role):
        if role == 'admin':
            excel = self.create_and_replace_product_admin(rest_internal_client, ppinfo_client, self.get_moves['user'])
        else:
            excel = self.create_and_replace_product_user(rest_internal_client, ppinfo_client, ppinfo_user_client,
                                                         self.get_moves['user'])

        assert excel.cell(row=4, column=4).value == '' and excel.cell(row=4,
                                                                      column=5).value == 'Светов Даниил Дмитриевич (ddsvetov1)', 'Запись на добавление юзера не записалось'
        assert excel.cell(row=3, column=4).value == 'Светов Даниил Дмитриевич (ddsvetov1)' and excel.cell(row=3,
                                                                                                           column=5).value == 'Гладышева Алёна Ивановна (aigladyshev)', 'Запись на изменение юзера не записалось'
        assert excel.cell(row=2, column=4).value == 'Гладышева Алёна Ивановна (aigladyshev)' and excel.cell(row=2,
                                                                                                       column=5).value == '', 'Запись на очищение юзера не записалось'

    @allure.title('Изменение Юзера в продукте и проверка отображения записей в историчности на фронте')
    @pytest.mark.parametrize('role', ['admin', 'user'])
    def test_story_for_ui_user(self, rest_internal_client, ppinfo_client, ppinfo_user_client, role):
        if role == 'admin':
            story = self.create_and_replace_product_admin(rest_internal_client, ppinfo_client, self.get_moves['user'],
                                                          for_ui=True)
        else:
            story = self.create_and_replace_product_user(rest_internal_client, ppinfo_client, ppinfo_user_client,
                                                         self.get_moves['user'],
                                                         for_ui=True)

        assert story[0]['currentValues'] == [], 'Запись на очищение юзера не записалось'

        assert story[1]['currentValues'] == [
            'Гладышева Алёна Ивановна (aigladyshev)'], 'Запись на изменение юзера не записалось'

        assert story[2]['currentValues'] == [
            'Светов Даниил Дмитриевич (ddsvetov1)'], 'Запись на добавление юзера не записалось'

    @allure.title('Изменение множества в продукте и проверка отображения записей в историчности')
    @pytest.mark.parametrize('role', ['admin', 'user'])
    def test_story_multi(self, rest_internal_client, ppinfo_client, ppinfo_user_client, role):
        if role == 'admin':
            excel = self.create_and_replace_product_admin(rest_internal_client, ppinfo_client, self.get_moves['multi'])
        else:
            excel = self.create_and_replace_product_user(rest_internal_client, ppinfo_client, ppinfo_user_client,
                                                         self.get_moves['multi'])

        assert excel.cell(row=4, column=4).value == '' and excel.cell(row=4,
                                                                      column=5).value == 'Второй,Первый,Третий', 'Запись на добавление множества не записалось'
        assert excel.cell(row=3, column=4).value == 'Второй,Первый,Третий' and excel.cell(row=3,
                                                                                          column=5).value == 'Второй', 'Запись на изменение множества не записалось'
        assert excel.cell(row=2, column=4).value == 'Второй' and excel.cell(row=2,
                                                                            column=5).value == '', 'Запись на очищение множества не записалось'

    @allure.title('Изменение множества в продукте и проверка отображения записей в историчности на фронте')
    @pytest.mark.parametrize('role', ['admin', 'user'])
    def test_story_for_ui_multi(self, rest_internal_client, ppinfo_client, ppinfo_user_client, role):
        if role == 'admin':
            story = self.create_and_replace_product_admin(rest_internal_client, ppinfo_client, self.get_moves['multi'],
                                                          for_ui=True)
        else:
            story = self.create_and_replace_product_user(rest_internal_client, ppinfo_client, ppinfo_user_client,
                                                         self.get_moves['multi'],
                                                         for_ui=True)

        assert story[0]['currentValues'] == [], 'Запись на очищение множества не записалось'

        assert story[1]['currentValues'] == ['Второй'], 'Запись на изменение множества не записалось'

        assert story[2]['currentValues'] == ['Второй', 'Первый', 'Третий'], 'Запись на добавление множества не записалось'

    @allure.title('Изменение многострочного текста в продукте и проверка отображения записей в историчности')
    @pytest.mark.parametrize('role', ['admin', 'user'])
    def test_story_multistring(self, rest_internal_client, ppinfo_client, ppinfo_user_client, role):
        if role == 'admin':
            excel = self.create_and_replace_product_admin(rest_internal_client, ppinfo_client,
                                                          self.get_moves['multistring'])
        else:
            excel = self.create_and_replace_product_user(rest_internal_client, ppinfo_client, ppinfo_user_client,
                                                         self.get_moves['multistring'])

        assert excel.cell(row=4, column=4).value == '' and excel.cell(row=4,
                                                                      column=5).value == 'test', 'Запись на добавление многострочного текста не записалось'
        assert excel.cell(row=3, column=4).value == 'test' and excel.cell(row=3,
                                                                          column=5).value == 'test2', 'Запись на изменение многострочного текста не записалось'
        assert excel.cell(row=2, column=4).value == 'test2' and excel.cell(row=2,
                                                                           column=5).value == '', 'Запись на очищение многострочного текста не записалось'

    @allure.title('Изменение многострочного текста в продукте и проверка отображения записей в историчности на фронте')
    @pytest.mark.parametrize('role', ['admin', 'user'])
    def test_story_for_ui_multistring(self, rest_internal_client, ppinfo_client, ppinfo_user_client, role):
        if role == 'admin':
            story = self.create_and_replace_product_admin(rest_internal_client, ppinfo_client,
                                                          self.get_moves['multistring'],
                                                          for_ui=True)
        else:
            story = self.create_and_replace_product_user(rest_internal_client, ppinfo_client, ppinfo_user_client,
                                                         self.get_moves['multistring'],
                                                         for_ui=True)

        assert story[0]['currentValues'] == [], 'Запись на очищение многострочного текста не записалось'

        assert story[1]['currentValues'] == ['test2'], 'Запись на изменение многострочного текста не записалось'

        assert story[2]['currentValues'] == ['test'], 'Запись на добавление многострочного текста не записалось'

    @allure.title('Изменение ссылки в продукте и проверка отображения записей в историчности')
    @pytest.mark.parametrize('role', ['admin', 'user'])
    def test_story_link(self, rest_internal_client, ppinfo_client, ppinfo_user_client, role):
        if role == 'admin':
            excel = self.create_and_replace_product_admin(rest_internal_client, ppinfo_client, self.get_moves['link'])
        else:
            excel = self.create_and_replace_product_user(rest_internal_client, ppinfo_client, ppinfo_user_client,
                                                         self.get_moves['link'])

        assert excel.cell(row=4, column=4).value == '' and excel.cell(row=4,
                                                                      column=5).value == 'https://cashback.mts.ru', 'Запись на добавление ссылки не записалось'
        assert excel.cell(row=3, column=4).value == 'https://cashback.mts.ru' and excel.cell(row=3,
                                                                                             column=5).value == 'https://stage.prodboard.mts.ru/product/BI_42/main', 'Запись на изменение ссылки не записалось'
        assert excel.cell(row=2, column=4).value == 'https://stage.prodboard.mts.ru/product/BI_42/main' and excel.cell(
            row=2,
            column=5).value == '', 'Запись на очищение ссылки не записалось'

    @allure.title('Изменение ссылки в продукте и проверка отображения записей в историчности на фронте')
    @pytest.mark.parametrize('role', ['admin', 'user'])
    def test_story_for_ui_link(self, rest_internal_client, ppinfo_client, ppinfo_user_client, role):
        if role == 'admin':
            story = self.create_and_replace_product_admin(rest_internal_client, ppinfo_client, self.get_moves['link'],
                                                          for_ui=True)
        else:
            story = self.create_and_replace_product_user(rest_internal_client, ppinfo_client, ppinfo_user_client,
                                                         self.get_moves['link'],
                                                         for_ui=True)

        assert story[0]['currentValues'] == [], 'Запись на очищение ссылки не записалось'

        assert story[1]['currentValues'] == [
            'https://stage.prodboard.mts.ru/product/BI_42/main'], 'Запись на изменение ссылки не записалось'

        assert story[2]['currentValues'] == ['https://cashback.mts.ru'], 'Запись на добавление ссылки не записалось'

    @allure.title('Изменение по куратором попадает в историчность продукта')
    @allure.issue('https://jira.mts.ru/browse/PPI-3455', 'PPInfo - История изменений (кураторы)')
    @pytest.mark.parametrize('curators', (['pymaslenkov', 'ddsvetov1'], ['aikostrov', 'sayariko']))
    def test_story_for_ui_curators(self, rest_internal_client, ppinfo_client, ppinfo_user_client, curators):

        self.change_curators(rest_internal_client, curators,
                             attribute_id='04e8b2af-ebbc-40b6-b6cb-2f86863f36af',
                             value_id='373280ee-225d-4ddc-844d-e575cb45436a')

        current_values = self.get_story_for_ui_by_product(rest_internal_client, 'BI_2062')[0]['currentValues']

        only_logins = [user.split(' (')[1].rstrip(')') for user in current_values]

        assert curators == only_logins, 'Изменение кураторов не отобразилось в историчности'

    @allure.title('Изменение основного продукта в продукте и проверка отображения записей в историчности')
    @pytest.mark.parametrize('role', ['admin'])
    def test_story_main_product(self, rest_internal_client, ppinfo_client, ppinfo_user_client, role):
        if role == 'admin':
            excel = self.create_and_replace_product_admin(rest_internal_client, ppinfo_client,
                                                          self.get_moves['main_product'])
        else:
            excel = self.create_and_replace_product_user(rest_internal_client, ppinfo_client, ppinfo_user_client,
                                                         self.get_moves['main_product'])

        assert excel.cell(row=6, column=4).value == '' and excel.cell(row=6,
                                                                      column=5).value == '1_Не трогать, для АТ, делегирование del', 'Запись на добавление основного продукта не записалось'
        assert excel.cell(row=4, column=4).value == '1_Не трогать, для АТ, делегирование del' and excel.cell(
            row=4,
            column=5).value == 'Не трогать (продукт для автотестов)', 'Запись на изменение основного продукта не записалось'
        assert excel.cell(row=3, column=4).value == 'Не трогать (продукт для автотестов)' and excel.cell(
            row=3, column=5).value == '', 'Запись на очищение основного продукта не записалось'

        assert excel.cell(row=2, column=4).value == 'Атомарный' and excel.cell(
            row=2,
            column=5).value == 'Основной', 'Запись на изменение основного продукта не записалось'
        assert excel.cell(row=5, column=4).value == 'Основной' and excel.cell(
            row=5, column=5).value == 'Атомарный', 'Запись на очищение основного продукта не записалось'

    @allure.title('Изменение ссылки в продукте и проверка отображения записей в историчности на фронте')
    def test_story_for_ui_main_product(self, rest_internal_client, ppinfo_client, ppinfo_user_client):
        story = self.create_and_replace_product_admin(rest_internal_client, ppinfo_client,
                                                      self.get_moves['main_product'],
                                                      for_ui=True)

        assert story[0]['currentValues'] == ['Основной'], 'Запись на изменение с Атомарного на Основной не произошла'

        assert story[1]['currentValues'] == [], 'Запись на очистку основного продукта не произошла'

        assert story[2]['currentValues'] == [
            'Не трогать (продукт для автотестов) ' '(https://stage.prodboard.mts.ru/product/3266/main)'], 'Запись на добавление основного продукта не произошла'

    @allure.title('Изменение двух атрибутов в продукте и проверка отображения записей в историчности')
    @pytest.mark.parametrize('role', ['admin', 'user'])
    def test_story_two_attributes(self, rest_internal_client, ppinfo_client, ppinfo_user_client, role):
        if role == 'admin':
            excel = self.create_and_replace_product_admin(rest_internal_client, ppinfo_client,
                                                          ['string_add', 'user_add'])
        else:
            excel = self.create_and_replace_product_user(rest_internal_client, ppinfo_client, ppinfo_user_client,
                                                         ['string_add', 'user_add'])

        assert [excel['C2'].value, excel['C3'].value] == ['Business owner',
                                                          'Витрина'], 'Изменяение двух атриюутов не записались'

    @allure.title('Изменение двух атрибутов в продукте и проверка отображения записей в историчности на фронте')
    @pytest.mark.parametrize('role', ['admin', 'user'])
    def test_story_for_ui_two_attributes(self, rest_internal_client, ppinfo_client, ppinfo_user_client, role):
        if role == 'admin':
            story = self.create_and_replace_product_admin(rest_internal_client, ppinfo_client,
                                                          ['string_add', 'user_add'],
                                                          for_ui=True)
        else:
            story = self.create_and_replace_product_user(rest_internal_client, ppinfo_client, ppinfo_user_client,
                                                         ['string_add', 'user_add'],
                                                         for_ui=True)

        assert story[0]['currentValues'] == ['Светов Даниил Дмитриевич (ddsvetov1)'] and story[1]['currentValues'] == [
            'test'], 'Запись на изменение двух атрибутов не произошла'

    @allure.title(
        'Корректность отображения инициатора и модератора в икселе историчности при изменений сделанных админом')
    def test_users_in_excel_admin(self, ppinfo_client, rest_internal_client):
        excel = self.create_and_replace_product_admin(rest_internal_client, ppinfo_client, ['string_add'])

        assert self.get_initiator_from_excel(excel, 2) == (
            'Светов Даниил Дмитриевич (ddsvetov1)', 'ddsvetov1@mts.ru'), 'Указан некоторый инициатор'
        assert self.get_moderator_from_excel(excel, 2) == (
            'Светов Даниил Дмитриевич (ddsvetov1)', 'ddsvetov1@mts.ru'), 'Указан некоторый модератор'

    @allure.title(
        'Корректность отображения инициатора и модератора в UI историчности при изменений сделанных админом')
    def test_users_for_ui_admin(self, ppinfo_client, rest_internal_client):
        story = self.create_and_replace_product_admin(rest_internal_client, ppinfo_client, ['string_add'], for_ui=True)

        assert (story[0]['initiator'] == {'fullName': 'Светов Даниил Дмитриевич', 'login': 'ddsvetov1'}
                and story[0]['moderator'] == {'fullName': 'Светов Даниил Дмитриевич', 'login': 'ddsvetov1'}), \
            'Неверный инициатор или модератор'

    @allure.title(
        'Корректность отображения инициатора и модератора в икселе историчности при изменений сделанных пользователем')
    def test_users_in_excel_user(self, rest_internal_client, ppinfo_client, ppinfo_user_client, ):
        excel = self.create_and_replace_product_user(rest_internal_client, ppinfo_client, ppinfo_user_client,
                                                     ['string_add'])

        assert self.get_initiator_from_excel(excel, 2) == (
            'Костров Алексей Игоревич (aikostrov1)', 'aikostrov1@mts.ru'), 'Указан некоторый инициатор'
        assert self.get_moderator_from_excel(excel, 2) == (
            'Светов Даниил Дмитриевич (ddsvetov1)', 'ddsvetov1@mts.ru'), 'Указан некоторый модератор'

    @allure.title(
        'Корректность отображения инициатора и модератора в UI историчности при изменений сделанных пользователем')
    def test_users_for_ui_user(self, rest_internal_client, ppinfo_client, ppinfo_user_client, ):
        story = self.create_and_replace_product_user(rest_internal_client, ppinfo_client, ppinfo_user_client,
                                                     ['string_add'], for_ui=True)

        assert story[0]['initiator'] == {'fullName': 'Костров Алексей Игоревич', 'login': 'aikostrov1'} and story[0][
            'moderator'] == {'fullName': 'Светов Даниил Дмитриевич',
                             'login': 'ddsvetov1'}, 'Неверный инициатор или модератор'

    @allure.title('Выгрузка на две даты всех атрибутов')
    def test_get_story_by_two_dates_all_attributes(self, rest_internal_client):

        excel = self.get_story_excel_by_product(rest_internal_client, 'BI_60', is_date_from=True)
        assert excel.max_row > 50, f'Количество строк в Excel файле меньше 50, фактическое количество строк - {excel.max_row}'

    @allure.title('Выгрузка на две даты всех атрибутов для фронта')
    def test_get_story_by_two_dates_all_attributes_for_ui(self, rest_internal_client):

        story = self.get_story_for_ui_by_product(rest_internal_client, 'BI_60', is_date_from=True)
        assert len(story) > 50, f'Количество элементов в списке {len(story)}'

    @allure.title('Выгрузка на две даты')
    def test_get_story_by_two_dates(self, rest_internal_client):

        excel = self.get_story_excel_by_product(rest_internal_client, 'BI_60',
                                                attributes_list=['EXTRA_OldProductName', 'SYSTEM_Delay'],
                                                is_date_from=True)
        assert excel.max_row > 10, f'Количество строк в Excel файле меньше 10, фактическое количество строк - {excel.max_row}'

    @allure.title('Выгрузка на две даты для фронта')
    def test_get_story_by_two_dates_for_ui(self, rest_internal_client):

        story = self.get_story_for_ui_by_product(rest_internal_client, 'BI_60',
                                                 attributes_list=['EXTRA_OldProductName', 'SYSTEM_Delay'],
                                                 is_date_from=True)
        assert len(story) > 10, f'Количество элементов в списке {len(story)}'

    @allure.title(
        'Изменение значения через автомодерацию')
    def test_users_in_excel_user_auto_moderation(self, rest_internal_client, ppinfo_client, ppinfo_user_client, ):
        excel = self.create_and_replace_product_user(rest_internal_client, ppinfo_client, ppinfo_user_client,
                                                     self.get_moves['string'],
                                                     auto_moderation=True)

        assert excel.cell(row=4, column=4).value == '' and excel.cell(row=4,
                                                                      column=5).value == 'test', 'Запись на добавление строку не записалось'
        assert excel.cell(row=3, column=4).value == 'test' and excel.cell(row=3,
                                                                          column=5).value == 'test2', 'Запись на добавление строку не записалось'
        assert excel.cell(row=2, column=4).value == 'test2' and excel.cell(row=2,
                                                                           column=5).value == '', 'Запись на добавление строку не записалось'

    @allure.title(
        'Изменение значения через автомодерацию для фронта')
    def test_users_auto_moderation_for_ui(self, rest_internal_client, ppinfo_client, ppinfo_user_client, ):
        story = self.create_and_replace_product_user(rest_internal_client, ppinfo_client, ppinfo_user_client,
                                                     self.get_moves['string'],
                                                     auto_moderation=True, for_ui=True)

        assert story[0]['currentValues'] == [], 'Запись на очистку строки не произошла'

        assert story[1]['currentValues'] == ['test2'], 'Запись на изменение строки не произошла'

        assert story[2]['currentValues'] == ['test'], 'Запись на добавление строки не произошла'

    @allure.title(
        'Корректность отображения инициатора и модератора в икселе историчности при изменений сделаных пользователем')
    def test_users_in_excel_auto_moderation(self, rest_internal_client, ppinfo_client, ppinfo_user_client, ):
        excel = self.create_and_replace_product_user(rest_internal_client, ppinfo_client, ppinfo_user_client,
                                                     ['string_add', 'string_replace', 'string_remove'],
                                                     auto_moderation=True)

        assert self.get_initiator_from_excel(excel, 2) == (
            'Светов Даниил Дмитриевич (ddsvetov1)', 'ddsvetov1@mts.ru'), 'Указан некоторый инициатор'
        assert self.get_moderator_from_excel(excel, 2) == (
            'Светов Даниил Дмитриевич (ddsvetov1)', 'ddsvetov1@mts.ru'), 'Указан некоторый модератор'

    @allure.title(
        'Корректность отображения инициатора и модератора в UI историчности при изменений сделаных пользователем с автомодерацией')
    def test_users_auto_moderation_for_ui_moderator_and_initiator(self, rest_internal_client, ppinfo_client,
                                                                  ppinfo_user_client, ):
        story = self.create_and_replace_product_user(rest_internal_client, ppinfo_client, ppinfo_user_client,
                                                     ['string_add', 'string_replace', 'string_remove'],
                                                     auto_moderation=True, for_ui=True)

        assert story[0]['initiator'] == {'fullName': 'Светов Даниил Дмитриевич', 'login': 'ddsvetov1'} and story[0][
            'moderator'] == {'fullName': 'Светов Даниил Дмитриевич',
                             'login': 'ddsvetov1'}, 'Неверный инициатор или модератора'

    @allure.title('В фильтрах историчности приходят атрибуты согласно ролевой модели пользователь')
    @allure.issue('https://jira.mts.ru/browse/PPI-4327',
                  'PPInfo - Журнал изменений: отображение истории только по атрибутам, доступным пользователям')
    def test_attributes_in_filters_by_role(self, rest_internal_user2_client, ppinfo_client,
                                           ppinfo_user_client, pmd_admin_gw_client):

        self.change_visibility_attribute(pmd_admin_gw_client, False)

        filters_name = []
        filters = self.get_filters_story_for_ui_by_product(rest_internal_user2_client, 'BI_60')
        for f in filters:
            filters_name.append(f['name'])

        assert 'Дата ПК' not in filters_name, 'Фильтр есть, хотя согласно ролевке не должен быть'

        self.change_visibility_attribute(pmd_admin_gw_client, True)

        filters_name = []
        filters = self.get_filters_story_for_ui_by_product(rest_internal_user2_client, 'BI_60')
        for f in filters:
            filters_name.append(f['name'])

        assert 'Дата ПК' in filters_name, 'Фильтра нет, хотя согласно ролевке должен быть'

    @allure.title('В историчности приходят атрибуты согласно ролевой модели пользователь')
    @allure.issue('https://jira.mts.ru/browse/PPI-4327',
                  'PPInfo - Журнал изменений: отображение истории только по атрибутам, доступным пользователям')
    def test_attributes_in_story_by_role(self, rest_internal_user2_client, ppinfo_client,
                                         ppinfo_user_client, pmd_admin_gw_client):

        self.change_visibility_attribute(pmd_admin_gw_client, False)

        attributes_name = []
        attributes = self.get_story_for_ui_by_product(rest_internal_user2_client, 'BI_60')
        for a in attributes:
            attributes_name.append(a['name'])

        assert 'Дата ПК' not in attributes_name, 'Фильтра есть, хотя согласно ролевке не должено быть'

        self.change_visibility_attribute(pmd_admin_gw_client, True)

        filters_name = []
        filters = self.get_story_for_ui_by_product(rest_internal_user2_client, 'BI_60')
        for f in filters:
            filters_name.append(f['name'])

        assert 'Дата ПК' in filters_name, 'Фильтра нет, хотя согласно ролевке должен быть'

    @allure.title('В фильтрах историчности приходят атрибуты согласно ролевой модели ПО')
    @allure.issue('https://jira.mts.ru/browse/PPI-4327',
                  'PPInfo - Журнал изменений: отображение истории только по атрибутам, доступным пользователям')
    def test_attributes_in_filters_by_role_po(self, rest_internal_user2_client, ppinfo_client,
                                              ppinfo_user_client, pmd_admin_gw_client):

        self.change_visibility_attribute(pmd_admin_gw_client, False, role_id='602c3590-989d-4b72-b22d-654ce381bea8',
                                         attribute_id='91eb808e-cebb-432e-869d-5fddc9e55e9b')

        filters_name = []
        filters = self.get_filters_story_for_ui_by_product(rest_internal_user2_client, 'BI_203')
        for f in filters:
            filters_name.append(f['name'])

        assert 'Группа продуктов СТ-137' not in filters_name, 'Фильтр есть, хотя согласно ролевке не должен быть'

        self.change_visibility_attribute(pmd_admin_gw_client, True, role_id='602c3590-989d-4b72-b22d-654ce381bea8',
                                         attribute_id='91eb808e-cebb-432e-869d-5fddc9e55e9b')

        filters_name = []
        filters = self.get_filters_story_for_ui_by_product(rest_internal_user2_client, 'BI_203')
        for f in filters:
            filters_name.append(f['name'])

        assert 'Группа продуктов СТ-137' in filters_name, 'Фильтра нет, хотя согласно ролевке должен быть'

    @allure.title('В историчности приходят атрибуты согласно ролевой модели ПО')
    @allure.issue('https://jira.mts.ru/browse/PPI-4327',
                  'PPInfo - Журнал изменений: отображение истории только по атрибутам, доступным пользователям')
    def test_attributes_in_story_by_role_po(self, rest_internal_user2_client, ppinfo_client,
                                            ppinfo_user_client, pmd_admin_gw_client):

        self.change_visibility_attribute(pmd_admin_gw_client, False, role_id='602c3590-989d-4b72-b22d-654ce381bea8',
                                         attribute_id='91eb808e-cebb-432e-869d-5fddc9e55e9b')

        attributes_name = []
        attributes = self.get_story_for_ui_by_product(rest_internal_user2_client, 'BI_203')
        for a in attributes:
            attributes_name.append(a['name'])

        assert 'Группа продуктов СТ-137' not in attributes_name, 'Фильтра есть, хотя согласно ролевке не должено быть'

        self.change_visibility_attribute(pmd_admin_gw_client, True, role_id='602c3590-989d-4b72-b22d-654ce381bea8',
                                         attribute_id='91eb808e-cebb-432e-869d-5fddc9e55e9b')

        filters_name = []
        filters = self.get_story_for_ui_by_product(rest_internal_user2_client, 'BI_203')
        for f in filters:
            filters_name.append(f['name'])

        assert 'Группа продуктов СТ-137' in filters_name, 'Фильтра нет, хотя согласно ролевке должен быть'


    @allure.title('В историчности приходят атрибуты согласно ролевой модели Контролер Направление бизнеса')
    @allure.issue('https://jira.mts.ru/browse/PPI-4315',
                  'PPInfo - Роль "Контролёр направления бизнеса" (админка)')
    def test_attributes_in_story_by_role_for_business_direction(self, rest_internal_user_client, ppinfo_client, pmd_admin_gw_client):

        self.manage_role_and_user_business_direction_attributes(pmd_admin_gw_client, True)


        attributes_name = []
        attributes = self.get_story_for_ui_by_product(rest_internal_user_client, 'BI_224')
        for a in attributes:
            attributes_name.append(a['name'])

        assert set(self.get_attributes_ids().keys()).issubset(attributes_name), f'{set(self.get_attributes_ids().keys()) - set(attributes_name)} - атрибутов нет в историчности'

        self.manage_role_and_user_business_direction_attributes(pmd_admin_gw_client, False)


        attributes_name = []
        attributes = self.get_story_for_ui_by_product(rest_internal_user_client, 'BI_224')
        for a in attributes:
            attributes_name.append(a['name'])

        assert set(self.get_attributes_ids().keys()).isdisjoint(attributes_name), f'{set(self.get_attributes_ids().keys()) & set(attributes_name)} - атрибутов нет в историчности'



#### ЖИЗНЕННЫЙ ЦИКЛ
# TODO: разобраться с легким стартом, концом финансирования; подумать как сделать все эти тесты для рандомных продуктов
@pytest.mark.last
@pytest.mark.api
@allure.label('priority', 'Высокий')
@allure.feature('Прогрессбар')
@allure.issue('https://jira.mts.ru/browse/PPI-3790', 'PPInfo - Редизайн прогресс-бара')
class TestLifeCycleApi(InternalProduct):

    @allure.title('Проверяем жизненный цикл у 10 рандомных внешних продуктов')
    @pytest.mark.parametrize('product_code',
                             ['BI_60', 'BI_42', 'BI_1361', 'BI_143', 'BI_50', 'BI_23', 'BI_28', 'BI_59', 'BI_131',
                              'BI_261'])
    def test_life_cycle_external_products(self, rest_internal_client, product_code):
        main_l = self.get_life_cycle_fields
        statuses = self.get_life_cycle(rest_internal_client, product_code)['statuses']

        self.check_sorted_subset(main_l, [i['code'] for i in statuses])

        with allure.step('Проверяем, что у продуктов установлен любой статус'):
            assert any(stat['isActive'] for stat in statuses)

    @allure.title('Проверяем жизненный цикл у 10 рандомных внутренних продуктов')
    @pytest.mark.parametrize('product_code',
                             ['BI_3060', 'BI_1921', 'BI_1261', 'BI_215', 'BI_2024', 'BI_101', 'BI_62', 'BI_55',
                              'BI_101', 'BI_202'])
    def test_life_cycle_internal_products(self, rest_internal_client, product_code):
        main_l = self.get_life_cycle_fields
        statuses = self.get_life_cycle(rest_internal_client, product_code)['statuses']

        self.check_sorted_subset(main_l, [i['code'] for i in statuses])

        with allure.step('Проверяем, что у продуктов установлен любой статус'):
            assert any(stat['isActive'] for stat in statuses)

    @allure.title('Проверяем жизненный цикл у 10 рандомных архивных продуктов')
    @pytest.mark.parametrize('product_code',
                             ['BI_270', 'BI_89', 'BI_82', 'BI_30', 'BI_72', 'BI_1886', 'BI_251', 'BI_78',
                              'BI_272', 'BI_96'])
    def test_life_cycle_archive_products(self, rest_internal_client, product_code):
        main_l = self.get_life_cycle_fields
        statuses = self.get_life_cycle(rest_internal_client, product_code)['statuses']

        self.check_sorted_subset(main_l, [i['code'] for i in statuses])

        with allure.step('Проверяем, что у продуктов установлен архивный статус'):
            arch_statuses = [i['code'] for i in statuses if i['isActive'] and not
            i['code'] == 'Arkhiv']
            assert not arch_statuses, f'У продукта статус {arch_statuses}'

    @allure.title('Проверяем жизненный цикл у удаленного продукта')
    def test_life_cycle_deleted_products(self, rest_internal_client):
        main_l = self.get_life_cycle_fields
        statuses = self.get_life_cycle(rest_internal_client, 'BI_2982')['statuses']

        self.check_sorted_subset(main_l, [i['code'] for i in statuses])

    @allure.title('Проверяем смену основных статусов')
    @pytest.mark.parametrize('status_code, status_name', (
            ['Arkhiv', 'Архив'], ['(PPinfo_status)In_use', 'Запущен в КЭ'],
            ['(PPinfo_status)Pilot', 'Пилот'], ['(PPinfo_status)In_progress', 'Разработка'],
            ['(PPinfo_status)Idea_formation', 'Формирование идеи']))
    def test_life_cycle_change_status(self, ppinfo_client, rest_internal_client, status_code, status_name):
        self.change_status(ppinfo_client, status_code, status_name)
        self.change_start_closed(ppinfo_client, remove=True)

        statuses = self.get_life_cycle(rest_internal_client)['statuses']

        with allure.step(f'Проверяем, что у продукта установился статус {status_name}'):
            act_statuses = [i['code'] for i in statuses if i['isActive'] and i['code'] != status_code]
            assert not act_statuses, f'У продукта статус {act_statuses}'

    # Формирование идеи
    @allure.title('Проверяем дату у статуса Формирование идеи')
    def test_life_cycle_idea_form_check_date(self, ppinfo_client, rest_internal_client):
        self.change_status(ppinfo_client, '(PPinfo_status)Idea_formation', 'Формирование идеи')
        self.change_status_date(ppinfo_client, 'PPInfo_date_Idea_formation')

        with allure.step('Проверяем, что есть только одна дата'):
            assert self.get_life_cycle(rest_internal_client)['statuses'][0][
                       'startDate'] != '0001-01-01T00:00:00Z', 'Нет даты формирования идеи'
            assert self.get_life_cycle(rest_internal_client)['statuses'][0][
                       'endDate'] == '0001-01-01T00:00:00Z', 'У продукта 2 даты формирования идеи'

        self.change_status_date(ppinfo_client, 'PPInfo_date_Idea_formation', include_date=False)

        with allure.step('Проверяем, что дат нет'):
            assert self.get_life_cycle(rest_internal_client)['statuses'][0][
                       'startDate'] == '0001-01-01T00:00:00Z', 'Есть дата формирования идеи'
            assert self.get_life_cycle(rest_internal_client)['statuses'][0][
                       'endDate'] == '0001-01-01T00:00:00Z', 'Есть дата формирования идеи'

    # Разработка
    @allure.title('Проверяем дату у активного статуса Разработка')
    @allure.issue('https://jira.mts.ru/browse/PPI-2151',
                  'PPinfo - Не отображается дата окончания разработки на прогрессбаре')
    def test_life_cycle_in_progr_check_date_active(self, ppinfo_client, rest_internal_client):
        self.change_status(ppinfo_client, '(PPinfo_status)In_progress', 'Разработка')
        self.change_status_date(ppinfo_client, 'PPInfo_date_In_progress')
        self.change_status_date(ppinfo_client, 'PPinfo_close_date', include_date=False)

        statuses = self.get_life_cycle(rest_internal_client)['statuses']
        status_pos = [statuses.index(i) for i in statuses if i['code'] == '(PPinfo_status)In_progress'][0]

        with allure.step('Проверяем, значение дат при наличии только даты начала разработки'):
            assert statuses[status_pos]['startDate'] != '0001-01-01T00:00:00Z', 'Нет даты начала разработки'
            assert statuses[status_pos][
                       'endDate'] == '0001-01-01T00:00:00Z', f"Конец разработки указан как {statuses[status_pos]['endDate']}"

        self.change_status_date(ppinfo_client, 'PPinfo_close_date')

    @allure.title('Проверяем дату у неактивного статусе Разработка')
    @allure.issue('https://jira.mts.ru/browse/PPI-2152',
                  'Не отображается дата окончания разработки на прогрессбаре при архивном статусе')
    @allure.issue('https://jira.mts.ru/browse/PPI-2153',
                  'PPinfo - Дата окончания разработки на прогрессбаре указывается, как по н.в. при архивном статусе Выведен из КЭ')
    def test_life_cycle_in_progr_check_date_archive(self, ppinfo_client, rest_internal_client):
        self.change_status(ppinfo_client, 'Arkhiv', 'Архив')
        self.change_status_date(ppinfo_client, 'PPInfo_date_In_progress')
        self.change_status_date(ppinfo_client, 'PPinfo_close_date', include_date=False)

        statuses = self.get_life_cycle(rest_internal_client)['statuses']
        status_pos = [statuses.index(i) for i in statuses if i['code'] == '(PPinfo_status)In_progress'][0]

        with allure.step('Проверяем, значение дат при наличии только даты начала разработки'):
            assert statuses[status_pos]['startDate'] != '0001-01-01T00:00:00Z', 'Нет даты начала разработки'
            assert statuses[status_pos][
                       'endDate'] == '0001-01-01T00:00:00Z', f"Конец разработки указан как {statuses[status_pos]['endDate']}"

        self.change_status_date(ppinfo_client, 'PPinfo_close_date')
        statuses = self.get_life_cycle(rest_internal_client)['statuses']

        with allure.step('Проверяем, значение дат при наличии обеих дат разработки'):
            assert statuses[status_pos]['startDate'] != '0001-01-01T00:00:00Z', 'Нет даты начала разработки'
            assert statuses[status_pos]['endDate'] and statuses[status_pos][
                'endDate'] == '0001-01-01T00:00:00Z', f"Конец разработки указан как {statuses[status_pos]['endDate']}"

        self.change_status_date(ppinfo_client, 'PPinfo_close_date', include_date=False)
        self.change_status_date(ppinfo_client, 'PPInfo_date_In_progress', include_date=False)

    @allure.title('Проверяем порядок у статуса Разработка')
    def test_life_cycle_in_progr_check_order(self, ppinfo_client, rest_internal_client):
        self.change_status(ppinfo_client, '(PPinfo_status)In_progress', 'Разработка')

        statuses = self.get_life_cycle(rest_internal_client)['statuses']
        status_pos = [statuses.index(i) for i in statuses if i['code'] == '(PPinfo_status)In_progress'][0]

        with allure.step('Проверяем, что после статуса в разработке идет допустимый статус'):
            assert statuses[status_pos + 1]['code'] in ['(PPinfo_status)Pilot', '(PPinfo_status)In_use',
                                                        'PPinfo_start_close', 'Arkhiv'], \
                statuses[status_pos + 1]['code']

    # Пилот
    @allure.title('Проверяем дату у статуса Пилот')
    def test_life_cycle_pilot_check_date(self, ppinfo_client, rest_internal_client):
        self.change_status(ppinfo_client, '(PPinfo_status)Pilot', 'Пилот')
        self.change_status_date(ppinfo_client, 'PPinfo_start_date_MVP')
        self.change_status_date(ppinfo_client, 'PPinfo_finish_date_MVP', include_date=False)

        statuses = self.get_life_cycle(rest_internal_client)['statuses']
        status_pos = [statuses.index(i) for i in statuses if i['code'] == '(PPinfo_status)Pilot'][0]

        with allure.step('Проверяем, что есть только одна дата начала'):
            assert statuses[status_pos]['startDate'] != '0001-01-01T00:00:00Z', 'Нет даты начала пилота'
            assert statuses[status_pos]['endDate'] == '0001-01-01T00:00:00Z', 'Есть дата окончания пилота'

        self.change_status_date(ppinfo_client, 'PPinfo_finish_date_MVP')
        statuses = self.get_life_cycle(rest_internal_client)['statuses']

        with allure.step('Проверяем, что есть обе даты'):
            assert statuses[status_pos]['startDate'] != '0001-01-01T00:00:00Z', 'Нет даты начала пилота'
            assert statuses[status_pos]['endDate'] != '0001-01-01T00:00:00Z', 'Нет даты окончания пилота'

        self.change_status_date(ppinfo_client, 'PPinfo_finish_date_MVP', include_date=False)
        self.change_status_date(ppinfo_client, 'PPinfo_start_date_MVP', include_date=False)

    @allure.title('Проверяем порядок у статуса Пилот')
    def test_life_cycle_pilot_check_order(self, ppinfo_client, rest_internal_client):
        self.change_status(ppinfo_client, '(PPinfo_status)Pilot', 'Пилот')

        statuses = self.get_life_cycle(rest_internal_client)['statuses']
        status_pos = [statuses.index(i) for i in statuses if i['code'] == '(PPinfo_status)Pilot'][0]

        with allure.step('Проверяем, что после статуса в разработке идет допустимый статус'):
            assert statuses[status_pos + 1]['code'] in ['(PPinfo_status)In_use', '(PPinfo_status)Waiting_decision',
                                                        'PPinfo_start_close', '(PPinfo_status)Canceled',
                                                        'Zapushchen_v_PE'], \
                statuses[status_pos + 1]['code']

    # Запущен в КЭ
    @allure.title('Проверяем дату у статуса Запущен в КЭ')
    def test_life_cycle_in_use_check_date(self, ppinfo_client, rest_internal_client):
        self.change_status(ppinfo_client, '(PPinfo_status)In_use', 'Запущен в КЭ')
        self.change_status_date(ppinfo_client, 'PPinfo_execution_date')

        statuses = self.get_life_cycle(rest_internal_client)['statuses']
        status_pos = [statuses.index(i) for i in statuses if i['code'] == '(PPinfo_status)In_use'][0]

        with allure.step('Проверяем, что есть только одна дата'):
            assert statuses[status_pos]['startDate'] != '0001-01-01T00:00:00Z', 'Нет даты запуска в КЭ'
            assert statuses[status_pos]['endDate'] == '0001-01-01T00:00:00Z', 'Есть дата окончания КЭ'

        self.change_status_date(ppinfo_client, 'PPinfo_execution_date', include_date=False)

    @allure.title('Проверяем порядок у статуса Запущен в КЭ')
    def test_life_cycle_in_use_check_order(self, ppinfo_client, rest_internal_client):
        self.change_status(ppinfo_client, 'Zapushchen_v_PE', 'Запущен в ПЭ')

        statuses = self.get_life_cycle(rest_internal_client)['statuses']
        status_pos = [statuses.index(i) for i in statuses if i['code'] == 'Zapushchen_v_PE'][0]

        with allure.step('Проверяем, что после статуса в разработке идет допустимый статус'):
            assert statuses[status_pos + 1]['code'] in 'Arkhiv', \
                statuses[status_pos + 1]['code']

    # Выведен из КЭ
    @allure.title('Проверяем дату у статуса Выведен в КЭ')
    def test_life_cycle_out_of_use_check_date(self, ppinfo_client, rest_internal_client):
        self.change_status(ppinfo_client, 'Arkhiv', 'Архив')
        self.change_status_date(ppinfo_client, 'PPinfo_close_date')

        statuses = self.get_life_cycle(rest_internal_client)['statuses']
        status_pos = [statuses.index(i) for i in statuses if i['code'] == 'Arkhiv'][0]

        with allure.step('Проверяем, что есть только одна дата'):
            assert statuses[status_pos]['startDate'] != '0001-01-01T00:00:00Z', 'Нет даты выведен из КЭ'
            assert statuses[status_pos]['endDate'] == '0001-01-01T00:00:00Z', 'Есть дата вывода из КЭ'

        self.change_status_date(ppinfo_client, 'PPinfo_close_date', include_date=False)

    @allure.title('Проверяем порядок у статуса Выведен в КЭ')
    def test_life_cycle_out_of_use_check_order(self, ppinfo_client, rest_internal_client):
        self.change_status(ppinfo_client, 'Arkhiv', 'Архив')

        statuses = self.get_life_cycle(rest_internal_client)['statuses']
        status_pos = [statuses.index(i) for i in statuses if i['code'] == 'Arkhiv'][0]

        with allure.step('Проверяем, что после статуса в Выведен из КЭ нет статусов'):
            assert statuses[-1]['code'] == statuses[status_pos]['code'], statuses[-1]['code']

    # Ожидание решения
    @allure.title('Проверяем смену доп статуса Ожидание решения')
    def test_life_waiting_des_check_change(self, ppinfo_client, rest_internal_client):
        self.change_status(ppinfo_client, '(PPinfo_status)Waiting_decision', 'Ожидание решения')

        with allure.step(f'Проверяем, что у продукта установился статус Ожидание решения'):
            act_statuses = [i['code'] for i in self.get_life_cycle(rest_internal_client)['statuses'] if
                            i['isActive'] and i['code'] != '(PPinfo_status)Waiting_decision']
            assert not act_statuses, f'У продукта статус {act_statuses}'

        self.change_status(ppinfo_client, '(PPinfo_status)In_use', 'Запущен в КЭ')

        with allure.step(f'Проверяем, что у продукта пропал статус Ожидание решения'):
            assert all(i['code'] != '(PPinfo_status)Waiting_decision' for i in
                       self.get_life_cycle(rest_internal_client)['statuses']), 'Статус Ожидает решения не пропал'

    @allure.title('Проверяем порядок статусов при Ожидание решения')
    def test_life_cycle_waiting_des_check_order(self, ppinfo_client, rest_internal_client):
        self.change_status(ppinfo_client, '(PPinfo_status)Waiting_decision', 'Ожидание решения')

        statuses = self.get_life_cycle(rest_internal_client)['statuses']
        status_pos = [statuses.index(i) for i in statuses if i['code'] == '(PPinfo_status)Waiting_decision'][0]

        with allure.step('Проверяем, что статус Ожидание решения находится после статуса Запуск пилота'):
            assert statuses[status_pos - 1][
                       'code'] == '(PPinfo_status)Pilot', f'Перед Ожидание решения статус{statuses[status_pos - 1]}'

        with allure.step('Проверяем, что статус Ожидание решения находится перед статусом Запущен в G"'):
            assert statuses[status_pos + 1][
                       'code'] == 'Zapushchen_v_PE', f'После Ожидание решения статус{statuses[status_pos + 1]}'

    @allure.title('Проверяем отсутствие даты у статуса Ожидание решения')
    def test_life_cycle_waiting_des_check_date(self, ppinfo_client, rest_internal_client):
        self.change_status(ppinfo_client, '(PPinfo_status)Waiting_decision', 'Ожидание решения')

        statuses = self.get_life_cycle(rest_internal_client)['statuses']
        status_pos = [statuses.index(i) for i in statuses if i['code'] == '(PPinfo_status)Waiting_decision'][0]

        with allure.step('Проверяем, что у статуса нет даты'):
            assert statuses[status_pos]['endDate'] == '0001-01-01T00:00:00Z' and statuses[status_pos][
                'startDate'] == '0001-01-01T00:00:00Z', 'У статуса есть даты'

    # Инициировано закрытие
    @allure.title('Проверяем смену доп статуса Инициировано закрытие у допустимых статусов')
    @pytest.mark.parametrize('status_code, status_name', (['(PPinfo_status)In_use', 'Запущен в КЭ'],
                                                          ['(PPinfo_status)Pilot', 'Пилот'],
                                                          ['(PPinfo_status)In_progress', 'Разработка']))
    def test_life_cycle_start_close_change_status(self, ppinfo_client, rest_internal_client, status_code, status_name):
        self.change_status(ppinfo_client, status_code, status_name)
        self.change_start_closed(ppinfo_client)

        with allure.step(f'Проверяем, что у продукта установился доп статус Инициировано закрытие'):
            act_statuses = [i['code'] for i in self.get_life_cycle(rest_internal_client)['statuses'] if
                            i['isActive'] and i['code'] != 'PPinfo_start_close' and i['code'] != status_code]
            assert not act_statuses, f'У продукта статус {act_statuses}'

        self.change_start_closed(ppinfo_client, remove=True)

        with allure.step(f'Проверяем, что у продукта пропал доп статус Инициировано закрытие'):
            assert all(i['code'] != 'PPinfo_start_close' for i in
                       self.get_life_cycle(rest_internal_client)['statuses']), 'Статус Инициировано закрытие не пропал'

    @allure.title('Проверяем отсутствие иниц. закрытие у недопустимых статусов')
    @pytest.mark.parametrize('status_code, status_name', (
            ['(PPinfo_status)Idea_formation', 'Формирование идеи'], ['(PPinfo_status)Out_of_use', 'Выведен из КЭ'],
            ['(PPinfo_status)Canceled', 'Запуск отменен']))
    def test_life_cycle_start_close_change_incorrect_status(self, ppinfo_client, rest_internal_client, status_code,
                                                            status_name):
        self.change_status(ppinfo_client, status_code, status_name)
        self.change_start_closed(ppinfo_client)

        with allure.step(f'Проверяем, что у продукта нет доп статус Инициировано закрытие'):
            assert all(i['code'] != 'PPinfo_start_close' for i in
                       self.get_life_cycle(rest_internal_client)['statuses']), 'Статус Инициировано закрытие не пропал'

        self.change_start_closed(ppinfo_client, remove=True)

    @allure.title('Проверяем порядок статусов при Инициировано закрытие')
    @pytest.mark.parametrize('status_code, status_name', (['(PPinfo_status)In_use', 'Запущен в КЭ'],
                                                          ['(PPinfo_status)Pilot', 'Пилот'],
                                                          ['(PPinfo_status)In_progress', 'Разработка']))
    def test_life_cycle_start_close_check_order(self, ppinfo_client, rest_internal_client, status_code, status_name):
        self.change_status(ppinfo_client, status_code, status_name)
        self.change_start_closed(ppinfo_client)

        statuses = self.get_life_cycle(rest_internal_client)['statuses']

        with allure.step(f'Проверяем, что статус Иниц.закрытие относится к статусу {status_name}'):
            for status_in_lc in statuses:
                if status_in_lc['code'] == status_code:
                    assert status_in_lc['additionalStatuses'][0]['name'] == 'Инициировано закрытие'

        self.change_start_closed(ppinfo_client, remove=True)

    @allure.title('Проверяем дату у доп статуса Инициировано закрытие')
    def test_life_cycle_start_close_check_date(self, ppinfo_client, rest_internal_client):
        self.change_status(ppinfo_client, '(PPinfo_status)In_use', 'Разработка')
        self.change_start_closed(ppinfo_client)

        statuses = self.get_life_cycle(rest_internal_client)['statuses']

        for status_in_lc in statuses:
            if status_in_lc['code'] == '(PPinfo_status)In_use':
                assert status_in_lc['additionalStatuses'][0][
                           'startDate'] != '0001-01-01T00:00:00Z', 'Нет даты начала Иниц. закрытие'
                assert status_in_lc['additionalStatuses'][0][
                           'endDate'] == '0001-01-01T00:00:00Z', 'Есть дата конца иниц закрытие'

        self.change_start_closed(ppinfo_client, remove=True)

    @allure.title('Проверяем порядок доп статуса Инициировано закрытие при отсутствии даты')
    @allure.issue('https://jira.mts.ru/browse/PPI-2185', 'PPInfo - Инициировано закрытие с/без дат на прогрессбаре')
    @pytest.mark.parametrize('status_code, status_name', (
            ['Arkhiv', 'Архив'], ['(PPinfo_status)In_use', 'Запущен в КЭ'],
            ['(PPinfo_status)Pilot', 'Пилот'], ['(PPinfo_status)In_progress', 'Разработка']))
    def test_life_cycle_start_close_check_order_without_date(self, ppinfo_client, rest_internal_client, status_code,
                                                             status_name):
        self.change_status(ppinfo_client, status_code, status_name)
        self.change_start_closed(ppinfo_client)
        self.change_status_date(ppinfo_client, 'PPinfo_start_close_date', include_date=False)

        statuses = self.get_life_cycle(rest_internal_client)['statuses']
        if status_code != 'Arkhiv':
            for status_in_lc in statuses:
                if status_in_lc['code'] == status_code:
                    assert status_in_lc['additionalStatuses'][0]['name'] == 'Инициировано закрытие'

        else:
            with allure.step('Проверяем, что при Выведен из КЭ не отображается иниц закрытие'):
                assert not [i for i in statuses if i['code'] == 'PPinfo_start_close'], 'Иниц закрытие отображается'

        self.change_start_closed(ppinfo_client, remove=True)

    # Запуск отменен
    @allure.title('Проверяем установку доп статуса Отменен')
    def test_life_cycle_cancel_change_status(self, ppinfo_client, rest_internal_client):
        self.change_status(ppinfo_client, 'Arkhiv', 'Архив')

        with allure.step(f'Проверяем, что у продукта установился доп статус Инициировано закрытие'):
            act_statuses = [i['code'] for i in self.get_life_cycle(rest_internal_client)['statuses'] if
                            i['isActive'] and i['code'] != 'Arkhiv']
            assert not act_statuses, f'У продукта статус {act_statuses}'

    @allure.title('Проверяем дату у доп статуса Отменен')
    def test_life_cycle_cancel_check_date(self, ppinfo_client, rest_internal_client):
        self.change_status(ppinfo_client, 'Arkhiv', 'Архив')
        self.change_status_date(ppinfo_client, 'PPinfo_close_date')

        statuses = self.get_life_cycle(rest_internal_client)['statuses']
        status_pos = [statuses.index(i) for i in statuses if i['code'] == 'Arkhiv'][0]

        for status_in_lc in statuses:
            if status_in_lc['code'] == 'Arkhiv':
                assert statuses[status_pos]['startDate'] != '0001-01-01T00:00:00Z', 'Нет даты начала Запуск отменен'
                assert statuses[status_pos]['endDate'] == '0001-01-01T00:00:00Z', 'Есть дата конца Запуск отменен'

    @allure.title('Проверяем порядок статусов при Запуск отменен')
    def test_life_cycle_cancel_check_order(self, ppinfo_client, rest_internal_client):
        self.change_status(ppinfo_client, 'Arkhiv', 'Архив')

        self.change_status_date(ppinfo_client, 'PPInfo_date_Idea_formation', date_days='10')
        self.change_status_date(ppinfo_client, 'PPInfo_date_In_progress', date_days='12')
        self.change_status_date(ppinfo_client, 'PPinfo_start_date_MVP', date_days='14')
        self.change_status_date(ppinfo_client, 'PPinfo_finish_date_MVP', date_days='16')

        self.change_status_date(ppinfo_client, 'PPinfo_close_date', date_days='11')

        with allure.step('Проверяем отображение статуса Выведен из КЭ после формирования идеи'):
            statuses = self.get_life_cycle(rest_internal_client)['statuses']
            status_pos = [statuses.index(i) for i in statuses if i['code'] == 'Arkhiv'][0]
            assert statuses[status_pos - 1][
                       'code'] == '(PPinfo_status)In_progress', f'Статус до: {statuses[status_pos - 1]}'

        self.change_status_date(ppinfo_client, 'PPinfo_close_date', date_days='13')

        with allure.step('Проверяем отображение статуса Выведен из КЭ после разработки'):
            statuses = self.get_life_cycle(rest_internal_client)['statuses']
            status_pos = [statuses.index(i) for i in statuses if i['code'] == 'Arkhiv'][0]
            assert statuses[status_pos - 1][
                       'code'] == '(PPinfo_status)In_progress', f'Статус до: {statuses[status_pos - 1]}'

        self.change_status_date(ppinfo_client, 'PPinfo_close_date', date_days='17')

        with allure.step('Проверяем отображение статуса Выведен из КЭ после пилота'):
            statuses = self.get_life_cycle(rest_internal_client)['statuses']
            status_pos = [statuses.index(i) for i in statuses if i['code'] == 'Arkhiv'][0]
            assert statuses[status_pos - 1][
                       'code'] == '(PPinfo_status)In_progress', f'Статус до: {statuses[status_pos - 1]}'

    @allure.title('Проверяем порядок статусов при Запуск отменен по умолчанию')
    def test_life_cycle_cancel_check_order_default(self, ppinfo_client, rest_internal_client):
        self.change_status(ppinfo_client, 'Arkhiv', 'Архив')

        self.change_status_date(ppinfo_client, 'PPInfo_date_Idea_formation', include_date=False)
        self.change_status_date(ppinfo_client, 'PPInfo_date_In_progress', include_date=False)
        self.change_status_date(ppinfo_client, 'PPinfo_start_date_MVP', include_date=False)
        self.change_status_date(ppinfo_client, 'PPinfo_finish_date_MVP', include_date=False)

        self.change_status_date(ppinfo_client, 'PPinfo_close_date', date_days='17')

        with allure.step('Проверяем отображение статуса Выведен из КЭ по умолчанию при наличии даты'):
            statuses = self.get_life_cycle(rest_internal_client)['statuses']
            status_pos = [statuses.index(i) for i in statuses if i['code'] == 'Arkhiv'][0]
            assert statuses[status_pos - 1][
                       'code'] == '(PPinfo_status)In_progress', f'Статус до: {statuses[status_pos - 1]}'

        self.change_status_date(ppinfo_client, 'PPinfo_close_date', include_date=False)

        with allure.step('Проверяем отображение статуса Выведен из КЭ по умолчанию при отсутствии даты'):
            statuses = self.get_life_cycle(rest_internal_client)['statuses']
            status_pos = [statuses.index(i) for i in statuses if i['code'] == 'Arkhiv'][0]
            assert statuses[status_pos - 1][
                       'code'] == '(PPinfo_status)In_progress', f'Статус до: {statuses[status_pos - 1]}'

    @allure.issue('https://jira.mts.ru/browse/PPI-3791', 'PPInfo - Метка альфа-тестирования (прогресс-бар)')
    @pytest.mark.parametrize('status, status_name', (['Pilot', 'Пилот'], ['In_progress', 'Разработка']))
    @pytest.mark.parametrize('yes', (True, False))
    @pytest.mark.parametrize('start', (True, False))
    @pytest.mark.parametrize('end', (True, False))
    def test_alpha_testing(self, ppinfo_client, rest_internal_client, status, status_name, yes, start, end):

        allure.dynamic.title(
            f'Проверка метки альфа тестирования в статусе {status_name}\n Установленная метка = {yes}\n Установленная дата начала = {start}\n Установленная дкончания = {end}')

        self.change_status(ppinfo_client, f'(PPinfo_status){status}', status_name=status_name,
                           product_id='BI_3266')  # (PPinfo_status)Pilot или (PPinfo_status)In_progress
        self.change_alpha_testing(ppinfo_client, status, yes=yes, start=start, end=end)

        life_cycle = self.get_life_cycle(rest_internal_client, product_code='BI_3266')['statuses']

        try:
            for status_in_lc in life_cycle:
                if status_in_lc['name'] == status_name and yes:
                    assert len(status_in_lc[
                                   'additionalStatuses']) == 1, 'Значение в альфа тестирование по статусу установлено как Да, но метка не пришла'
                else:
                    assert len(status_in_lc[
                                   'additionalStatuses']) == 0, 'Значение в альфа тестирование по статусу установлено как Нет, но метка пришла'

                if status_in_lc['name'] == status_name and start and yes:
                    assert status_in_lc['additionalStatuses'][0][
                               'startDate'] == '2025-01-30T21:00:00Z', 'Дата указана, но не пришла'

                if status_in_lc['name'] == status_name and end and yes:
                    assert status_in_lc['additionalStatuses'][0][
                               'endDate'] == '2025-02-27T21:00:00Z', 'Дата указана, но не пришла'


        finally:
            self.change_alpha_testing(ppinfo_client, status, yes=False, start=False, end=False)

    @allure.issue('https://jira.mts.ru/browse/PPI-3789', 'PPInfo - Отображение этапов PLM PG в прогресс-баре')
    @pytest.mark.parametrize('status_code, status_name', (['(PPinfo_status)In_use', 'Запущен в КЭ'],
                                                          ['(PPinfo_status)Pilot', 'Пилот'],
                                                          ['(PPinfo_status)In_progress', 'Разработка'],
                                                          ['(PPinfo_status)Idea_formation', 'Формирование идеи'],
                                                          ['(PPinfo_status)Waiting_decision', 'Ожидание решения']))
    @pytest.mark.parametrize('plm_stage', (
            'Закрытие продукта', 'Развитие продукта', 'Разработка и запуск MVP', 'Разработка концепции'))
    def test_plm_stages(self, ppinfo_client, rest_internal_client, status_code, status_name, plm_stage):

        allure.dynamic.title(
            f'Этапы PLM {plm_stage} отображается для статуса {status_name}')

        self.change_status(ppinfo_client, status_code, status_name)

        self.change_plm_stages(ppinfo_client, plm_stage)

        life_cycle = self.get_life_cycle(rest_internal_client, product_code='BI_2687')['statuses']

        for status in life_cycle:
            if status['code'] == status_code:
                assert status['plm']

                assert unquote(status['plm']['links'][0][
                                   'link']) == f"https://stage.prodboard.mts.ru/product/BI_2687/guide?tab={plm_stage.replace(' ', '+')}"
                assert status['plm']['links'][0]['name'] == "Перейти в Product Guide"

                assert status['plm']['links'][1][
                           'link'] == "https://confluence.mts.ru/x/kRaHXw"

                assert status['plm']['links'][1]['name'] == "Больше о связи статуса с PLM"

            else:
                assert not status['plm']

    @allure.title('Этап PLM не отображается для статуса Архив')
    @allure.issue('https://jira.mts.ru/browse/PPI-3789', 'PPInfo - Отображение этапов PLM PG в прогресс-баре')
    @pytest.mark.parametrize('plm_stage', (
            'Закрытие продукта', 'Развитие продукта', 'Разработка и запуск MVP', 'Разработка концепции'))
    def test_plm_stages(self, ppinfo_client, rest_internal_client, plm_stage):

        self.change_status(ppinfo_client, 'Arkhiv', 'Архив')

        self.change_plm_stages(ppinfo_client, plm_stage)

        life_cycle = self.get_life_cycle(rest_internal_client, product_code='BI_2687')['statuses']

        for status in life_cycle:
            assert not status['plm']

    @allure.title('Документ в статусах жизненного цикла')
    @pytest.mark.parametrize('status_code, status_name', [['(PPinfo_status)Waiting_decision', 'Ожидание решения'],
                                                          ['(PPinfo_status)Pilot', 'Пилот'],
                                                          ['(PPinfo_status)In_progress', 'Разработка'],
                                                          ['Zapushchen_v_PE', 'Запущен в ПЭ'], ['Arkhiv', 'Архив'],
                                                          ['(PPinfo_status)Idea_formation', 'Формирование идеи']])
    def test_doc_in_life_cycle(self, ppinfo_client, rest_internal_client, status_code, status_name):

        doc_name = 'filename_test_' + '.xlsx'[1:] + 'public'

        data = {
            'name': doc_name,
            'description': '.xlsx',
            'type': 'document',
            'accessType': 'public',
            'lifeCycleAttributeCode': 'PPinfo_status',
            'lifeCycleAttributeValue': status_code
        }

        doc_id = self.add_doc(rest_internal_client, data)

        self.change_status(ppinfo_client, status_code, status_name)

        doc_link = None
        get_docs = self.get_docs_by_bi_code(rest_internal_client, 'BI_2687')['documents']
        for doc in get_docs:
            if doc['id'] == doc_id:
                doc_link = doc['link']

        life_cycle = self.get_life_cycle(rest_internal_client, product_code='BI_2687')['statuses']

        for status in life_cycle:
            if status['code'] == status_code:
                doc_links = [doc['link'] for doc in status['documents']]
                doc_names = [doc['name'] for doc in status['documents']]
                assert doc_link in doc_links
                assert doc_name in doc_names

        self.delete_doc(rest_internal_client, doc_id)

    @allure.title('Документы в жизненном цикле в альфа атрибутах')
    @allure.issue('https://jira.mts.ru/browse/PPI-3791', 'PPInfo - Метка альфа-тестирования (прогресс-бар)')
    @pytest.mark.parametrize('status, status_name', (['Pilot', 'Пилот'], ['In_progress', 'Разработка']))
    def test_docs_in_alpha_testing(self, ppinfo_client, rest_internal_client, status, status_name):

        doc_name = 'filename_test_' + '.xlsx'[1:] + 'public'

        data = {
            'name': doc_name,
            'description': '.xlsx',
            'type': 'document',
            'accessType': 'public',
            'lifeCycleAttributeCode': f'Alpha_{status}',
            'lifeCycleAttributeValue': 'Da'
        }

        doc_id = self.add_doc(rest_internal_client, data)

        self.change_status(ppinfo_client, f'(PPinfo_status){status}',
                           status_name=status_name)  # (PPinfo_status)Pilot или (PPinfo_status)In_progress

        self.change_alpha_testing(ppinfo_client, status, product_id='BI_2687', yes=True)

        doc_link = None
        get_docs = self.get_docs_by_bi_code(rest_internal_client, 'BI_2687')['documents']
        for doc in get_docs:
            if doc['id'] == doc_id:
                doc_link = doc['link']

        life_cycle = self.get_life_cycle(rest_internal_client)['statuses']

        try:
            for status_in_lc in life_cycle:
                if status_in_lc['code'] == f'(PPinfo_status){status}':
                    for additional_status in status_in_lc['additionalStatuses']:
                        for document in additional_status['documents']:
                            if document['link'] == doc_link:
                                assert document['name'] == doc_name
                                assert document['link'] == doc_link
                                continue
                            else:
                                assert False, 'Документ не отображается в прогрессбаре'
        finally:
            self.change_alpha_testing(ppinfo_client, status, product_id='BI_2687', yes=False, start=False, end=False)
            self.delete_doc(rest_internal_client, doc_id)
