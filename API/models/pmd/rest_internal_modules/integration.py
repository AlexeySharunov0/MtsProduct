import warnings
from typing import Any

import allure
import requests

from API.data.pmd import Integrations
from API.utils.headers import JIRA_TOKEN
from API.utils.helpers import assert_status_code

warnings.filterwarnings("ignore", message="numpy.dtype size changed")

HOST = 'https://stage.prodboard.example.com'


class IntegrationUrls:
    """
    https://stage.prodboard.example.com/pmd/swagger/rest/internal/index.html#/
    """

    #### INTEGRATION

    # Получение информации по изменениям статусов в Изменения свойств продуктов.
    RECORDS = 'v2/integration/monetization-console-records'

    # Запись сообщения из кафки
    RECORD_ACCEPT = 'v2/product/integration'


class Integration(IntegrationUrls):
    #### INTEGRATION

    @allure.step('Получение информации по изменениям Статусов')
    def get_integration_records(self, client) -> list[dict[str, Any]]:
        response = client.get(self.RECORDS)

        Integrations(integrations=response)

        return response

    def accept_integration_record(self, client, record_id):
        data = {
            'integrationType': 'status',
            'recordId': record_id,
            'sendNotification': True
        }

        client.post(self.RECORD_ACCEPT, json=data)

    @allure.step('Получение информации по проектам из jira')
    def get_project_from_jira(self, bi_code):
        response = requests.get(
            f'https://jira.example.com/rest/scriptrunner/latest/custom/projectAttributes?ppinfo_productcode={bi_code}',
            verify=False, headers=JIRA_TOKEN)
        assert_status_code(response)
        return response.json()
