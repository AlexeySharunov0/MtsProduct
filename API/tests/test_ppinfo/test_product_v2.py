import datetime
import time
from datetime import datetime, timezone, date
from datetime import timedelta

import allure
import pytest

from API.models.pmd.rest_internal_modules.actions import Actions
from API.models.pmd.rest_internal_modules.demo import Demo
from API.models.pmd.rest_internal_modules.internal_product import InternalProduct
from API.models.ppinfo.product_v1 import ProductV1


@pytest.mark.api
@pytest.mark.last
@allure.feature('Системные атрибуты')
@allure.feature('Получение информации о продукте')
class TestProductV2(Actions, InternalProduct, Demo, ProductV1):

    @allure.title('Получение информации о продукте')
    @pytest.mark.parametrize('code', ['41', 'BI_60'])
    def test_info_product(self, ppinfo_client, code):
        with allure.step('Получаем информацию о продукте'):
            self.get_info_by_product_code(ppinfo_client, code)

    @allure.title('Получение блока финансирования')
    @allure.issue('https://jira.mts.ru/browse/PPI-2467',
                  'PPInfo - Backend - Добавить блок "Цикл финансирования"')
    @pytest.mark.parametrize('code', ['BI_1905', 'BI_60', 'BI_271', 'BI_1883'])
    def test_info_financing(self, ppinfo_client, code):
        with allure.step('Получаем информацию о продукте'):
            financing_info = self.get_info_by_product_code(ppinfo_client, code)['financing']
        expected_attributes = ['Data_planiruemogo_komiteta', 'PPInfo_data_endmoney', 'SYSTEM_Delay', 'TechCommittee',
                               'PPInfo_product_com']
        system_attributes = ['SYSTEM_Delay', 'TechCommittee']

        with allure.step('Проверяем, что в блоке финансирования пришли нужные атрибуты'):
            assert all(i['id'] in expected_attributes for i in financing_info)

        with allure.step('Проверяем, что можно редактировать только пользовательские атрибуты'):
            for attr in financing_info:
                if attr['id'] in system_attributes:
                    assert not attr['editable'], 'Системный атрибут можно редактировать'
                else:
                    assert attr['editable'], 'Пользовательский атрибут нельзя редактировать'

    @allure.title('Проверяем, что все системные атрибуты нельзя редактировать')
    @pytest.mark.parametrize('attr_code', (
            'test_vychisliaemaia_ssylka', 'SYSTEM_Delay', 'SYSTEM_CostCenter', 'SYSTEM_CreatedAt',
            'Vychisliaemaia_ssylka',
            'Prichina_udaleniia', 'Kommentarii_pri_udalenii', 'SYSTEM_Jira', 'Data_nachala_Legkogo_starta',
            'Data_okonchaniia_Legkogo_starta', 'Konets_finansirovaniya', 'SYSTEM_ProductType', 'TechCommittee'))
    def test_check_system_attributes_not_editable(self, ppinfo_client, attr_code):
        required_attr = [attr for attr in self.get_info_by_product_code(ppinfo_client, 'BI_2769')['hidingAttributes'] if
                         attr['id'] == attr_code][0]

        with allure.step(f'Проверяем, что атрибут {attr_code} нельзя редактировать'):
            assert not required_attr['editable'], f'Атрибут {attr_code} можно редактировать'

    #### Вычисляемые ссылки
    @allure.title('Проверяем что вычисляемые ссылки корректно отображаются в продукте')
    @allure.issue('https://jira.mts.ru/browse/PPI-515', 'PPInfo - Новый тип ссылки - Вычисляемый атрибут')
    @pytest.mark.parametrize('code', ['BI_41', 'BI_60'])
    def test_info_calculate_link(self, ppinfo_client, code):
        required_link = [attr for attr in self.get_info_by_product_code(ppinfo_client, code)['actionLinks'] if
                         attr['id'] == 'test_vychisliaemaia_ssylka'][0]

        with allure.step('Проверяем, что вычисляемая ссылка отображается в верном формате'):
            assert required_link['values'] == [
                {'code': f'http://radar.mcc.mts-corp.ru/product/mcc/{code}',
                 'value': ''}], f'С ссылкой что не так \n {required_link["values"]}'

    #### JIRA
    @allure.title('Проверяем, что атрибут JIRA отображается корректно')
    @pytest.mark.parametrize('code', ['BI_41', 'BI_60'])
    def test_attr_jira(self, ppinfo_client, code):
        required_link = [attr for attr in self.get_info_by_product_code(ppinfo_client, code)['hidingAttributes'] if
                         attr['id'] == 'SYSTEM_Jira'][0]

        with allure.step('Проверяем, что ссылка JIRA отображается в верном формате'):
            for value in required_link['values']:
                assert 'https://jira.mts.ru/browse/' in value['code'], 'Ссылка в неверном формате'

                code = value['code'].replace('https://jira.mts.ru/browse/', '')
                assert code in value['value'], 'В названии ссылки нет кода Jira'

    #### Дата создания карточки
    @allure.title('Проверяем артибут Дата создания карточки')
    @pytest.mark.parametrize('product_type', ['Vneshnii', 'Vnutrennii'])
    def test_attr_creation_date(self, pmd_internal_gw_client, ppinfo_client, product_type):
        data = self.get_data_for_product_creation(product_type)

        product_id = self.create_product(ppinfo_client, data)
        self.delete_product(pmd_internal_gw_client, product_id)

        required_attr = \
        [attr for attr in self.get_info_by_product_code(ppinfo_client, product_id)['hidingAttributes'] if
         attr['id'] == 'SYSTEM_CreatedAt'][0]

        with allure.step('Проверяем, что дата создания карточки совпадает с сегодняшней'):
            assert f"{date.today()}" in required_attr['values'][0][
                'value'], 'Дата создания карточки не совпадает с текущей'

    #### Причина удаления
    @allure.title('Проверяем артибут причина удаления')
    @pytest.mark.parametrize('product_type', ['Vneshnii', 'Vnutrennii'])
    def test_attr_deletion_reason(self, pmd_internal_gw_client, ppinfo_client, product_type):
        data = self.get_data_for_product_creation(product_type)

        product_id = self.create_product(ppinfo_client, data)
        self.delete_product(pmd_internal_gw_client, product_id)

        required_attr = \
        [attr for attr in self.get_info_by_product_code(ppinfo_client, product_id)['hidingAttributes'] if
         attr['id'] == 'Prichina_udaleniia'][0]

        with allure.step('Проверяем, что причина удаления содержит значения из заданного набора'):
            ac_list = ['Ошибочное заведение', 'Ревью каталога', 'Решение команды продукта']
            assert required_attr['values'][0][
                       'value'] in ac_list, f'Причина указана как {required_attr["values"][0]["value"]}'

    #### Тип продукта (системный)
    @allure.title('Проверяем атрибут тип продукта')
    @pytest.mark.parametrize('product_code', ['BI_41', 'BI_60', 'BI_1561', 'BI_2202'])
    def test_attr_system_product_type(self, ppinfo_client, product_code):
        required_attr = \
        [attr for attr in self.get_info_by_product_code(ppinfo_client, product_code)['hidingAttributes'] if
         attr['id'] == 'SYSTEM_ProductType'][0]

        type_attr = [attr for attr in self.get_info_by_product_code(ppinfo_client, product_code)['hidingAttributes'] if
                     attr['id'] == 'EXTRA_ProductType'][0]

        with allure.step('Проверяем, что системный тип продукта совпадает с обычным'):
            assert required_attr['values'] == type_attr['values'], f'{required_attr["values"]}!= {type_attr["values"]}'

    #### Участник QBR

    @allure.title('Проверяем атрибут тип продукта')
    @allure.issue('https://jira.mts.ru/browse/PPI-2750', 'PPInfo - Продукт - участник QBR')
    @pytest.mark.parametrize('product_code, value', [('BI_203', 'Да'), ('BI_63', 'Нет')])
    def test_attr_qbr_member(self, ppinfo_client, product_code, value):

        qbr_value = \
            [attr['values'][0]['value'] for attr in
             self.get_info_by_product_code(ppinfo_client, product_code)['hidingAttributes'] if
             attr['id'] == 'SYSTEM_qbr'][0]

        with allure.step('Проверяем, что у продуктов установлен корректный Участник QBR'):
            assert qbr_value == value, f'Ожидаемое значение участника QBR - {value}, фактическое - {qbr_value}'

    #### Просрочка
    @allure.title(
        'Если конец срока финансирования больше месяца от текущей даты, то в атрибуте просрочка должно быть указано количество месяцев от текущей даты до конца срока финансирования')
    @allure.issue('https://jira.mts.ru/browse/PPI-165', 'PPInfo - Системный атрибут "Просрочка"')
    @pytest.mark.parametrize('days', [31, 46])
    def test_attr_prosrochka_1_month(self, ppinfo_client, days):
        today = date.today()
        delta = timedelta(days=days)
        new_date = today - delta

        data = self.get_data_for_attr_change('PPInfo_data_endmoney', f'{new_date}T21:00:00.000Z',
                                             f'{new_date}T21:00:00.000Z')

        self.change_product(ppinfo_client, data)

        result = f'1 мес' if days == 31 else f'2 мес'
        with allure.step(f'Проверяем, что атрибут просрочка равен {result}'):
            required_attr = \
            [attr for attr in self.get_info_by_product_code(ppinfo_client, 'BI_2769')['hidingAttributes'] if
             attr['id'] == 'SYSTEM_Delay'][0]
            assert required_attr['values'][0]['value'] == result, f'{required_attr["values"][0]["value"]} != {result}'

    @allure.title(
        'Если конец срока финансирования закончился в пределах месяца от текущей даты, то в атрибуте просрочка должно быть указано Нет')
    @allure.issue('https://jira.mts.ru/browse/PPI-165', 'PPInfo - Системный атрибут "Просрочка"')
    @pytest.mark.parametrize('days', [1, 15, 30])
    def test_attr_prosrochka_no(self, ppinfo_client, days):
        today = date.today()
        delta = timedelta(days=days)
        new_date = today - delta

        data = self.get_data_for_attr_change('PPInfo_data_endmoney', f'{new_date}T21:00:00.000Z',
                                             f'{new_date}T21:00:00.000Z')

        self.change_product(ppinfo_client, data)

        with allure.step(f'Проверяем, что атрибут просрочка равен Нет'):
            required_attr = \
            [attr for attr in self.get_info_by_product_code(ppinfo_client, 'BI_2769')['hidingAttributes'] if
             attr['id'] == 'SYSTEM_Delay'][0]
            assert required_attr['values'][0]['value'] == 'Нет', f'{required_attr["values"][0]["value"]} != Нет'

    @allure.title('Если конец срока финансирования не заполнен, то в атрибуте просрочка тоже должно быть пусто')
    @allure.issue('https://jira.mts.ru/browse/PPI-165', 'PPInfo - Системный атрибут "Просрочка"')
    def test_attr_prosrochka_empty(self, ppinfo_client):
        data = self.get_data_for_attr_change('PPInfo_data_endmoney')

        self.change_product(ppinfo_client, data)

        with allure.step(f'Проверяем, что атрибут просрочка пустой'):
            required_attr = \
            [attr for attr in self.get_info_by_product_code(ppinfo_client, 'BI_2769')['hidingAttributes'] if
             attr['id'] == 'SYSTEM_Delay'][0]
            assert required_attr['values'] == [], f'{required_attr["values"][0]["value"]} не пустой'

    #### Центр затрат
    @allure.title('Если есть PO, то должен отображаться атрибут Центр Затрат')
    @allure.issue('https://jira.mts.ru/browse/PPI-186', 'PPInfo - Системный атрибут "Центр затрат"')
    @pytest.mark.skip(reason='не используется на проде')
    def test_attr_centr_zatrat_po(self, ppinfo_client):
        data = self.get_data_for_attr_change('employee_product_owner', 'ddsvetov1', 'Фамилия Имя Отчество')
        data['attributes'][0]['values'][0].update({'compatibility': False})

        self.change_product(ppinfo_client, data)

        with allure.step('Проверяем, что центр затрат заполнен'):
            required_attr = \
            [attr for attr in self.get_info_by_product_code(ppinfo_client, 'BI_2769')['hidingAttributes'] if
             attr['id'] == 'SYSTEM_CostCenter'][0]
            assert required_attr['values'][0]['value'] == 'RRJ', required_attr['values'][0]['value']

    @allure.title('Если нет PO, то должен отображаться атрибут Центр Затрат согласно CPO')
    @allure.issue('https://jira.mts.ru/browse/PPI-186', 'PPInfo - Системный атрибут "Центр затрат"')
    @pytest.mark.skip(reason='не используется на проде')
    def test_attr_centr_zatrat_cpo(self, ppinfo_client):
        data = self.get_data_for_attr_change('employee_product_owner')
        self.change_product(ppinfo_client, data)

        data = self.get_data_for_attr_change('employee_chief_PO', 'ddsvetov1', 'Фамилия Имя Отчество')
        data['attributes'][0]['values'][0].update({'compatibility': False})

        self.change_product(ppinfo_client, data)

        with allure.step('Проверяем, что центр затрат заполнен в зависимости от CPO'):
            required_attr = \
            [attr for attr in self.get_info_by_product_code(ppinfo_client, 'BI_2769')['hidingAttributes'] if
             attr['id'] == 'SYSTEM_CostCenter'][0]
            assert required_attr['values'][0]['value'] == 'RRJ', required_attr['values'][0]['value']

    @allure.title('Если нет PO и CPO, то должен отображаться пустой атрибут Центр Затрат')
    @allure.issue('https://jira.mts.ru/browse/PPI-186', 'PPInfo - Системный атрибут "Центр затрат"')
    @pytest.mark.skip(reason='не используется на проде')
    def test_attr_centr_zatrat_empty(self, ppinfo_client):
        data = self.get_data_for_attr_change('employee_product_owner')
        self.change_product(ppinfo_client, data)

        data = self.get_data_for_attr_change('employee_chief_PO')
        self.change_product(ppinfo_client, data)

        with allure.step('Проверяем, что центр затрат пустой '):
            required_attr = \
            [attr for attr in self.get_info_by_product_code(ppinfo_client, 'BI_2769')['hidingAttributes'] if
             attr['id'] == 'SYSTEM_CostCenter'][0]
            assert required_attr['values'] == [], required_attr['values']

    #### Основной продукт
    @allure.title('Установка основного продукта')
    def test_patch_main_product(self, ppinfo_client, rest_internal_client):
        data = self.get_data_for_attr_change('PPInfo_main_product', 'BI_3266', 'BI_3266')
        data['id'] = 'BI_19321'
        self.change_product(ppinfo_client, data)

        with allure.step(f"Проверяем, что продукт установлен в качестве атомарного"):
            assert any(i["code"] == "BI_19321" for i in
                       self.get_atomic_by_code(rest_internal_client, "BI_3266")['categories'][-1][
                           'products']), "BI_19321 нет в списке атомарных у BI_3266"

    @allure.title('Очистка основного продукта')
    def test_delete_main_product(self, ppinfo_client, rest_internal_client):
        data = self.get_data_for_attr_change('PPInfo_main_product')
        data['id'] = 'BI_19321'

        self.change_product(ppinfo_client, data)

        with allure.step(f"Проверяем, что продукт удален из атомарных"):
            if products := self.get_atomic_by_code(rest_internal_client, "BI_3266")['categories']:
                assert not any(i["code"] == "BI_19321" for i in
                               self.get_atomic_by_code(rest_internal_client, "BI_3266")['categories'][-1][
                                   'products']), "BI_19321 остался в списке атомарных у BI_3266"
            else:
                assert not products, 'BI_19321 остался в списке атомарных у BI_3266'

    @allure.title('Установка некорректного основного продукта')
    def test_patch_invalid_main_product(self, ppinfo_client):
        data = self.get_data_for_attr_change('PPInfo_main_product', 'BI_12345', 'BI_12345')
        data['id'] = 'BI_19321'
        self.error_change_product(ppinfo_client, data, status_code=400)

    @allure.title('Поиск продуктов в атрибуте по названию')
    @pytest.mark.parametrize('expected, pattern',
                             (['BI_60', 'Маркетолог'], ['BI_42', 'Cashback'], ['BI_41', 'Мой МТС']))
    def test_search_products_in_attr(self, ppinfo_client, expected, pattern):
        with allure.step(f'Проверяем, что продукт с кодом {expected} появился по запросу {pattern}'):
            name_list = all(
                pattern in i['name'] for i in self.search_products_in_attribute(ppinfo_client, pattern)['products'])
            code_list = any(
                expected == i['code'] for i in self.search_products_in_attribute(ppinfo_client, pattern)['products'])
            assert name_list and code_list, f"Продукт не найден: {self.search_products_in_attribute(ppinfo_client, pattern)['products']}"

    @allure.title('Поиск продуктов в атрибуте по несуществующему названию')
    @pytest.mark.parametrize('pattern', ['лабуда', 'ajsdjasjdoj'])
    def test_search_products_in_attr_invalid_name(self, ppinfo_client, pattern):
        with allure.step(f'Проверяем, что по запросу {pattern} ничего не найдено'):
            assert not self.search_products_in_attribute(ppinfo_client, pattern)[
                'products'], f'По паттерну {pattern} нашлось {self.search_products_in_attribute(ppinfo_client, pattern)["products"]}'

    #### Дата обновления атрибута

    @allure.title('Проверка наличия информации о дате обновления атрибута')
    @allure.issue('https://jira.mts.ru/browse/PPI-2861',
                  'PPinfo - На странице продукта у атрибутов не отображается Дата обновления атрибута')
    def test_attr_update_date(self, ppinfo_client):
        with allure.step(f'Проверяем, что информация о дате обновления атрибута есть'):
            data = self.get_info_by_product_code_by_user(ppinfo_client, 'BI_60')
            for i in data['groupAttributes']:
                if i['id'] == 'groupGeneral':
                    for attr in i['attributes']:
                        if attr['id'] == 'PPInfo_admin_data':
                            assert attr['updatedAt'], 'У атрибуты из группы атрибутов нет дата обновления'
            for user in data['users']:
                if user['id'] == 'employee_tech_lead':
                    assert user['updatedAt'], 'У атрибуты из руководства нет дата обновления'

    #### Активность RMS

    @allure.title('Атрибут Активность RMS, у продуктов отображено значение Да')
    @allure.issue('https://jira.mts.ru/browse/PPI-3121', 'PPInfo - Активность продукта в RMS')
    @pytest.mark.parametrize('bi_code', ['BI_0', 'BI_49'])
    def test_rms_active_yes(self, ppinfo_client, bi_code):
        data = self.get_info_by_product_code_by_user(ppinfo_client, bi_code)
        for i in data['groupAttributes']:
            if i['id'] == 'groupGeneral':
                for attr in i['attributes']:
                    if attr['id'] == 'Aktivnost_produkta_v_RMS':
                        assert attr['values'][0]['code'] == 'Yes', 'У атрибуты из группы атрибутов нет дата обновления'

    @allure.title('Атрибут Активность RMS, у продуктов отображено значение Нет')
    @allure.issue('https://jira.mts.ru/browse/PPI-3121', 'PPInfo - Активность продукта в RMS')
    @pytest.mark.parametrize('bi_code', ['BI_42', 'BI_241', 'BI_325'])
    def test_rms_active_no(self, ppinfo_client, bi_code):
        data = self.get_info_by_product_code_by_user(ppinfo_client, bi_code)
        for i in data['groupAttributes']:
            if i['id'] == 'groupGeneral':
                for attr in i['attributes']:
                    if attr['id'] == 'Aktivnost_produkta_v_RMS':
                        assert attr['values'][0]['code'] == 'No', 'У атрибуты из группы атрибутов нет дата обновления'

    @allure.title('Изменение атрибута и проверка даты обновления в разделе Основная информация')
    @allure.issue('https://jira.mts.ru/browse/PPI-3459',
                  'PPInfo - Отображение актуальности данных на странице продукта')
    def test_updated_at_main(self, ppinfo_client):

        with allure.step('Делаем изменение атрибута в продукте'):
            data = self.get_attribute_update_body('string_add')
            self.change_product(ppinfo_client, data)
            time.sleep(1)

        with allure.step('Записываем текущие дату и время и переводим в ISO 8601'):
            now_utc = datetime.now(timezone.utc)
            iso_format = now_utc.strftime('%Y-%m-%dT%H:%M')

        with allure.step('Записываем дату от бека и сравниваем с ранее записанной датой'):
            second_date = self.get_info_by_product_code(ppinfo_client, 'BI_2769')
            second_date = second_date['updatedAt']
            second_date = second_date[:16]

            assert iso_format == second_date, 'Дата не изменилась'

    @allure.title('Изменение атомарных продуктов и проверка даты обновления в разделе Атомарные')
    @allure.issue('https://jira.mts.ru/browse/PPI-3459',
                  'PPInfo - Отображение актуальности данных на странице продукта')
    def test_updated_at_atomic(self, ppinfo_client, rest_internal_client):

        with allure.step('Делаем изменение Основной продукт'):
            data = self.get_attribute_update_body('main_product_add')
            self.change_product(ppinfo_client, data)
            data = self.get_attribute_update_body('main_product_remove')
            self.change_product(ppinfo_client, data)
            time.sleep(1)

        with allure.step('Записываем текущие дату и время и переводим в ISO 8601'):
            now_utc = datetime.now(timezone.utc)
            iso_format = now_utc.strftime('%Y-%m-%dT%H:%M')

        with allure.step('Записываем дату от бека и сравниваем с ранее записанной датой'):
            second_date = self.get_atomic_by_code(rest_internal_client, 'BI_2683')
            second_date = second_date['updatedAt']
            second_date = second_date[:16]

            assert iso_format == second_date, 'Дата не изменилась'

    @allure.title('Изменение документов и проверка даты обновления в разделе Документы')
    @allure.issue('https://jira.mts.ru/browse/PPI-3459',
                  'PPInfo - Отображение актуальности данных на странице продукта')
    def test_updated_at_documents(self, ppinfo_client, rest_internal_client):

        data = {
            'name': 'filename_test_' + '.mp4'[1:] + 'public',
            'description': '.mp4',
            'type': 'document',
            'accessType': 'public'
        }

        with allure.step('Делаем изменение документа'):
            self.delete_doc(rest_internal_client, self.add_doc(rest_internal_client, data, '.mp4'))
            time.sleep(1)

        with allure.step('Записываем текущие дату и время и переводим в ISO 8601'):
            now_utc = datetime.now(timezone.utc)
            iso_format = now_utc.strftime('%Y-%m-%dT%H:%M')

        with allure.step('Записываем дату от бека и сравниваем с ранее записанной датой'):
            second_date = self.get_docs_by_bi_code(rest_internal_client, 'BI_2687')
            second_date = second_date['updatedAt']
            second_date = second_date[:16]

            assert iso_format == second_date, 'Дата не изменилась'

    @allure.title('Изменение демо и проверка даты обновления в разделе Демо')
    @allure.issue('https://jira.mts.ru/browse/PPI-3459',
                  'PPInfo - Отображение актуальности данных на странице продукта')
    def test_updated_at_demo(self, ppinfo_client, rest_internal_client):

        with allure.step('Делаем изменение демо'):
            demo_id = self.create_demo(rest_internal_client, self.get_demo_data(other={'linkedProducts': ["BI_3266"]}))['demoID']
            self.delete_demo(rest_internal_client, demo_id)
            time.sleep(1)

        with allure.step('Записываем текущие дату и время и переводим в ISO 8601'):
            now_utc = datetime.now(timezone.utc)
            iso_format = now_utc.strftime('%Y-%m-%dT%H:%M')

        with allure.step('Записываем дату от бека и сравниваем с ранее записанной датой'):
            second_date = self.get_demo_by_product_code(rest_internal_client, 'BI_3266')
            print(second_date)
            second_date = second_date['updatedAt']
            second_date = second_date[:16]

            assert second_date == iso_format, 'Дата не изменилась'

    @allure.title('Изменение ПГ и проверка даты обновления в разделе ПГ')
    @allure.issue('https://jira.mts.ru/browse/PPI-3459',
                  'PPInfo - Отображение актуальности данных на странице продукта')
    def test_updated_at_pg(self, ppinfo_client, rest_internal_client):
        before_swap = [i['actions'] for i in self.get_actions_list(rest_internal_client) if
                       i['id'] == 'abfe6e2a-b86c-49e2-990b-2d07e6087c31'][0]

        with allure.step('Делаем изменение ПГ'):
            if len(before_swap) > 2:
                id_1 = before_swap[1]['id']
                id_2 = before_swap[2]['id']

                self.swap_guides(rest_internal_client,
                                 {'id': id_1, 'groupID': 'abfe6e2a-b86c-49e2-990b-2d07e6087c31', 'toID': id_2})

                id_1 = before_swap[2]['id']
                id_2 = before_swap[1]['id']

                self.swap_guides(rest_internal_client,
                                 {'id': id_1, 'groupID': 'abfe6e2a-b86c-49e2-990b-2d07e6087c31', 'toID': id_2})

            time.sleep(1)

        with allure.step('Записываем текущие дату и время и переводим в ISO 8601'):
            now_utc = datetime.now(timezone.utc)
            iso_format = now_utc.strftime('%Y-%m-%dT%H:%M')

        with allure.step('Записываем дату от бека и сравниваем с ранее записанной датой'):
            second_date = self.get_active_actions(rest_internal_client, 'BI_3266')
            second_date = second_date['updatedAt']
            second_date = second_date[:16]

            assert iso_format == second_date, 'Дата не изменилась'
