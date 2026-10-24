import allure
import pytest

from API.models.ppinfo.product_v1 import ProductV1
from API.models.ppinfo.product_v2 import ProductV2


@pytest.mark.api
@allure.feature('ПО, ИМС, Атомарные')
class TestProductV1(ProductV1):

    @allure.title('Получение приложений и ИС для отображения тех. состав')
    @pytest.mark.parametrize('code', ['BI_42'])
    def test_ims_sam(self, ppinfo_api_client, code):
        self.get_ims_sam(ppinfo_api_client, code)

    @allure.title('Невалидное получение приложений и ИС')
    @pytest.mark.parametrize('code', ['aasd'])
    def test_ims_sam_error(self, ppinfo_api_client, code):
        self.get_ims_sam_error(ppinfo_api_client, code)

    @allure.title('Получаем атрибуты по спецификации внешних')
    @pytest.mark.parametrize('product_type', ['Vneshnii', 'Vnutrennii'])
    def test_get_attr_by_spec(self, ppinfo_client, product_type):
        self.get_attr_by_spec(ppinfo_client, product_type)

    @allure.title('Получение проектов давинчи')
    @pytest.mark.parametrize('bi', ['60', '1361'])
    def test_davinci(self, ppinfo_client, bi):
        count = len(self.get_davinci(ppinfo_client, bi)['projects'])
        assert count <= 15, 'Проектов Слишком много'

@pytest.mark.api
@pytest.mark.last
@allure.feature('Создание и редактирование админом')
class TestAddAndReplaceProductAdminApi(ProductV1, ProductV2):

    @allure.title('Создание внешнего/внутреннего продукта админом')
    @allure.issue('https://jira.mts.ru/browse/PPI-857', 'PPInfo - Определять новые продукты по дате создания')
    @pytest.mark.parametrize('product_type', ['Vneshnii', 'Vnutrennii'])
    def test_create_product_by_admin(self, ppinfo_client, pmd_internal_gw_client, product_type):
        data = self.get_data_for_product_creation(product_type)

        product_id = self.create_product(ppinfo_client, data)

        with allure.step('Проверяем, что продукт создался'):
            assert (result := self.get_info_by_product_code(ppinfo_client, product_id)), 'Нет информации по продукту'

        with allure.step('Проверяем что у продукта есть параметр NEW'):
            assert result['isNew'], 'У продукта нет чипса NEW'

        self.delete_product(pmd_internal_gw_client, product_id)

        with allure.step('Проверяем, что продукт удалился'):
            assert self.get_info_by_product_code(ppinfo_client, product_id)['reasonDeletion'], 'Продукт не удалился'

    @allure.title('Невалидное создание продукта админом без названия')
    @pytest.mark.parametrize('product_type', ['Vneshnii', 'Vnutrennii'])
    def test_create_invalid_product_empty_name(self, ppinfo_client, product_type):
        data = self.get_data_for_product_creation(product_type=product_type, name="")

        self.error_create_product(ppinfo_client, data)

    @allure.title('Невалидное создание продукта админом без описания')
    @pytest.mark.parametrize('product_type', ['Vneshnii', 'Vnutrennii'])
    def test_create_invalid_product_empty_description(self, ppinfo_client, product_type):
        data = self.get_data_for_product_creation(product_type=product_type, descr="")

        self.error_create_product(ppinfo_client, data)

    @allure.title('Невалидное создание внешнего продукта админом без статуса')
    def test_create_invalid_product_no_status(self, ppinfo_client):
        data = self.get_data_for_product_creation(product_type='Vneshnii')
        data['attributes'] = [{
            'id': 'PPinfo_category_product',
            'values': [
                {
                    'value': '(PPInfo_category_spravochnik)Other'
                }
            ]
        }]
        self.error_create_product(ppinfo_client, data)

    @allure.title('Невалидное создание внешнего продукта админом без категории')
    def test_create_invalid_product_no_category(self, ppinfo_client):
        data = self.get_data_for_product_creation(product_type='Vneshnii')
        data['attributes'] = [{
            'id': 'PPinfo_status',
            'values': [
                {
                    'value': '(PPinfo_status)Out_of_use'
                }
            ]
        }]
        self.error_create_product(ppinfo_client, data)

    ########################################################### Изменение продукта

    ######################### Строка

    @allure.title('Изменение атрибута в продукте / стринга / add')
    def test_update_product_string_add(self, ppinfo_client):
        data = self.get_attribute_update_body('string_add')

        self.change_product(ppinfo_client, data)

        self.check_updates(ppinfo_client, data)

    @allure.title('Изменение атрибута в продукте / стринга / replace')
    def test_update_product_string_replace(self, ppinfo_client):
        data = self.get_attribute_update_body('string_replace')

        self.change_product(ppinfo_client, data)

        self.check_updates(ppinfo_client, data)

    @allure.title('Изменение атрибута в продукте / стринга / remove')
    def test_update_product_string_remove(self, ppinfo_client):
        data = self.get_attribute_update_body('string_remove')

        self.change_product(ppinfo_client, data)

        self.check_updates(ppinfo_client, data)



    ############################ Мэни селект

    @allure.title('Изменение атрибута в продукте / Мэни селект / add ')
    def test_update_product_select_add(self, ppinfo_client):
        data = self.get_attribute_update_body('manyselect_add')

        self.change_product(ppinfo_client, data)

        self.check_updates(ppinfo_client, data)

    @allure.title('Изменение атрибута в продукте / Мэни селект / replace ')
    def test_update_product_select_replace(self, ppinfo_client):
        data = self.get_attribute_update_body('manyselect_replace')

        self.change_product(ppinfo_client, data)

        self.check_updates(ppinfo_client, data)

    @allure.title('Изменение атрибута в продукте / Мэни селект / remove ')
    def test_update_product_select_remove(self, ppinfo_client):
        data = self.get_attribute_update_body('manyselect_remove')

        self.change_product(ppinfo_client, data)

        self.check_updates(ppinfo_client, data)

    ############################ Дата

    @allure.title('Изменение атрибута в продукте / Дата / add ')
    def test_update_product_date_add(self, ppinfo_client):
        data = self.get_attribute_update_body('date_add')

        self.change_product(ppinfo_client, data)

        self.check_updates(ppinfo_client, data)

    @allure.title('Изменение атрибута в продукте / Дата / replace ')
    def test_update_product_date_replace(self, ppinfo_client):
        data = self.get_attribute_update_body('date_replace')

        self.change_product(ppinfo_client, data)

        self.check_updates(ppinfo_client, data)

    @allure.title('Изменение атрибута в продукте / Дата / remove ')
    def test_update_product_date_remove(self, ppinfo_client):
        data = self.get_attribute_update_body('date_remove')

        self.change_product(ppinfo_client, data)

        self.check_updates(ppinfo_client, data)

    ############################ Число

    @allure.title('Изменение атрибута в продукте / Число / add ')
    def test_update_product_num_add(self, ppinfo_client):
        data = self.get_attribute_update_body('num_add')

        self.change_product(ppinfo_client, data)

        self.check_updates(ppinfo_client, data)

    @allure.title('Изменение атрибута в продукте / Число / replace ')
    def test_update_product_num_replace(self, ppinfo_client):
        data = self.get_attribute_update_body('num_replace')

        self.change_product(ppinfo_client, data)

        self.check_updates(ppinfo_client, data)

    @allure.title('Изменение атрибута в продукте / Число / remove ')
    def test_update_product_num_remove(self, ppinfo_client):
        data = self.get_attribute_update_body('num_remove')

        self.change_product(ppinfo_client, data)

        self.check_updates(ppinfo_client, data)

    ############################ Юзер

    @allure.title('Изменение атрибута в продукте / Юзер / add ')
    def test_update_product_user_add(self, ppinfo_client):
        data = self.get_attribute_update_body('user_add')

        self.change_product(ppinfo_client, data)

        self.check_updates(ppinfo_client, data)

    @allure.title('Изменение атрибута в продукте / Юзер / replace ')
    def test_update_product_user_replace(self, ppinfo_client):
        data = self.get_attribute_update_body('user_replace')

        self.change_product(ppinfo_client, data)

        self.check_updates(ppinfo_client, data)

    @allure.title('Изменение атрибута в продукте / Юзер / remove ')
    def test_update_product_user_remove(self, ppinfo_client):
        data = self.get_attribute_update_body('user_remove')

        self.change_product(ppinfo_client, data)

        self.check_updates(ppinfo_client, data)

    ############################ Множество

    @allure.title('Изменение атрибута в продукте / Множество / add ')
    def test_update_product_multi_add(self, ppinfo_client):
        data = self.get_attribute_update_body('multi_add')

        self.change_product(ppinfo_client, data)

        self.check_updates(ppinfo_client, data)

    @allure.title('Изменение атрибута в продукте / Множество / replace ')
    def test_update_product_multi_replace(self, ppinfo_client):
        data = self.get_attribute_update_body('multi_replace')

        self.change_product(ppinfo_client, data)

        self.check_updates(ppinfo_client, data)

    @allure.title('Изменение атрибута в продукте / Множество / remove ')
    def test_update_product_multi_remove(self, ppinfo_client):
        data = self.get_attribute_update_body('multi_remove')

        self.change_product(ppinfo_client, data)

        self.check_updates(ppinfo_client, data)

    ############################ Мультиюзер

    @allure.title('Изменение атрибута в продукте / Мультиюзер / add ')
    @allure.issue('https://jira.mts.ru/browse/PPI-168',
                  'PPInfo - Множественный выбор в атрибуте с типом "Сотрудник"')
    def test_update_product_multiuser_add(self, ppinfo_client):
        data = self.get_attribute_update_body('multiuser_add')

        self.change_product(ppinfo_client, data)

        self.check_updates(ppinfo_client, data)

    @allure.title('Изменение атрибута в продукте / Мультиюзер / replace -1 ')
    @allure.issue('https://jira.mts.ru/browse/PPI-168',
                  'PPInfo - Множественный выбор в атрибуте с типом "Сотрудник"')
    def test_update_product_multiuser_replace_minus(self, ppinfo_client):
        data = self.get_attribute_update_body('multiuser_replace_minus')

        self.change_product(ppinfo_client, data)

        self.check_updates(ppinfo_client, data)

    @allure.title('Изменение атрибута в продукте / Мультиюзер / replace +1 ')
    @allure.issue('https://jira.mts.ru/browse/PPI-168',
                  'PPInfo - Множественный выбор в атрибуте с типом "Сотрудник"')
    def test_update_product_multiuser_replace_plus(self, ppinfo_client):
        data = self.get_attribute_update_body('multiuser_replace_plus')

        self.change_product(ppinfo_client, data)

        self.check_updates(ppinfo_client, data)

    @allure.title('Изменение атрибута в продукте / Мультиюзер / remove ')
    @allure.issue('https://jira.mts.ru/browse/PPI-168',
                  'PPInfo - Множественный выбор в атрибуте с типом "Сотрудник"')
    def test_update_product_multiuser_remove(self, ppinfo_client):
        data = self.get_attribute_update_body('multiuser_remove')

        self.change_product(ppinfo_client, data)

        self.check_updates(ppinfo_client, data)

    ############################ Продукт

    @allure.title('Изменение атрибута в продукте / Продукт / add ')
    @allure.issue('https://jira.mts.ru/browse/PPI-126', 'PPInfo - Отображение связанных продуктов на странице продукта')
    def test_update_product_product_add(self, ppinfo_client):
        data = self.get_attribute_update_body('product_add')

        self.change_product(ppinfo_client, data)

        self.check_updates(ppinfo_client, data)

    @allure.title('Изменение атрибута в продукте / Продукт / replace ')
    @allure.issue('https://jira.mts.ru/browse/PPI-126', 'PPInfo - Отображение связанных продуктов на странице продукта')
    def test_update_product_product_replace(self, ppinfo_client):
        data = self.get_attribute_update_body('product_replace')

        self.change_product(ppinfo_client, data)

        self.check_updates(ppinfo_client, data)

    @allure.title('Изменение атрибута в продукте / Продукт / remove ')
    @allure.issue('https://jira.mts.ru/browse/PPI-126', 'PPInfo - Отображение связанных продуктов на странице продукта')
    def test_update_product_product_remove(self, ppinfo_client):
        data = self.get_attribute_update_body('product_remove')

        self.change_product(ppinfo_client, data)

        self.check_updates(ppinfo_client, data)

    ############################ Мультипродукт

    @allure.title('Изменение атрибута в продукте / Мультипродукт / add ')
    @allure.issue('https://jira.mts.ru/browse/PPI-126',
                  'PPInfo - Отображение связанных продуктов на странице продукта')
    def test_update_product_multiproduct_add(self, ppinfo_client):
        data = self.get_attribute_update_body('multiproduct_add')

        self.change_product(ppinfo_client, data)

        self.check_updates(ppinfo_client, data)

    @allure.title('Изменение атрибута в продукте / Мультипродукт / replace -1 ')
    @allure.issue('https://jira.mts.ru/browse/PPI-126',
                  'PPInfo - Отображение связанных продуктов на странице продукта')
    def test_update_product_multiproduct_replace_minus(self, ppinfo_client):
        data = self.get_attribute_update_body('multiproduct_replace_minus')

        self.change_product(ppinfo_client, data)

        self.check_updates(ppinfo_client, data)

    @allure.title('Изменение атрибута в продукте / Мультипродукт / replace +1 ')
    @allure.issue('https://jira.mts.ru/browse/PPI-126',
                  'PPInfo - Отображение связанных продуктов на странице продукта')
    def test_update_product_multiproduct_replace_plus(self, ppinfo_client):
        data = self.get_attribute_update_body('multiproduct_replace_plus')

        self.change_product(ppinfo_client, data)

        self.check_updates(ppinfo_client, data)

    @allure.title('Изменение атрибута в продукте / Мультипродукт / remove ')
    @allure.issue('https://jira.mts.ru/browse/PPI-126',
                  'PPInfo - Отображение связанных продуктов на странице продукта')
    def test_update_product_multiproduct_remove(self, ppinfo_client):
        data = self.get_attribute_update_body('multiproduct_remove')

        self.change_product(ppinfo_client, data)

        self.check_updates(ppinfo_client, data)

    ############################ Множественная ссылка

    @allure.title('Изменение атрибута в продукте / Мультиссылка / add ')
    @allure.issue('https://jira.mts.ru/browse/PPI-666', 'PPInfo - Добавление ссылок (объединённая)')
    def test_update_product_multilink_add(self, ppinfo_client):
        data = self.get_attribute_update_body('multilink_add')

        self.change_product(ppinfo_client, data)

        self.check_updates(ppinfo_client, data)

    @allure.title('Изменение атрибута в продукте / Мультиссылка / replace - 1')
    @allure.issue('https://jira.mts.ru/browse/PPI-666', 'PPInfo - Добавление ссылок (объединённая)')
    def test_update_product_multilink_replace_minus(self, ppinfo_client):
        data = self.get_attribute_update_body('multilink_replace_minus')

        self.change_product(ppinfo_client, data)

        self.check_updates(ppinfo_client, data)

    @allure.title('Изменение атрибута в продукте / Мультиссылка / replace + 1')
    @allure.issue('https://jira.mts.ru/browse/PPI-666', 'PPInfo - Добавление ссылок (объединённая)')
    def test_update_product_multilink_replace_plus(self, ppinfo_client):
        data = self.get_attribute_update_body('multilink_replace_plus')

        self.change_product(ppinfo_client, data)

        self.check_updates(ppinfo_client, data)

    @allure.title('Изменение атрибута в продукте / Мультиссылка / remove ')
    @allure.issue('https://jira.mts.ru/browse/PPI-666', 'PPInfo - Добавление ссылок (объединённая)')
    def test_update_product_multilink_remove(self, ppinfo_client):
        data = self.get_attribute_update_body('multilink_remove')

        self.change_product(ppinfo_client, data)

        self.check_updates(ppinfo_client, data)

    ############################ Многострочный текст

    @allure.title('Изменение атрибута в продукте / Многострочный текст / add ')
    def test_update_product_multistring_add(self, ppinfo_client):
        data = self.get_attribute_update_body('multistring_add')

        self.change_product(ppinfo_client, data)

        self.check_updates(ppinfo_client, data)

    @allure.title('Изменение атрибута в продукте / Многострочный текст / replace ')
    def test_update_product_multistring_replace(self, ppinfo_client):
        data = self.get_attribute_update_body('multistring_replace')

        self.change_product(ppinfo_client, data)

        self.check_updates(ppinfo_client, data)

    @allure.title('Изменение атрибута в продукте / Многострочный текст / remove ')
    def test_update_product_multistring_remove(self, ppinfo_client):
        data = self.get_attribute_update_body('multistring_remove')

        self.change_product(ppinfo_client, data)

        self.check_updates(ppinfo_client, data)

    ############################ Ссылка

    @allure.title('Изменение атрибута в продукте / Ссылка / add ')
    def test_update_product_link_add(self, ppinfo_client):
        data = self.get_attribute_update_body('link_add')

        self.change_product(ppinfo_client, data)

        self.check_updates(ppinfo_client, data)

    @allure.title('Изменение атрибута в продукте / Ссылка / replace ')
    def test_update_product_link_replace(self, ppinfo_client):
        data = self.get_attribute_update_body('link_replace')

        self.change_product(ppinfo_client, data)

        self.check_updates(ppinfo_client, data)

    @allure.title('Изменение атрибута в продукте / Ссылка / remove ')
    def test_update_product_link_remove(self, ppinfo_client):
        data = self.get_attribute_update_body('link_remove')

        self.change_product(ppinfo_client, data)

        self.check_updates(ppinfo_client, data)

    ############################ Тип продукта

    @allure.title('Изменение атрибута в продукте / Тип продукта / external ')
    @allure.issue('https://jira.mts.ru/browse/PPI-659', 'PPInfo - Исправление изменение типа')
    def test_update_product_type_ext(self, ppinfo_client):
        data = {
            'id': 'BI_2769',
            'attributes': [

            ],
            'notification': True,
            'type': 'Vneshnii'}
        self.change_product(ppinfo_client, data)

        with allure.step('Проверяем что изменение действительно применились'):
            assert self.get_info_by_product_code(ppinfo_client, 'BI_2769')['type'] == {'code': 'Vneshnii', 'value': 'Внешний'}

    @allure.title('Изменение атрибута в продукте / Тип продукта / internal ')
    @allure.issue('https://jira.mts.ru/browse/PPI-659', 'PPInfo - Исправление изменение типа')
    def test_update_product_type_int(self, ppinfo_client):
        data = {
            'id': 'BI_2769',
            'attributes': [

            ],
            'notification': True,
            'type': 'Vnutrennii'}
        self.change_product(ppinfo_client, data)

        with allure.step('Проверяем что изменение действительно применились'):
            assert self.get_info_by_product_code(ppinfo_client, 'BI_2769')['type'] == {'code': 'Vnutrennii', 'value': 'Внутренний'}

    ############################ Основной продукт

    @allure.title('Изменение атрибута в продукте / Основной продукт/ add ')
    @allure.issue('https://jira.mts.ru/browse/PPI-3208', 'PPInfo - Автоматизация изменения структурного типа продукта')
    def test_update_product_main_product_add(self, ppinfo_client):
        data = self.get_attribute_update_body('main_product_add')

        self.change_product(ppinfo_client, data)

        self.check_updates(ppinfo_client, data)

        assert self.check_structural_product_type(ppinfo_client,
            'BI_2769') == 'Атомарный', 'Структурный тип у продукта не поменялся, хотя был установлен Основной продукт'
        assert self.check_structural_product_type(ppinfo_client,
            'BI_2683') == 'Основной', 'Структурный тип у продукта поменялся, хотя не должен был'

    @allure.title('Изменение атрибута в продукте / Основной продукт/ replace ')
    @allure.issue('https://jira.mts.ru/browse/PPI-3208', 'PPInfo - Автоматизация изменения структурного типа продукта')
    def test_update_product_main_product_replace(self, ppinfo_client):
        data = self.get_attribute_update_body('main_product_replace')

        self.change_product(ppinfo_client, data)

        self.check_updates(ppinfo_client, data)

        assert self.check_structural_product_type(ppinfo_client,
            'BI_2769') == 'Атомарный', 'Структурный тип у продукта не поменялся, хотя был установлен Основной продукт'
        assert self.check_structural_product_type(ppinfo_client,
            'BI_3266') == 'Основной', 'Структурный тип у продукта поменялся, хотя не должен был'

    @allure.title('Изменение атрибута в продукте / Основной продукт/ remove')
    @allure.issue('https://jira.mts.ru/browse/PPI-3208', 'PPInfo - Автоматизация изменения структурного типа продукта')
    def test_update_product_main_product_remove(self, ppinfo_client):
        data = self.get_attribute_update_body('main_product_remove')

        self.change_product(ppinfo_client, data)

        self.check_updates(ppinfo_client, data)

        assert self.check_structural_product_type(ppinfo_client,
            'BI_2769') == 'Основной', 'Структурный тип у продукта не поменялся, хотя был убран Основной продукт'
        assert self.check_structural_product_type(ppinfo_client,
            'BI_3266') == 'Основной', 'Структурный тип у продукта поменялся, хотя не должен был'
        assert self.check_structural_product_type(ppinfo_client,
            'BI_2683') == 'Основной', 'Структурный тип у продукта поменялся, хотя не должен был'


    ############################ Основной проект


    @allure.title('Изменение атрибута в продукте / Основной проект jira/ add ')
    @allure.issue('https://jira.mts.ru/browse/PPI-4125', 'PPInfo - Основной проект Jira продукта')
    def test_update_product_main_project_jira_add(self, ppinfo_client):
        data = self.get_attribute_update_body('main_project_jira_add')

        self.change_product(ppinfo_client, data)

        self.check_updates(ppinfo_client, data)


    @allure.title('Изменение атрибута в продукте / Основной продукт/ replace ')
    @allure.issue('https://jira.mts.ru/browse/PPI-4125', 'PPInfo - Основной проект Jira продукта')
    def test_update_product_main_project_jira_replace(self, ppinfo_client):
        data = self.get_attribute_update_body('main_project_jira_product_replace')

        self.change_product(ppinfo_client, data)

        self.check_updates(ppinfo_client, data)


    @allure.title('Изменение атрибута в продукте / Основной продукт/ remove')
    @allure.issue('https://jira.mts.ru/browse/PPI-4125', 'PPInfo - Основной проект Jira продукта')
    def test_update_product_main_project_jira_remove(self, ppinfo_client):
        data = self.get_attribute_update_body('main_project_jira_product_remove')

        self.change_product(ppinfo_client, data)

        self.check_updates(ppinfo_client, data)



