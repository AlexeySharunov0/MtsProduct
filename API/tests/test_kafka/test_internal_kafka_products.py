import json
import time

import allure
import pytest

from API.models.kafka_external_message.kafka_external_message import KafkaExternal
from API.models.pmd.admin_role_model import RoleModelApi
from API.models.pmd.admin_specification import SpecificationApi
from API.models.ppinfo.product_v1 import ProductV1


@allure.issue('https://jira.mts.ru/browse/PPI-3291', 'Передача сообщений системам потребителям')
@pytest.mark.last
class TestKafkaInternal(KafkaExternal, ProductV1, SpecificationApi, RoleModelApi):
    @allure.title('Изменение текстового атрибута и проверка сообщения из Kafka')
    @pytest.mark.parametrize('string, value',
                             [['string_add', [{'value': 'test'}]], ['string_replace', [{'value': 'test2'}]]])
    def test_get_kafka_message_string(self, ppinfo_client, string, value):

        data = self.get_attribute_update_body(string)
        self.change_product(ppinfo_client, data)
        time.sleep(1)
        message = self.message_get_from_kafka_internal_products()

        print(message)

        for item in message['data']['current']['attributes']:
            if item['code'] == 'PPInfo_showcase':
                assert item['values'][0]['value'] == value[0]['value'], 'Значения в кафке неверные'
                break
        else:
            assert False, 'Аттрибут не найден в сообщении кафки'

    @allure.title('Изменение мениселекта и проверка сообщения из Kafka')
    @pytest.mark.parametrize('string, value',
                             [['manyselect_add',
                               [{'code': '(PPInfo_spravochnic_Structural)Main', 'value': 'Основной'}]],
                              ['manyselect_replace',
                               [{'code': '(PPInfo_spravochnic_Structural)Atomic', 'value': 'Атомарный'}]]])
    def test_get_kafka_message_manyselect(self, ppinfo_client, string, value):
        data = self.get_attribute_update_body(string)
        self.change_product(ppinfo_client, data)
        time.sleep(1)
        message = self.message_get_from_kafka_internal_products()

        for item in message['data']['current']['attributes']:
            if item['code'] == 'PPinfo_StructuralProductType1':
                assert item['values'][0]['value'] == value[0]['value'], 'Значения в кафке неверные'
                break
        else:
            assert False, 'Аттрибут не найден в сообщении кафки'

    @allure.title('Изменение даты и проверка сообщения из Kafka')
    @pytest.mark.parametrize('string, value',
                             [['date_add', [{'value': '2024-01-23T03:00:00Z'}]],
                              ['date_replace', [{'value': '2024-01-24T03:00:00Z'}]]])
    def test_get_kafka_message_date(self, ppinfo_client, string, value):
        data = self.get_attribute_update_body(string)
        self.change_product(ppinfo_client, data)
        time.sleep(1)
        message = self.message_get_from_kafka_internal_products()

        for item in message['data']['current']['attributes']:
            if item['code'] == 'PPinfo_start_close_date':
                assert item['values'][0]['value'] == value[0]['value'], 'Значения в кафке неверные'
                break
        else:
            assert False, 'Аттрибут не найден в сообщении кафки'

    @allure.title('Изменение числа и проверка сообщения из Kafka')
    @pytest.mark.parametrize('string, value',
                             [['num_add', [{'value': '666'}]],
                              ['num_replace', [{'value': '777'}]]])
    def test_get_kafka_message_num(self, ppinfo_client, string, value):
        data = self.get_attribute_update_body(string)
        self.change_product(ppinfo_client, data)
        time.sleep(1)
        message = self.message_get_from_kafka_internal_products()

        for item in message['data']['current']['attributes']:
            if item['code'] == 'Identifikator_SOL':
                assert item['values'][0]['value'] == value[0]['value'], 'Значения в кафке неверные'
                break
        else:
            assert False, 'Аттрибут не найден в сообщении кафки'

    @allure.title('Изменение юзера и проверка сообщения из Kafka')
    @pytest.mark.parametrize('string, value',
                             [['user_add', [{'value': 'Светов Даниил Дмитриевич (ddsvetov1)'}]],
                              ['user_replace', [{'value': 'Гладышева Алёна Ивановна (aigladyshev)'}]]])
    def test_get_kafka_message_user(self, ppinfo_client, string, value):
        data = self.get_attribute_update_body(string)
        self.change_product(ppinfo_client, data)
        time.sleep(1)
        message = self.message_get_from_kafka_internal_products()

        for item in message['data']['current']['attributes']:
            if item['code'] == 'employee_business_owner':
                assert item['values'][0]['value'] == value[0]['value'], 'Значения в кафке неверные'
                break
        else:
            assert False, 'Аттрибут не найден в сообщении кафки'

    @allure.title('Изменение множества и проверка сообщения из Kafka')
    @pytest.mark.parametrize('string, value',
                             [['multi_add', [{"code": "Vtoroi", "value": "Второй"},
                                             {"code": "Pervyi", "value": "Первый"},
                                             {"code": "Tretii", "value": "Третий"}]],
                              ['multi_replace', [{"code": "Vtoroi", "value": "Второй"}]]])
    def test_get_kafka_message_multi(self, ppinfo_client, string, value):
        data = self.get_attribute_update_body(string)
        self.change_product(ppinfo_client, data)
        time.sleep(1)
        message = self.message_get_from_kafka_internal_products()

        for item in message['data']['current']['attributes']:
            if item['code'] == 'Mnozhestvo':
                assert item['values'][0]['value'] == value[0]['value'], 'Значения в кафке неверные'
                break
        else:
            assert False, 'Аттрибут не найден в сообщении кафки'

    @allure.title('Изменение multiuser и проверка сообщения из Kafka')
    @pytest.mark.parametrize('string, value', [
        ['multiuser_add',
         [{'code': '', 'value': 'Масленков Павел Юрьевич (pymaslenkov)', 'createdAt': '0001-01-01T00:00:00Z'},
          {'code': '', 'value': 'Светов Даниил Дмитриевич (ddsvetov1)', 'createdAt': '0001-01-01T00:00:00Z'},
          {'code': '', 'value': 'Костров Алексей Игоревич (aikostrov1)', 'createdAt': '0001-01-01T00:00:00Z'}]],
        ['multiuser_replace_minus', [{'code': '',
                                      'createdAt': '0001-01-01T00:00:00Z',
                                      'value': 'Масленков Павел Юрьевич (pymaslenkov)'},
                                     {'code': '',
                                      'createdAt': '0001-01-01T00:00:00Z',
                                      'value': 'Светов Даниил Дмитриевич (ddsvetov1)'}]],
        ['multiuser_replace_plus',
         [{'code': '',
           'createdAt': '0001-01-01T00:00:00Z',
           'value': 'Масленков Павел Юрьевич (pymaslenkov)'},
          {'code': '',
           'createdAt': '0001-01-01T00:00:00Z',
           'value': 'Светов Даниил Дмитриевич (ddsvetov1)'},
          {'code': '',
           'createdAt': '0001-01-01T00:00:00Z',
           'value': 'Костров Алексей Игоревич (aikostrov1)'}]]])
    def test_get_kafka_message_multiuser(self, ppinfo_client, string, value):
        data = self.get_attribute_update_body(string)
        self.change_product(ppinfo_client, data)
        message = self.message_get_from_kafka_internal_products()

        print(message)

        for item in message['data']['current']['attributes']:
            if item['code'] == 'Rukovoditel_etogo_balagana':
                assert item['values'] == value, 'Значения в кафке неверные'
                break
        else:
            assert False, 'Аттрибут не найден в сообщении кафки'

    @allure.title('Изменение один продукт и проверка сообщения из Kafka')
    @pytest.mark.parametrize('string, value', [
        ['product_add', [{'code': '', 'value': 'МТС Маркетолог (BI_60)'}]],
        ['product_replace', [{'code': '', 'value': 'Kaspersky Security для МТС (BI_25)'}]]])
    def test_get_kafka_message_odin_product(self, ppinfo_client, string, value):
        data = self.get_attribute_update_body(string)
        self.change_product(ppinfo_client, data)
        time.sleep(1)
        message = self.message_get_from_kafka_internal_products()
        print(message)

        for item in message['data']['current']['attributes']:
            if item['code'] == 'Odin_produkt':
                assert item['values'][0]['value'] == value[0]['value'], 'Значения в кафке неверные'
                break
        else:
            assert False, 'Аттрибут не найден в сообщении кафки'

    @allure.title('Изменение мультипродукт и проверка сообщения из Kafka')
    @pytest.mark.parametrize('string, value', [
        ['multiproduct_add', [
            {'code': '', 'value': 'GPS-Трекер с МТС Поиск (BI_270)', 'createdAt': '0001-01-01T00:00:00Z'},
            {'code': '', 'value': 'Kaspersky Security для МТС (BI_25)', 'createdAt': '0001-01-01T00:00:00Z'},
            {'code': '', 'value': 'Весь МТС (BI_1901)', 'createdAt': '0001-01-01T00:00:00Z'},
            {'code': '', 'value': 'Весь МТС Полный дом (BI_1972)', 'createdAt': '0001-01-01T00:00:00Z'}]],
        ['multiproduct_replace_minus', [
            {'code': '', 'value': 'Весь МТС Полный дом (BI_1972)',
             'createdAt': '0001-01-01T00:00:00Z'},
            {'code': '', 'value': 'GPS-Трекер с МТС Поиск (BI_270)',
             'createdAt': '0001-01-01T00:00:00Z'},
            {'code': '', 'value': 'Kaspersky Security для МТС (BI_25)',
             'createdAt': '0001-01-01T00:00:00Z'}]],
        ['multiproduct_replace_plus', [
            {'code': '', 'value': 'Kaspersky Security для МТС (BI_25)',
             'createdAt': '0001-01-01T00:00:00Z'},
            {'code': '', 'value': 'Весь МТС Полный дом (BI_1972)',
             'createdAt': '0001-01-01T00:00:00Z'},
            {'code': '', 'value': 'GPS-Трекер с МТС Поиск (BI_270)',
             'createdAt': '0001-01-01T00:00:00Z'},
            {'code': '', 'value': 'МТС Маркетолог. Скоринг (BI_1984)',
             'createdAt': '0001-01-01T00:00:00Z'}]]])
    def test_get_kafka_message_multiproduct(self, ppinfo_client, string, value):
        data = self.get_attribute_update_body(string)
        self.change_product(ppinfo_client, data)
        time.sleep(1)
        message = self.message_get_from_kafka_internal_products()

        for item in message['data']['current']['attributes']:
            if item['code'] == 'Mnogo_produktov':
                assert item['values'][0]['value'] == value[0]['value'], 'Значения в кафке неверные'
                break
        else:
            assert False, 'Аттрибут не найден в сообщении кафки'

    @allure.title('Изменение мультиссылка и проверка сообщения из Kafka')
    @pytest.mark.parametrize('string, value', [
        ('multilink_add',
         [{'name': 'Название ссылки1', 'value': 'Линк1'}, {'name': 'Название ссылки2', 'value': 'Линк2'}]),
        ('multilink_replace_minus', [{'name': 'Название ссылки1', 'value': 'Линк1'}]),
        ('multilink_replace_plus',
         [{'name': 'Название ссылки1', 'value': 'Линк1'}, {'name': 'Название ссылки2', 'value': 'Линк2'}])])
    def test_get_kafka_message_multilink(self, ppinfo_client, string, value):
        data = self.get_attribute_update_body(string)
        self.change_product(ppinfo_client, data)
        time.sleep(1)
        message = self.message_get_from_kafka_internal_products()
        values = []

        for item in message['data']['current']['attributes']:
            if item['code'] == 'Test_mnozh_ssylki':
                for val in item['values']:
                    values.append({key: val for key, val in json.loads(val['value']).items() if key != 'id'})
                assert values == value, 'Значения в кафке неверные'
                break
        else:
            assert False, 'Аттрибут не найден в сообщении кафки'

    @allure.title('Изменение многострочный текст и проверка сообщения из Kafka')
    @pytest.mark.parametrize('string, value', [
        ['multistring_add', [{'value': 'test'}]],
        ['multistring_replace', [{'value': 'test2'}]]])
    def test_get_kafka_message_manystring(self, ppinfo_client, string, value):
        data = self.get_attribute_update_body(string)
        self.change_product(ppinfo_client, data)
        time.sleep(1)
        message = self.message_get_from_kafka_internal_products()

        for item in message['data']['current']['attributes']:
            if item['code'] == 'PPinfo_resolution':
                assert item['values'][0]['value'] == value[0]['value'], 'Значения в кафке неверные'
                break
        else:
            assert False, 'Аттрибут не найден в сообщении кафки'

    @allure.title('Изменение ссылка текст и проверка сообщения из Kafka')
    @pytest.mark.parametrize('string, value', [
        ['link_add', [{'name': None, 'value': 'https://cashback.mts.ru'}]],
        ['link_replace', [{'name': None, 'value': 'https://stage.prodboard.mts.ru/product/BI_42/main'}]]])
    def test_get_kafka_message_link(self, ppinfo_client, string, value):
        data = self.get_attribute_update_body(string)
        self.change_product(ppinfo_client, data)
        time.sleep(1)
        message = self.message_get_from_kafka_internal_products()

        values = []

        for item in message['data']['current']['attributes']:
            if item['code'] == 'PPInfo_site_landing':
                for val in item['values']:
                    values.append({key: val for key, val in json.loads(val['value']).items() if key != 'id'})
                assert values == value, 'Значения в кафке неверные'
                break
        else:
            assert False, 'Аттрибут не найден в сообщении кафки'

    @allure.title('Изменение основного продукта текст и проверка сообщения из Kafka')
    @pytest.mark.parametrize('string, value', [
        ['main_product_add', [{'code': '', 'value': '1_Не трогать, для АТ, делегирование del (BI_2683)',
                               'createdAt': '0001-01-01T00:00:00Z'}]],
        ['main_product_replace',
         [{'code': '', 'value': 'Не трогать (продукт для автотестов) (BI_3266)', 'createdAt': '0001-01-01T00:00:00Z'}]]])
    def test_get_kafka_message_main_product(self, ppinfo_client, string, value):
        data = self.get_attribute_update_body(string)
        self.change_product(ppinfo_client, data)
        time.sleep(1)
        message = self.message_get_from_kafka_internal_products()

        for item in message['data']['current']['attributes']:
            if item['code'] == 'PPInfo_main_product':
                assert item['values'][0]['value'] == value[0]['value'], 'Значения в кафке неверные'
                break
        else:
            assert False, 'Аттрибут не найден в сообщении кафки'
