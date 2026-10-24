from typing import Any

import allure

from API.data.pmd import Specifications, Attributes, Sources, SourceItem, SpecificationCreation, AttributeCreation, \
    SourceCreation, AttributeById, SpecificationById
from API.utils.generate import Gen

HOST = 'https://stage.prodboard.example.com'


class SpecificationApiUrl:
    """
    https://stage.prodboard.example.com/pmd/swagger/admin/specification/index.html
    """

    # Получает список спецификаций
    GET_SPECIFICATIONS = 'v1/specification'

    # Создание новой спецификации
    CREATE_SPECIFICATION = 'v1/specification'

    # Получение списка атрибутов
    GET_ATTRIBUTES = 'v1/specification/attribute'

    # Создание нового атрибута
    CREATE_ATTRIBUTE = 'v1/specification/attribute'

    # Получение списка источников
    GET_SOURCES = 'v1/specification/attribute/source'

    # Создание источников
    CREATE_SOURCE = 'v1/specification/attribute/source'

    # Получение источника по ID
    GET_SOURCE_BY_ID = 'v1/specification/attribute/source/{}'

    # Удаление источника по ID
    DELETE_SOURCE_BY_ID = 'v1/specification/attribute/source/{}'

    # Изменение источника по ID
    PATCH_SOURCE_BY_ID = 'v1/specification/attribute/source/{}'

    # Удаление атрибута по ID
    DELETE_ATTRIBUTE_BY_ID = 'v1/specification/attribute/{}'

    # Создание значение атрибута мениселект
    CREATE_ATTRIBUTE_VALUE = 'v1/specification/attribute/{}/value'

    # Получение атрибута по ID
    GET_ATTRIBUTE_BY_ID = 'v1/specification/attribute/{}'

    # Изменение атрибута по ID
    PATCH_ATTRIBUTE_BY_ID = 'v1/specification/attribute/{}'

    # Скрытие значения атрибута у созданного атрибута мэниселект
    PATCH_ATTRIBUTE_VALUE_BY_ID = 'v1/specification/attribute/{}/value'

    # Получение спецификации по ID
    GET_SPECIFICATION_BY_ID = 'v1/specification/{}'

    # Удаление спецификации по ID
    DELETE_SPECIFICATION_BY_ID = 'v1/specification/{}'

    # Изменение спецификации по ID
    PATCH_SPECIFICATION_BY_ID = 'v1/specification/{}'

    # Удаление всех атрибутов из спецификации
    DELETE_ATTRIBUTE_FROM_SPECIFICATION = 'v1/specification/{}/attribute'

    # Управление атрибутами внутри спецификации
    MANAGE_ATTRIBUTES_IN_SPECIFICATION = 'v1/specification/{}/attributes/manage'


class SpecificationApi(SpecificationApiUrl):

    @property
    def text(self):
        return Gen.generate_text(7).replace(' ', '') + 'test'

    @allure.step('Получение даты для manage_specification')
    def get_data_manage_spec(self, attribute_id: str, is_required: bool = None):
        if is_required is not None:
            return {
                'attributeIdsToAdd': [
                    {
                        'id': attribute_id,
                        'required': is_required
                    }
                ],
                'attributeIdsToRemove': []
            }
        else:
            return {
                'attributeIdsToAdd': [],
                'attributeIdsToRemove': [
                    attribute_id
                ]
            }

    @allure.step('Получение данных для атрибута')
    def get_data_for_attribute(self, new_data: dict[str, Any] = None):
        data = {
            'id': '',
            'code': '',
            'name': self.text + ' test',
            'description': '123',
            'type': 'string',
            'maxCount': 1,
            'minCount': 1,
            'isActive': True,
            'isMultiple': False,
            'canDelete': False,
            'createdAt': '',
            'specificationLink': [],
            'values': [],
            'group': {
                'id': '',
                'name': ''
            },
            'usageType': 'user',
            'formula': '',
            'reasonForDeletion': 'Не определено',
            'specifications': []
        }
        if new_data:
            data.update(new_data)

        return data

    @allure.step('Получение всех спецификаций')
    def get_specifications(self, client) -> dict[str, Any]:
        response = client.get(self.GET_SPECIFICATIONS)

        Specifications(**response)

        return response

    @allure.step('Создание спецификации')
    def create_specification(self, client, data: dict[str, Any]) -> str:
        response = client.post(self.CREATE_SPECIFICATION, json=data)

        SpecificationCreation(**response)

        return response['id']

    @allure.step('Невалидное создание спецификации')
    def create_specification_400(self, client, data: dict[str, Any]) -> None:
        client.post(SpecificationApi.CREATE_SPECIFICATION, json=data, expected_status_code=400)

    @allure.step('Получение всех атрибутов')
    def get_attributes(self, client) -> dict[str, Any]:
        response = client.get(self.GET_ATTRIBUTES)

        Attributes(**response)

        return response

    @allure.step('Создание атрибута')
    def create_attribute(self, client, data: dict[str, Any]) -> str:
        response = client.post(self.CREATE_ATTRIBUTE, json=data)

        AttributeCreation(**response)

        return response['id']

    @allure.step('Невалидное создание атрибута')
    def create_attribute_400(self, client, data: dict[str, Any]) -> None:
        client.post(self.CREATE_ATTRIBUTE, json=data, expected_status_code=400)

    @allure.step('Получение всех источников')
    def get_source(self, client) -> dict[str, Any]:
        response = client.get(self.GET_SOURCES)

        Sources(**response)

        return response

    @allure.step('Создание источника')
    def create_source(self, client, data: dict[str, Any]) -> str:
        response = client.post(self.CREATE_SOURCE, json=data)

        SourceCreation(**response)

        return response['id']

    @allure.step('Невалидное создание источника')
    def create_source_400(self, client, data: dict[str, Any]) -> None:
        client.post(self.CREATE_SOURCE, json=data, expected_status_code=400)

    @allure.step('Получение источника по id')
    def get_source_by_id(self, client, source_id: str) -> dict[str, Any]:
        response = client.get(self.GET_SOURCE_BY_ID.format(source_id))

        SourceItem(**response)

        return response

    @allure.step('Невалидное получение источника по id')
    def get_source_by_id_400(self, client, source_id: str) -> None:
        client.get(self.GET_SOURCE_BY_ID.format(source_id), expected_status_code=400)

    @allure.step('Удаление источника по id')
    def delete_source_by_id(self, client, source_id: str) -> None:
        client.delete(self.DELETE_SOURCE_BY_ID.format(source_id))

    @allure.step('Изменение источника по id')
    def patch_source_by_id(self, client, source_id: str, data: dict[str, Any]) -> None:
        client.patch(self.PATCH_SOURCE_BY_ID.format(source_id),
                     json=data)

    @allure.step('Невалидное изменение источника по id')
    def patch_source_by_id_400(self, client, source_id: str, data: dict[str, Any]) -> None:
        client.patch(self.PATCH_SOURCE_BY_ID.format(source_id),
                     json=data, expected_status_code=400)

    @allure.step('Удаление атрибута по id')
    def delete_attribute_by_id(self, client, attribute_id: str) -> None:
        client.delete(self.DELETE_ATTRIBUTE_BY_ID.format(attribute_id))

    @allure.step('Создание значения атрибута по id')
    def create_attribute_value(self, client, attribute_id: str, data: dict[str, Any]) -> None:
        client.post(self.CREATE_ATTRIBUTE_VALUE.format(attribute_id),
                    json=data)

    @allure.step('Получение атрибута по id')
    def get_attribute_by_id(self, client, attribute_id: str) -> dict[str, Any]:
        response = client.get(self.GET_ATTRIBUTE_BY_ID.format(attribute_id))

        AttributeById(**response)

        return response

    @allure.step('Невалидное получение атрибута по id')
    def get_attribute_by_id_404(self, client, attribute_id: str) -> None:
        client.get(self.GET_ATTRIBUTE_BY_ID.format(attribute_id), expected_status_code=404)

    @allure.step('Изменение атрибута по id')
    def patch_attribute_by_id(self, client, attribute_id: str, data: dict[str, Any]) -> None:
        client.patch(self.PATCH_ATTRIBUTE_BY_ID.format(attribute_id),
                     json=data)

    @allure.step('Невалидное изменение атрибута по id')
    def patch_attribute_by_id_400(self, client, attribute_id: str, data: dict[str, Any]) -> None:
        client.patch(self.PATCH_ATTRIBUTE_BY_ID.format(attribute_id),
                     json=data, expected_status_code=400)

    @allure.step('Изменение значения атрибута по id')
    def patch_attribute_value_by_id(self, client, value_id: str, value: str, is_active: bool,
                                    attribute_id: str = '39e22a59-e85b-41a9-9044-8fcdbcb20e62') -> None:
        data = {
            'value': value,
            'attributeId': attribute_id,
            'isActive': is_active
        }
        client.patch(self.PATCH_ATTRIBUTE_VALUE_BY_ID.format(value_id),
                     json=data)

    @allure.step('Получение спецификации по id')
    def get_specification_by_id(self, client, specification_id: str) -> dict[str, Any]:
        response = client.get(self.GET_SPECIFICATION_BY_ID.format(specification_id))

        SpecificationById(**response)

        return response

    @allure.step('Невалидное получение спецификации по id')
    def get_specification_by_id_404(self, client, specification_id: str) -> None:
        client.get(self.GET_SPECIFICATION_BY_ID.format(specification_id), expected_status_code=404)

    @allure.step('Удаление спецификации по id')
    def delete_specification_by_id(self, client, specification_id: str) -> None:
        client.delete(self.DELETE_SPECIFICATION_BY_ID.format(specification_id))

    @allure.step('Изменение названия спецификации по id')
    def patch_specification_by_id(self, client, specification_id: str, data: dict[str, Any]) -> None:
        client.patch(self.PATCH_SPECIFICATION_BY_ID.format(specification_id),
                     json=data)

    @allure.step('Невалидное изменение названия спецификации по id')
    def patch_specification_by_id_404(self, client, specification_id: str, data: dict[str, Any]) -> None:
        client.patch(self.PATCH_SPECIFICATION_BY_ID.format(specification_id),
                     json=data, expected_status_code=404)

    @allure.step('Невалидное изменение названия спецификации по id')
    def patch_specification_by_id_400(self, client, specification_id: str, data: dict[str, Any]) -> None:
        client.patch(self.PATCH_SPECIFICATION_BY_ID.format(specification_id),
                     json=data, expected_status_code=400)

    @allure.step('Изменение тоглов атрибутов внутри спецификации')
    def manage_attributes_in_specification(self, client, specification_id: str, data: dict[str, Any]) -> None:
        client.post(self.MANAGE_ATTRIBUTES_IN_SPECIFICATION.format(specification_id),
                    json=data)

    @allure.step('Полный цикл создания и удаления атрибута')
    def full_cycle_attr(self, client, data: dict[str, Any]) -> None:
        attribute_id = self.create_attribute(client, data)

        with allure.step('Проверяем, что атрибут создался'):
            self.get_attribute_by_id(client, attribute_id)

        self.delete_attribute_by_id(client, attribute_id)

        with allure.step('Проверяем, что атрибут удалился'):
            self.get_attribute_by_id_404(client, attribute_id)
