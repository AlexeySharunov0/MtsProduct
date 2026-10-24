import os
import warnings
from typing import Any

import allure

from API.data.pmd_dir.rest_internal_data.tool import Tool, ToolGroups, ToolGroup
from API.utils.generate import Gen

warnings.filterwarnings("ignore", message="numpy.dtype size changed")

HOST = 'https://stage.prodboard.example.com'


class ToolUrls:
    """
    https://stage.prodboard.example.com/pmd/swagger/rest/internal/index.html#/
    """

    # Создание инструмента
    ADD_TOOL = 'v1/tool'

    # Добавление файла в инструмент
    ADD_FILE_IN_TOOL = 'v1/tool/file'

    # Получение файла из инструмента по id (что пользователь мог скачать файл)
    GET_FILE_BY_ID = 'v1/tool/file/{}'

    # Получение списка групп инструментов
    GET_TOOL_GROUPS = 'v1/tool/group'

    # Создание группы инструментов
    ADD_TOOL_GROUP = 'v1/tool/group'

    # Изменение порядка групп инструментов
    SWAP_TOOL_GROUP = 'v1/tool/group/swap'

    # Получение группы инструментов по id
    GET_TOOL_GROUP_BY_ID = 'v1/tool/group/{}'

    # Удаление группы инструментов по id
    DELETE_TOOL_GROUP_BY_ID = 'v1/tool/group/{}'

    # Изменение группы инструментов по id
    PATCH_TOOL_GROUP_BY_ID = 'v1/tool/group/{}'

    # Изменение порядка инструментов внутри группы
    SWAP_TOOL = 'v1/tool/swap'

    #  Получение инструмента по id
    GET_TOOL_BY_ID = 'v1/tool/{}'

    # Удаление инструмента по id
    DELETE_TOOL_BY_ID = 'v1/tool/{}'

    # Изменение инструмента по id
    PATCH_TOOL_BY_ID = 'v1/tool/{}'

    # Изменение активности инструмента по id
    CHANGE_ACTIVE_TOOL_BY_ID = 'v1/tool/{}/active'

    # Просмотр схемы
    GET_SCHEMA = 'v1/tool/scheme/{}'

    # Добавление схемы в группу инструментов
    ADD_SCHEMA = 'v1/tool/scheme'


class ToolApi(ToolUrls):

    @allure.step('Заполняем данные для инструмента')
    def get_tool_data(self, group_id: str, params: dict[str, Any] | None = None) -> dict[str, str]:
        data = {
            "shortDescription": "test description",
            "employees": [
            ],
            "files": [
            ],
            "groupId": group_id,
            "isActive": True,
            ''
            "links": [
                {
                    "name": "test_link_name",
                    "url": "https://gitlab.example.com/prodboard/tests/prodboard-ui"
                }
            ],
            "name": 'test_tool' + Gen.generate_text(7).replace(' ', ''),
            "tags": [
            ],
            "productCode": ""
        }
        if params:
            data.update(params)

        return data

    @allure.step('Заполняем данные для группы инструментов')
    def get_tool_group_data(self, params: dict[str, Any] | None = None) -> dict:
        data = {
                "name": "test_tool_group" + Gen.generate_text(7).replace(' ', ''),
                "description": "test description",
                "numImage": 1,
                "links": [
                    {
                        "name": "Ссылка",
                        "url": "https://stage.prodboard.example.com/admin-toolbox/current/0ef47b94-30ed-4959-8e94-09b77e200176"
                    }
                ]
        }
        if params:
            data.update(params)

        return data

    @allure.step('Получение инструмента по id')
    def get_tool_by_id(self, client, tool_id: str) -> dict:
        response = client.get(self.GET_TOOL_BY_ID.format(tool_id))
        Tool(**response)
        return response

    @allure.step('Некорректное получение инструмента по id')
    def get_tool_by_invalid_id(self, client, tool_id: str) -> None:
        client.get(self.GET_TOOL_BY_ID.format(tool_id), expected_status_code=404)

    @allure.step('Создание нового инструмента')
    def add_tool(self, client, tool_data: dict) -> str:
        response = client.post(self.ADD_TOOL, json=tool_data)
        return response

    @allure.step('Невалидное создание нового инструмента')
    def add_invalid_tool(self, client, tool_data: dict) -> None:
        client.post(self.ADD_TOOL, json=tool_data, expected_status_code=400)

    @allure.step('Добавление файла в инструмент')
    def add_file_in_tool(self, client) -> str:
        with open('filename_test.xlsx', 'w'):
            with open('filename_test.xlsx', 'rb') as f:
                files = {'file': f}
                response = client.post(self.ADD_FILE_IN_TOOL, files=files)
                os.remove('filename_test.xlsx')

                return response

    @allure.step('Получение файла из инструмента по id')
    def get_file_by_id(self, client, file_id: str) -> bytes:
        response = client.get(self.GET_FILE_BY_ID.format(file_id), raw_format=True)
        return response.content

    @allure.step('Получение списка групп инструментов')
    def get_tool_groups(self, client) -> list[dict]:
        response = client.get(self.GET_TOOL_GROUPS)
        ToolGroups(tool_groups=response)
        return response

    @allure.step('Создание новой группы инструментов')
    def add_tool_group(self, client, group_data: dict) -> str:
        response = client.post(self.ADD_TOOL_GROUP, json=group_data)
        return response

    @allure.step('Некорректное создание новой группы инструментов')
    def add_invalid_tool_group(self, client, group_data: dict) -> None:
        client.post(self.ADD_TOOL_GROUP, json=group_data, expected_status_code=400, raw_format=True)

    @allure.step('Изменение порядка групп инструментов')
    def swap_tool_group(self, client, group_id: str, to_id: str) -> None:

        data = {
            "id": group_id,
            "toId": to_id
        }
        client.patch(self.SWAP_TOOL_GROUP, json=data, raw_format=True)

    @allure.step('Получение группы инструментов по id')
    def get_tool_group_by_id(self, client, group_id: str) -> dict:
        response = client.get(self.GET_TOOL_GROUP_BY_ID.format(group_id))
        ToolGroup(**response)
        return response

    @allure.step('Удаление группы инструментов по id')
    def delete_tool_group_by_id(self, client, group_id: str) -> None:
        client.delete(self.DELETE_TOOL_GROUP_BY_ID.format(group_id))

    @allure.step('Изменение группы инструментов по id')
    def patch_tool_group_by_id(self, client, group_id: str, group_data: dict) -> None:
        client.patch(self.PATCH_TOOL_GROUP_BY_ID.format(group_id), json=group_data, raw_format=True)

    @allure.step('Изменение порядка инструментов внутри группы')
    def swap_tool(self, client, group_id: str, tool_id: str, to_id: str) -> None:

        data = {
            "groupId": group_id,
            "id": tool_id,
            "toId": to_id
        }
        client.patch(self.SWAP_TOOL, json=data, raw_format=True)

    @allure.step('Получение инструмента по id')
    def get_tool_by_id(self, client, tool_id: str) -> dict:
        response = client.get(self.GET_TOOL_BY_ID.format(tool_id))
        return response

    @allure.step('Удаление инструмента по id')
    def delete_tool_by_id(self, client, tool_id: str) -> None:
        client.delete(self.DELETE_TOOL_BY_ID.format(tool_id))

    @allure.step('Изменение инструмента по id')
    def patch_tool_by_id(self, client, tool_id: str, tool_data: dict) -> None:
        client.patch(self.PATCH_TOOL_BY_ID.format(tool_id), json=tool_data, raw_format=True)

    @allure.step('Изменение активности инструмента по id')
    def change_active_tool_by_id(self, client, tool_id: str, is_active: bool) -> None:
        data = {'active': is_active}
        client.patch(self.CHANGE_ACTIVE_TOOL_BY_ID.format(tool_id), json=data, raw_format=True)

    @allure.step('Просмотр схемы')
    def get_schema(self, client, tool_id: str) -> bytes:

        response = client.get(self.GET_SCHEMA.format(tool_id), raw_format=True)
        return response.content

    @allure.step('Добавление схемы в группу инструментов')
    def add_schema(self, client, file_path: str) -> str:

        if os.path.exists(file_path):
            with open(file_path, 'rb') as f:
                files = {'file': f}
                response = client.post(self.ADD_SCHEMA, files=files, raw_format=True)
                return response.text
        else:
            raise FileNotFoundError(f'Файл {file_path} не найден')
