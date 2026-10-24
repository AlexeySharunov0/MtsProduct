import json
import time
import warnings
from datetime import datetime
from uuid import UUID

import allure
import pytest

from API.models.pmd.rest_internal_modules.demo import Demo
from API.models.ppinfo.brief import Brief
from API.models.search.search import Search

warnings.filterwarnings('ignore', message='numpy.dtype size changed')


#### Демо
@pytest.mark.api
@allure.label('priority', 'Высокий')
@allure.feature("Демо продуктов")
@allure.issue('https://jira.mts.ru/browse/PPI-3286', 'PPInfo - Создание раздела "Демо" в карточке продукта')
class TestDemo(Demo, Brief, Search):

    @allure.title('Получение демо продукта')
    @pytest.mark.parametrize('bi_code', ['BI_60', 'BI_42'])
    def test_get_demo_by_bi_code(self, rest_internal_client, bi_code):

        assert self.get_demo_by_product_code(rest_internal_client,
                                             bi_code), f'Список полученных демо по продукту {bi_code} пуст'

    @allure.title('Получение всех демо')
    def test_get_demos(self, rest_internal_client):

        assert self.get_demos(rest_internal_client), f'Список полученных демо пуст'

    @allure.title('Получение всех демо и проверка сортировки')
    def test_get_demos_sorted(self, rest_internal_client):

        first_requests = []
        second_requests = []

        for quarter in self.get_demos(rest_internal_client):
            for demo in quarter['demos']:
                first_requests.append(demo['name'])

        for quarter in self.get_demos(rest_internal_client):
            for demo in quarter['demos']:
                second_requests.append(demo['name'])

        assert len(first_requests) == len(second_requests)

        assert first_requests == second_requests, f'Порядок демо некорректный'

    @allure.title('Получение всех категорий демо')
    def test_get_categories_demos(self, rest_internal_client):

        assert self.get_categories(rest_internal_client), f'Список полученных категорий демо пуст'

    @allure.title('Создание категории демо')
    @pytest.mark.parametrize('is_active', [True, False])
    def test_create_category_demo(self, rest_internal_client, is_active):

        category_count = len(self.get_categories(rest_internal_client))
        category_id = self.add_category(rest_internal_client, self.get_category_data(is_active=is_active))
        category_count_after_add = self.get_categories(rest_internal_client)

        assert category_count + is_active == len(category_count_after_add), 'Категория не добавлена'
        if is_active:
            assert any(i['id'] == category_id for i in
                       self.get_categories(
                           rest_internal_client)), f'id добавленной категории не найден в списке категорий'

    @allure.title('Некорректное создание категории демо')
    @pytest.mark.parametrize('name', ['',
                                      'qweqweqweqweqweqw1eqweqweqweqweqweqweqweqweqweqweqweqweqweqweqweqweqweqweqweqweqweqweqweqweqweqweqweqweqweqweqweqweqweqwew'])
    def test_create_category_demo_invalid_name(self, rest_internal_client, name):

        category_count = len(self.get_categories(rest_internal_client))
        self.add_category_400(rest_internal_client, self.get_category_data(name=name))
        category_count_after_add = self.get_categories(rest_internal_client)

        assert category_count == len(category_count_after_add), 'Категория добавлена'

    @allure.title('Изменение категории демо')
    def test_patch_category_demo(self, rest_internal_client):

        category_id = self.add_category(rest_internal_client, self.get_category_data())
        self.patch_category_by_id(rest_internal_client, category_id, self.get_category_data(name='test_name_patched',
                                                                                            description='test_description_patched',
                                                                                            is_active=False,
                                                                                            color='#12345'))

        category_info = self.get_category_by_id(rest_internal_client, category_id)
        assert category_info['name'] == 'test_name_patched', 'Название категории не изменено'
        assert category_info['description'] == 'test_description_patched', 'Описание категории не изменено'
        assert not category_info['isActive'], 'Активность категории не изменено'
        assert category_info['color'] == '#12345', 'Цвет категории не изменен'

    @allure.title('Добавление файла, проверка его наличия и удаление')
    @pytest.mark.parametrize('file_format',
                             ['.xlsx', '.xls', '.doc', '.docx', '.ppt', '.pptx', '.txt', '.pdf', '.3gp', '.avi', '.mov',
                              '.mp4',
                              '.mp3', '.mkv', '.wav', '.jpg', '.jpeg', '.svg', '.png', '.zip', '.rar', '.gif', '.msg',
                              '.exe', '.rtf'])
    def test_add_patch_delete_file(self, rest_internal_client, file_format):

        file_id = self.add_file(rest_internal_client, 'test', file_format)
        try:
            UUID(file_id, version=4)
            is_valid_uuid = True
        except ValueError:
            is_valid_uuid = False

        assert is_valid_uuid, f"Ответ не  {file_id}"
        assert self.get_file_by_id(rest_internal_client, file_id), 'Не удалось получить файл по id'

        self.delete_file_by_id(rest_internal_client, file_id)
        self.get_file_by_id_404(rest_internal_client, file_id), 'Файл не удален'

    @allure.title('Проверка уникальности ссылки')
    def test_check_uniqueness_link(self, rest_internal_client):

        self.check_uniqueness_link(rest_internal_client, self.text)

    @allure.title('Проверка не уникальности ссылки')
    def test_check_not_uniqueness_link(self, rest_internal_client):
        link = self.text

        demo_id = self.create_demo(rest_internal_client, self.get_demo_data(other={'link': link}))['demoID']

        self.check_not_uniqueness_link(rest_internal_client, link)

        self.delete_demo(rest_internal_client, demo_id)

    @allure.title('Создание демо и удаление демо')
    def test_create_demo(self, rest_internal_client):

        demo_id = self.create_demo(rest_internal_client, self.get_demo_data())['demoID']

        demos_id = []

        for quarter in self.get_demos(rest_internal_client):
            for demo in quarter['demos']:
                demos_id.append(demo['id'])

        assert demo_id in demos_id, 'Демо не создано'

        self.delete_demo(rest_internal_client, demo_id)

    @allure.title('Создание демо с файлом')
    @pytest.mark.parametrize('file_format',
                             ['.xlsx', '.xls', '.doc', '.docx', '.ppt', '.pptx', '.txt', '.pdf', '.3gp', '.avi', '.mov',
                              '.mp4',
                              '.mp3', '.mkv', '.wav', '.jpg', '.jpeg', '.svg', '.png', '.zip', '.rar', '.gif', '.msg',
                              '.exe', '.rtf'])
    def test_create_demo_with_file(self, rest_internal_client, file_format):

        file_id1 = self.add_file(rest_internal_client, 'test', file_format)
        file_id2 = self.add_file(rest_internal_client, 'test2', '.xlsx')

        demo_id = self.create_demo(rest_internal_client, self.get_demo_data(other={'files': [file_id1, file_id2]}))[
            'demoID']

        demos_id = []

        for quarter in self.get_demos(rest_internal_client):
            for demo in quarter['demos']:
                demos_id.append(demo['id'])

        assert demo_id in demos_id, 'Демо не создано'

        self.delete_file_by_id(rest_internal_client, file_id1)
        self.delete_file_by_id(rest_internal_client, file_id2)
        self.delete_demo(rest_internal_client, demo_id)

    @allure.title('Создание демо с ссылкой на продукт')
    def test_create_demo_with_link(self, rest_internal_client):

        product_id1 = 'BI_60'
        product_id2 = 'BI_42'

        demo_id = self.create_demo(rest_internal_client,
                                   self.get_demo_data(other={'linkedProducts': [product_id1, product_id2]}))['demoID']

        demos_id = []

        for quarter in self.get_demos(rest_internal_client):
            for demo in quarter['demos']:
                demos_id.append(demo['id'])

        assert demo_id in demos_id, 'Демо не создано'

        assert any(
            demo['id'] == demo_id for demo in
            self.get_demo_by_product_code(rest_internal_client, product_id1)[
                'demos']), 'Демо не отображено в первом продукте'

        assert any(
            demo['id'] == demo_id for demo in
            self.get_demo_by_product_code(rest_internal_client, product_id2)[
                'demos']), 'Демо не отображено во втором продукте'

        self.delete_demo(rest_internal_client, demo_id)

    @allure.title('Создание демо с невалидным именем')
    @pytest.mark.parametrize('name', [
        'qweqweqweqweqweqw1eqweqweqweqweqweqweqweqweqweqweqweqweqweqweqweqweqweqweqweqweqweqweqweqweqweqweqweqweqweqweqweqweqweqwew',
        ''])
    def test_create_demo_invalid_name(self, rest_internal_client, name):

        self.create_demo_400(rest_internal_client, self.get_demo_data(name=name))

    @allure.title('Изменение демо и удаление демо')
    def test_patch_demo(self, rest_internal_client):

        demo_id = self.create_demo(rest_internal_client, self.get_demo_data())['demoID']

        demos_id = []

        for quarter in self.get_demos(rest_internal_client):
            for demo in quarter['demos']:
                demos_id.append(demo['id'])

        assert demo_id in demos_id, 'Демо не создано'

        self.patch_demo(rest_internal_client, demo_id,
                        self.get_demo_data(name='test_name_patched', description='test_description_patched',
                                           link='test_link_patched'))

        for quarter in self.get_demos(rest_internal_client):
            for demo in quarter['demos']:
                if demo['id'] == demo_id:
                    assert demo['name'] == 'test_name_patched', 'Название демо не изменено'
                    assert demo['description'] == 'test_description_patched', 'Описание демо не изменено'
                    assert 'test_link_patched' in demo['link'], 'Ссылка демо не изменена'

        self.delete_demo(rest_internal_client, demo_id)

    @allure.title('Скрытие категории демо')
    def test_hiding_category(self, rest_internal_client, search_client):

        category_id = self.add_category(rest_internal_client, self.get_category_data())
        demo_id = self.create_demo(rest_internal_client,
                                   self.get_demo_data(name='test_demo_new_york', category_id=category_id,
                                                      other={'linkedProducts': ['BI_3266']}))[
            'demoID']

        demos_id = []

        for quarter in self.get_demos(rest_internal_client):
            for demo in quarter['demos']:
                demos_id.append(demo['id'])

        assert demo_id in demos_id, 'Демо не создано'

        assert any(demo['id'] == demo_id for demo in self.get_demo_by_product_code(
            rest_internal_client)['demos']), 'Демо не отображается в продукте к которому он привязан'
        assert any(demo['id'] == demo_id for demo in
                   self.search_demo(search_client, 'test_demo_new_york')), 'Демо не отображается в поиске'

        self.patch_category_by_id(rest_internal_client, category_id, self.get_category_data(is_active=False))

        demos_id = []

        for quarter in self.get_demos(rest_internal_client):
            for demo in quarter['demos']:
                demos_id.append(demo['id'])

        assert demo_id not in demos_id, 'Демо не создано'

        assert not any(demo['id'] == demo_id for demo in self.get_demo_by_product_code(
            rest_internal_client)[
            'demos']), 'Демо отображается в продукте к которому он привязан, хотя категория в котором находится демо скрыта'
        assert not any(demo['id'] == demo_id for demo in self.search_demo(search_client,
                                                                          'test_demo_new_york')), 'Демо отображается в поиске, хотя категория в котором находится демо скрыта'

        self.delete_demo(rest_internal_client, demo_id)

    @allure.title('Фильтрация демо по периоду')
    def test_filter_demos_by_dates(self, rest_internal_client, search_client):

        date_to = int(datetime.now().timestamp())
        date_from = int(datetime(2025, 1, 1).timestamp())

        search_result = self.search_demo(search_client, date_to=date_to, date_from=date_from)
        assert all(date_from <= int(
            time.mktime(datetime.strptime(demo['conductedAt'], "%Y-%m-%dT%H:%M:%SZ").timetuple())) <= date_to for demo
                   in search_result)

    @allure.title('Фильтрация демо по категориям')
    def test_filter_demos_by_categories(self, rest_internal_client, search_client):

        categories_ids = [category_id for category_id in self.get_categories(rest_internal_client)]

        for category_id in categories_ids:
            search_result = self.search_demo(search_client, category_list=category_id)
            assert all(demo['categoryID'] == category_id for demo in search_result)

    @allure.title('Поиск демо по названию')
    @pytest.mark.parametrize("pattern",
                             ["#ПростоОСложном", 'Rushbe', 'остоОСлож'])
    def test_search_demo_by_name(self, rest_internal_client, search_client, pattern):

        search_result = self.search_demo(search_client, pattern=pattern)
        assert search_result, "Поиск не дал результатов"
        demos = []
        for demo in search_result:
            if pattern.lower() not in demo["name"].lower():
                demos.append(demo["name"])
        with allure.step("Проверяем результаты поиска"):
            assert not demos, f"{demos=} появились по паттерну {pattern}"

    @allure.title('Поиск демо по продукту')
    def test_search_demo_change_name(self, rest_internal_client, search_client):

        pattern = 'london'

        demo_id = self.create_demo(rest_internal_client, self.get_demo_data(name=f'test_{pattern}'))['demoID']

        search_result = self.search_demo(search_client, pattern=pattern)
        assert search_result, "Поиск не дал результатов"
        self.check_demo_in_search_result(pattern, search_result)

        new_pattern = 'brussels'

        self.patch_demo(rest_internal_client, demo_id, self.get_demo_data(name=f'test_{new_pattern}'))

        new_search_result = self.search_demo(search_client, pattern=new_pattern)
        self.check_demo_in_search_result(new_pattern, new_search_result)

        self.delete_demo(rest_internal_client, demo_id)

    @allure.title('Поиск демо по продукту')
    @pytest.mark.parametrize("pattern", ["Маркетолог", 'Private LTE', 'Big Data'])
    def test_search_demo_by_product(self, rest_internal_client, search_client, pattern):
        search_result = self.search_demo(search_client, pattern=pattern)
        assert search_result, "Поиск не дал результатов"

        for demo in search_result:
            try:
                demo_info = self.get_demo_by_id(rest_internal_client, demo['id'])
                assert any(pattern.lower() in product['productName'].lower() for product in
                           demo_info['linkedProducts']), 'У найденных демо нет продуктов по которым мы искали'
            except:
                pass

    @allure.title('Поиск демо по продукту')
    def test_search_demo_by_change_product(self, rest_internal_client, search_client):

        pattern = 'Для автотестов, еще один'

        demo_id = self.create_demo(rest_internal_client, self.get_demo_data(other={'linkedProducts': ['BI_5691']}))[
            'demoID']
        time.sleep(10)
        search_result = self.search_demo(search_client, pattern=pattern)

        assert search_result, "Поиск не дал результатов"
        for demo in search_result:
            try:
                demo_info = self.get_demo_by_id(rest_internal_client, demo['id'])
                assert all(pattern.lower() in product['productName'].lower() for product in
                           demo_info['linkedProducts']), 'У найденных демо нет продуктов по которым мы искали'
            except:
                pass

        self.delete_demo(rest_internal_client, demo_id)

    @allure.title('Согласование заявки на добавление демо')
    def test_approval_brief_demo(self, rest_internal_client, rest_internal_user_client, ppinfo_client):

        name = f'test_user_demo_{self.text}'

        brief_id = self.create_demo_user(rest_internal_user_client, self.get_demo_data(name=name))[
            'briefID']
        self.take_to_work(ppinfo_client, brief_id, {"login": "ddsvetov1"})
        self.approval(ppinfo_client, brief_id)

        assert self.get_brief_by_id(ppinfo_client, brief_id)[
                   'status'] == 'statusDone', f'Текущий статус: {self.get_brief_by_id(ppinfo_client, brief_id)["status"]}'

        demos_names = []

        for quarter in self.get_demos(rest_internal_client):
            for demo in quarter['demos']:
                demos_names.append(demo['name'])

        assert name in demos_names, 'Демо не создано'

    @allure.title('Отклонение заявки на добавление демо')
    def test_declined_brief_demo(self, rest_internal_client, rest_internal_user_client, ppinfo_client):
        brief_id = self.create_demo_user(rest_internal_user_client, self.get_demo_data())['briefID']
        self.take_to_work(ppinfo_client, brief_id, {"login": "ddsvetov1"})
        self.declined(ppinfo_client, brief_id)

        assert self.get_brief_by_id(ppinfo_client, brief_id)[
                   'status'] == 'statusDeclined', f'Текущий статус: {self.get_brief_by_id(ppinfo_client, brief_id)["status"]}'

    @allure.title('Редактирование заявки на добавление демо')
    def test_patch_brief_demo(self, rest_internal_client, rest_internal_user_client, ppinfo_client):
        brief_id = self.create_demo_user(rest_internal_user_client, self.get_demo_data())['briefID']
        self.take_to_work(ppinfo_client, brief_id, {"login": "ddsvetov1"})
        data = {
            "data": json.dumps({
                "link": "test_link_patched" + self.text,
                "name": 'test_name_patched',
                "files": [],
                "category": {
                    "id": "0040360f-9ab3-63d0-b4c8-cfc6294438de",
                    "name": "Открытое демо"
                },
                "products": [],
                "conductedAt": 1742083200,
                "description": "test_description_patched",
                "attributes": []
            })
        }

        self.patch_brief_by_id(ppinfo_client, brief_id,
                               data)
        self.approval(ppinfo_client, brief_id)

        assert self.get_brief_by_id(ppinfo_client, brief_id)[
                   'status'] == 'statusDone', f'Текущий статус: {self.get_brief_by_id(ppinfo_client, brief_id)["status"]}'

    @allure.title('Согласование заявки на удаление демо')
    def test_approval_brief_delete_demo(self, rest_internal_client, rest_internal_user_client, ppinfo_client):

        demo_id = self.create_demo(rest_internal_client, self.get_demo_data())['demoID']

        brief_id = self.delete_demo_user(rest_internal_user_client, demo_id)

        self.take_to_work(ppinfo_client, brief_id, {"login": "ddsvetov1"})

        self.approval(ppinfo_client, brief_id)

        assert self.get_brief_by_id(ppinfo_client, brief_id)[
                   'status'] == 'statusDone', f'Текущий статус: {self.get_brief_by_id(ppinfo_client, brief_id)["status"]}'

        demos_id = []

        for quarter in self.get_demos(rest_internal_client):
            for demo in quarter['demos']:
                demos_id.append(demo['id'])

        assert demo_id not in demos_id, 'Демо не создано'

    @allure.title('Отклонение заявки на удаление демо')
    def test_declined_brief_delete_demo(self, rest_internal_client, rest_internal_user_client, ppinfo_client):

        demo_id = self.create_demo(rest_internal_client, self.get_demo_data())['demoID']

        brief_id = self.delete_demo_user(rest_internal_user_client, demo_id)

        self.take_to_work(ppinfo_client, brief_id, {"login": "ddsvetov1"})

        self.declined(ppinfo_client, brief_id)

        demos_id = []

        for quarter in self.get_demos(rest_internal_client):
            for demo in quarter['demos']:
                demos_id.append(demo['id'])

        assert demo_id in demos_id, 'Демо удалилось, хотя не должно было'

        assert self.get_brief_by_id(ppinfo_client, brief_id)[
                   'status'] == 'statusDeclined', f'Текущий статус: {self.get_brief_by_id(ppinfo_client, brief_id)["status"]}'

    @allure.title('Отправка заявки на изменение демо')
    def test_patch_demo_user(self, rest_internal_client, rest_internal_user_client, ppinfo_client):

        demo_id = self.create_demo(rest_internal_client, self.get_demo_data())['demoID']
        demos_id = []

        for quarter in self.get_demos(rest_internal_client):
            for demo in quarter['demos']:
                demos_id.append(demo['id'])

        assert demo_id in demos_id, 'Демо удалилось, хотя не должно было'

        brief_id = self.patch_demo_user(rest_internal_user_client, demo_id, self.get_demo_data(name='test_name_patched',
                                                                                               description='test_description_patched',
                                                                                               link='test_link_patched'))

        self.take_to_work(ppinfo_client, brief_id, {"login": "ddsvetov1"})

        self.approval(ppinfo_client, brief_id)

        for quarter in self.get_demos(rest_internal_client):
            for demo in quarter['demos']:
                if demo['id'] == demo_id:
                    assert demo['name'] == 'test_name_patched', 'Название демо не изменено'
                    assert demo['description'] == 'test_description_patched', 'Описание демо не изменено'
                    assert 'test_link_patched' in demo['link'], 'Ссылка демо не изменена'

        self.delete_demo(rest_internal_client, demo_id)

    @allure.title('Иксель демо не пуст')
    @allure.issue('https://jira.mts.ru/browse/PPI-4105', 'PPInfo - Выгрузка в Excel списка всех демо')
    def test_exel_demos_link(self, rest_internal_client):

        assert not self.get_excel_demos(rest_internal_client).empty, 'Эксель пуст'
