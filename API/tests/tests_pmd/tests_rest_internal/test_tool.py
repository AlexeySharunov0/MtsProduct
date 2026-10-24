import uuid

import allure
import pytest

from API.models.pmd.rest_internal_modules.tool import ToolApi
from API.utils.generate import Gen


@pytest.mark.api
@allure.link('https://jira.mts.ru/browse/PPI-3751', 'issue',
             'PPInfo - Добавление инструмента (Админка "Toolbox для продукта")')
@allure.link('https://jira.mts.ru/browse/PPI-3770', 'issue',
             'PPInfo - Добавление и изменение раздела (Админка "Toolbox для продукта")')
@allure.feature('Инструменты')
class TestToolApi(ToolApi):

    @allure.title('Создание нового инструмента')
    def test_add_tool(self, rest_internal_client):
        group_id = self.add_tool_group(rest_internal_client, self.get_tool_group_data())

        with allure.step('Создаем новый инструмент'):
            tool_id = self.add_tool(rest_internal_client, self.get_tool_data(group_id))

            all_tools_in_group = self.get_tool_group_by_id(rest_internal_client, group_id)

            assert any(tool['id'] == tool_id for tool in
                       all_tools_in_group['tool']), f'Инструмент с id {tool_id} не найден в группе, хотя должен быть'

        self.delete_tool_by_id(rest_internal_client, tool_id)
        self.delete_tool_group_by_id(rest_internal_client, group_id)

    @allure.title('Создание нового инструмента с некорректным названием')
    @pytest.mark.parametrize('name', [
        'qweqwe wef weqf we f wqe f ewf ew fwe fw jniu huguijoijfoicjweoin nhiuhiohciunweoidjioj oisiodjfijwqoidjioqjwdijhidqjkw o',
        ''])
    def test_add_tool_invalid_name(self, rest_internal_client, name):
        group_id = self.add_tool_group(rest_internal_client, self.get_tool_group_data())

        with allure.step('Пытаемся создать инструмент с некорректными данными'):
            self.add_invalid_tool(rest_internal_client, self.get_tool_data(group_id, {'name': name}))

    @allure.title('Создание инструмента c ссылками и проверка сортировки ссылок ')
    def test_create_tool_and_check_link_sort(self, rest_internal_client):
        group_id = self.add_tool_group(rest_internal_client, self.get_tool_group_data())
        tool_id = self.add_tool(rest_internal_client, self.get_tool_data(group_id, {'links': [
            {
                'name': '3',
                'url': 'https://jira.mts.ru/browse/PPI-2642'
            },
            {
                'name': '2',
                'url': 'https://jira.mts.ru/browse/PPI-2642'
            },
            {
                'name': '1',
                'url': 'https://jira.mts.ru/browse/PPI-2642'
            },
            {
                'name': '4',
                'url': 'https://jira.mts.ru/browse/PPI-2642'
            },
            {
                'name': 's',
                'url': 'https://jira.mts.ru/browse/PPI-2642'
            },
            {
                'name': 'a',
                'url': 'https://jira.mts.ru/browse/PPI-2642'
            }
        ]}))
        with allure.step('Проверяем, что такой инструмент создался'):
            assert self.get_tool_by_id(rest_internal_client, tool_id), 'инструмент не создался'

        with allure.step('Проверяем, что порядок ссылок такой же как при создании'):
            links = [link['name'] for link in self.get_tool_by_id(rest_internal_client, tool_id)['links']]

            assert links == ['3', '2', '1', '4', 's', 'a'], f'Не совпадает порядок ссылок: {links}'

        self.delete_tool_by_id(rest_internal_client, tool_id)
        with allure.step('Проверяем, что инструмента по этому айди больше нет'):
            self.get_tool_by_invalid_id(rest_internal_client, tool_id), 'инструмент есть'

    @allure.title('Создание инструментов c сотрудниками и проверка сортировки сотрудников ')
    def test_create_tool_and_check_employees_sort(self, rest_internal_client):
        group_id = self.add_tool_group(rest_internal_client, self.get_tool_group_data())

        tool_id = self.add_tool(rest_internal_client, self.get_tool_data(group_id, {'employees': [
            'aikostrov',
            'ddsvetov1',
            'svkurochkin',
            'sayariko',
            'pymaslenkov'
        ]}))
        with allure.step('Проверяем, что такой шаг создался'):
            assert self.get_tool_by_id(rest_internal_client, tool_id), 'Шаг не создался'

        with allure.step('Проверяем, что порядок сотрудников такой же как при создании'):
            employees = [employee['login'][0] for employee in
                         self.get_tool_by_id(rest_internal_client, tool_id)['employees']]

            assert employees == ['a', 'd', 's', 's', 'p'], f'Не совпадает порядок сотрудников: {employees}'

        self.delete_tool_by_id(rest_internal_client, tool_id)
        with allure.step('Проверяем, что шага по этому айди больше нет'):
            self.get_tool_by_invalid_id(rest_internal_client, tool_id), 'Шаг есть'

    @allure.title('Получение инструмента по невалидному id')
    def test_get_tool_by_invalid_id(self, rest_internal_client):
        with allure.step('Получаем инструмент по id'):
            self.get_tool_by_invalid_id(rest_internal_client,
                                        'bb57b084-c94d-4093-b8bd-41b4b8bfe9b5')  # Инструмента с таким id не существует

    @allure.title('Создание нового инструмента и добавление файла в него')
    def test_add_file_in_tool_and_get_file_by_id(self, rest_internal_client):
        group_id = self.add_tool_group(rest_internal_client, self.get_tool_group_data())

        file_id = self.add_file_in_tool(rest_internal_client)
        tool_id = self.add_tool(rest_internal_client, self.get_tool_data(group_id, {'files': [file_id]}))

        assert self.get_tool_by_id(rest_internal_client, tool_id)[
                   'files'] != [], f'Файл не добавлен в инструмент {tool_id}'

        self.get_file_by_id(rest_internal_client, file_id)

    @allure.title('Создание новой группы инструментов и проверяем что оно отобразилась в общем списке')
    def test_add_tool_group(self, rest_internal_client):
        with allure.step('Создаем новую группу инструментов'):
            group_id = self.add_tool_group(rest_internal_client, self.get_tool_group_data())

            groups = self.get_tool_groups(rest_internal_client)

            assert any(group['id'] == group_id for group in groups), f'Группа инструментов не добавлена в общем списке'

        self.delete_tool_group_by_id(rest_internal_client, group_id)

    @allure.title('Изменение порядка группы инструментов')
    def test_swap_tool_group(self, rest_internal_client, clear_db_tools):
        with allure.step('Создаем новую группу инструментов'):
            group_id1 = self.add_tool_group(rest_internal_client, self.get_tool_group_data())
            group_id2 = self.add_tool_group(rest_internal_client, self.get_tool_group_data())
            group_id3 = self.add_tool_group(rest_internal_client, self.get_tool_group_data())

            groups = self.get_tool_groups(rest_internal_client)

            assert groups[-3][
                       'id'] == group_id1, f'Первое созданное демо ({group_id1}) не находится на предпоследнем месте \n (Последняя {groups[-1]} \n Предпоследняя {groups[-2]} \n Предпредпоследняя {groups[-3]})'
            assert groups[-2][
                       'id'] == group_id2, f'Второе созданное демо ({group_id1}) не находится на предпоследнем месте \n (Последняя {groups[-1]} \n Предпоследняя {groups[-2]} \n Предпредпоследняя {groups[-3]})'
            assert groups[-1][
                       'id'] == group_id3, f'Третье созданное демо ({group_id1}) не находится на последнем месте \n (Последняя {groups[-1]} \n Предпоследняя {groups[-2]} \n Предпредпоследняя {groups[-3]})'

            self.swap_tool_group(rest_internal_client, group_id1, group_id2)

            groups_new = self.get_tool_groups(rest_internal_client)

            assert groups_new[-3][
                       'id'] == group_id2, f'Первое созданное демо ({group_id1}) не находится на предпоследнем месте \n (Последняя {groups[-1]} \n Предпоследняя {groups[-2]} \n Предпредпоследняя {groups[-3]})'
            assert groups_new[-2][
                       'id'] == group_id1, f'Второе созданное демо ({group_id1}) не находится на предпоследнем месте \n (Последняя {groups[-1]} \n Предпоследняя {groups[-2]} \n Предпредпоследняя {groups[-3]})'
            assert groups_new[-1][
                       'id'] == group_id3, f'Третье созданное демо ({group_id1}) не находится на последнем месте \n (Последняя {groups[-1]} \n Предпоследняя {groups[-2]} \n Предпредпоследняя {groups[-3]})'

        self.delete_tool_group_by_id(rest_internal_client, group_id1)
        self.delete_tool_group_by_id(rest_internal_client, group_id2)
        self.delete_tool_group_by_id(rest_internal_client, group_id3)

    @allure.title('Добавление группы инструментов c невалидным именем')
    @pytest.mark.parametrize('name', [
        'qweqwe wef weqf we f wqe f ewf ew fwe fw jniu huguijoijfoicjweoin nhiuhiohciunweoidjioj oisiodjfijwqoidjioqjwdijhidqjkw o',
        ''])
    def test_add_tool_group_invalid_name(self, rest_internal_client, name):
        self.add_invalid_tool_group(rest_internal_client, self.get_tool_group_data({'name': name}))

    @allure.title('Изменение группы инструментов')
    def test_change_tool_group(self, rest_internal_client):
        with allure.step('Создаем новую группу инструментов'):
            group_id = self.add_tool_group(rest_internal_client, self.get_tool_group_data())

            name = "new test name" + Gen.generate_text(3)

            self.patch_tool_group_by_id(rest_internal_client, group_id, {
                "shortDescription": "new test description",
                "name": name,
                "numImage": 5
            })

            assert self.get_tool_group_by_id(rest_internal_client, group_id)[
                       'groupName'] == name, f'Новое имя группы инструментов не соответствует имени группы'
            assert self.get_tool_group_by_id(rest_internal_client, group_id)[
                       'numImage'] == 5, f'Новый номер картинки группы инструментов не соответствует номеру картинки'

        self.delete_tool_group_by_id(rest_internal_client, group_id)

    @allure.title('Изменение порядка инструментов внутри группы')
    def test_swap_tool_in_group(self, rest_internal_client):
        with allure.step('Создаем новую группу инструментов'):
            group_id = self.add_tool_group(rest_internal_client, self.get_tool_group_data())

            tool_id1 = self.add_tool(rest_internal_client, self.get_tool_data(group_id))

            tool_id2 = self.add_tool(rest_internal_client, self.get_tool_data(group_id))

            group = self.get_tool_group_by_id(rest_internal_client, group_id)

            assert group['tool'][0]['id'] == tool_id1, f'Инструмент с id {tool_id1} не был добавлен в группу'
            assert group['tool'][1]['id'] == tool_id2, f'Инструмент с id {tool_id2} не был добавлен в группу'

            self.swap_tool(rest_internal_client, group_id, tool_id2, '')

            new_group = self.get_tool_group_by_id(rest_internal_client, group_id)

            assert new_group['tool'][1]['id'] == tool_id1, f'Инструмент с id {tool_id1} не был добавлен в группу'
            assert new_group['tool'][0]['id'] == tool_id2, f'Инструмент с id {tool_id2} не был добавлен в группу'

        self.delete_tool_group_by_id(rest_internal_client, group_id)
        self.delete_tool_by_id(rest_internal_client, tool_id1)
        self.delete_tool_by_id(rest_internal_client, tool_id2)

    @allure.title('Изменение инструмента по id')
    def test_change_tool_by_id(self, rest_internal_client):
        group_id = self.add_tool_group(rest_internal_client, self.get_tool_group_data())
        tool_id = self.add_tool(rest_internal_client, self.get_tool_data(group_id))

        name = "new test name" + Gen.generate_text(3)

        with allure.step(f'Изменяем инструмент с id {tool_id}'):
            self.patch_tool_by_id(rest_internal_client, tool_id, self.get_tool_data(group_id, {
                "shortDescription": "new test description",
                "name": name,
            }))

        assert self.get_tool_by_id(rest_internal_client, tool_id)[
                   'shortDescription'] == "new test description", f'Новое описание инструмента не соответствует описанию инструмента'
        assert self.get_tool_by_id(rest_internal_client, tool_id)[
                   'name'] == name, f'Новое имя инструмента не соответствует имени инструмента'

        self.delete_tool_by_id(rest_internal_client, tool_id)

    @allure.title('Удаление файла из инструмента по id')
    def test_delete_file_in_tool(self, rest_internal_client):
        group_id = self.add_tool_group(rest_internal_client, self.get_tool_group_data())

        file_id = self.add_file_in_tool(rest_internal_client)
        tool_id = self.add_tool(rest_internal_client, self.get_tool_data(group_id, {'files': [file_id]}))

        assert self.get_tool_by_id(rest_internal_client, tool_id)[
                   'files'] != [], f'Файл не добавлен в инструмент {tool_id}'

        with allure.step(f'Удаление файла из инструмент с id {tool_id}'):
            self.patch_tool_by_id(rest_internal_client, tool_id, self.get_tool_data(group_id, {'files': []}))

        assert self.get_tool_by_id(rest_internal_client, tool_id)[
                   'files'] == [], f'Файл не удален из инструмент {tool_id}'
        self.get_file_by_id(rest_internal_client, file_id)

    @allure.title('Удаление инструмента по id')
    def test_delete_tool_by_id(self, rest_internal_client):
        group_id = self.add_tool_group(rest_internal_client, self.get_tool_group_data())
        tool_id = self.add_tool(rest_internal_client, self.get_tool_data(group_id))

        assert self.get_tool_group_by_id(rest_internal_client, group_id)[
            'tool'], f'Инструмент с id {tool_id} не был добавлен в группу'
        self.delete_tool_by_id(rest_internal_client, tool_id)
        assert not self.get_tool_group_by_id(rest_internal_client, group_id)[
            'tool'], f'Инструмент с id {tool_id} не был удалён из группы'

    @allure.title('Изменение активности инструмента по id')
    def test_change_active_tool_by_id(self, rest_internal_client):
        group_id = self.add_tool_group(rest_internal_client, self.get_tool_group_data())
        tool_id = self.add_tool(rest_internal_client, self.get_tool_data(group_id))

        with allure.step(f'Изменяем активность инструмента на {False}'):
            self.change_active_tool_by_id(rest_internal_client, tool_id, False)

            tool = self.get_tool_by_id(rest_internal_client, tool_id)

            assert not tool['isActive'], f'Активность инструмента с id {tool_id} не изменилась на {False}'

        with allure.step(f'Изменяем активность инструмента на {True}'):
            self.change_active_tool_by_id(rest_internal_client, tool_id, True)

            tool = self.get_tool_by_id(rest_internal_client, tool_id)

            assert tool['isActive'], f'Активность инструмента с id {tool_id} не изменилась на {True}'

        self.delete_tool_by_id(rest_internal_client, tool_id)
        self.delete_tool_group_by_id(rest_internal_client, group_id)

    @allure.title('Добавление и получение схемы')
    @allure.issue('https://jira.mts.ru/browse/PPI-4399', 'PPInfo - Отображение схемы процесса для разработчика')
    def test_add_schema(self, rest_internal_client):
        response = self.add_schema(rest_internal_client,
                                   'schema_for_download.svg').strip('"')

        assert uuid.UUID(response), "При добавлении схемы в ответе мы не получили ее id"

        self.get_schema(rest_internal_client, response)

    @allure.title('Добавление группы инструментов со схемой')
    @allure.issue('https://jira.mts.ru/browse/PPI-4399', 'PPInfo - Отображение схемы процесса для разработчика')
    def test_add_tool_group_with_schema(self, rest_internal_client):
        schema_id = self.add_schema(rest_internal_client, 'schema_for_download.svg')

        schema_data = {
            "id": schema_id,
            "name": "Тестовая схема",
            "description": "Описание тестовой схемы",
        }

        group_id = self.add_tool_group(rest_internal_client, self.get_tool_group_data({'groupScheme': schema_data}))

        assert any(g_id['id'] == group_id for g_id in
                   self.get_tool_groups(rest_internal_client)), 'Созданная группа не отображается в общем списке'

        self.delete_tool_group_by_id(rest_internal_client, group_id)
