from typing import Any

import allure

from API.data.pmd import InternalAttributes

HOST = 'https://stage.prodboard.example.com'


class InternalSpecificationUrls:
    """
    https://stage.prodboard.example.com/pmd/swagger/internal/v1/specification/index.html#/
    """

    # Получение спецификации по логину и коду в заявках
    GET_SPECIFICATION_BY_CODE_AND_LOGIN = 'v1/specification/{}'


class InternalSpecification(InternalSpecificationUrls):

    @allure.step('Получение спецификации по логину')
    def get_specification_by_code_and_login(self, client, specification_code: str, login: str = None) -> dict[str, Any]:
        response = client.get(self.GET_SPECIFICATION_BY_CODE_AND_LOGIN.format(specification_code),
                              params=login)

        InternalAttributes(**response)

        return response

    @allure.step('Невалидное получение спецификации по логину')
    def get_specification_by_code_and_login_404(self, client, specification_code: str, login: str = None) -> None:
        client.get(self.GET_SPECIFICATION_BY_CODE_AND_LOGIN.format(specification_code),
                   params=login, expected_status_code=404)
