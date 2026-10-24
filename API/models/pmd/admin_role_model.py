from typing import Any

import allure

from API.data.pmd import RoleById, RoleCreation, RolesByLogin, AllUsersModels, RoleGroup
from API.models.ppinfo.product_v2 import ProductV2
from API.utils.generate import Gen

HOST = 'https://stage.prodboard.example.com'


class RoleModelApiUrls:
    """
    https://stage.prodboard.example.com/pmd/swagger/admin/roles-model/index.html#/
    """
    # Получение групп ролей
    GET_ROLES = 'v1/role'

    # Создание группы ролей
    CREATE_ROLE = 'v1/role'

    # Получение конкретной группы с пользователями, атрибутами и.т.п
    GET_ROLE = 'v1/role/{}'

    # Удаление конкретной группы
    DELETE_ROLE = 'v1/role/{}'

    # Изменение статуса роли
    PATCH_ROLE_STATUS = 'v1/role/{}'

    # Получение роли по лоигну не используется на стаге
    GET_ROLE_BY_LOGIN = 'v1/role/{}/by-login'

    # Добавить или убрать атрибут из группы
    MANAGE_ATTRIBUTE = 'v1/role/{}/attribute/manage'

    # Добавить юзера в группу
    ADD_USER_IN_ROLE = 'v1/role/{}/user/{}'

    # Получение всех пользователей
    GET_USER = 'v1/user'

    # Удалить юзера из группы
    DELETE_USER_FROM_ROLE = 'v1/user/{}/role'


class RoleModelApi(RoleModelApiUrls, ProductV2):

    @property
    def text(self):
        """
        Генерит рандомный текст
        Returns: текст + test

        """
        return Gen.generate_text(7) + 'test'

    @property
    def role_id(self):
        """
        Возвращает Id
        Returns: Возвращает Id

        """
        return '12a35eea-7aea-4d12-89d2-019640284cfd'

    @allure.step('Данные для новой роли')
    def get_new_role_data(self, name: str = None, is_active: bool | str = False) -> dict[str, Any]:
        """

        Args:
            name: имя роли
            is_active: активность роли

        Returns: данные для заполнения

        """
        return {
            'name': self.text if name is None else name,
            'isActive': is_active
        }

    @allure.step('Получение данных для manage')
    def get_data_for_manage(self, new_data: dict[str, Any] = None) -> dict[str, Any]:
        data = {
            'attributeId': '0f4375d8-2a2c-42b9-8aa9-e0e2e6c5bcdb',
            'isEditable': True,
            'isOwnedView': False,
            'isOwnedEditable': False,
            'isView': True,
            'isEditingWithoutModeration': False
        }
        if new_data:
            data.update(new_data)

        return {'updateAttributes': [data]}

    @allure.step('Получение всех ролей')
    def get_roles(self, client) -> dict[str, Any]:
        response = client.get(self.GET_ROLES)

        RoleGroup(role_group=response)

        return response

    @allure.step('Создание роли')
    def create_role(self, client, body: dict[str, Any]) -> str:
        response = client.post(self.CREATE_ROLE, params=body)

        RoleCreation(**response)

        return response['id']

    @allure.step('Невалидное создание роли')
    def create_role_400(self, client, body: dict[str, Any]) -> None:
        client.post(self.CREATE_ROLE, json=body, expected_status_code=400)

    @allure.step('Получение роли по id')
    def get_role_by_id(self, client, role_id: str) -> dict[str, Any]:
        response = client.get(self.GET_ROLE.format(role_id))

        RoleById(**response)

        return response

    @allure.step('Невалидное получение роли по id')
    def get_role_by_id_404(self, client, role_id: str) -> None:
        client.get(self.GET_ROLE.format(role_id), expected_status_code=404)

    @allure.step('Удаление роли')
    def delete_role(self, client, role_id: str) -> None:
        client.delete(self.DELETE_ROLE.format(role_id))

    @allure.step('Невалидное удаление роли')
    def delete_role_400(self, client, role_id: str) -> None:
        client.delete(self.DELETE_ROLE.format(role_id), expected_status_code=400)

    @allure.step('Изменение роли')
    def patch_role_status(self, client, role_id: str, params: dict[str, Any]) -> None:
        client.patch(self.PATCH_ROLE_STATUS.format(role_id), params=params)

    @allure.step('Невалидное изменение роли')
    def patch_role_status_400(self, client, role_id: str, params: dict[str, Any]) -> None:
        client.patch(self.PATCH_ROLE_STATUS.format(role_id), json=params, expected_status_code=400)

    @allure.step('Получение ролей по логину')
    def get_role_by_login(self, client, login: str) -> dict[str, Any]:
        response = client.get(self.GET_ROLE_BY_LOGIN.format(login))

        RolesByLogin(**response)

        return response

    @allure.step('Управление атрибутами в роли')
    def manage_attr(self, client, role_id: str, body: dict[str, Any]) -> None:
        client.post(self.MANAGE_ATTRIBUTE.format(role_id), json=body)

    @allure.step('Невалидное управление атрибутами в роли')
    def manage_attr_400(self, client, role_id: str, body: dict[str, Any]) -> None:
        client.post(self.MANAGE_ATTRIBUTE.format(role_id), json=body, expected_status_code=400)

    @allure.step('Добавление юзера в роль')
    def add_user_role(self, client, role_id: str, login: str) -> None:
        client.post(self.ADD_USER_IN_ROLE.format(role_id, login))

    @allure.step('Невалидное обновление юзера в роль')
    def add_user_role_400(self, client, role_id: str, login: str) -> None:
        client.post(self.ADD_USER_IN_ROLE.format(role_id, login), expected_status_code=400)

    @allure.step('Невалидное обновление юзера в роль')
    def add_user_role_404(self, client, role_id: str, login: str) -> None:
        client.post(self.ADD_USER_IN_ROLE.format(role_id, login), expected_status_code=404)

    @allure.step('Получение юзеров с их ролями')
    def get_users(self, client) -> dict[str, Any]:
        response = client.get(self.GET_USER)

        AllUsersModels(**response)

        return response

    @allure.step('Удаление юзера из роли')
    def delete_user_from_role(self, client, login: str, params: dict[str, Any]) -> None:
        client.delete(self.DELETE_USER_FROM_ROLE.format(login), params=params)

    @allure.step('Получение id атрибутов всех типов')
    def get_attributes_ids(self) -> dict:
        return {
            'text для ат': '6390bdef-21a6-4022-adce-f369504a9774',
            'multiple values для ат': '5b64b32f-2ff1-4ffd-828c-141318c0e0bc',
            'date для ат': '2700a71a-69a3-4f40-b79f-94174a8f1eff',
            'number для ат': '64c477c6-74ea-41d1-a483-dd9c116481ab',
            'employee для ат': '85a9edfb-d279-4f5f-934b-55fcf4b9f38e',
            'text with n для ат': '8da7aefb-d473-42e3-b496-304233756557',
            'url для ат': '59267790-55aa-4ece-979e-4f901f6b2a8b'
        }

    @allure.step('Активация и деактивация атрибутов')
    def manage_role_business_direction_attributes(self, client, role_id: str, attributes_ids: tuple,
                                                  activate: bool) -> None:

        update_attributes = []
        for attr_id in attributes_ids:
            attribute = {
                "attributeId": attr_id,
                "isEditable": activate,
                "isOwnedView": False,
                "isOwnedEditable": False,
                "isView": activate,
                "isEditingWithoutModeration": False
            }
            update_attributes.append(attribute)

        data = {"updateAttributes": update_attributes}

        self.manage_attr(client, role_id, data)

    @allure.step('Активация и деактивация атрибутов')
    def manage_role_and_user_business_direction_attributes(self, client, activate: bool, role_attribute: str = 'c117229a-e3d7-4987-a1a6-992b584c634d', role_users: str = '43e72f01-cea3-420a-bc6b-3f507b39af80') -> None:

        try:
            self.manage_role_business_direction_attributes(client, role_attribute,
                                                           tuple(self.get_attributes_ids().values()), activate=activate)
            self.add_user_role(client, role_users, 'regular_user')
        except:
            pass
