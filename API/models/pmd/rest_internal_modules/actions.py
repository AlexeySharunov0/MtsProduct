import os
import warnings
from typing import Any

import allure
import openpyxl

from API.data.pmd import ProductGuide, ListProductGuide, \
    ActionsInProduct, ActionsInGeneral

warnings.filterwarnings("ignore", message="numpy.dtype size changed")

HOST = 'https://stage.prodboard.example.com'


class ActionsUrls:
    """
    https://stage.prodboard.example.com/pmd/swagger/rest/internal/index.html#/
    """

    #### ACTION PG steps

    # Добавить файл в шаг PG
    POST_FILE_IN_ACTION = 'v1/action/file'

    # Загрузить файл по ID
    GET_FILE_IN_ACTION_BY_ID = 'v1/action/file/{}'

    # Поменять шаги местами
    SWAP_ACTION = 'v1/action/swap'

    # Получение шага по ID
    GET_ACTION = 'v1/action/{}'

    # Удаление шага по ID
    DELETE_ACTION = 'v1/action/{}'

    # Изменение шага по ID
    PATCH_ACTION = 'v1/action/{}'

    # Создание шага
    CREATE_ACTION = 'v1/action'

    # Получение активных шагов по типу (Внешний, Внутренний) продукта
    GET_ACTIVE_ACTIONS_BY_PRODUCT_CODE = 'v1/action/{}/active-list'

    # Получение списка шагов
    GET_ACTIONS_LIST = 'v1/action/list'

    # Смена активности шага
    CHANGE_ACTIVITY = 'v1/action/{}/active'

    # Получение всех шагов по типу продукта (Внешний, Внутренний) для общего PG
    GET_ALL_ACTIONS = 'v1/action/{}/action-main'

    # Получение Excel Product Guide по типу продукта
    GET_EXCEL_BY_TYPE = 'v1/action/excel/{}/general'

    # Получение Excel Product Guide по BI code определенного продукта
    GET_EXCEL_BY_BI_CODE = 'v1/action/excel/{}'


class Actions(ActionsUrls):

    #### ACTIONS
    @property
    def get_statuses(self):
        return ['(PPinfo_status)Out_of_use', '(PPinfo_status)Canceled', '(PPinfo_status)In_use',
                '(PPinfo_status)Waiting_decision', '(PPinfo_status)Pilot', '(PPinfo_status)In_progress',
                '(PPinfo_status)Idea_formation']

    @staticmethod
    def get_filter_value(attributes: list[list]) -> list:
        filter_item = [{"codeAttribute": "SYSTEM_ProductType", "valueCodes": ['Vneshnii', 'Vnutrennii']}]
        for value in attributes:
            filter_item.append({
                "codeAttribute": value[0],
                "valueCodes": [value[1]] if isinstance(value[1], str) else value[1]
            })
        return filter_item

    @allure.step('Заполняем данные для шага')
    def get_guide_data(self, params: dict[str, Any] | None = None, product_type: str = None,
                       group_name: list[str] = None) -> dict[str, str]:
        data = {'name': 'test_name',
                'description': 'test_description',
                'isActive': False,
                'actionButtons': [],
                'links': [],
                'files': [],
                'employees': [],
                'required': False,
                'repeatable': False,
                'for_po': False,
                'for_cto': False,
                'duration': 0,
                'tags': [''],
                'schemeLink': '',
                'groups': group_name if group_name is not None else ['3cb9b512-af19-4aca-b2ec-84a4bd1209ed'],
                'filter': [
                    {
                        'codeAttribute': 'SYSTEM_ProductType',
                        'valueCodes': [product_type] if product_type is not None else ['Vneshnii', 'Vnutrennii']
                    }
                ]
                }
        if params:
            data.update(params)

        return data

    @allure.step('Создание вложенного шага')
    def create_sub_action(self, client,
                          params: dict[str, Any] = None,
                          group_name: str = 'abfe6e2a-b86c-49e2-990b-2d07e6087c31', for_po: bool = False,
                          for_cto: bool = False) -> list[str]:
        with allure.step('Создаем обычный шаг'):
            main_action_id = self.create_action(client,
                                                self.get_guide_data(group_name=[group_name], params={'isActive': True}))
        data = self.get_guide_data(
            params={'groups': [], 'filter': [], 'mainActionId': main_action_id, 'isActive': True, 'repeatable': False,
                    'required': False, 'for_po': for_po, 'for_cto': for_cto})
        if params:
            data.update(params)
        with allure.step('Создаем вложенный шаг'):
            sub_action_id = self.create_action(client, self.get_guide_data(params=data))
        return [main_action_id, sub_action_id]

    @allure.issue('https://jira.example.com/browse/PPI-1761', 'PPInfo - 1 этап - Админка действий ЖЦП для продукта')
    @allure.step('Получение шага по id')
    def get_action(self, client, action_id: str) -> dict[str, Any]:
        response = client.get(self.GET_ACTION.format(action_id))

        ProductGuide(**response)

        return response

    @allure.issue('https://jira.example.com/browse/PPI-1761', 'PPInfo - 1 этап - Админка действий ЖЦП для продукта')
    @allure.step('Неудачное получение шага по id')
    def get_action_404(self, client, action_id: str) -> None:
        client.get(self.GET_ACTION.format(action_id), expected_status_code=404, raw_format=True)

    @allure.issue('https://jira.example.com/browse/PPI-1761', 'PPInfo - 1 этап - Админка действий ЖЦП для продукта')
    @allure.step('Удаление шага по id')
    def delete_action(self, client, action_id: str) -> None:
        client.delete(self.DELETE_ACTION.format(action_id))

    @allure.issue('https://jira.example.com/browse/PPI-1761', 'PPInfo - 1 этап - Админка действий ЖЦП для продукта')
    @allure.step('Редактирование шага по id')
    def patch_action(self, client, action_id: str, data: dict[str, Any]) -> None:
        client.patch(self.PATCH_ACTION.format(action_id), json=data, raw_format=True)

    @allure.issue('https://jira.example.com/browse/PPI-1761', 'PPInfo - 1 этап - Админка действий ЖЦП для продукта')
    @allure.step('Некорректное редактирование шага по id')
    def patch_action_400(self, client, action_id: str, data: dict[str, Any]) -> None:
        client.patch(self.PATCH_ACTION.format(action_id), json=data, expected_status_code=400)

    @allure.issue('https://jira.example.com/browse/PPI-1761', 'PPInfo - 1 этап - Админка действий ЖЦП для продукта')
    @allure.step('Создание шага')
    def create_action(self, client, data: dict[str, Any]) -> str:
        response = client.post(self.CREATE_ACTION, json=data, raw_format=True)

        return response.text.strip('"')

    @allure.issue('https://jira.example.com/browse/PPI-1761', 'PPInfo - 1 этап - Админка действий ЖЦП для продукта')
    @allure.step('Создание некорректного шага')
    def create_invalid_action_400(self, client, data: dict[str, Any]) -> None:
        client.post(self.CREATE_ACTION, json=data, expected_status_code=400)

    @allure.issue('https://jira.example.com/browse/PPI-1761', 'PPInfo - 1 этап - Админка действий ЖЦП для продукта')
    @allure.step('Получение активных шагов по Коду продукта')
    def get_active_actions(self, client, product_code: str) -> dict:
        response = client.get(self.GET_ACTIVE_ACTIONS_BY_PRODUCT_CODE.format(product_code))

        ActionsInProduct(**response)

        return response

    @allure.issue('https://jira.example.com/browse/PPI-1761', 'PPInfo - 1 этап - Админка действий ЖЦП для продукта')
    @allure.step('Получение списка шагов Product Guide')
    def get_actions_list(self, client) -> list[dict[str, Any]]:
        response = client.get(self.GET_ACTIONS_LIST)

        ListProductGuide(guides=response)

        return response

    @allure.issue('https://jira.example.com/browse/PPI-1898',
                  'PPInfo-Backend - 2 этап - Админка "Product Guide" - Добавить файлы')
    @allure.step('Добавление файла в шагах')
    def add_file_to_action(self, client, filename: str, file_format: str = '.xlsx') -> str:
        with open(filename + file_format, 'w'):
            with open(filename + file_format, 'rb') as f:
                file_dict = {'file': f}
                with allure.step('Добавляем документ'):
                    response = client.post(self.POST_FILE_IN_ACTION, files=file_dict)

        os.remove(filename + file_format)

        return response

    @allure.issue('https://jira.example.com/browse/PPI-1898',
                  'PPInfo-Backend - 2 этап - Админка "Product Guide" - Добавить файлы')
    @allure.step('Получение файла в шагах по айди')
    def get_file_in_action_by_id(self, client, file_id: str) -> str:
        response = client.get(self.GET_FILE_IN_ACTION_BY_ID.format(file_id), raw_format=True)

        return response.headers['Content-Disposition']

    @allure.step('Смена активности шага')
    def change_step_activity(self, client, step_id: str) -> None:
        client.patch(self.CHANGE_ACTIVITY.format(step_id), raw_format=True)

    @allure.step('Невалидная смена активности шага')
    def change_step_activity_400(self, client, step_id: str) -> None:
        client.patch(self.CHANGE_ACTIVITY.format(step_id), expected_status_code=400)

    @allure.step('Свап шагов')
    def swap_guides(self, client, data: dict[str, Any]) -> None:
        client.patch(self.SWAP_ACTION, json=data, raw_format=True)

    @allure.step('Получение шагов для общего Product Guide')
    def get_all_steps(self, client, product_type: str) -> list[dict[str, Any]]:
        response = client.get(self.GET_ALL_ACTIONS.format(product_type))

        ActionsInGeneral(actions_list=response)

        return response

    @allure.step('Получение списка кол-ва активных шагов по типу продукта  Product Guide (включая вложенные)')
    def count_all_steps_by_type(self, client, product_type: str) -> list[int]:
        """
        Получаем кол-во всех активных шагов по группам, включая вложенные
        Args:
            product_type: Тип продукта по которому нужно получить кол-во. Можем быть Vneshnii и Vnutrennii
            client: API Клиент для запросов


        Returns:
            Список, где каждый элемент это кол-во шагов в группе

        """
        data = self.get_all_steps(client, product_type)
        count_for_groups = []
        count = 0

        for group in data:
            count += len(group['actions'])

            for action in group['actions']:

                if action['subActions']:
                    count += len(action['subActions'])

            count_for_groups.append(count)
            count = 0

        return count_for_groups

    @allure.step('Получение списка кол-ва активных шагов по коду BI  Product Guide (включая вложенные)')
    def count_all_steps_by_bi_code(self, client, bi_code: str) -> list[int]:
        """
        Получаем кол-во всех активных шагов по группам, включая вложенные
        Args:
            client: API Клиент для запросов
            bi_code: BI CODE продукта по которому нужно получить кол-во. Можем быть Vneshnii и Vnutrennii

        Returns:
            Список, где каждый элемент это кол-во шагов в группе

        """
        data = self.get_active_actions(client, bi_code)['actions']
        count_for_groups = []
        count = 0

        for group in data:
            count += len(group['actions'])

            for action in group['actions']:

                if action['subActions']:
                    count += len(action['subActions'])

            count_for_groups.append(count)
            count = 0

        return count_for_groups

    @allure.step('Получение Excel Product Guide по типу продукта')
    def get_excel_pg_by_type(self, client, product_type: str) -> openpyxl.Workbook:
        """
        Получение Excel Product Guide по типу продукта
        Args:
            product_type: Тип продукта
            client: API Клиент для запросов

        Returns:
            Excel Product Guide по типу продукта

        """
        response = client.get(self.GET_EXCEL_BY_TYPE.format(product_type), raw_format=True)

        with open('filename_excel.xlsx', 'wb') as f:
            f.write(response.content)

        xls = 'filename_excel.xlsx'

        wb = openpyxl.load_workbook(xls)

        return wb

    @allure.step('Получение Excel Product Guide по коду BI продукта')
    def get_excel_pg_by_bi_code(self, client, bi_code: str) -> openpyxl.Workbook:
        """
        Получение Excel Product Guide по коду BI продукта
        Args:
            bi_code: BI код продукта

        Returns:
            Excel Product Guide по коду BI продукта

        """
        response = client.get(self.GET_EXCEL_BY_BI_CODE.format(bi_code), raw_format=True)

        with open('filename_excel.xlsx', 'wb') as f:
            f.write(response.content)

        xls = 'filename_excel.xlsx'

        wb = openpyxl.load_workbook(xls)

        return wb
