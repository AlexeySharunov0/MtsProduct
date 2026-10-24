import re
import warnings

import allure
import pytest

from API.models.kafka_external_message.kafka_external_message import KafkaExternal
from API.models.pmd.rest_internal_modules.integration import Integration
from API.models.pmd.rest_internal_modules.internal_product import InternalProduct
from API.models.ppinfo.product_v2 import ProductV2

warnings.filterwarnings('ignore', message='numpy.dtype size changed')


#### INTEGRATION
@pytest.mark.api
@allure.feature('Интеграции')
class TestIntegrationsApi(InternalProduct, Integration, ProductV2, KafkaExternal):

    @allure.title('Отправляем сообщение в Kafka с атрибутом Дата Запуска Пилота')
    @pytest.mark.parametrize('attribute, status', [('PPinfo_start_date_MVP', '(PPinfo_status)Pilot'),
                                                   ('PPinfo_close_date', 'Arkhiv'),
                                                   ('PPinfo_execution_date', '(PPinfo_status)In_use'),
                                                   ('PPinfo_finish_date_MVP', '(PPinfo_status)Pilot')])
    def test_send_message_kafka(self, pmd_admin_rest_client, ppinfo_client, attribute, status):

        with allure.step('Отправляем сообщение в Kafka'):
            self.message_send_to_kafka_monetization_console(attribute_id=attribute)

        message = self.get_integration_records(pmd_admin_rest_client)
        with allure.step('Забираем сообщение от бека и проверяем правильное ли сообщение пришло'):
            assert message[0]['receivedStatus'] is not None, 'receivedStatus пустой'
            assert message[0]['receivedStatus'][
                       'statusCode'] == status, f'Статус в сообщении неверный: {message[0]["receivedStatus"]["statusCode"]}'

        with allure.step('Записываем изменение статуса и проверяем изменился ли статус продукта'):
            self.accept_integration_record(ppinfo_client, message[0]['id'])
            product = self.get_info_by_product_code(ppinfo_client, 'BI_56907')

            try:
                assert product['status'][
                           'code'] == status, f'Статус в продукте после записи неверный: {product["status"]["code"]}'
                self.change_status(ppinfo_client, '(PPinfo_status)Waiting_decision', 'Ожидание решения', 'BI_56907')
            except AssertionError as e:
                self.change_status(ppinfo_client, '(PPinfo_status)Waiting_decision', 'Ожидание решения', 'BI_56907')
                raise e

    @allure.title('Получаем статусы которые были получены через брокер сообщений')
    def test_integration_records(self, pmd_admin_rest_client):
        self.get_integration_records(pmd_admin_rest_client)

    @allure.title('Проверка корректности атрибутов из Jira')
    @allure.issue('https://jira.mts.ru/browse/PPI-3811', 'PPInfo - Не отображать архивные проекты Jira в МТС Product')
    @pytest.mark.parametrize('bi_code', ['BI_307'])
    def test_jira_attributes(self, ppinfo_client, bi_code):

        projects_in_product = []

        for attr in self.get_info_by_product_code(ppinfo_client, bi_code)['hidingAttributes']:
            if attr['id'] == 'SYSTEM_Jira':
                for project in attr['values']:
                    projects_in_product.append(project['value'])

        projects_in_product = [re.sub(r" \([^)]*\)", "", elem) for elem in projects_in_product]

        projects_in_jira = []

        for project in self.get_project_from_jira(bi_code):
            if not project['archived']:
                projects_in_jira.append(project['project_name'])

        assert projects_in_product == projects_in_jira, 'Атрибуты не совпадают'
