import allure
import pytest

from API.models.pmd.admin_specification import SpecificationApi
from API.models.ppinfo.product_v2 import ProductV2


@pytest.mark.api
@allure.label('priority', 'Высокий')
@allure.feature('Спецификации')
class TestSpecificationApi(SpecificationApi, ProductV2):

    ######################################### Спецификации

    @allure.title('Получение всех спецификаций')
    def test_get_specifications(self, pmd_admin_gw_client):
        self.get_specifications(pmd_admin_gw_client)

    @allure.title('Получение спецификации по Id')
    @pytest.mark.parametrize('spec_id',
                             ('37b386a8-6dde-5947-8307-b117266b82da', '9dffdd8b-935d-31c7-6b1a-f3d58e649b9c'))
    def test_get_specification_by_id(self, pmd_admin_gw_client, spec_id):
        self.get_specification_by_id(pmd_admin_gw_client, spec_id)

    @allure.title('Невалидное получение спецификации по несуществующему Id')
    def test_get_specification_by_id_404(self, pmd_admin_gw_client):
        self.get_specification_by_id_404(pmd_admin_gw_client, '37b386a8-6dde-5947-1234-b117266b82da')

    @allure.title('Скрытие значения внутри атрибута')
    @allure.issue('https://jira.mts.ru/browse/CAKF-1559', 'При скрытии значения атрибута, он не скрывается')
    @pytest.mark.parametrize('is_active', [True, False])
    def test_hide_attribute_value(self, ppinfo_client, pmd_admin_gw_client, is_active):
        self.patch_attribute_value_by_id(pmd_admin_gw_client, 'fc335a6d-b65a-40f2-8744-0fdf98844bc9', 'авада',
                                         is_active)
        response = self.get_info_by_product_code(ppinfo_client, 'BI_60')
        req_val = [i for i in response['hidingAttributes'] if i['id'] == '0_test_mnozh_vybor_v_eksel'][0]['answers']
        if is_active:
            with allure.step('Проверяем, что значение атрибута отображается на странице продукта'):
                assert any(i['value'] == 'авада' for i in req_val), 'Значения скрытого атрибута нет'
        else:
            with allure.step('Проверяем, что значение атрибута не отображается на странице продукта'):
                assert all(i['value'] != 'авада' for i in req_val), 'Значение скрытого атрибута есть'

    @allure.title('Создание и удаление спецификации')
    def test_create_specifications(self, pmd_admin_gw_client):
        specification_id = self.create_specification(pmd_admin_gw_client, {'name': self.text})

        with allure.step('Проверяем, что спецификация создалась'):
            self.get_specification_by_id(pmd_admin_gw_client, specification_id)

        self.delete_specification_by_id(pmd_admin_gw_client, specification_id)

        with allure.step('Проверяем, что спецификация удалилась'):
            self.get_specification_by_id_404(pmd_admin_gw_client, specification_id)

    @allure.title('Создание спецификации с невалидным названием')
    @pytest.mark.parametrize('name', ('',
                                      'wdasdasdasdasdwdasdasdasdasdwdasdasdвasdasdwdadasdasdasdwdasdasdasdasdwdasdasdasdasdwdasdasdasdasdwdasdasdasdasdwdasdasdasdasdqq'))
    def test_create_invalid_specification(self, pmd_admin_gw_client, name):
        self.create_specification_400(pmd_admin_gw_client, {'name': name})

    @allure.title('Редактирование названия спецификации')
    def test_patch_specification_name(self, pmd_admin_gw_client):
        specification_id = self.create_specification(pmd_admin_gw_client, {'name': self.text})

        self.patch_specification_by_id(pmd_admin_gw_client, specification_id, {'name': 'тест33'})

        with allure.step('Проверяем, что название изменилось'):
            assert self.get_specification_by_id(pmd_admin_gw_client, specification_id)[
                       'name'] == 'тест33', f'Текущее название {self.get_specification_by_id(specification_id)["name"]}'

        self.delete_specification_by_id(pmd_admin_gw_client, specification_id)

    @allure.title('Невалидное редактирование названия спецификации')
    @pytest.mark.parametrize('name', ('',
                                      'wdasdasdasdasdwdasdasdasdasdwdasdasdвasdasdwdadasdasdasdwdasdasdasdasdwdasdasdasdasdwdasdasdasdasdwdasdasdasdasdwdasdasdasdasdqq'))
    def test_patch_specification_invalid_name(self, pmd_admin_gw_client, name):
        specification_id = self.create_specification(pmd_admin_gw_client, {'name': self.text})

        self.patch_specification_by_id_400(pmd_admin_gw_client, specification_id, {'name': name})

        with allure.step('Проверяем, что название не изменилось'):
            assert self.get_specification_by_id(pmd_admin_gw_client, specification_id)[
                       'name'] != name, f'Текущее название {self.get_specification_by_id(pmd_admin_gw_client, specification_id)["name"]}'

        self.delete_specification_by_id(pmd_admin_gw_client, specification_id)

    @allure.title('Редактирование названия спецификации по несуществующему айди')
    @allure.issue('https://jira.mts.ru/browse/PPI-2049',
                  '500 ошибка в методе получения спецификации по айди при запросе по несуществующему айди')
    def test_patch_specification_invalid_name(self, pmd_admin_gw_client):
        self.patch_specification_by_id_404(pmd_admin_gw_client, '37b386a8-6dde-5947-1234-b117266b82da', {'name': 'qwe'})

    @allure.title('Изменение атрибутов внутри спецификации')
    @pytest.mark.parametrize(('attr_id', 'is_required'), (
            ['afc32820-9ce1-41ed-8aa9-881030ec7ee3', True],
            ['afc32820-9ce1-41ed-8aa9-881030ec7ee3', False]
    ))
    def test_add_attributes_in_specification(self, pmd_admin_gw_client, attr_id, is_required):
        specification_id = self.create_specification(pmd_admin_gw_client, {'name': self.text})

        data = self.get_data_manage_spec(attr_id, is_required)
        with allure.step('Добавляем атрибут в спецификацию'):
            self.manage_attributes_in_specification(pmd_admin_gw_client, specification_id, data)

        with allure.step('Проверяем, что атрибут добавился'):
            assert self.get_specification_by_id(pmd_admin_gw_client, specification_id)['attributes'][0][
                       'id'] == attr_id and \
                   self.get_specification_by_id(pmd_admin_gw_client, specification_id)['attributes'][0][
                       'isRequired'] == is_required, 'Изменения не применились'

        data = self.get_data_manage_spec(attr_id)
        with allure.step('Удаляем атрибут в спецификации'):
            self.manage_attributes_in_specification(pmd_admin_gw_client, specification_id, data)

        with allure.step('Проверяем, что атрибут удалился'):
            assert not self.get_specification_by_id(pmd_admin_gw_client, specification_id)[
                'attributes'], 'Изменения не применились'

        self.delete_specification_by_id(pmd_admin_gw_client, specification_id)


#########################################  Атрибуты
@pytest.mark.api
@allure.feature('Атрибуты')
class TestAttributesApi(SpecificationApi):
    @allure.title('Создание атрибута')
    @allure.issue('https://jira.mts.ru/browse/PPI-616', 'PPInfo - Многострочный текстовый атрибут')
    @pytest.mark.parametrize('attr_type', ['string', 'text', 'numeric', 'time', 'user', 'bool', 'link', 'product'])
    def test_add_attribute(self, pmd_admin_gw_client, attr_type):
        data = self.get_data_for_attribute({'type': attr_type})

        self.full_cycle_attr(pmd_admin_gw_client, data)

    @allure.title('Создание атрибута со спецификацией')
    @pytest.mark.parametrize('attr_type', ['string', 'text', 'numeric', 'time', 'user', 'bool', 'link', 'product'])
    def test_add_attribute_with_specification(self, pmd_admin_gw_client, attr_type):
        data = self.get_data_for_attribute(
            {'type': attr_type, 'specifications': [{'specificationId': '37b386a8-6dde-5947-8307-b117266b82da'}]})

        self.full_cycle_attr(pmd_admin_gw_client, data)

    @allure.title('Создание атрибута с источником')
    @pytest.mark.parametrize('attr_type', ['string', 'text', 'numeric', 'time', 'user', 'bool', 'link', 'product'])
    def test_add_attribute_with_source(self, pmd_admin_gw_client, attr_type):
        data = self.get_data_for_attribute(
            {'type': attr_type, 'sourceId': 'c38169c2-ef46-4353-8260-e0b1cf5e8f44'})

        self.full_cycle_attr(pmd_admin_gw_client, data)

    @allure.title('Создание атрибута Вычисляемый сотрудник')
    @allure.issue('https://jira.mts.ru/browse/PPI-2522',
                  'PPInfo - Backend - Добавление типа атрибута "Вычисляемый сотрудник"')
    @pytest.mark.parametrize('is_multiple', [True, False])
    def test_add_attribute_curator(self, pmd_admin_gw_client, is_multiple):
        data = self.get_data_for_attribute({'type': 'user', 'usageType': 'cluster-curator', 'isMultiple': is_multiple})

        self.full_cycle_attr(pmd_admin_gw_client, data)

    @allure.title('Создание атрибута Вычисляемый сотрудник со спецификацией')
    @allure.issue('https://jira.mts.ru/browse/PPI-2522',
                  'PPInfo - Backend - Добавление типа атрибута "Вычисляемый сотрудник"')
    @pytest.mark.parametrize('is_multiple', [True, False])
    def test_add_attribute_curator_with_specification(self, pmd_admin_gw_client, is_multiple):
        data = self.get_data_for_attribute({'type': 'user', 'usageType': 'cluster-curator', 'isMultiple': is_multiple,
                                            'specifications': [
                                                {'specificationId': '37b386a8-6dde-5947-8307-b117266b82da'}]})

        self.full_cycle_attr(pmd_admin_gw_client, data)

    @allure.title('Создание атрибута Вычисляемый сотрудник с источником')
    @allure.issue('https://jira.mts.ru/browse/PPI-2522',
                  'PPInfo - Backend - Добавление типа атрибута "Вычисляемый сотрудник"')
    @pytest.mark.parametrize('is_multiple', [True, False])
    def test_add_attribute_curator_with_source(self, pmd_admin_gw_client, is_multiple):
        data = self.get_data_for_attribute({'type': 'user', 'usageType': 'cluster-curator', 'isMultiple': is_multiple,
                                            'sourceId': 'c38169c2-ef46-4353-8260-e0b1cf5e8f44'})

        self.full_cycle_attr(pmd_admin_gw_client, data)

    @allure.title('Создание атрибута с невалидным названием')
    @allure.issue('https://jira.mts.ru/browse/PPI-616', 'PPInfo - Многострочный текстовый атрибут')
    @pytest.mark.parametrize('attr_type', ['string', 'text', 'numeric', 'time', 'user', 'bool', 'link', 'product'])
    @pytest.mark.parametrize('name', ('',
                                      'wdasdasdasdasdwdasdasdasdasdwdasdasda2sdasdwdadasdasdasdwdasdasdasdasdwdasdasdasdasdwdasdasdasdasdwdasdasdasdasdwdasdasdasdasdqq'))
    def test_add_attribute_invalid_name(self, pmd_admin_gw_client, attr_type, name):
        data = self.get_data_for_attribute({'name': name, 'type': attr_type})

        self.create_attribute_400(pmd_admin_gw_client, data)

    @allure.title('Создание атрибута с некорректным типом')
    @pytest.mark.parametrize('attr_type', ['йцу', 'qweqwe', '123123123'])
    def test_add_attribute_invalid_type(self, pmd_admin_gw_client, attr_type):
        data = self.get_data_for_attribute({'type': attr_type})

        self.create_attribute_400(pmd_admin_gw_client, data)

    @allure.title('Создание атрибута с самостоятельным заведением кода')
    @allure.issue('https://jira.mts.ru/browse/PPI-616', 'PPInfo - Многострочный текстовый атрибут')
    @pytest.mark.parametrize('attr_type', ['string', 'text', 'numeric', 'time', 'user', 'bool'])
    def test_add_attribute_custom_code(self, pmd_admin_gw_client, attr_type):
        data = self.get_data_for_attribute({'code': self.text, 'type': attr_type})

        self.full_cycle_attr(pmd_admin_gw_client, data)

    @allure.title('Создание атрибута с некорректным самостоятельным заведением кода')
    @allure.issue('https://jira.mts.ru/browse/PPI-616', 'PPInfo - Многострочный текстовый атрибут')
    @pytest.mark.parametrize('attr_type', ['string', 'text', 'numeric', 'time', 'user', 'bool', 'link', 'product'])
    @pytest.mark.parametrize('code', ('привет', 'employee_business_owner', 'test code'))
    def test_add_attribute_custom_invalid_code(self, pmd_admin_gw_client, attr_type, code):
        data = self.get_data_for_attribute({'code': code, 'type': attr_type})

        self.create_attribute_400(pmd_admin_gw_client, data)

    @allure.title('Создание атрибута Вычисляемая ссылка')
    @allure.issue('https://jira.mts.ru/browse/PPI-515', 'PPInfo - Новый тип ссылки - Вычисляемый атрибут')
    def test_add_attribute_calculate_link(self, pmd_admin_gw_client):
        data = self.get_data_for_attribute(
            {'type': 'link', 'usageType': 'calculated', 'formula': 'http://radar.mcc.mts-corp.ru/product/mcc/[code]'})

        self.full_cycle_attr(pmd_admin_gw_client, data)

    @allure.title('Создание атрибута Множественная ссылка')
    @allure.issue('https://jira.mts.ru/browse/PPI-666', 'PPInfo - Добавление ссылок (объединённая)')
    def test_add_attribute_multy_link(self, pmd_admin_gw_client):
        data = self.get_data_for_attribute({'type': 'link', 'isMultiple': True})

        self.full_cycle_attr(pmd_admin_gw_client, data)

    @allure.title('Добавление значения в атрибут')
    def test_add_value_in_attribute(self, pmd_admin_gw_client):
        data = self.get_data_for_attribute()

        attribute_id = self.create_attribute(pmd_admin_gw_client, data)

        with allure.step('Проверяем, что атрибут создался'):
            self.get_attribute_by_id(pmd_admin_gw_client, attribute_id)

        data_value = {
            'value': '1'
        }

        self.create_attribute_value(pmd_admin_gw_client, attribute_id, data_value)
        with allure.step('Проверяем, что набор значений обновился и не пустой'):
            assert self.get_attribute_by_id(pmd_admin_gw_client, attribute_id)['values'], 'Набор значений пустой'

        self.delete_attribute_by_id(pmd_admin_gw_client, attribute_id)

        with allure.step('Проверяем, что атрибут удалился'):
            self.get_attribute_by_id_404(pmd_admin_gw_client, attribute_id)

    @allure.title('Получения атрибута Кластер')
    @allure.issue('https://jira.mts.ru/browse/PPI-266', 'PPInfo - Интеграционный атрибут "Кластер"')
    def test_get_attribute_by_id_cluster(self, pmd_admin_gw_client):
        assert self.get_attribute_by_id(pmd_admin_gw_client, 'f1ee1305-de95-42c2-8e07-0846bb80b6ad')[
            'values'], 'Кластеры не пришли'

    @allure.title('Получения атрибута блок')
    @allure.issue('https://jira.mts.ru/browse/PPI-187', 'PPInfo - Системный атрибут "Блок"')
    def test_get_attribute_by_id_block(self, pmd_admin_gw_client):
        assert 18 <= len(
            [d for d in self.get_attribute_by_id(pmd_admin_gw_client, 'd2480d48-60c8-484b-aa55-8e2b394f62b5')['values']
             if
             d['isActive']]) <= 22, 'кол-во значений не в выбранном диапазоне'

    @allure.title('Получения атрибутов')
    def test_get_attributes(self, pmd_admin_gw_client):
        self.get_attributes(pmd_admin_gw_client)

    @allure.title('Изменение атрибута по id')
    @pytest.mark.parametrize('attr_name, value', [
        ('name', 'asdasdasd'), ('description', 'тестовое описание'), ('isActive', False),
        ('reasonForDeletion', 'Определено'), ('sourceId', 'c38169c2-ef46-4353-8260-e0b1cf5e8f44'),
        ('specifications', [{'specificationId': '37b386a8-6dde-5947-8307-b117266b82da'}])])
    def test_patch_attribute(self, pmd_admin_gw_client, attr_name, value):
        data = self.get_data_for_attribute()

        attribute_id = self.create_attribute(pmd_admin_gw_client, data)
        if attr_name == 'name':
            value = self.text
        data = self.get_data_for_attribute({attr_name: value})

        self.patch_attribute_by_id(pmd_admin_gw_client, attribute_id, data)
        if attr_name != 'specifications':
            with allure.step('Проверяем, что изменения применились'):
                assert self.get_attribute_by_id(pmd_admin_gw_client, attribute_id)[
                           attr_name] == value, (
                    f'Текущее значение {self.get_attribute_by_id(pmd_admin_gw_client, attribute_id)[attr_name]}'
                    f'!= {value}')

        self.delete_attribute_by_id(pmd_admin_gw_client, attribute_id)

    @allure.title('Невалидное изменение атрибута по id')
    @pytest.mark.parametrize('name', ('',
                                      'wdasdasdasdasdwdasdasdasdasdwdasdasda2sdasdwdadasdasdasdwdasdasdasdasdwdasdasdasdasdwdasdasdasdasdwdasdasdasdasdwdasdasdasdasdqq'))
    def test_invalid_patch_attribute(self, pmd_admin_gw_client, name):
        data = self.get_data_for_attribute()

        attribute_id = self.create_attribute(pmd_admin_gw_client, data)

        data = self.get_data_for_attribute({'name': name})

        self.patch_attribute_by_id_400(pmd_admin_gw_client, attribute_id, data)

        with allure.step('Проверяем, что изменения не применились'):
            assert self.get_attribute_by_id(pmd_admin_gw_client, attribute_id)[
                       'name'] != name, (f'Текущее значение {self.get_attribute_by_id(attribute_id)["name"]} '
                                         f'!= {name}')

        self.delete_attribute_by_id(pmd_admin_gw_client, attribute_id)


#### Источники
@pytest.mark.api
@allure.feature('Источники')
class TestSourcesApi(SpecificationApi):
    @allure.title('Получение источников')
    def test_get_source(self, pmd_admin_gw_client):
        self.get_source(pmd_admin_gw_client)

    @allure.title('Создание источника')
    def test_create_source(self, pmd_admin_gw_client):
        data = {
            'name': self.text,
            'link': 'https://chat.openai.com/chat'
        }
        source_id = self.create_source(pmd_admin_gw_client, data)

        with allure.step('Проверяем, что источник создался'):
            self.get_source_by_id(pmd_admin_gw_client, source_id)

        self.delete_source_by_id(pmd_admin_gw_client, source_id)

        with allure.step('Проверяем, что источник удалился'):
            self.get_source_by_id_400(pmd_admin_gw_client, source_id)

    @allure.title('Создание источника с невалидным именем')
    @pytest.mark.parametrize('name', ('',
                                      'wdasdasdasdasdwdasdasdasdasdwdasdasda2sdasdwdadasdasdasdwdasdasdasdasdwdasdasdasdasdwdasdasdasdasdwdasdasdasdasdwdasdasdasdasdqq'))
    def test_create_source_invalid_name(self, pmd_admin_gw_client, name):
        data = {
            'name': name,
            'link': 'https://chat.openai.com/chat'
        }
        self.create_source_400(pmd_admin_gw_client, data)

    @allure.title('Создание источника c некорректной ссылкой')
    def test_create_source_invalid_link(self, pmd_admin_gw_client):
        data = {
            'name': self.text,
            'link': 'йцу'
        }
        self.create_source_400(pmd_admin_gw_client, data)

    @allure.title("Изменение источника")
    def test_patch_source(self, pmd_admin_gw_client):
        data = {
            'name': self.text,
            'link': 'https://chat.openai.com/chat'
        }

        source_id = self.create_source(pmd_admin_gw_client, data)
        new_value = self.text
        data = {
            'name': new_value,
            'link': 'https://jsontopydantic.com/'
        }

        self.patch_source_by_id(pmd_admin_gw_client, source_id, data)

        with allure.step('Проверяем, что источник изменился'):
            assert self.get_source_by_id(pmd_admin_gw_client, source_id)['name'] == new_value and \
                   self.get_source_by_id(pmd_admin_gw_client, source_id)[
                       'link'] == 'https://jsontopydantic.com/', 'Изменения не произошли'

        self.delete_source_by_id(pmd_admin_gw_client, source_id)

    @allure.title('Изменение источника некорректным именем')
    @pytest.mark.parametrize('name', ('',
                                      'wdasdasdasdasdwdasdasdasdasdwdasdasda2sdasdwdadasdasdasdwdasdasdasdasdwdasdasdasdasdwdasdasdasdasdwdasdasdasdasdwdasdasdasdasdqq'))
    def test_patch_source_invalid_name(self, pmd_admin_gw_client, name):
        data = {
            'name': name,
            'link': 'https://jsontopydantic.com/'
        }

        self.patch_source_by_id_400(pmd_admin_gw_client, '71801890-8f88-43e0-a696-608621d1f24b', data)

    @allure.title('Изменение источника некорректной ссылкой')
    def test_patch_source_invalid_name(self, pmd_admin_gw_client):
        data = {
            'name': 'name',
            'link': 'cerf'
        }

        self.patch_source_by_id_400(pmd_admin_gw_client, '71801890-8f88-43e0-a696-608621d1f24b', data)
