import allure
import pytest

from API.api_fixtures import pmd_admin_rest_client
from API.models.criticality_class.criticality_class import CriticalityClass


@pytest.mark.api
@allure.feature("Класс критичности")
@allure.issue('https://jira.mts.ru/browse/PPI-1865',
              'PPInfo - Добавление документа "Класс критичности" из Service Desk')
@allure.issue('https://jira.mts.ru/browse/PPI-2195', 'PPInfo - Раздел "Изменение класса критичности"')
class TestCriticalityClass(CriticalityClass):

    @allure.title('Сообщение об изменении класс критичности отображается в списке')
    def test_create_cc_message(self, rest_external_client, pmd_admin_rest_client):
        cc_message_id = self.create_criticality_class_message(rest_external_client, self.data_criticality_class())

        assert any(item['id'] == cc_message_id for item in
                   self.get_integration_records_criticality_class(
                       pmd_admin_rest_client)), 'Созданное сообщение об изменении класс критичности не появилось в списке'

    @allure.title('Запись изменения класса критичности')
    @pytest.mark.parametrize('cc_value', ['Business Critical', 'Business Support', 'Mission Critical'])
    def test_approve_cc_message(self, rest_external_client, pmd_admin_rest_client, ppinfo_client, cc_value):
        cc_message_id = self.create_criticality_class_message(rest_external_client, self.data_criticality_class(
            {"productCriticalityClass": cc_value}))

        assert any(item['id'] == cc_message_id for item in
                   self.get_integration_records_criticality_class(
                       pmd_admin_rest_client)), 'Созданное сообщение об изменении класс критичности не появилось в списке'

        self.approve_criticality_class(ppinfo_client, self.data_approve_criticality_class(cc_message_id))

        self.check_cc_in_product(ppinfo_client, cc_value)

    @allure.title('При получении сообщения об изменение Класса критичности в продукт добавляется документ')
    @pytest.mark.parametrize('cc_value', ['Business Critical', 'Business Support', 'Mission Critical'])
    def test_add_cc_document(self, rest_internal_client, rest_external_client, cc_value):
        count_documents = self.check_cc_documents(rest_internal_client)
        self.create_criticality_class_message(rest_external_client,
                                              self.data_criticality_class({'productCriticalityClass': cc_value}))
        count_documents_after_message = self.check_cc_documents(rest_internal_client)

        assert count_documents < count_documents_after_message, 'После появления сообщения об изменения Класса критичности документ в продукт не добавлен'
