import time
from datetime import datetime, timedelta

import allure
import pytest
from numpy.core.defchararray import title

from API.models.pmd.rest_external import RestApiExternal
from API.models.pmd.rest_internal_modules.actions import Actions
from API.models.ppinfo.rest import Rest
from API.models.ppinfo.tag import Tag


@allure.label('priority', 'Высокий')
@allure.feature('Получение продуктов')
@pytest.mark.api
class TestRestApiExternal(RestApiExternal, Rest, Tag):

    @allure.title('Получение продуктов без фильтрации')
    @pytest.mark.parametrize('limit', [1, 10, 100, 1000, 10000])
    def test_get_products(self, rest_external_client, limit):
        params = self.get_data_for_products_rest({'limit': limit})

        with allure.step('Проверяем, что поиск дал результаты'):
            assert (products := self.get_products_with_params(rest_external_client, params)), f'Поиск нашел {products}'

    @allure.title('Получение продуктов c атрибутами согласно ролевке')
    @allure.issue('https://jira.mts.ru/browse/PPI-4328', 'PPInfo - Управление передачей атрибутов по External API')
    @pytest.mark.parametrize('attribute', ['PPInfo_showcase', 'PPinfo_StructuralProductType1', 'PPinfo_start_close_date', 'Identifikator_SOL', 'employee_business_owner', 'Mnozhestvo', 'Rukovoditel_etogo_balagana', 'Odin_produkt', 'Mnogo_produktov', 'Test_mnozh_ssylki', 'PPinfo_resolution', 'PPInfo_site_landing', 'Osnovnoi_proekt_Jira'])
    def test_get_products_with_attributes_by_roles(self, rest_external_client, ppinfo_client, attribute):

        try:
            self.delete_attr(ppinfo_client, attr_id=attribute, tag_id='transfer_settings')
            time.sleep(1)
        except AssertionError:
            pass

        params = self.get_data_for_products_rest()
        products = self.get_products_with_params(rest_external_client, params)

        count = 0

        for product in products:
            for attr in product['attributes']:
                if attr['code'] == attribute:
                    count += 1
        assert count == 0, f'С выключенным атрибутом в настройке в  external api передается атрибут '
        try:
            self.add_attr(ppinfo_client, attr_id=attribute, tag_id='transfer_settings')
            time.sleep(1)
        except AssertionError:
            pass

        params = self.get_data_for_products_rest()
        products = self.get_products_with_params(rest_external_client, params)

        count = 0

        for product in products:
            for attr in product['attributes']:
                if attr['code'] == attribute:
                    count += 1
        assert count > 0, f'Со включенным атрибутом в настройке в  external api не передается атрибут '

    @allure.title('Получение одного продукта c атрибутами согласно ролевке')
    @allure.issue('https://jira.mts.ru/browse/PPI-4328', 'PPInfo - Управление передачей атрибутов по External API')
    @pytest.mark.parametrize('attribute', ['PPInfo_showcase', 'PPinfo_StructuralProductType1', 'PPinfo_start_close_date', 'Identifikator_SOL', 'employee_business_owner', 'Mnozhestvo', 'Rukovoditel_etogo_balagana', 'Odin_produkt', 'Mnogo_produktov', 'Test_mnozh_ssylki', 'PPinfo_resolution', 'PPInfo_site_landing', 'Osnovnoi_proekt_Jira'])
    def test_get_product_with_attributes_by_roles(self, rest_external_client, ppinfo_client, attribute):

        try:
            self.delete_attr(ppinfo_client, attr_id=attribute, tag_id='transfer_settings')
            time.sleep(1)
        except AssertionError:
            pass

        product = self.get_product_by_code(rest_external_client, 'BI_60')

        count = 0

        for attr in product['attributes']:
            if attr['code'] == attribute:
                count += 1
        assert count == 0, f'С выключенным атрибутом в настройке в  external api передается атрибут '
        try:
            self.add_attr(ppinfo_client, attr_id=attribute, tag_id='transfer_settings')
            time.sleep(1)
        except AssertionError:
            pass

        product = self.get_product_by_code(rest_external_client, 'BI_60')

        count = 0

        for attr in product['attributes']:
            if attr['code'] == attribute:
                count += 1
        assert count > 0, f'Со включенным атрибутом в настройке в  external api не передается атрибут '

    @allure.title('В историчности приходят атрибуты согласно настройке')
    @allure.issue('https://jira.mts.ru/browse/PPI-4328', 'PPInfo - Управление передачей атрибутов по External API')
    def test_attributes_in_filters_by_role(self, rest_external_client, ppinfo_client,
                                           ppinfo_user_client, pmd_admin_gw_client):

        try:
            self.delete_attr(ppinfo_client, attr_id='PPInfo_product_com', tag_id='transfer_settings')
            time.sleep(1)
        except AssertionError:
            pass

        product_attrs = []
        product_story = self.get_story_by_product_code(rest_external_client, 'BI_60')

        for attr in product_story:
            product_attrs.append(attr['name'])

        assert 'Дата ПК' not in product_attrs, 'Фильтр есть, хотя согласно ролевке не должен быть'

        try:
            self.add_attr(ppinfo_client, attr_id='PPInfo_product_com', tag_id='transfer_settings')
            time.sleep(1)
        except AssertionError:
            pass

        product_attrs = []
        product_story = self.get_story_by_product_code(rest_external_client, 'BI_60')

        for attr in product_story:
            product_attrs.append(attr['name'])

        assert 'Дата ПК' in product_attrs, 'Фильтр есть, хотя согласно ролевке не должен быть'



    @allure.title('Получение продуктов со всеми параметрами в запросе')
    def test_get_public_product_all_params(self, rest_external_client):
        params = self.get_data_for_products_rest(
            {'limit': 10, 'offset': 0, 'version': 1688998150, 'filterResponse': 'PPinfo_market'})

        self.get_products_with_params(rest_external_client, params)

    @allure.title('Получение продуктов с атрибутом "Причина удаления"')
    def test_get_public_product_deleted(self, ppinfo_client, rest_external_client, cache_client):
        params = self.get_data_for_products_rest({'filterResponse': 'Prichina_udaleniia'})

        response = self.get_products_with_params(rest_external_client, params)

        categories_codes = []

        for item in self.get_archive_on_main_page(cache_client):
            if item['code'] == 'deleted':
                for product in item['products']:
                    categories_codes.append(product['code'])

        pr_codes = []
        for product in response:
            if product['attributes']:
                pr_codes.append(product['code'])

        assert sorted(categories_codes) == sorted(pr_codes), f'Количество удаленных продуктов {len(pr_codes)}, а количество ' \
                                                   f'продуктов с причиной удаления {len(categories_codes)}'


    @allure.title('Получение продуктов с фильтрацией ответа по двум атрибутам')
    def test_get_public_product_2filters(self, rest_external_client):

        params = self.get_data_for_products_rest({'filterResponse': 'Prichina_udaleniia,PPinfo_market'})

        response = self.get_products_with_params(rest_external_client, params)

        with allure.step('Проверяем, что количество атрибутов у продуктов в ответе не больше 2'):
            for product in response:
                assert len(product['attributes']) in (
                    0, 1, 2), f"Количество атрибутов у продукта {product['name']} в ответе {len(product['attributes'])}"

    @allure.title('Получение продуктов с фильтрацией ответа по несуществующему атрибуту')
    def test_get_public_product_invalid_filter(self, rest_external_client):

        params = self.get_data_for_products_rest({'filterResponse': 'not_an_attr'})

        response = self.get_products_with_params(rest_external_client, params)

        with allure.step('Проверяем, что количество атрибутов у продуктов в ответе равно нулю'):
            for product in response:
                assert len(product[
                               'attributes']) == 0, f"Количество атрибутов у продукта {product['name']} в ответе {len(product['attributes'])}"

    @allure.title('Получение продуктов по code')
    @pytest.mark.parametrize('product_code', ['BI_60', 'BI_41'])
    def test_get_product_by_code(self, rest_external_client, product_code):
        assert self.get_product_by_code(rest_external_client, product_code)

    @allure.title('Получение продуктов по несуществующему code')
    @allure.issue('https://jira.mts.ru/browse/PPI-2088',
                  'PPinfo - 500 ошибка в методе удаления продукта по несуществующему BI коду')
    @pytest.mark.parametrize('product_code', ['BI_12345'])
    def test_get_product_by_invalid_code(self, rest_external_client, product_code):
        self.get_product_by_code_404(rest_external_client, product_code)

    @allure.title('Получение лого продуктов по code')
    @allure.issue('https://jira.mts.ru/browse/PPI-2552', 'PPInfo - Добавить метод GET/ logo в External API')
    @pytest.mark.parametrize('product_code', ['BI_60', 'BI_1905', 'BI_1984'])
    def test_get_product_logo_by_code(self, rest_external_client, product_code):
        assert self.get_logo_by_code(rest_external_client, product_code) in ['image/png',
                                                                             'image/jpeg'], 'Формат картинок не тот'

    @allure.title('Получение информации по атрибутам')
    @pytest.mark.parametrize('attributes_code', ['PPinfo_MTS_Brand', 'PPInfo_type_develop', 'PPInfo_business_area'])
    def test_get_info_about_attribute(self, rest_external_client, attributes_code):
        params = {
            "codes": attributes_code
        }

        assert self.get_attribute_by_code(rest_external_client,
                                          params), f'Ничего не нашло по заданному атрибуту {attributes_code}'

    @allure.title('Получение информации по несуществующим атрибутам')
    @pytest.mark.parametrize('attributes_code', ['фыввфы', 'attr'])
    def test_get_info_about_attribute_error(self, rest_external_client, attributes_code):
        params = {
            'codes': attributes_code
        }

        assert not self.get_attribute_by_code(rest_external_client,
                                              params), f'По заданному атрибуту {attributes_code} нашлось {self.get_attribute_by_code(rest_external_client, params)}'

    @allure.title('Изменение строки в продукте и проверка отображения записей в историчности для external api')
    @allure.issue('https://jira.mts.ru/browse/PPI-3339',
                  'PPInfo - Передача истории изменений атрибутов по External API')
    @pytest.mark.parametrize('role', ['admin', 'user'])
    def test_story_for_external_string(self, ppinfo_user_client, ppinfo_client, rest_external_client,
                                       rest_internal_client, role):
        if role == 'admin':
            product_id = self.create_and_replace_product_admin(rest_internal_client, ppinfo_client,
                                                               self.get_moves['string'],
                                                               external=True)
        else:
            product_id = self.create_and_replace_product_user(rest_internal_client, ppinfo_client, ppinfo_user_client,
                                                              self.get_moves['string'],
                                                              external=True)
        data = self.get_story_by_product_code(rest_external_client, product_id)

        assert data[0]['currentValues'] == [], 'Запись на очистку строки не произошла'
        assert data[0]['previousValue'] == ['test2'], 'Запись на очистку строки не произошла'

        assert data[1]['currentValues'] == ['test2'], 'Запись на изменение строки не произошла'
        assert data[1]['previousValue'] == ['test'], 'Запись на изменение строки не произошла'

        assert data[2]['currentValues'] == ['test'], 'Запись на добавление строки не произошла'
        assert data[2]['previousValue'] == [], 'Запись на добавление строки не произошла'

    @allure.title('Изменение мэниселекта в продукте и проверка отображения записей в историчности для external api')
    @allure.issue('https://jira.mts.ru/browse/PPI-3339',
                  'PPInfo - Передача истории изменений атрибутов по External API')
    @pytest.mark.parametrize('role', ['admin', 'user'])
    def test_story_for_external_manyselect(self, ppinfo_user_client, ppinfo_client, rest_external_client,
                                           rest_internal_client, role):

        if role == 'admin':
            product_id = self.create_and_replace_product_admin(rest_internal_client, ppinfo_client,
                                                               self.get_moves['many_select'],
                                                               external=True)
        else:
            product_id = self.create_and_replace_product_user(rest_internal_client, ppinfo_client, ppinfo_user_client,
                                                              self.get_moves['many_select'],
                                                              external=True)
        data = self.get_story_by_product_code(rest_external_client, product_id)

        assert data[0]['currentValues'] == [], 'Запись на очищение мэниселекта не записалось'
        assert data[0]['previousValue'] == ['Атомарный'], 'Запись на изменение мэниселекта не записалось'

        assert data[1]['currentValues'] == ['Атомарный'], 'Запись на изменение мэниселекта не записалось'
        assert data[1]['previousValue'] == ['Основной'], 'Запись на добавление мэниселекта не записалось'

        assert data[2]['currentValues'] == ['Основной'], 'Запись на добавление мэниселекта не записалось'
        assert data[2]['previousValue'] == [], 'Запись на очищение мэниселекта не записалось'

    @allure.title('Изменение даты в продукте и проверка отображения записей в историчности для external api')
    @allure.issue('https://jira.mts.ru/browse/PPI-3339',
                  'PPInfo - Передача истории изменений атрибутов по External API')
    @pytest.mark.parametrize('role', ['admin', 'user'])
    def test_story_for_external_date(self, ppinfo_user_client, ppinfo_client, rest_external_client,
                                     rest_internal_client, role):

        if role == 'admin':
            product_id = self.create_and_replace_product_admin(rest_internal_client, ppinfo_client,
                                                               self.get_moves['date'],
                                                               external=True)
        else:
            product_id = self.create_and_replace_product_user(rest_internal_client, ppinfo_client, ppinfo_user_client,
                                                              self.get_moves['date'],
                                                              external=True)
        data = self.get_story_by_product_code(rest_external_client, product_id)

        assert data[0]['currentValues'] == [], 'Запись на очищение даты не записалось'
        assert data[0]['previousValue'] == ['2024-01-24T03:00:00Z'], 'Запись на изменение даты не записалось'

        assert data[1]['currentValues'] == ['2024-01-24T03:00:00Z'], 'Запись на изменение даты не записалось'
        assert data[1]['previousValue'] == ['2024-01-23T03:00:00Z'], 'Запись на добавление даты не записалось'

        assert data[2]['currentValues'] == ['2024-01-23T03:00:00Z'], 'Запись на добавление даты не записалось'
        assert data[2]['previousValue'] == [], 'Запись на очищение даты не записалось'

    @allure.title('Изменение числа в продукте и проверка отображения записей в историчности для external api')
    @allure.issue('https://jira.mts.ru/browse/PPI-3339',
                  'PPInfo - Передача истории изменений атрибутов по External API')
    @pytest.mark.parametrize('role', ['admin', 'user'])
    def test_story_for_external_num(self, ppinfo_user_client, ppinfo_client, rest_external_client, rest_internal_client,
                                    role):

        if role == 'admin':
            product_id = self.create_and_replace_product_admin(rest_internal_client, ppinfo_client,
                                                               self.get_moves['num'],
                                                               external=True)
        else:
            product_id = self.create_and_replace_product_user(rest_internal_client, ppinfo_client, ppinfo_user_client,
                                                              self.get_moves['num'],
                                                              external=True)
        data = self.get_story_by_product_code(rest_external_client, product_id)

        assert data[0]['currentValues'] == [], 'Запись на очищение числа не записалось'
        assert data[0]['previousValue'] == ['777'], 'Запись на изменение числа не записалось'

        assert data[1]['currentValues'] == ['777'], 'Запись на изменение числа не записалось'
        assert data[1]['previousValue'] == ['666'], 'Запись на добавление числа не записалось'

        assert data[2]['currentValues'] == ['666'], 'Запись на добавление числа не записалось'
        assert data[2]['previousValue'] == [], 'Запись на очищение числа не записалось'

    @allure.title('Изменение Юзера в продукте и проверка отображения записей в историчности для external api')
    @allure.issue('https://jira.mts.ru/browse/PPI-3339',
                  'PPInfo - Передача истории изменений атрибутов по External API')
    @pytest.mark.parametrize('role', ['admin', 'user'])
    def test_story_for_external_user(self, ppinfo_user_client, ppinfo_client, rest_external_client,
                                     rest_internal_client, role):

        if role == 'admin':
            product_id = self.create_and_replace_product_admin(rest_internal_client, ppinfo_client,
                                                               self.get_moves['user'],
                                                               external=True)
        else:
            product_id = self.create_and_replace_product_user(rest_internal_client, ppinfo_client, ppinfo_user_client,
                                                              self.get_moves['user'],
                                                              external=True)
        data = self.get_story_by_product_code(rest_external_client, product_id)

        assert data[0]['currentValues'] == [], 'Запись на очищение юзера не записалось'
        assert data[0]['previousValue'] == [
            'Гладышева Алёна Ивановна (aigladyshev)'], 'Запись на изменение юзера не записалось'

        assert data[1]['currentValues'] == [
            'Гладышева Алёна Ивановна (aigladyshev)'], 'Запись на изменение юзера не записалось'
        assert data[1]['previousValue'] == [
            'Светов Даниил Дмитриевич (ddsvetov1)'], 'Запись на добавление юзера не записалось'

        assert data[2]['currentValues'] == [
            'Светов Даниил Дмитриевич (ddsvetov1)'], 'Запись на добавление юзера не записалось'
        assert data[2]['previousValue'] == [], 'Запись на очищение юзера не записалось'

    @allure.title('Изменение множества в продукте и проверка отображения записей в историчности для external api')
    @allure.issue('https://jira.mts.ru/browse/PPI-3339',
                  'PPInfo - Передача истории изменений атрибутов по External API')
    @pytest.mark.parametrize('role', ['admin', 'user'])
    def test_story_for_external_multi(self, ppinfo_user_client, ppinfo_client, rest_external_client,
                                      rest_internal_client, role):

        if role == 'admin':
            product_id = self.create_and_replace_product_admin(rest_internal_client, ppinfo_client,
                                                               self.get_moves['multi'],
                                                               external=True)
        else:
            product_id = self.create_and_replace_product_user(rest_internal_client, ppinfo_client, ppinfo_user_client,
                                                              self.get_moves['multi'],
                                                              external=True)
        data = self.get_story_by_product_code(rest_external_client, product_id)

        assert data[0]['currentValues'] == [], 'Запись на очищение множества не записалось'
        assert data[0]['previousValue'] == ['Второй'], 'Запись на изменение множества не записалось'

        assert data[1]['currentValues'] == ['Второй'], 'Запись на изменение множества не записалось'
        assert sorted(data[1]['previousValue']) == ['Второй', 'Первый', 'Третий'], 'Запись на добавление множества не записалось'

        assert sorted(data[2]['currentValues']) == ['Второй', 'Первый', 'Третий'], 'Запись на добавление множества не записалось'
        assert data[2]['previousValue'] == [], 'Запись на очищение множества не записалось'

    @allure.title(
        'Изменение многострочного текста в продукте и проверка отображения записей в историчности для external api')
    @allure.issue('https://jira.mts.ru/browse/PPI-3339',
                  'PPInfo - Передача истории изменений атрибутов по External API')
    @pytest.mark.parametrize('role', ['admin', 'user'])
    def test_story_for_external_multistring(self, ppinfo_user_client, ppinfo_client, rest_external_client,
                                            rest_internal_client, role):

        if role == 'admin':
            product_id = self.create_and_replace_product_admin(rest_internal_client, ppinfo_client,
                                                               self.get_moves['multistring'],
                                                               external=True)
        else:
            product_id = self.create_and_replace_product_user(rest_internal_client, ppinfo_client, ppinfo_user_client,
                                                              self.get_moves['multistring'],
                                                              external=True)
        data = self.get_story_by_product_code(rest_external_client, product_id)

        assert data[0]['currentValues'] == [], 'Запись на очищение многострочного текста не записалось'
        assert data[0]['previousValue'] == ['test2'], 'Запись на изменение многострочного текста не записалось'

        assert data[1]['currentValues'] == ['test2'], 'Запись на изменение многострочного текста не записалось'
        assert data[1]['previousValue'] == ['test'], 'Запись на добавление многострочного текста не записалось'

        assert data[2]['currentValues'] == ['test'], 'Запись на добавление многострочного текста не записалось'
        assert data[2]['previousValue'] == [], 'Запись на очищение многострочного текста не записалось'

    @allure.title('Изменение ссылки в продукте и проверка отображения записей в историчности для external api')
    @allure.issue('https://jira.mts.ru/browse/PPI-3339',
                  'PPInfo - Передача истории изменений атрибутов по External API')
    @pytest.mark.parametrize('role', ['admin', 'user'])
    def test_story_for_external_link(self, ppinfo_user_client, ppinfo_client, rest_external_client,
                                     rest_internal_client, role):

        if role == 'admin':
            product_id = self.create_and_replace_product_admin(rest_internal_client, ppinfo_client,
                                                               self.get_moves['link'],
                                                               external=True)
        else:
            product_id = self.create_and_replace_product_user(rest_internal_client, ppinfo_client, ppinfo_user_client,
                                                              self.get_moves['link'],
                                                              external=True)
        data = self.get_story_by_product_code(rest_external_client, product_id)

        assert data[0]['currentValues'] == [], 'Запись на очищение ссылки не записалось'
        assert data[0]['previousValue'] == [
            'https://stage.prodboard.mts.ru/product/BI_42/main'], 'Запись на изменение ссылки не записалось'

        assert data[1]['currentValues'] == [
            'https://stage.prodboard.mts.ru/product/BI_42/main'], 'Запись на изменение ссылки не записалось'
        assert data[1]['previousValue'] == ['https://cashback.mts.ru'], 'Запись на добавление ссылки не записалось'

        assert data[2]['currentValues'] == ['https://cashback.mts.ru'], 'Запись на добавление ссылки не записалось'
        assert data[2]['previousValue'] == [], 'Запись на очищение ссылки не записалось'

    @allure.title('Изменение ссылки в продукте и проверка отображения записей в историчности для external api')
    @allure.issue('https://jira.mts.ru/browse/PPI-3339',
                  'PPInfo - Передача истории изменений атрибутов по External API')
    def test_story_for_external_main_product(self, ppinfo_user_client, ppinfo_client, rest_external_client,
                                             rest_internal_client):

        product_id = self.create_and_replace_product_admin(rest_internal_client, ppinfo_client,
                                                           self.get_moves['main_product'],
                                                           external=True)
        data = self.get_story_by_product_code(rest_external_client, product_id)

        assert data[0]['currentValues'] == ['Основной'], 'Запись на изменение с Атомарного на Основной не произошла'
        assert data[0]['previousValue'] == [
            'Атомарный'], 'Предыдущее значение для изменения с Атомарного на Основной не соответствует'

        assert data[1]['currentValues'] == [], 'Запись на очистку основного продукта не произошла'
        assert data[1]['previousValue'] == [
            'Не трогать (продукт для автотестов) (https://stage.prodboard.mts.ru/product/3266/main)'], 'Предыдущее значение для очистки основного продукта не соответствует'

        assert data[2]['currentValues'] == [
            'Не трогать (продукт для автотестов) (https://stage.prodboard.mts.ru/product/3266/main)'], 'Запись на добавление основного продукта не произошла'
        assert data[2]['previousValue'] == [
            '1_Не трогать, для АТ, делегирование del (https://stage.prodboard.mts.ru/product/2683/main)'], 'Предыдущее значение для добавления основного продукта не соответствует'

        assert data[3]['currentValues'] == ['Атомарный'], 'Запись на изменение с Основного на Атомарный не произошла'
        assert data[3]['previousValue'] == [
            'Основной'], 'Предыдущее значение для изменения с Основного на Атомарный не соответствует'

        assert data[4]['currentValues'] == [
            '1_Не трогать, для АТ, делегирование del (https://stage.prodboard.mts.ru/product/2683/main)'], 'Запись на добавление основного продукта не произошла'
        assert data[4]['previousValue'] == [], 'Предыдущее значение для добавления основного продукта не соответствует'

    @allure.title(
        'Корректность отображения инициатора и модератора для external api историчности при изменений сделанных админом')
    @allure.issue('https://jira.mts.ru/browse/PPI-3339',
                  'PPInfo - Передача истории изменений атрибутов по External API')
    def test_users_for_external_admin(self, ppinfo_client, rest_external_client, rest_internal_client):
        product_id = self.create_and_replace_product_admin(rest_internal_client, ppinfo_client, ['string_add'],
                                                           external=True)

        data = self.get_story_by_product_code(rest_external_client, product_id)

        assert (data[0]['initiator'] == {'fullName': 'Светов Даниил Дмитриевич', 'login': 'ddsvetov1'}
                and data[0]['moderator'] == {'fullName': 'Светов Даниил Дмитриевич', 'login': 'ddsvetov1'}), \
            'Неверный инициатор или модератор'

    @allure.title(
        'Корректность отображения инициатора и модератора для external api историчности при изменений сделанных пользователем')
    @allure.issue('https://jira.mts.ru/browse/PPI-3339',
                  'PPInfo - Передача истории изменений атрибутов по External API')
    def test_users_for_external_user(self, ppinfo_user_client, ppinfo_client, rest_external_client,
                                     rest_internal_client):
        product_id = self.create_and_replace_product_user(rest_internal_client, ppinfo_client, ppinfo_user_client,
                                                          ['string_add'], external=True)
        data = self.get_story_by_product_code(rest_external_client, product_id)

        assert data[0]['initiator'] == {'fullName': 'Костров Алексей Игоревич', 'login': 'aikostrov1'} and data[0][
            'moderator'] == {'fullName': 'Светов Даниил Дмитриевич',
                             'login': 'ddsvetov1'}, 'Неверный инициатор или модератор'

    @allure.title(
        'Корректное отображение даты и времени в историчности  для external api')
    @allure.issue('https://jira.mts.ru/browse/PPI-3339',
                  'PPInfo - Передача истории изменений атрибутов по External API')
    def test_users_for_external_date(self, ppinfo_user_client, ppinfo_client, rest_external_client,
                                     rest_internal_client):
        product_id = self.create_and_replace_product_user(rest_internal_client, ppinfo_client, ppinfo_user_client,
                                                          ['string_add'], external=True)
        data = self.get_story_by_product_code(rest_external_client, product_id)

        current_datetime = datetime.now() + timedelta(hours=3)

        date_from_response = datetime.strptime(data[0]['date'], '%d.%m.%Y %H:%M')

        assert date_from_response.date() == current_datetime.date(), f'Дата не соответствует текущему {date_from_response.date()} != {current_datetime.date()}'
        assert date_from_response.time().strftime("%H:%M") == current_datetime.time().strftime(
            "%H:%M"), f'Время не соответствует текущему {date_from_response.time()} != {current_datetime.time()}'

    @allure.title(
        'Изменение значения через автомодерацию для external api')
    @allure.issue('https://jira.mts.ru/browse/PPI-3339',
                  'PPInfo - Передача истории изменений атрибутов по External API')
    def test_users_auto_moderation_for_external(self, ppinfo_user_client, ppinfo_client, rest_external_client,
                                                rest_internal_client):
        product_id = self.create_and_replace_product_user(rest_internal_client, ppinfo_client, ppinfo_user_client,
                                                          self.get_moves['string'],
                                                          auto_moderation=True, external=True)
        data = self.get_story_by_product_code(rest_external_client, product_id)

        assert data[0]['currentValues'] == [], 'Запись на очистку строки не произошла'
        assert data[0]['previousValue'] == ['test2'], 'Запись на изменение строки не произошла'

        assert data[1]['currentValues'] == ['test2'], 'Запись на изменение строки не произошла'
        assert data[1]['previousValue'] == ['test'], 'Запись на добавление строки не произошла'

        assert data[2]['currentValues'] == ['test'], 'Запись на добавление строки не произошла'
        assert data[2]['previousValue'] == [], 'Запись на очистку строки не произошла'



@allure.label('priority', 'Высокий')
@allure.feature('PG external')
@pytest.mark.api
class TestPGExternal(RestApiExternal, Actions):

    @allure.title(
        'Получение списка шагов для внешних сервисов')
    def test_get_steps(self, rest_external_client):

        print(self.get_pg_steps(rest_external_client, 'Vneshnii'))

    @allure.title('Получение шагов для общего Product Guide')
    @pytest.mark.parametrize('product_type', ['Vneshnii', 'Vnutrennii'])
    def test_get_all_pg_steps(self, rest_external_client, product_type):
        with allure.step('Проверяем, что хотя бы в одной группе пришли шаги'):
            assert any(actions['actions'] for actions in
                       self.get_pg_steps(rest_external_client, product_type)), 'Шаги не пришли'

    @allure.title('В общий Product Guide приходят все активные шаги нужного типа')
    @pytest.mark.parametrize('product_type', ['Vneshnii', 'Vnutrennii'])
    def test_common_pg_has_all_steps(self, rest_internal_client, rest_external_client, product_type):
        settings_steps = self.get_actions_list(rest_internal_client)
        common_steps = self.get_pg_steps(rest_external_client, product_type)

        req_type = 'внешний' if product_type == 'Vneshnii' else 'внутренний'

        for ind in range(len(settings_steps)):
            required_steps_ids = [step['id'] for step in settings_steps[ind]['actions'] if
                                  step['isActive'] and req_type in step['typeProduct'].lower()]
            common_steps_ids = [step['id'] for step in common_steps[ind]['actions']]
            with allure.step(f'Проверяем, что в группе {settings_steps[ind]["groupName"]} нужные шаги'):
                assert required_steps_ids == common_steps_ids, f'В группе {settings_steps[ind]["groupName"]} не те шаги'


    @allure.title('В общий Product Guide попадают все шаги, вне зависимости от фильтров')
    @pytest.mark.parametrize('product_type', ['Vneshnii', 'Vnutrennii'])
    @pytest.mark.parametrize(['attr_name', 'value'], [['PPinfo_status', 'Arkhiv'],
                                                      ['PPinfo_MTS_Brand', '(PPinfo_MTSBrand)MTSBrand_no'],
                                                      ['PPinfo_category_product', '(PPInfo_category_spravochnik)AI'],
                                                      ['PPinfo_market', '(PPinfo_market)B2C'],
                                                      ['PPInfo_type_develop', '(PPInfo_spravoch_type)Own'],
                                                      ['Nalichie_vneshnikh_KTS', 'Da']])
    def test_common_pg_no_filter_affection(self, rest_internal_client, rest_external_client, attr_name, value, product_type):
        with allure.step(f'Проверяем фильтр {attr_name}'):
            filter_value = self.get_filter_value([[attr_name, value]])
        action_id = self.create_action(rest_internal_client,
                                       self.get_guide_data(params={'isActive': True, 'filter': filter_value}))

        all_steps = self.get_pg_steps(rest_external_client, product_type)[-1]['actions']
        self.delete_action(rest_internal_client, action_id)
        with allure.step('Проверяем, что шаг есть в общем Product Guide'):
            assert any(action_id == new_id['id'] for new_id in all_steps), 'Шаг не появился'

    @allure.title('Создание вложенного шага PG / Отображение в общем Product Guide')
    @pytest.mark.parametrize('product_type', ['Vneshnii', 'Vnutrennii'])
    def test_add_sub_action_product_guide(self, rest_internal_client, rest_external_client, product_type):
        action_ids = self.create_sub_action(rest_internal_client)
        main_action_id, sub_action_id = action_ids[0], action_ids[1]

        with allure.step(f'Проверяем, что вложенный шаг отображается на вкладке {product_type}'):
            action = [i for i in self.get_pg_steps(rest_external_client, product_type)[0]['actions'] if
                      i['id'] == main_action_id][0]
            assert action['subActions'], 'Вложенных шагов нет'
            assert any(
                i['id'] == sub_action_id for i in action['subActions']), 'Нужный вложенный шаг не добавился к главному'

        self.delete_action(rest_internal_client, main_action_id)
        with allure.step('Проверяем, что шага по этому айди больше нет'):
            self.get_action_404(rest_internal_client, main_action_id), 'Шаг есть'


    @allure.title('Получение всех файлов')
    @pytest.mark.parametrize('product_type', ['Vneshnii', 'Vnutrennii'])
    def test_add_sub_action_product_guide(self, rest_internal_client, rest_external_client, product_type):
        action_ids = self.create_sub_action(rest_internal_client)
        main_action_id, sub_action_id = action_ids[0], action_ids[1]

        with allure.step(f'Проверяем, что вложенный шаг отображается на вкладке {product_type}'):
            action = [i for i in self.get_pg_steps(rest_external_client, product_type)[0]['actions'] if
                      i['id'] == main_action_id][0]
            assert action['subActions'], 'Вложенных шагов нет'
            assert any(
                i['id'] == sub_action_id for i in action['subActions']), 'Нужный вложенный шаг не добавился к главному'

        self.delete_action(rest_internal_client, main_action_id)
        with allure.step('Проверяем, что шага по этому айди больше нет'):
            self.get_action_404(rest_internal_client, main_action_id), 'Шаг есть'

