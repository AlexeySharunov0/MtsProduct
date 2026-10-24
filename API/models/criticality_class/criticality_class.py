import time
from typing import Any

import allure

from API.data.criticality_class import IntegrationsCriticalityClass
from API.models.ppinfo.rest import Rest


class CriticalityClassUrls:
    # Создание сообщения об изменении Класса критичности
    CRITICALITY_CLASS = 'v1/product/document'

    # Получение списка изменений по Классу Критичности
    CRITICALITY_CLASS_RECORDS = 'v2/integration/criticality-class-records'

    # Запись изменений по Классу Критичности
    INTEGRATION = 'v2/product/integration'


class CriticalityClass(CriticalityClassUrls, Rest):

    @allure.step('Заполняем данные для Класса критичности')
    def data_criticality_class(self, params: dict[str, Any] | None = None, product_code: str = "BI_2970") -> dict[
        str, str]:
        data = {"productId": product_code,
                "orderNumber": "J00000000044022",
                "orderAuthorLogin": "admin_user",
                "documentUrls": [
                    "https://ap.example.com/s3/jocasta-stage-taskfiles/14f681fc-18e4-4f3b-b546-e89aae23edac"
                ],
                "productCriticalityClass": "Business Support"}
        if params:
            data.update(params)

        return data

    @allure.step('Создаем сообщение на изменение/добавление класса критичности')
    def create_criticality_class_message(self, client, data: dict[str, Any]) -> str:

        response = client.post(self.CRITICALITY_CLASS, json=data, raw_format=True)

        time.sleep(3)

        return response.text.strip('"')

    @allure.step('Получение информации по изменениям Класса критичности')
    def get_integration_records_criticality_class(self, client) -> list[dict[str, Any]]:

        response = client.get(self.CRITICALITY_CLASS_RECORDS)

        IntegrationsCriticalityClass(integrations_cc=response)

        return response

    @allure.step('Генерация тела для записи изменения Класса Критичности')
    def data_approve_criticality_class(self, record_id: str, params: dict[str, Any] | None = None) -> dict[str, str]:
        data = {
            "recordId": record_id,
            "sendNotification": True,
            "integrationType": "criticalityClass"
        }
        if params:
            data.update(params)

        return data

    @allure.step("Запись изменения Класса критичности")
    def approve_criticality_class(self, client, data: dict[str, Any]) -> None:

        client.post(self.INTEGRATION, json=data)

    @allure.step('Проверка Класса Критичности в продукте')
    def check_cc_in_product(self, client, cc_value: str) -> None:
        for attr in self.get_info_by_product_code(client, 'BI_2970')['hidingAttributes']:
            if attr['id'] == 'PPInfo_class_criticality':
                fr_cc_value = attr['values'][0]['value']
                assert fr_cc_value == cc_value, f'Значение класса критичности не соответствует ожидаемому \n ОР - {cc_value} \n ФР - {fr_cc_value}'

    @allure.step('Получение кол-ва документов в продукте')
    def check_cc_documents(self, rest_internal_client) -> int:
        return len(self.get_docs_by_bi_code(rest_internal_client, 'BI_2970')['documents'])
