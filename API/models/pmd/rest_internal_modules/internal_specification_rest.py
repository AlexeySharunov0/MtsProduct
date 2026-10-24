import warnings
from typing import Any

import allure

from API.data.pmd import OracleValidate, IndividualSpecification

warnings.filterwarnings("ignore", message="numpy.dtype size changed")

HOST = 'https://stage.prodboard.example.com'


class InternalSpecificationUrls:
    """
    https://stage.prodboard.example.com/pmd/swagger/rest/internal/index.html#/
    """

    #### INTERNAL SPECIFICATION

    # Валидация уникального кода oracle
    VALIDATE_ORACLE = 'v1/specification/validate/oracleCode/{}'

    # Получение уникальной спецификации
    GET_SPECIFICATION = 'v1/specification/form/{}'


class InternalSpecification(InternalSpecificationUrls):

    #### INTERNAL SPECIFICATION
    @allure.step('Валидация кода оракл')
    def validate_oracle(self, client, oracle_code: str) -> dict[str, Any]:
        response = client.get(self.VALIDATE_ORACLE.format(oracle_code))

        OracleValidate(**response)

        return response

    @allure.step('Получаем индивидуальную спецификацию')
    def get_individual_specification(self, client, form_id: str) -> list[dict[str, Any]]:
        response = client.get(self.GET_SPECIFICATION.format(form_id))

        IndividualSpecification(attributes=response)

        return response
