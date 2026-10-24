from typing import Any

import allure

from API.data.pmd import PublicSpecifications, PublicAttributes, PublicAttributesByCode

HOST = 'https://stage.prodboard.example.com'


class PublicSpecificationUrls:
    """
    https://stage.prodboard.example.com/pmd/swagger/public/specification/index.html#/
    """
    # Получение всех спецификаций
    GET_SPECIFICATIONS = 'v1/specification'

    # Получение атрибутов по коду атрибута
    GET_ATTRIBUTES_BY_CODE = 'v1/specification/attribute'

    # Получение спецификации по коду Vneshnii или Vnetrennii
    GET_SPECIFICATION_BY_CODE = 'v1/specification/{}/code'

    # Получение определенной спецификации по ID
    GET_SPECIFICATION_BY_ID = 'v1/specification/{}'


class PublicSpecification(PublicSpecificationUrls):

    @allure.step('Получение всех спецификаций')
    def get_specifications(self, client) -> dict[str, Any]:
        response = client.get(self.GET_SPECIFICATIONS)

        PublicSpecifications(**response)

        return response

    @allure.step('Получение атрибутов по code')
    def get_attributes_by_code(self, client, attribute_code: dict[str, Any]) -> dict[str, Any]:
        response = client.get(self.GET_ATTRIBUTES_BY_CODE, params=attribute_code)

        PublicAttributes(**response)

        return response

    @allure.step('Получение спецификации по code')
    def get_specification_by_code(self, client, specification_code: str) -> dict[str, Any]:
        response = client.get(self.GET_SPECIFICATION_BY_CODE.format(specification_code))

        PublicAttributesByCode(**response)
        return response

    @allure.step('Невалидное получение спецификации по code')
    def get_specification_by_code_404(self, client, specification_code: str) -> None:
        client.get(self.GET_SPECIFICATION_BY_CODE.format(specification_code), expected_status_code=404)

    @allure.step('Получение спецификации по id')
    def get_specification_by_id(self, client, specification_id: str) -> dict[str, Any]:
        response = client.get(self.GET_SPECIFICATION_BY_ID.format(specification_id))

        PublicAttributesByCode(**response)

        return response

    @allure.step('Инвалидное получение спецификации по id')
    def get_specification_by_id_400(self, client, specification_id: str) -> None:
        client.get(self.GET_SPECIFICATION_BY_ID.format(specification_id), expected_status_code=400)
