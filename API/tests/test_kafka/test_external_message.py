import time

import allure
import pytest

from API.models.kafka_external_message.kafka_external_message import KafkaExternal
from API.models.pmd.admin_role_model import RoleModelApi
from API.models.pmd.admin_specification import SpecificationApi
from API.models.ppinfo.product_v1 import ProductV1
from API.models.ppinfo.tag import Tag


@allure.issue('https://jira.mts.ru/browse/PPI-3291', 'Передача сообщений системам потребителям')
@pytest.mark.last
class TestKafkaExternal(KafkaExternal, ProductV1, SpecificationApi, RoleModelApi, Tag):
    @allure.title('Изменение текстового атрибута и проверка сообщения из Kafka')
    @pytest.mark.parametrize('string, value',
                             [['string_add', [{'value': 'test'}]], ['string_replace', [{'value': 'test2'}]],
                              ['string_remove', []]])
    def test_get_kafka_message_string(self, ppinfo_client, string, value):
        data = self.get_attribute_update_body(string)
        self.change_product(ppinfo_client, data)
        time.sleep(1)
        message = self.message_get_from_kafka_external()

        for item in message['data']['attributes']:
            if item['code'] == 'PPInfo_showcase':
                assert item['values'] == value, 'Значения в кафке неверные'
                break
        else:
            assert False, 'Аттрибут не найден в сообщении кафки'

    @allure.title('Изменение мениселекта и проверка сообщения из Kafka')
    @pytest.mark.parametrize('string, value',
                             [['manyselect_add',
                               [{'code': '(PPInfo_spravochnic_Structural)Main', 'value': 'Основной'}]],
                              ['manyselect_replace',
                               [{'code': '(PPInfo_spravochnic_Structural)Atomic', 'value': 'Атомарный'}]],
                              ['manyselect_remove', []]])
    def test_get_kafka_message_manyselect(self, ppinfo_client, string, value):
        data = self.get_attribute_update_body(string)
        self.change_product(ppinfo_client, data)
        time.sleep(1)
        message = self.message_get_from_kafka_external()

        for item in message['data']['attributes']:
            if item['code'] == 'PPinfo_StructuralProductType1':
                assert item['values'] == value, 'Значения в кафке неверные'
                break
        else:
            assert False, 'Аттрибут не найден в сообщении кафки'

    @allure.title('Изменение даты и проверка сообщения из Kafka')
    @pytest.mark.parametrize('string, value',
                             [['date_add', [{'value': '2024-01-23T03:00:00Z'}]],
                              ['date_replace', [{'value': '2024-01-24T03:00:00Z'}]],
                              ['date_remove', []]])
    def test_get_kafka_message_date(self, ppinfo_client, string, value):
        data = self.get_attribute_update_body(string)
        self.change_product(ppinfo_client, data)
        time.sleep(1)
        message = self.message_get_from_kafka_external()

        for item in message['data']['attributes']:
            if item['code'] == 'PPinfo_start_close_date':
                assert item['values'] == value, 'Значения в кафке неверные'
                break
        else:
            assert False, 'Аттрибут не найден в сообщении кафки'

    @allure.title('Изменение числа и проверка сообщения из Kafka')
    @pytest.mark.parametrize('string, value',
                             [['num_add', [{'value': '666'}]],
                              ['num_replace', [{'value': '777'}]],
                              ['num_remove', []]])
    def test_get_kafka_message_num(self, ppinfo_client, string, value):
        data = self.get_attribute_update_body(string)
        self.change_product(ppinfo_client, data)
        time.sleep(1)
        message = self.message_get_from_kafka_external()

        for item in message['data']['attributes']:
            if item['code'] == 'Identifikator_SOL':
                assert item['values'] == value, 'Значения в кафке неверные'
                break
        else:
            assert False, 'Аттрибут не найден в сообщении кафки'

    @allure.title('Изменение юзера и проверка сообщения из Kafka')
    @pytest.mark.parametrize('string, value',
                             [['user_add', [{'login': 'ddsvetov1'}]],
                              ['user_replace', [{'login': 'aigladyshev'}]],
                              ['user_remove', []]])
    def test_get_kafka_message_user(self, ppinfo_client, string, value):
        data = self.get_attribute_update_body(string)
        self.change_product(ppinfo_client, data)
        time.sleep(1)
        message = self.message_get_from_kafka_external()

        for item in message['data']['attributes']:
            if item['code'] == 'employee_business_owner':
                assert item['values'] == value, 'Значения в кафке неверные'
                break
        else:
            assert False, 'Аттрибут не найден в сообщении кафки'

    @allure.title('Изменение множества и проверка сообщения из Kafka')
    @pytest.mark.parametrize('string, value',
                             [['multi_add', [{"code": "Vtoroi", "value": "Второй"},
                                             {"code": "Pervyi", "value": "Первый"},
                                             {"code": "Tretii", "value": "Третий"}]],
                              ['multi_replace', [{"code": "Vtoroi", "value": "Второй"}]],
                              ['multi_remove', []]])
    def test_get_kafka_message_multi(self, ppinfo_client, string, value):
        data = self.get_attribute_update_body(string)
        self.change_product(ppinfo_client, data)
        time.sleep(1)
        message = self.message_get_from_kafka_external()

        for item in message['data']['attributes']:
            if item['code'] == 'Mnozhestvo':
                assert item['values'] == value, 'Значения в кафке неверные'
                break
        else:
            assert False, 'Аттрибут не найден в сообщении кафки'

    @allure.title('Изменение multiuser и проверка сообщения из Kafka')
    @pytest.mark.parametrize('string, value', [
        ['multiuser_add', [{'login': 'pymaslenkov'}, {'login': 'ddsvetov1'}, {'login': 'aikostrov1'}]],
        ['multiuser_replace_minus', [{'login': 'pymaslenkov'}, {'login': 'ddsvetov1'}]],
        ['multiuser_replace_plus', [{'login': 'pymaslenkov'}, {'login': 'ddsvetov1'}, {'login': 'aikostrov1'}]],
        ['multiuser_remove', []]])
    def test_get_kafka_message_multiuser(self, ppinfo_client, string, value):
        data = self.get_attribute_update_body(string)
        self.change_product(ppinfo_client, data)
        message = self.message_get_from_kafka_external()

        for item in message['data']['attributes']:
            if item['code'] == 'Rukovoditel_etogo_balagana':
                assert item['values'] == value, 'Значения в кафке неверные'
                break
        else:
            assert False, 'Аттрибут не найден в сообщении кафки'

    @allure.title('Изменение один продукт и проверка сообщения из Kafka')
    @pytest.mark.parametrize('string, value', [
        ['product_add', [{'code': 'BI_60', 'name': 'МТС Маркетолог'}]],
        ['product_replace', [{'code': 'BI_25', 'name': 'Kaspersky Security для МТС'}]],
        ['product_remove', []]])
    def test_get_kafka_message_odin_product(self, ppinfo_client, string, value):
        data = self.get_attribute_update_body(string)
        self.change_product(ppinfo_client, data)
        time.sleep(1)
        message = self.message_get_from_kafka_external()

        for item in message['data']['attributes']:
            if item['code'] == 'Odin_produkt':
                assert item['values'] == value, 'Значения в кафке неверные'
                break
        else:
            assert False, 'Аттрибут не найден в сообщении кафки'

    @allure.title('Изменение мультипродукт и проверка сообщения из Kafka')
    @pytest.mark.parametrize('string, value', [
        ['multiproduct_add', [
            {"code": "BI_270", "name": "GPS-Трекер с МТС Поиск"},
            {"code": "BI_25", "name": "Kaspersky Security для МТС"},
            {"code": "BI_1901", "name": "Весь МТС"},
            {"code": "BI_1972", "name": "Весь МТС Полный дом"}]],
        ['multiproduct_replace_minus', [
            {"code": "BI_1972", "name": "Весь МТС Полный дом"},
            {"code": "BI_270", "name": "GPS-Трекер с МТС Поиск"},
            {"code": "BI_25", "name": "Kaspersky Security для МТС"}]],
        ['multiproduct_replace_plus', [
            {'code': 'BI_25', 'name': 'Kaspersky Security для МТС'},
            {'code': 'BI_1972', 'name': 'Весь МТС Полный дом'},
            {'code': 'BI_270', 'name': 'GPS-Трекер с МТС Поиск'},
            {'code': 'BI_1984', 'name': 'МТС Маркетолог. Скоринг'}]],
        ['multiproduct_remove', []]])
    def test_get_kafka_message_multiproduct(self, ppinfo_client, string, value):
        data = self.get_attribute_update_body(string)
        self.change_product(ppinfo_client, data)
        time.sleep(1)
        message = self.message_get_from_kafka_external()

        for item in message['data']['attributes']:
            if item['code'] == 'Mnogo_produktov':
                assert item['values'] == value, 'Значения в кафке неверные'
                break
        else:
            assert False, 'Аттрибут не найден в сообщении кафки'

    @allure.title('Изменение мультиссылка и проверка сообщения из Kafka')
    @pytest.mark.parametrize('string, value', [
        ['multilink_add', [
            {'name': 'Название ссылки1', 'url': 'Линк1'}, {'name': 'Название ссылки2', 'url': 'Линк2'}]],
        ['multilink_replace_minus', [{'name': 'Название ссылки1', 'url': 'Линк1'}]],
        ['multilink_replace_plus', [
            {'name': 'Название ссылки1', 'url': 'Линк1'}, {'name': 'Название ссылки2', 'url': 'Линк2'}]],
        ['multilink_remove', []]])
    def test_get_kafka_message_multilink(self, ppinfo_client, string, value):
        data = self.get_attribute_update_body(string)
        self.change_product(ppinfo_client, data)
        time.sleep(1)
        message = self.message_get_from_kafka_external()

        for item in message['data']['attributes']:
            if item['code'] == 'Test_mnozh_ssylki':
                assert item['values'] == value, 'Значения в кафке неверные'
                break
        else:
            assert False, 'Аттрибут не найден в сообщении кафки'

    @allure.title('Изменение многострочный текст и проверка сообщения из Kafka')
    @pytest.mark.parametrize('string, value', [
        ['multistring_add', [{'value': 'test'}]],
        ['multistring_replace', [{'value': 'test2'}]],
        ['multistring_remove', []]])
    def test_get_kafka_message_manystring(self, ppinfo_client, string, value):
        data = self.get_attribute_update_body(string)
        self.change_product(ppinfo_client, data)
        time.sleep(1)
        message = self.message_get_from_kafka_external()

        for item in message['data']['attributes']:
            if item['code'] == 'PPinfo_resolution':
                assert item['values'] == value, 'Значения в кафке неверные'
                break
        else:
            assert False, 'Аттрибут не найден в сообщении кафки'

    @allure.title('Изменение ссылка текст и проверка сообщения из Kafka')
    @pytest.mark.parametrize('string, value', [
        ['link_add', [{'url': 'https://cashback.mts.ru'}]],
        ['link_replace', [{'url': 'https://stage.prodboard.mts.ru/product/BI_42/main'}]],
        ['link_remove', []]])
    def test_get_kafka_message_link(self, ppinfo_client, string, value):
        data = self.get_attribute_update_body(string)
        self.change_product(ppinfo_client, data)
        time.sleep(1)
        message = self.message_get_from_kafka_external()

        for item in message['data']['attributes']:
            if item['code'] == 'PPInfo_site_landing':
                assert item['values'] == value, 'Значения в кафке неверные'
                break
        else:
            assert False, 'Аттрибут не найден в сообщении кафки'

    @allure.title('Изменение основного продукта текст и проверка сообщения из Kafka')
    @pytest.mark.parametrize('string, value', [
        ['main_product_add', [{'code': 'BI_2683', 'name': '1_Не трогать, для АТ, делегирование del'}]],
        ['main_product_replace', [{'code': 'BI_3266', 'name': 'Не трогать (продукт для автотестов)'}]],
        ['main_product_remove', []]])
    def test_get_kafka_message_main_product(self, ppinfo_client, string, value):
        data = self.get_attribute_update_body(string)
        self.change_product(ppinfo_client, data)
        time.sleep(1)
        message = self.message_get_from_kafka_external()

        for item in message['data']['attributes']:
            if item['code'] == 'PPInfo_main_product':
                assert item['values'] == value, 'Значения в кафке неверные'
                break
        else:
            assert False, 'Аттрибут не найден в сообщении кафки'

    @allure.title('Получение сообщения из кафки после создания продукта и сравнение с пользовательской ролевкой')
    @pytest.mark.parametrize('product_type', ['Vneshnii', 'Vnutrennii'])
    def test_get_kafka_message_after_create(self, ppinfo_client, product_type):
        product_bi_code = self.create_product(ppinfo_client,
                                              self.get_data_for_product_creation(product_type,
                                                                                 status='(PPinfo_status)Waiting_decision'))

        time.sleep(1)
        message = self.message_get_from_kafka_external(product_bi_code)

        attribute = ['PPInfo_site_landing', 'PPInfo_main_product',
                     'PPinfo_resolution', 'Test_mnozh_ssylki', 'Mnogo_produktov',
                     'Odin_produkt', 'Rukovoditel_etogo_balagana', 'Mnozhestvo',
                     'employee_business_owner', 'Identifikator_SOL', 'PPinfo_start_close_date',
                     'PPinfo_StructuralProductType1', 'PPInfo_showcase']

        for item in message['data']['attributes']:
            if item['code'] in attribute:
                assert item['values'] == [], 'Значения в кафке неверные'
                break
        else:
            assert False, 'Аттрибут не найден в сообщении кафки'

    @allure.title('Получение сообщений из кафки после создания продукта и сравнение с атрибутами вне ролевки')
    @pytest.mark.parametrize('product_type', ['Vneshnii', 'Vnutrennii'])
    def test_get_kafka_message_after_create_product_without_user_group(self, ppinfo_client, product_type):
        product_bi_code = self.create_product(ppinfo_client,
                                              self.get_data_for_product_creation(product_type,
                                                                                 status='(PPinfo_status)Waiting_decision'))
        time.sleep(2)

        attribute = ['bool_for_at', 'date_for_at', 'employee_for_at', 'multiple_values_for_at', 'number_for_at',
                     'product_for_at', 'text_for_at', 'text_for_at_with_n', 'url_for_at']

        message = self.message_get_from_kafka_external(product_bi_code)

        for item in message['data']['attributes']:
            if item['code'] in attribute:
                assert False, 'В сообщении кафки атрибут, которого нет в пользовательской ролевке'

    @allure.title('Получение сообщения из кафки после создания и изменения атрибута вне продукта')
    def test_get_kafka_message_after_attribute_edit(self, ppinfo_client, pmd_admin_gw_client, clear_db_attribute):
        data = self.get_attribute_update_body('link_add')
        self.change_product(ppinfo_client, data)
        data = self.get_attribute_update_body('link_remove')
        self.change_product(ppinfo_client, data)
        time.sleep(1)

        message_before = self.message_get_from_kafka_external()

        data = self.get_data_for_attribute()
        attribute_id = self.create_attribute(pmd_admin_gw_client, data)
        time.sleep(1)

        message_after = self.message_get_from_kafka_external()

        assert message_before['createdAt'] == message_after[
            'createdAt'], 'В Кафку пришло новое сообщение после создания атрибута'

        data = self.get_data_for_attribute({'name': 'qwerty test'})
        self.patch_attribute_by_id(pmd_admin_gw_client, attribute_id, data)

        time.sleep(1)

        message_finale = self.message_get_from_kafka_external()

        assert message_finale['createdAt'] != message_after[
            'createdAt'], 'В кафку не пришло новое сообщение после изменения аттрибута'

    @allure.title('Получение сообщения из кафки и сравнение с пользовательской ролевкой')
    def test_get_kafka_message_with_attributes_after_attribute_edit(self, pmd_admin_gw_client, ppinfo_client,
                                                                    clear_db_attribute):
        product_bi_code = self.create_product(ppinfo_client,
                                              self.get_data_for_product_creation('Vneshnii',
                                                                                 status='(PPinfo_status)Waiting_decision'))

        data = self.get_data_for_attribute()
        attribute_id = self.create_attribute(pmd_admin_gw_client, data)
        data = self.get_data_for_attribute({'name': 'qwerty test'})
        self.patch_attribute_by_id(pmd_admin_gw_client, attribute_id, data)

        time.sleep(1)
        message = self.message_get_from_kafka_external(product_bi_code)

        attribute = ['PPInfo_site_landing', 'PPInfo_main_product',
                     'PPinfo_resolution', 'Test_mnozh_ssylki', 'Mnogo_produktov',
                     'Odin_produkt', 'Rukovoditel_etogo_balagana', 'Mnozhestvo',
                     'employee_business_owner', 'Identifikator_SOL', 'PPinfo_start_close_date',
                     'PPinfo_StructuralProductType1', 'PPInfo_showcase']

        for item in message['data']['attributes']:
            if item['code'] in attribute:
                assert item['values'] == [], 'Значения в кафке неверные'
                break
        else:
            assert False, 'Аттрибут не найден в сообщении кафки'

    @allure.title('Получение сообщения из кафки и сравнение с пользовательской ролевкой вне ролевки')
    def test_get_kafka_message_with_attributes_after_attribute_edit_without_user_role(self, pmd_admin_gw_client,
                                                                                      ppinfo_client,
                                                                                      clear_db_attribute):
        product_bi_code = self.create_product(ppinfo_client,
                                              self.get_data_for_product_creation('Vneshnii',
                                                                                 status='(PPinfo_status)Waiting_decision'))

        data = self.get_data_for_attribute()
        attribute_id = self.create_attribute(pmd_admin_gw_client, data)
        data = self.get_data_for_attribute({'name': 'qwerty test'})
        self.patch_attribute_by_id(pmd_admin_gw_client, attribute_id, data)
        time.sleep(1)

        message = self.message_get_from_kafka_external(product_bi_code)

        attribute = ['bool_for_at', 'date_for_at', 'employee_for_at', 'multiple_values_for_at', 'number_for_at',
                     'product_for_at', 'text_for_at', 'text_with_n_for_at', 'url_for_at']

        for item in message['data']['attributes']:
            if item['code'] in attribute:
                assert False, 'В сообщении кафки атрибут, которого нет в пользовательской ролевке'

    @allure.title('Получение сообщения из кафки после изменения спецификации')
    def test_get_kafka_message_after_spec_edit(self, ppinfo_client, pmd_admin_gw_client, clear_db_spec):
        data = self.get_attribute_update_body('link_add')
        self.change_product(ppinfo_client, data)
        data = self.get_attribute_update_body('link_remove')
        self.change_product(ppinfo_client, data)
        time.sleep(1)

        message_before = self.message_get_from_kafka_external()

        specification_id = self.create_specification(pmd_admin_gw_client, {'name': self.text + ' test'})

        data = self.get_data_manage_spec('afc32820-9ce1-41ed-8aa9-881030ec7ee3', True)
        self.manage_attributes_in_specification(pmd_admin_gw_client, specification_id, data)

        time.sleep(1)

        message_after = self.message_get_from_kafka_external()

        assert message_before['createdAt'] != message_after[
            'createdAt'], 'В кафку не пришло новое сообщение после изменения спецификации'

    @allure.title('Получение сообщения из кафки после изменения ролевки Пользователи')
    def test_get_message_kafka_after_role_manage(self, ppinfo_client, pmd_admin_gw_client):
        data = self.get_attribute_update_body('link_add')
        self.change_product(ppinfo_client, data)
        data = self.get_attribute_update_body('link_remove')
        self.change_product(ppinfo_client, data)
        time.sleep(1)

        message_before = self.message_get_from_kafka_external()

        data = self.get_data_for_manage(
            {'attributeId': '64c477c6-74ea-41d1-a483-dd9c116481ab', 'isEditable': False, 'isView': True,
             'isOwnedView': False})
        data_finale = self.get_data_for_manage(
            {'attributeId': '64c477c6-74ea-41d1-a483-dd9c116481ab', 'isEditable': False, 'isView': False,
             'isOwnedView': False})

        try:
            self.manage_attr(pmd_admin_gw_client, '733882ff-3b13-46eb-ad4a-31d1942e7def', data)
            time.sleep(5)
            message_after = self.message_get_from_kafka_external()
            assert message_before['createdAt'] != message_after[
                'createdAt'], 'В кафку не пришло сообщение после изменения пользовательской ролевки'
        finally:
            self.manage_attr(pmd_admin_gw_client, '733882ff-3b13-46eb-ad4a-31d1942e7def', data_finale)

    @allure.title('Получение сообщения c атрибутами согласно ролевке')
    @allure.issue('https://jira.mts.ru/browse/PPI-4339', 'PPInfo - Управление передачей атрибутов по Kafka')
    @pytest.mark.parametrize('attribute, move', [('PPInfo_showcase', 'string_replace'),
                                                 ('PPinfo_StructuralProductType1', 'manyselect_replace'),
                                                 ('PPinfo_start_close_date', 'date_replace'),
                                                 ('Identifikator_SOL', 'num_replace'),
                                                 ('employee_business_owner', 'user_replace'),
                                                 ('Mnozhestvo', 'multi_replace'),
                                                 ('Rukovoditel_etogo_balagana', 'multiuser_replace_minus'),
                                                 ('Odin_produkt', 'product_replace'),
                                                 ('Mnogo_produktov', 'multiproduct_replace_minus'),
                                                 ('Test_mnozh_ssylki', 'multilink_replace_minus'),
                                                 ('PPinfo_resolution', 'multistring_replace'),
                                                 ('PPInfo_site_landing', 'link_replace'),
                                                 ('Osnovnoi_proekt_Jira', 'main_project_jira_product_replace')])
    def test_get_products_with_attributes_by_roles(self, rest_external_client, ppinfo_client, attribute, move):

        try:
            self.delete_attr(ppinfo_client, attr_id=attribute, tag_id='transfer_settings')
        except AssertionError:
            pass

        data = self.get_attribute_update_body(move)
        self.change_product(ppinfo_client, data)
        time.sleep(1)

        messages = self.message_get_from_kafka_external()

        attributes_in_message = []

        for attr in messages['data']['attributes']:
            attributes_in_message.append(attr['code'])

        assert attribute not in attributes_in_message, f'Атрибут {attribute} передается в сообщении, хотя должен быть исключен'

        try:
            self.add_attr(ppinfo_client, attr_id=attribute, tag_id='transfer_settings')
        except AssertionError:
            pass

        data = self.get_attribute_update_body(move)
        self.change_product(ppinfo_client, data)
        time.sleep(1)

        messages = self.message_get_from_kafka_external()

        attributes_in_message = []

        for attr in messages['data']['attributes']:
            attributes_in_message.append(attr['code'])

        assert attribute in attributes_in_message, f'Атрибут {attribute} не передается в сообщении, хотя должен быть'
