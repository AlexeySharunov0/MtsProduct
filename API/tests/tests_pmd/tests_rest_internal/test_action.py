import warnings

import allure
import pytest

from API.models.pmd.rest_internal_modules.actions import Actions

warnings.filterwarnings('ignore', message='numpy.dtype size changed')


#### ACTIONS / PRODUCT GUIDE
@pytest.mark.api
@allure.label('priority', 'Высокий')
@allure.feature('Product Guide')
class TestAction(Actions):

    @allure.title('Создание шагов PG')
    @pytest.mark.parametrize('product_type', ['Vneshnii', 'Vnutrennii'])
    @pytest.mark.parametrize('group_id',
                             [['abfe6e2a-b86c-49e2-990b-2d07e6087c31'], ['76ed0eb2-e889-4b2b-80be-60b46007285e'],
                              ['83e92cfe-1257-49f5-80c8-5b953bcdb3a3'], ['3cb9b512-af19-4aca-b2ec-84a4bd1209ed']])
    def test_create_guide(self, rest_internal_client, product_type, group_id):
        action_id = self.create_action(rest_internal_client,
                                       self.get_guide_data(product_type=product_type, group_name=group_id))
        with allure.step('Проверяем, что такой шаг создался'):
            assert self.get_action(rest_internal_client, action_id), 'Шаг не создался'

        self.delete_action(rest_internal_client, action_id)
        with allure.step('Проверяем, что шага по этому айди больше нет'):
            self.get_action_404(rest_internal_client, action_id), 'Шаг есть'

    @allure.title('Создание шагов PG c ссылкой')
    @pytest.mark.parametrize('link_name, link_url',
                             [('test_link1', 'https://stage.prodboard.mts.ru/preset/external')])
    def test_create_guide_with_link(self, rest_internal_client, link_name, link_url):
        action_id = self.create_action(rest_internal_client,
                                       self.get_guide_data({'links': [{'name': link_name, 'url': link_url}]}))
        with allure.step('Проверяем, что такой шаг создался'):
            assert self.get_action(rest_internal_client, action_id), 'Шаг не создался'

        self.delete_action(rest_internal_client, action_id)
        with allure.step('Проверяем, что шага по этому айди больше нет'):
            self.get_action_404(rest_internal_client, action_id), 'Шаг есть'

    @allure.title('Создание шагов PG c ссылками и проверка сортировки ссылок ')
    @allure.issue('https://jira.mts.ru/browse/PPI-2642', 'PPInfo - Порядок отображения сотрудников, файлов, ссылок')
    def test_create_guide_and_check_link_sort(self, rest_internal_client):
        action_id = self.create_action(rest_internal_client, self.get_guide_data({'links': [
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
        with allure.step('Проверяем, что такой шаг создался'):
            assert self.get_action(rest_internal_client, action_id), 'Шаг не создался'

        with allure.step('Проверяем, что порядок ссылок такой же как при создании'):
            links = [link['name'] for link in self.get_action(rest_internal_client, action_id)['links']]

            assert links == ['3', '2', '1', '4', 's', 'a'], f'Не совпадает порядок ссылок: {links}'

        self.delete_action(rest_internal_client, action_id)
        with allure.step('Проверяем, что шага по этому айди больше нет'):
            self.get_action_404(rest_internal_client, action_id), 'Шаг есть'

    @allure.title('Создание шагов PG c кнопками')
    @allure.issue('https://jira.mts.ru/browse/PPI-4115', 'PPInfo - Product Guide: кнопки действий')
    @pytest.mark.parametrize('button_name, button_url',
                             [('test_button1', 'https://stage.prodboard.mts.ru/preset/external')])
    def test_create_guide_with_button(self, rest_internal_client, button_name, button_url):
        action_id = self.create_action(rest_internal_client,
                                       self.get_guide_data({'actionButtons': [{'name': button_name, 'url': button_url}]}))
        with allure.step('Проверяем, что такой шаг создался'):
            assert self.get_action(rest_internal_client, action_id), 'Шаг не создался'

        self.delete_action(rest_internal_client, action_id)
        with allure.step('Проверяем, что шага по этому айди больше нет'):
            self.get_action_404(rest_internal_client, action_id), 'Шаг есть'

    @allure.title('Создание шагов PG c кнопками и проверка сортировки кнопок')
    @allure.issue('https://jira.mts.ru/browse/PPI-4115', 'PPInfo - Product Guide: кнопки действий')
    def test_create_guide_and_check_buttons_sort(self, rest_internal_client):
        action_id = self.create_action(rest_internal_client, self.get_guide_data({'actionButtons': [
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
        with allure.step('Проверяем, что такой шаг создался'):
            assert self.get_action(rest_internal_client, action_id), 'Шаг не создался'

        with allure.step('Проверяем, что порядок ссылок такой же как при создании'):
            buttons = [button['name'] for button in self.get_action(rest_internal_client, action_id)['actionButtons']]

            assert buttons == ['3', '2', '1', '4', 's', 'a'], f'Не совпадает порядок ссылок: {buttons}'

        self.delete_action(rest_internal_client, action_id)
        with allure.step('Проверяем, что шага по этому айди больше нет'):
            self.get_action_404(rest_internal_client, action_id), 'Шаг есть'

    @allure.title('Создание шагов PG c сотрудниками и проверка сортировки сотрудников ')
    @allure.issue('https://jira.mts.ru/browse/PPI-2642', 'PPInfo - Порядок отображения сотрудников, файлов, ссылок')
    def test_create_guide_and_check_employees_sort(self, rest_internal_client):
        action_id = self.create_action(rest_internal_client, self.get_guide_data({'employees': [
            'aikostrov',
            'ddsvetov1',
            'svkurochkin',
            'sayariko',
            'pymaslenkov'
        ]}))
        with allure.step('Проверяем, что такой шаг создался'):
            assert self.get_action(rest_internal_client, action_id), 'Шаг не создался'

        with allure.step('Проверяем, что порядок сотрудников такой же как при создании'):
            employees = [employee['login'][0] for employee in
                         self.get_action(rest_internal_client, action_id)['employees']]

            assert employees == ['a', 'd', 's', 's', 'p'], f'Не совпадает порядок сотрудников: {employees}'

        self.delete_action(rest_internal_client, action_id)
        with allure.step('Проверяем, что шага по этому айди больше нет'):
            self.get_action_404(rest_internal_client, action_id), 'Шаг есть'

    @allure.title('Создание шагов PG c некорректной ссылкой')
    @pytest.mark.parametrize('link_name, link_url',
                             [('test_link1', 'no_link_here')])
    def test_create_guide_with_invalid_link(self, rest_internal_client, link_name, link_url):
        self.create_invalid_action_400(rest_internal_client,
                                       self.get_guide_data({'links': [{'name': link_name, 'url': link_url}]}))

    @allure.title('Создание шагов PG с некорректным id группы')
    @pytest.mark.parametrize('group_id', [['test1'], ['(PPinfo_status)Pilot1'], ['123']])
    def test_create_guide_invalid_group_id(self, rest_internal_client, group_id):
        self.create_invalid_action_400(rest_internal_client, self.get_guide_data(group_name=group_id))

    @allure.title('Создание шагов PG с некорректным productType')
    @pytest.mark.parametrize('product_type', ['External', 'internal777', '123'])
    def test_create_guide_invalid_product_type(self, rest_internal_client, product_type):
        self.create_invalid_action_400(rest_internal_client, self.get_guide_data(product_type=product_type))

    @allure.title('Создание шагов PG с некорректным именем')
    @pytest.mark.parametrize('invalid_name', ['',
                                              'SEO-анализ текста от Text.ru - это уникальный сервис, не имеющий '
                                              'аналогов. Возможность подсветки «воды», заспамленнос test'])
    def test_create_guide_invalid_name(self, rest_internal_client, invalid_name):
        self.create_invalid_action_400(rest_internal_client, self.get_guide_data({'name': invalid_name}))

    @allure.title('Получение активных шагов PG по Коду продукта')
    @allure.issue('https://jira.mts.ru/browse/PPI-2394',
                  'PPInfo - Условия отображения действий в Product Guide - Тип продукта, статусы, атрибуты - этап 2')
    @allure.issue(
        'https://jira.mts.ru/browse/PPI-2524', 'PPinfo - В атомарных продуктах не отображаются шаги PG')
    @pytest.mark.parametrize('product_code',
                             ['60', 'BI_0', 'BI_1905', 'BI_271', 'BI_2982'])
    def test_get_active_guide_list_by_product_code(self, rest_internal_client, product_code):
        assert any(i['actions'] for i in
                   self.get_active_actions(rest_internal_client, product_code)[
                       'actions']), 'Шаги не пришли ни в одной из групп'

    @allure.title('Получение  списка всех шагов PG')
    def test_get_guide_list_by_status(self, rest_internal_client):
        self.get_actions_list(rest_internal_client)

    @allure.title('Редактирование шага PG')
    @pytest.mark.parametrize('group_id',
                             [['abfe6e2a-b86c-49e2-990b-2d07e6087c31'], ['76ed0eb2-e889-4b2b-80be-60b46007285e'],
                              ['83e92cfe-1257-49f5-80c8-5b953bcdb3a3'], ['3cb9b512-af19-4aca-b2ec-84a4bd1209ed']])
    def test_patch_action(self, rest_internal_client, group_id):
        action_id = self.create_action(rest_internal_client, self.get_guide_data(group_name=group_id))

        self.patch_action(rest_internal_client, action_id, self.get_guide_data({'name': 'qwe2'}))

        with allure.step('Проверяем, что шаг отредактирован:'):
            assert self.get_action(rest_internal_client, action_id)['name'] == 'qwe2', 'Имя не отредактировалось'

        self.delete_action(rest_internal_client, action_id)
        with allure.step('Проверяем, что шага по этому айди больше нет'):
            self.get_action_404(rest_internal_client, action_id), 'Шаг есть'

    @allure.title('Редактирование обязательности шага PG')
    @allure.issue('https://jira.mts.ru/browse/PPI-2287',
                  'PPInfo - Backend - Метка "Обязательное/необязательное" у действий в Product Guide')
    @pytest.mark.parametrize('group_id',
                             [['abfe6e2a-b86c-49e2-990b-2d07e6087c31'], ['76ed0eb2-e889-4b2b-80be-60b46007285e'],
                              ['83e92cfe-1257-49f5-80c8-5b953bcdb3a3'], ['3cb9b512-af19-4aca-b2ec-84a4bd1209ed']])
    def test_patch_action_required(self, rest_internal_client, group_id):
        action_id = self.create_action(rest_internal_client, self.get_guide_data(group_name=group_id))

        self.patch_action(rest_internal_client, action_id, self.get_guide_data({'required': True}))

        with allure.step('Проверяем, что шаг отредактирован:'):
            assert self.get_action(rest_internal_client, action_id)['required'], 'Обязательность не отредактировалась'

        self.delete_action(rest_internal_client, action_id)
        with allure.step('Проверяем, что шага по этому айди больше нет'):
            self.get_action_404(rest_internal_client, action_id), 'Шаг есть'

    @allure.title('Редактирование ссылок в шаге PG')
    @pytest.mark.parametrize('link_name, link_url',
                             [('test_link1', 'https://stage.prodboard.mts.ru/preset/external')])
    def test_patch_guide_with_link(self, rest_internal_client, link_name, link_url):
        action_id = self.create_action(rest_internal_client,
                                       self.get_guide_data({'links': [{'name': link_name, 'url': link_url}]}))

        self.patch_action(rest_internal_client, action_id, self.get_guide_data(
            {'links': [{'name': link_name, 'url': 'https://product.mts.ru/preset/external'}]}))

        with allure.step('Проверяем, что ссылка в шаге отредактирована:'):
            assert self.get_action(rest_internal_client, action_id)['links'][0][
                       'url'] == 'https://product.mts.ru/preset/external', 'Ссылка не та'

        self.delete_action(rest_internal_client, action_id)
        with allure.step('Проверяем, что шага по этому айди больше нет'):
            self.get_action_404(rest_internal_client, action_id), 'Шаг есть'

    @allure.title('Удаление ссылок в шаге PG')
    @pytest.mark.parametrize('link_name, link_url',
                             [('test_link1', 'https://stage.prodboard.mts.ru/preset/external')])
    def test_patch_guide_delete_link(self, rest_internal_client, link_name, link_url):
        action_id = self.create_action(rest_internal_client,
                                       self.get_guide_data({'links': [{'name': link_name, 'url': link_url}]}))

        self.patch_action(rest_internal_client, action_id, self.get_guide_data({'links': []}))

        with allure.step('Проверяем, что ссылка в шаге удалена:'):
            assert not self.get_action(rest_internal_client, action_id)['links'], 'Ссылка не удалена'

        self.delete_action(rest_internal_client, action_id)
        with allure.step('Проверяем, что шага по этому айди больше нет'):
            self.get_action_404(rest_internal_client, action_id), 'Шаг есть'

    @allure.title('Редактирование шага PG невалидной ссылкой')
    @pytest.mark.parametrize('link_name, link_url',
                             [('test_link1', 'https://stage.prodboard.mts.ru/preset/external')])
    @pytest.mark.parametrize('invalid_link', ['no_link', ' '])
    def test_patch_action_invalid_link(self, rest_internal_client, link_name, link_url, invalid_link):
        action_id = self.create_action(rest_internal_client,
                                       self.get_guide_data({'links': [{'name': link_name, 'url': link_url}]}))
        self.patch_action_400(rest_internal_client, action_id, self.get_guide_data(
            {'links': [{'name': link_name, 'url': invalid_link}]}))

        with allure.step('Проверяем, что шаг не был отредактирован:'):
            assert self.get_action(rest_internal_client, action_id)['links'][0][
                       'url'] == 'https://stage.prodboard.mts.ru/preset/external', 'Шаг отредактирован'

        self.delete_action(rest_internal_client, action_id)
        with allure.step('Проверяем, что шага по этому айди больше нет'):
            self.get_action_404(rest_internal_client, action_id), 'Шаг есть'

    @allure.title('Редактирование шага PG невалидным именем')
    @pytest.mark.parametrize('invalid_name', ['',
                                              'SEO-анализ текста от Text.ru - это уникальный сервис, не имеющий '
                                              'аналогов. Возможность подсветки «воды», заспамленнос test'])
    def test_patch_action_invalid_name(self, rest_internal_client, invalid_name):
        action_id = self.create_action(rest_internal_client, self.get_guide_data())

        self.patch_action_400(rest_internal_client, action_id, self.get_guide_data({'name': invalid_name}))

        with allure.step('Проверяем, что шаг не был отредактирован:'):
            assert self.get_action(rest_internal_client, action_id)['name'] == 'test_name', 'Шаг отредактировался'

        self.delete_action(rest_internal_client, action_id)
        with allure.step('Проверяем, что шага по этому айди больше нет'):
            self.get_action_404(rest_internal_client, action_id), 'Шаг есть'

    @allure.title('Редактирование шага PG по невалидному id')
    @pytest.mark.parametrize('invalid_id', ['test1', '(PPinfo_status)Pilot1', '123'])
    def test_patch_action_invalid_id(self, rest_internal_client, invalid_id):
        action_id = self.create_action(rest_internal_client, self.get_guide_data())

        self.patch_action_400(rest_internal_client, invalid_id, self.get_guide_data({'name': 'qwe'}))

        self.delete_action(rest_internal_client, action_id)
        with allure.step('Проверяем, что шага по этому айди больше нет'):
            self.get_action_404(rest_internal_client, action_id), 'Шаг есть'

    @allure.title('Редактирование шага PG большим описанием')
    @pytest.mark.parametrize('invalid_description', ['Солнце взошло над горизонтом, покрывая всю округу теплыми '
                                                     'лучами света. От тепла воздуха стало комфортно. Птицы легко '
                                                     'перекидывались песнями, наполняя пространство приятными '
                                                     'звуками. Заброшенный дом стоял у самого берега реки. Крыши '
                                                     'слегка обвалились, но стены все еще держались. Внутри можно '
                                                     'было увидеть развалины множества комнат, наполненных пылью и '
                                                     'забвением. Это место, казалось, было забыто временем. Вдалеке '
                                                     'раздавался гул моторов. Мимо проплывали катера, оставляя за '
                                                     'собой длинные полосы воды. Среди них был и пароход – старинное '
                                                     'судно, которое тихо прокатывалось под прозрачной водой реки. '
                                                     'Наблюдая за этой красотой, невольно начинал задумываться о '
                                                     'приключениях и путешествиях, о том, какие тайны скрывает этот '
                                                     'мир за горизонтом. Все вокруг было погружено в спокойствие. '
                                                     'Падающий лист с дерева выглядел как пушистое перо, '
                                                     'выгравированное в воздухе. Картина изумляла своей простотой и '
                                                     'гармонией. Было невозможно не восхищаться такими сокровищами '
                                                     'природы. Но время шло, и сочинение на 500 символов подошло к '
                                                     'концу. Однако, этот текст лишь набросок того, что могло бы быть '
                                                     'описано. Мир – неисчерпаемые источник тем для размышлений и '
                                                     'вдохновения. Какое приключение ждет вас? Какие открытия? Это '
                                                     'только в ваших руках'])
    def test_patch_action_invalid_description(self, rest_internal_client, invalid_description):
        action_id = self.create_action(rest_internal_client, self.get_guide_data())

        self.patch_action_400(rest_internal_client, action_id,
                              self.get_guide_data({'description': invalid_description}))

        with allure.step('Проверяем, что шаг не был отредактирован:'):
            assert self.get_action(rest_internal_client, action_id)[
                       'description'] == 'test_description', 'Шаг отредактировался'

        self.delete_action(rest_internal_client, action_id)
        with allure.step('Проверяем, что шага по этому айди больше нет'):
            self.get_action_404(rest_internal_client, action_id), 'Шаг есть'

    @allure.issue('https://jira.mts.ru/browse/PPI-1898',
                  'PPInfo-Backend - 2 этап - Админка "Product Guide" - Добавить файлы')
    @allure.title('Добавление файла в шагах PG')
    @pytest.mark.parametrize('file_format',
                             ['.xlsx', '.xls', '.doc', '.docx', '.ppt', '.pptx', '.txt', '.pdf', '.3gp', '.avi', '.mov',
                              '.mp4',
                              '.mp3', '.mkv', '.wav', '.jpg', '.jpeg', '.svg', '.png', '.zip', '.rar', '.gif', '.msg',
                              '.exe', '.rtf'])
    def test_add_file_to_action(self, rest_internal_client, file_format):
        file_id = self.add_file_to_action(rest_internal_client, 'test', file_format)

        with allure.step('Проверяем, что такой файл загрузился'):
            assert 'test' + file_format in self.get_file_in_action_by_id(rest_internal_client,
                                                                         file_id), f'Файл test{file_format} не загрузился'

    @allure.issue('https://jira.mts.ru/browse/PPI-1898',
                  'PPInfo-Backend - 2 этап - Админка "Product Guide" - Добавить файлы')
    @allure.title('Создание шага PG с файлом')
    @pytest.mark.parametrize('group_id',
                             [['abfe6e2a-b86c-49e2-990b-2d07e6087c31'], ['76ed0eb2-e889-4b2b-80be-60b46007285e'],
                              ['83e92cfe-1257-49f5-80c8-5b953bcdb3a3'], ['3cb9b512-af19-4aca-b2ec-84a4bd1209ed']])
    def test_create_guide_with_file(self, rest_internal_client, group_id):
        file_id = self.add_file_to_action(rest_internal_client, 'test')

        action_id = self.create_action(rest_internal_client,
                                       self.get_guide_data({'files': [file_id]}, group_name=group_id))
        with allure.step('Проверяем, что такой шаг создался'):
            assert self.get_action(rest_internal_client, action_id), 'Шаг не создался'

        with allure.step('Проверяем, что файл записался в шаг'):
            assert self.get_action(rest_internal_client, action_id)["files"][0][
                       'name'] == 'test.xlsx', 'Файл не записался'

        self.delete_action(rest_internal_client, action_id)
        with allure.step('Проверяем, что шага по этому айди больше нет'):
            self.get_action_404(rest_internal_client, action_id), 'Шаг есть'

    @allure.issue('https://jira.mts.ru/browse/PPI-1898',
                  'PPInfo-Backend - 2 этап - Админка "Product Guide" - Добавить файлы')
    @allure.title('Редактирование файлов в шаге PG')
    def test_patch_guide_with_file(self, rest_internal_client):
        file_id_before = self.add_file_to_action(rest_internal_client, 'test')
        action_id = self.create_action(rest_internal_client, self.get_guide_data({'files': [file_id_before]}))

        with allure.step('Проверяем, что файл записался в шаг'):
            assert self.get_action(rest_internal_client, action_id)['files'][0][
                       'name'] == 'test.xlsx', 'Файл не записался'

        file_id_after = self.add_file_to_action(rest_internal_client, 'test2')
        self.patch_action(rest_internal_client, action_id,
                          self.get_guide_data(self.get_guide_data({'files': [file_id_after]})))

        with allure.step('Проверяем, что файл отредактирован в шаге'):
            assert self.get_action(rest_internal_client, action_id)['files'][0][
                       'name'] == 'test2.xlsx', f"Файл не перезаписался, массив файлов -  {self.get_action(action_id)['files']}"

        self.delete_action(rest_internal_client, action_id)
        with allure.step('Проверяем, что шага по этому айди больше нет'):
            self.get_action_404(rest_internal_client, action_id), 'Шаг есть'

    @allure.issue('https://jira.mts.ru/browse/PPI-1898',
                  'PPInfo-Backend - 2 этап - Админка "Product Guide" - Добавить файлы')
    @allure.title('Создание шага PG с более, чем 20 файлами')
    def test_create_guide_with_many_files(self, rest_internal_client):
        file_id = self.add_file_to_action(rest_internal_client, 'test')
        file_array = [file_id] * 21

        self.create_invalid_action_400(rest_internal_client, self.get_guide_data({'files': file_array}))

    @allure.issue('https://jira.mts.ru/browse/PPI-1898',
                  'PPInfo-Backend - 2 этап - Админка "Product Guide" - Добавить файлы')
    @allure.title('Редактирование шага более, чем 5 файлами')
    def test_patch_guide_with_many_files(self, rest_internal_client):
        file_id = self.add_file_to_action(rest_internal_client, 'test')
        file_array = [file_id] * 21

        action_id = self.create_action(rest_internal_client, self.get_guide_data())

        self.patch_action_400(rest_internal_client, action_id, self.get_guide_data({'files': file_array}))

        self.delete_action(rest_internal_client, action_id)
        with allure.step('Проверяем, что шага по этому айди больше нет'):
            self.get_action_404(rest_internal_client, action_id), 'Шаг есть'

    @allure.title('Создание шагов c юзером')
    @allure.issue('https://jira.mts.ru/browse/PPI-1900',
                  'PPInfo-Backend - 2 этап - Админка "Product Guide" - Добавить сотрудников')
    @pytest.mark.parametrize('login', ('asnikiforov1', 'ddsvetov1', 'bachuk'))
    def test_create_guide_with_user(self, rest_internal_client, login):
        action_id = self.create_action(rest_internal_client, self.get_guide_data({'employees': [login]}))

        with allure.step('Проверяем, что такой шаг создался'):
            assert self.get_action(rest_internal_client, action_id), 'Шаг не создался'

        with allure.step('Проверяем, что сотрудник записался в шаг'):
            assert self.get_action(rest_internal_client, action_id)['employees'][0][
                       'login'] == login, 'Сотрудник не записался в шаг'

        self.delete_action(rest_internal_client, action_id)
        with allure.step('Проверяем, что шага по этому айди больше нет'):
            self.get_action_404(rest_internal_client, action_id), 'Шаг есть'

    @allure.title('Создание шагов PG c несуществующим юзером')
    @allure.issue("https://jira.mts.ru/browse/PPI-1900",
                  'PPInfo-Backend - 2 этап - Админка "Product Guide" - Добавить сотрудников')
    @pytest.mark.parametrize('login', ('   ', 'no_such_login'))
    def test_create_guide_with_invalid_user(self, rest_internal_client, login):
        self.create_invalid_action_400(rest_internal_client, self.get_guide_data({'employees': [login]}))

    @allure.title('Cоздание шагов PG c несколькими одинаковыми юзерами')
    @allure.issue('https://jira.mts.ru/browse/PPI-1900',
                  'PPInfo-Backend - 2 этап - Админка "Product Guide" - Добавить сотрудников')
    def test_create_guide_with_same_users(self, rest_internal_client):
        action_id = self.create_action(rest_internal_client, self.get_guide_data({'employees': ['cvc', 'cvc']}))
        with allure.step('Проверяем, что юзеры не задублировались'):
            assert len(self.get_action(rest_internal_client, action_id)[
                           'employees']) == 1, f'Массив employees: {self.get_action(action_id)["employees"]}'

        self.delete_action(rest_internal_client, action_id)
        with allure.step('Проверяем, что шага по этому айди больше нет'):
            self.get_action_404(rest_internal_client, action_id), 'Шаг есть'

    @allure.title('Создание шага PG c более чем 20 юзерами')
    @allure.issue("https://jira.mts.ru/browse/PPI-1900",
                  'PPInfo-Backend - 2 этап - Админка "Product Guide" - Добавить сотрудников')
    def test_create_guide_with_many_users(self, rest_internal_client):
        self.create_invalid_action_400(rest_internal_client,
                                       self.get_guide_data(
                                           {'employees': ['cvc', 'asnikiforov1', 'bachuk', 'ddsvetov1', 'aikostrov',
                                                          'dpsazonov3', 'apetrov',
                                                          'tskvyatk', 'aaguryle', 'slpetrov', 'sspetrov', 'aasmirnov4',
                                                          'insmirn3', 'smas',
                                                          'kasmir18', 'smlv', 'rasmirno', 'osmirnva', 'nssmirn1',
                                                          'aasmir14', 'aysmirn1']}))

    @allure.title('Редактирование юзеров в шаге PG')
    @allure.issue('https://jira.mts.ru/browse/PPI-1900',
                  'PPInfo-Backend - 2 этап - Админка "Product Guide" - Добавить сотрудников')
    def test_patch_guide_with_user(self, rest_internal_client):
        action_id = self.create_action(rest_internal_client, self.get_guide_data({'employees': ['asnikiforov1']}))

        with allure.step('Проверяем, что пользователь записался в шаг'):
            assert self.get_action(rest_internal_client, action_id)['employees'][0][
                       'fullName'] == 'Никифоров Александр Сергеевич', 'Сотрудник не записался в шаг'

        self.patch_action(rest_internal_client, action_id, self.get_guide_data({'employees': ['ddsvetov1']}))

        with allure.step('Проверяем, что юзер отредактирован в шаге'):
            assert self.get_action(rest_internal_client, action_id)['employees'][0][
                       'fullName'] == 'Светов Даниил Дмитриевич', 'Сотрудник не записался в шаг'

        self.delete_action(rest_internal_client, action_id)
        with allure.step('Проверяем, что шага по этому айди больше нет'):
            self.get_action_404(rest_internal_client, action_id), 'Шаг есть'

    @allure.title('Редактирование шага PG c более чем 20 юзерами')
    @allure.issue('https://jira.mts.ru/browse/PPI-1900',
                  'PPInfo-Backend - 2 этап - Админка "Product Guide" - Добавить сотрудников')
    def test_patch_guide_with_many_users(self, rest_internal_client):
        action_id = self.create_action(rest_internal_client, self.get_guide_data())
        self.patch_action_400(rest_internal_client, action_id, self.get_guide_data(
            {'employees': ['cvc', 'asnikiforov1', 'bachuk', 'ddsvetov1', 'aikostrov', 'dpsazonov3', 'apetrov',
                           'tskvyatk', 'aaguryle', 'slpetrov', 'sspetrov', 'aasmirnov4', 'insmirn3', 'smas',
                           'kasmir18', 'smlv', 'rasmirno', 'osmirnva', 'nssmirn1', 'aasmir14', 'aysmirn1']}))

        self.delete_action(rest_internal_client, action_id)
        with allure.step('Проверяем, что шага по этому айди больше нет'):
            self.get_action_404(rest_internal_client, action_id), 'Шаг есть'

    @allure.title('Редактирование шагов PG c несуществующим юзером')
    @allure.issue('https://jira.mts.ru/browse/PPI-1900',
                  'PPInfo-Backend - 2 этап - Админка "Product Guide" - Добавить сотрудников')
    @pytest.mark.parametrize('login', ('   ', 'no_such_login'))
    def test_patch_guide_with_invalid_user(self, rest_internal_client, login):
        action_id = self.create_action(rest_internal_client, self.get_guide_data())
        self.patch_action_400(rest_internal_client, action_id, self.get_guide_data(
            {'employees': [login]}))

        self.delete_action(rest_internal_client, action_id)
        with allure.step('Проверяем, что шага по этому айди больше нет'):
            self.get_action_404(rest_internal_client, action_id), 'Шаг есть'

    @allure.title('Свап шагов PG')
    @pytest.mark.parametrize('group_id',
                             ['abfe6e2a-b86c-49e2-990b-2d07e6087c31', '76ed0eb2-e889-4b2b-80be-60b46007285e',
                              '83e92cfe-1257-49f5-80c8-5b953bcdb3a3', '3cb9b512-af19-4aca-b2ec-84a4bd1209ed'])
    @pytest.mark.parametrize('id_from, id_to', ([1, 2], [1, 2]))
    def test_swap_guides(self, rest_internal_client, id_from, id_to, group_id):
        before_swap = [i['actions'] for i in self.get_actions_list(rest_internal_client) if i['id'] == group_id][0]

        if len(before_swap) > 2:
            id_1 = before_swap[id_from]['id']
            id_2 = before_swap[id_to]['id']

            self.swap_guides(rest_internal_client, {'id': id_1, 'groupID': group_id, 'toID': id_2})

            with allure.step('Проверяем, что действия поменялись местами'):
                after_swap = [i['actions'] for i in self.get_actions_list(rest_internal_client) if i['id'] == group_id][
                    0]
                assert after_swap[id_from]["id"] == id_2 and after_swap[id_to][
                    'id'] == id_1, 'Действия не поменялись местами'

    @allure.title('Проверяем работу фильтров шагах PG / Тип продукта')
    @pytest.mark.parametrize('value', ['Vneshnii', 'Vnutrennii'])
    def test_product_guide_check_filter_product_type(self, rest_internal_client, value):
        action_id = self.create_action(rest_internal_client,
                                       self.get_guide_data(product_type=value, params={'isActive': True}))
        with allure.step('Проверяем, что такой шаг создался'):
            assert self.get_action(rest_internal_client, action_id), 'Шаг не создался'
        with allure.step('Получаем данные для продуктов'):
            data_1 = self.get_active_actions(rest_internal_client, 'BI_26551')['actions']
            data_2 = self.get_active_actions(rest_internal_client, 'BI_26552')['actions']

        if value == 'Vneshnii':
            with allure.step(f'Проверяем, что шаг отображается для продуктов с атрибутом {value}'):
                action_list = [i['actions'] for i in data_1 if i['groupName'] == 'Закрытие продукта'][0]
                assert any(i['id'] == action_id for i in action_list), 'Действие не появилось в нужной группе'
            with allure.step(f'Проверяем, что шаг не отображается для продуктов с атрибутом {value}'):
                action_list = [i['actions'] for i in data_2 if i['groupName'] == 'Закрытие продукта'][0]
                assert not any(i['id'] == action_id for i in action_list), 'Действие появилось в нужной группе'
        else:
            with allure.step(f'Проверяем, что шаг отображается для продуктов с атрибутом {value}'):
                action_list = [i['actions'] for i in data_2 if i['groupName'] == 'Закрытие продукта'][0]
                assert any(i['id'] == action_id for i in action_list), 'Действие не появилось в нужной группе'
            with allure.step(f'Проверяем, что шаг не отображается для продуктов с атрибутом {value}'):
                action_list = [i['actions'] for i in data_1 if i['groupName'] == 'Закрытие продукта'][0]
                assert not any(i['id'] == action_id for i in action_list), 'Действие появилось в нужной группе'

        self.delete_action(rest_internal_client, action_id)
        with allure.step('Проверяем, что шага по этому айди больше нет'):
            self.get_action_404(rest_internal_client, action_id), 'Шаг есть'

    @allure.title('Проверяем работу фильтров шагах PG / Создание / Дополнительные фильтры')
    @allure.issue('https://jira.mts.ru/browse/PPI-2473', 'PPInfo - Backend - Группы в PG, условие "статус"')
    @pytest.mark.parametrize(['attr_name', 'value'], [['PPinfo_status', 'Arkhiv'],
                                                      ['PPinfo_MTS_Brand', '(PPinfo_MTSBrand)MTSBrand_no'],
                                                      ['PPinfo_category_product', '(PPInfo_category_spravochnik)AI'],
                                                      ['PPinfo_market', '(PPinfo_market)B2C'],
                                                      ['PPInfo_type_develop', '(PPInfo_spravoch_type)Own']])
    def test_product_guide_check_additional_filters_create(self, rest_internal_client, attr_name, value):
        with allure.step(f'Проверяем фильтр {attr_name}'):
            filter_value = self.get_filter_value([[attr_name, value]])
        action_id = self.create_action(rest_internal_client,
                                       self.get_guide_data(params={'isActive': True, 'filter': filter_value}))
        with allure.step('Проверяем, что такой шаг создался'):
            assert self.get_action(rest_internal_client, action_id), 'Шаг не создался'
        with allure.step('Получаем данные для продуктов'):
            data_show = self.get_active_actions(rest_internal_client, 'BI_26551')['actions']
            data_hide = self.get_active_actions(rest_internal_client, 'BI_26552')['actions']

        with allure.step(f'Проверяем, что шаг отображается для продуктов с атрибутом {value}'):
            action_list = [i['actions'] for i in data_show if i['groupName'] == 'Закрытие продукта'][0]
            assert any(i['id'] == action_id for i in action_list), 'Фильтр скрыл шаг'
        with allure.step(f'Проверяем, что шаг не отображается для продуктов с атрибутом {value}'):
            action_list = [i['actions'] for i in data_hide if i['groupName'] == 'Закрытие продукта'][0]
            assert not any(i['id'] == action_id for i in action_list), 'Фильтр не скрыл шаг'

        self.delete_action(rest_internal_client, action_id)
        with allure.step('Проверяем, что шага по этому айди больше нет'):
            self.get_action_404(rest_internal_client, action_id), 'Шаг есть'

    @allure.title('Проверяем работу фильтров шагах PG / Редактирование / Дополнительные фильтры')
    @allure.issue('https://jira.mts.ru/browse/PPI-2473', 'PPInfo - Backend - Группы в PG, условие "статус"')
    @pytest.mark.parametrize(['attr_name', 'value', 'value_new'],
                             [['PPinfo_status', 'Arkhiv', '(PPinfo_status)In_progress'],
                              ['PPinfo_MTS_Brand', '(PPinfo_MTSBrand)MTSBrand_no', 'Sabbrend'],
                              ['PPinfo_category_product', '(PPInfo_category_spravochnik)AI',
                               '(PPInfo_category_spravochnik)Partner'],
                              ['PPinfo_market', '(PPinfo_market)B2C', '(PPinfo_market)B2G'],
                              ['PPInfo_type_develop', '(PPInfo_spravoch_type)Own', '(PPInfo_spravoch_type)Vendor']])
    def test_product_guide_check_change_additional_filters(self, rest_internal_client, attr_name, value, value_new):
        with allure.step(f'Проверяем фильтр {attr_name}'):
            filter_value = self.get_filter_value([[attr_name, value]])
        action_id = self.create_action(rest_internal_client,
                                       self.get_guide_data(params={'isActive': True, 'filter': filter_value}))
        with allure.step('Проверяем, что такой шаг создался'):
            assert self.get_action(rest_internal_client, action_id), 'Шаг не создался'
        with allure.step('Получаем данные для продуктов'):
            data_show = self.get_active_actions(rest_internal_client, 'BI_26551')['actions']
            data_hide = self.get_active_actions(rest_internal_client, 'BI_26552')['actions']

        with allure.step(f'Проверяем, что шаг отображается для продуктов с атрибутом {value}'):
            action_list = [i['actions'] for i in data_show if i['groupName'] == 'Закрытие продукта'][0]
            assert any(i['id'] == action_id for i in action_list), 'Фильтр скрыл шаг'
        with allure.step(f'Проверяем, что шаг не отображается для продуктов с атрибутом {value}'):
            action_list = [i['actions'] for i in data_hide if i['groupName'] == 'Закрытие продукта'][0]
            assert not any(i['id'] == action_id for i in action_list), 'Фильтр не скрыл шаг'

        with allure.step(f'Меняем фильтр на {value_new}'):
            filter_value = self.get_filter_value([[attr_name, value_new]])
            self.patch_action(rest_internal_client, action_id,
                              self.get_guide_data(params={'isActive': True, 'filter': filter_value}))
        with allure.step('Получаем данные для продуктов'):
            data_show = self.get_active_actions(rest_internal_client, 'BI_26551')['actions']
            data_hide = self.get_active_actions(rest_internal_client, 'BI_26552')['actions']

        with allure.step(f'Проверяем, что шаг не отображается для продуктов с атрибутом {value_new}'):
            action_list = [i['actions'] for i in data_show if i['groupName'] == 'Закрытие продукта'][0]
            assert not any(i['id'] == action_id for i in action_list), 'Фильтр скрыл шаг'
        with allure.step(f'Проверяем, что шаг отображается для продуктов с атрибутом {value_new}'):
            action_list = [i['actions'] for i in data_hide if i['groupName'] == 'Закрытие продукта'][0]
            assert any(i['id'] == action_id for i in action_list), 'Фильтр не скрыл шаг'

        self.delete_action(rest_internal_client, action_id)
        with allure.step('Проверяем, что шага по этому айди больше нет'):
            self.get_action_404(rest_internal_client, action_id), 'Шаг есть'

    @allure.title('Проверяем работу фильтров шагах PG / 2 совпадающих фильтра')
    @allure.issue('https://jira.mts.ru/browse/PPI-2473', 'PPInfo - Backend - Группы в PG, условие "статус"')
    def test_product_guide_check_two_filters(self, rest_internal_client):
        attr1 = ['PPinfo_status', '(PPinfo_status)Out_of_use']
        attr2 = ['PPinfo_MTS_Brand', '(PPinfo_MTSBrand)MTSBrand_no']
        with allure.step(f'Проверяем фильтр {attr1[0]} и {attr2[0]}'):
            filter_value = self.get_filter_value([attr1, attr2])
        action_id = self.create_action(rest_internal_client,
                                       self.get_guide_data(params={'isActive': True, 'filter': filter_value}))
        with allure.step('Проверяем, что такой шаг создался'):
            assert self.get_action(rest_internal_client, action_id), 'Шаг не создался'
        with allure.step('Получаем данные для продуктов'):
            data_show = self.get_active_actions(rest_internal_client, 'BI_26551')['actions']
            data_hide = self.get_active_actions(rest_internal_client, 'BI_26552')['actions']

        with allure.step('Проверяем, что шаг отображается для продукта с обоими фильтрами'):
            action_list = [i['actions'] for i in data_show if i['groupName'] == 'Закрытие продукта'][0]
            assert any(i['id'] == action_id for i in action_list), 'Фильтр скрыл шаг'
        with allure.step('Проверяем, что шаг не отображается для продукта с обоими не подходящими фильтрами'):
            action_list = [i['actions'] for i in data_hide if i['groupName'] == 'Закрытие продукта'][0]
            assert not any(i['id'] == action_id for i in action_list), 'Фильтр не скрыл шаг'

        self.delete_action(rest_internal_client, action_id)
        with allure.step('Проверяем, что шага по этому айди больше нет'):
            self.get_action_404(rest_internal_client, action_id), 'Шаг есть'

    @allure.title('Проверяем работу фильтров шагах PG / 2 противоречащих фильтра')
    @allure.issue('https://jira.mts.ru/browse/PPI-2473', 'PPInfo - Backend - Группы в PG, условие "статус"')
    def test_product_guide_check_two_wrong_filters(self, rest_internal_client):
        attr1 = ['PPinfo_status', 'Arkhiv']
        attr2 = ['PPinfo_MTS_Brand', 'Sabbrend']
        with allure.step(f'Проверяем фильтр {attr1[0]} и {attr2[0]}'):
            filter_value = self.get_filter_value([attr1, attr2])
        action_id = self.create_action(rest_internal_client,
                                       self.get_guide_data(params={'isActive': True, 'filter': filter_value}))
        with allure.step('Проверяем, что такой шаг создался'):
            assert self.get_action(rest_internal_client, action_id), 'Шаг не создался'
        with allure.step('Получаем данные для продуктов'):
            data_show = self.get_active_actions(rest_internal_client, 'BI_26551')['actions']
            data_hide = self.get_active_actions(rest_internal_client, 'BI_26552')['actions']

        with allure.step('Проверяем, что шаг не отображается для продукта с подходящим 1 фильтром, но не подходящим 2'):
            action_list = [i['actions'] for i in data_show if i['groupName'] == 'Закрытие продукта'][0]
            assert not any(i['id'] == action_id for i in action_list), 'Фильтр скрыл шаг'
        with allure.step('Проверяем, что шаг не отображается для продукта с подходящим 2 фильтром, но не подходящим 1'):
            action_list = [i['actions'] for i in data_hide if i['groupName'] == 'Закрытие продукта'][0]
            assert not any(i['id'] == action_id for i in action_list), 'Фильтр не скрыл шаг'

        self.delete_action(rest_internal_client, action_id)
        with allure.step('Проверяем, что шага по этому айди больше нет'):
            self.get_action_404(rest_internal_client, action_id), 'Шаг есть'

    @allure.title('Создание шага в несуществующей группе')
    @allure.issue('https://jira.mts.ru/browse/PPI-2473', 'PPInfo - Backend - Группы в PG, условие "статус"')
    @pytest.mark.parametrize('group_id', ['123', 'приветики!'])
    def test_create_action_wrong_group(self, rest_internal_client, group_id):
        self.create_invalid_action_400(rest_internal_client, self.get_guide_data(group_name=[group_id]))

    @allure.title('Создание шага с пустым обязательным свойством / Пустая группа')
    @allure.issue('https://jira.mts.ru/browse/PPI-2473', 'PPInfo - Backend - Группы в PG, условие "статус"')
    def test_create_action_empty_group(self, rest_internal_client):
        self.create_invalid_action_400(rest_internal_client, self.get_guide_data(group_name=[]))

    @allure.title('Создание шага с пустым обязательным свойством / Пустой тип продукта')
    @allure.issue('https://jira.mts.ru/browse/PPI-2473', 'PPInfo - Backend - Группы в PG, условие "статус"')
    def test_create_action_empty_type(self, rest_internal_client):
        self.create_invalid_action_400(rest_internal_client, self.get_guide_data(product_type=''))

    @allure.title('Проверка сортировки сотрудников внутри шага PG')
    def test_employees_pg_sorted(self, rest_internal_client):
        action_id = self.create_action(rest_internal_client,
                                       self.get_guide_data(
                                           {'employees': ['ivga', 'askorol1', 'ifivanov', 'ivvv', 'cvc']}))
        names = [name['fullName'] for name in self.get_action(rest_internal_client, action_id)['employees']]
        with allure.step('Проверяем, что сотрудники отсортированы по алфавиту'):
            assert names == sorted(names), 'Сотрудники не отсортированы по алфавиту'

    @allure.title('Проверка сортировки шагов PG на странице продукта')
    @pytest.mark.parametrize('product_code', ['60', 'BI_0', 'BI_1905', 'BI_271', 'BI_2982'])
    def test_pg_steps_sorted(self, rest_internal_client, product_code):
        actions_in_settings = self.get_actions_list(rest_internal_client)[0]['actions']
        ids_in_settings = [i['id'] for i in actions_in_settings if i['isActive']]

        actions_in_product = self.get_active_actions(rest_internal_client, product_code)['actions'][0]['actions']
        ids_in_product = [i['id'] for i in actions_in_product]

        expected_ids = [i for i in ids_in_settings if i in ids_in_product]

        with allure.step('Проверяем, что действия на странице отсортированы так же как и в настройках'):
            assert expected_ids == ids_in_product, 'Сортировка не та же'

    @allure.title('Смена активности шага через тогл')
    @allure.issue('https://jira.mts.ru/browse/PPI-2610', 'PPInfo - Backend - Активация шага PG')
    @pytest.mark.parametrize('is_active', [True, False])
    def test_pg_change_activity_by_toggle(self, rest_internal_client, is_active):
        with allure.step('Создаем шаг'):
            action_id = self.create_action(rest_internal_client, self.get_guide_data(params={'isActive': is_active}))
        self.change_step_activity(rest_internal_client, action_id)
        with allure.step('Проверяем, что активность шага сменилась'):
            assert is_active is not self.get_action(rest_internal_client, action_id), 'Активность шага не сменилась'
        self.delete_action(rest_internal_client, action_id)
        with allure.step('Проверяем, что шага по этому айди больше нет'):
            self.get_action_404(rest_internal_client, action_id), 'Шаг есть'

    @allure.title('Невалидная смена активности шага через тогл')
    @allure.issue('https://jira.mts.ru/browse/PPI-2610', 'PPInfo - Backend - Активация шага PG')
    @pytest.mark.parametrize('step_id', ['привет', '123123123'])
    def test_pg_change_activity_by_toggle(self, rest_internal_client, step_id):
        self.change_step_activity_400(rest_internal_client, step_id)

    @allure.title('Получение шагов для общего Product Guide')
    @allure.issue('https://jira.mts.ru/browse/PPI-2339', 'PPInfo - Общий Product Guide')
    @pytest.mark.parametrize('product_type', ['Vneshnii', 'Vnutrennii'])
    def test_get_all_pg_steps(self, rest_internal_client, product_type):
        with allure.step('Проверяем, что хотя бы в одной группе пришли шаги'):
            assert any(actions['actions'] for actions in
                       self.get_all_steps(rest_internal_client, product_type)), 'Шаги не пришли'

    @allure.title('В общий Product Guide приходят все активные шаги нужного типа')
    @allure.issue('https://jira.mts.ru/browse/PPI-2339', 'PPInfo - Общий Product Guide')
    @pytest.mark.parametrize('product_type', ['Vneshnii', 'Vnutrennii'])
    def test_common_pg_has_all_steps(self, rest_internal_client, product_type):
        settings_steps = self.get_actions_list(rest_internal_client)
        common_steps = self.get_all_steps(rest_internal_client, product_type)

        req_type = 'внешний' if product_type == 'Vneshnii' else 'внутренний'

        for ind in range(len(settings_steps)):
            required_steps_ids = [step['id'] for step in settings_steps[ind]['actions'] if
                                  step['isActive'] and req_type in step['typeProduct'].lower()]
            common_steps_ids = [step['id'] for step in common_steps[ind]['actions']]
            with allure.step(f'Проверяем, что в группе {settings_steps[ind]["groupName"]} нужные шаги'):
                assert required_steps_ids == common_steps_ids, f'В группе {settings_steps[ind]["groupName"]} не те шаги'

    @allure.title('В общий Product Guide попадают все шаги, вне зависимости от фильтров')
    @allure.issue('https://jira.mts.ru/browse/PPI-2339', 'PPInfo - Общий Product Guide')
    @pytest.mark.parametrize('product_type', ['Vneshnii', 'Vnutrennii'])
    @pytest.mark.parametrize(['attr_name', 'value'], [['PPinfo_status', 'Arkhiv'],
                                                      ['PPinfo_MTS_Brand', '(PPinfo_MTSBrand)MTSBrand_no'],
                                                      ['PPinfo_category_product', '(PPInfo_category_spravochnik)AI'],
                                                      ['PPinfo_market', '(PPinfo_market)B2C'],
                                                      ['PPInfo_type_develop', '(PPInfo_spravoch_type)Own'],
                                                      ['Nalichie_vneshnikh_KTS', 'Da']])
    def test_common_pg_no_filter_affection(self, rest_internal_client, attr_name, value, product_type):
        with allure.step(f'Проверяем фильтр {attr_name}'):
            filter_value = self.get_filter_value([[attr_name, value]])
        action_id = self.create_action(rest_internal_client,
                                       self.get_guide_data(params={'isActive': True, 'filter': filter_value}))

        all_steps = self.get_all_steps(rest_internal_client, product_type)[-1]['actions']
        self.delete_action(rest_internal_client, action_id)

        with allure.step('Проверяем, что шаг есть в общем Product Guide'):
            assert any(action_id == new_id['id'] for new_id in all_steps), 'Шаг не появился'

    @allure.title('Создание повторяемого шага PG')
    @allure.issue('https://jira.mts.ru/browse/PPI-2732', 'PPInfo - Повторяемые шаги - Флаг "Повторяемый')
    def test_patch_action_repeatable(self, rest_internal_client):
        action_id = self.create_action(rest_internal_client,
                                       self.get_guide_data(params={'repeatable': True, 'isActive': True}))

        with allure.step('Проверяем, что шаг создался как повторяемый:'):
            assert any(
                step['repeatable'] for step in self.get_active_actions(rest_internal_client, 'BI_60')[-1]['actions'] if
                step['id'] == action_id), 'Шаг не отмечен как повторяемый'

        self.delete_action(rest_internal_client, action_id)
        with allure.step('Проверяем, что шага по этому айди больше нет'):
            self.get_action_404(rest_internal_client, action_id), 'Шаг есть'

    @allure.title('Редактирование повторяемости шага PG')
    @allure.issue('https://jira.mts.ru/browse/PPI-2732', 'PPInfo - Повторяемые шаги - Флаг "Повторяемый')
    @pytest.mark.parametrize('group_id',
                             [['abfe6e2a-b86c-49e2-990b-2d07e6087c31'], ['76ed0eb2-e889-4b2b-80be-60b46007285e'],
                              ['83e92cfe-1257-49f5-80c8-5b953bcdb3a3'], ['3cb9b512-af19-4aca-b2ec-84a4bd1209ed']])
    def test_patch_action_repeatable(self, rest_internal_client, group_id):
        action_id = self.create_action(rest_internal_client, self.get_guide_data(group_name=group_id))

        self.patch_action(rest_internal_client, action_id, self.get_guide_data({'repeatable': True}))

        with allure.step('Проверяем, что шаг отредактирован:'):
            assert self.get_action(rest_internal_client, action_id)['repeatable'], 'Повторяемость не отредактирована'

        self.delete_action(rest_internal_client, action_id)
        with allure.step('Проверяем, что шага по этому айди больше нет'):
            self.get_action_404(rest_internal_client, action_id), 'Шаг есть'

    @allure.title('Создание вложенного шага PG')
    @pytest.mark.parametrize('group_id',
                             ['abfe6e2a-b86c-49e2-990b-2d07e6087c31', '76ed0eb2-e889-4b2b-80be-60b46007285e',
                              '83e92cfe-1257-49f5-80c8-5b953bcdb3a3', '3cb9b512-af19-4aca-b2ec-84a4bd1209ed'])
    def test_add_sub_action(self, rest_internal_client, group_id):
        action_ids = self.create_sub_action(rest_internal_client, group_name=group_id)
        main_action_id, sub_action_id = action_ids[0], action_ids[1]

        with allure.step('Проверяем, что вложенный шаг прикрепился к главному действию'):
            assert self.get_action(rest_internal_client, main_action_id)['subActions'], 'Вложенных шагов нет'
            assert any(i['id'] == sub_action_id for i in
                       self.get_action(rest_internal_client, main_action_id)[
                           'subActions']), 'Нужный вложенный шаг не добавился к главному'

        self.delete_action(rest_internal_client, main_action_id)
        with allure.step('Проверяем, что шага по этому айди больше нет'):
            self.get_action_404(rest_internal_client, main_action_id), 'Шаг есть'

    @allure.title('Создание вложенного шага PG / Отображение на странице продукта')
    @pytest.mark.parametrize('product_code', ['BI_60', 'BI_1905'])
    def test_add_sub_action_product_page(self, rest_internal_client, product_code):
        action_ids = self.create_sub_action(rest_internal_client)
        main_action_id, sub_action_id = action_ids[0], action_ids[1]

        with allure.step('Проверяем, что вложенный шаг отображается на странице продукта'):
            action = \
                [i for i in self.get_active_actions(rest_internal_client, product_code)['actions'][0]['actions'] if
                 i['id'] == main_action_id][0]
            assert action['subActions'], 'Вложенных шагов нет'
            assert any(
                i['id'] == sub_action_id for i in action['subActions']), 'Нужный вложенный шаг не добавился к главному'

        self.delete_action(rest_internal_client, main_action_id)
        with allure.step('Проверяем, что шага по этому айди больше нет'):
            self.get_action_404(rest_internal_client, main_action_id), 'Шаг есть'

    @allure.title('Создание вложенного шага PG / Отображение в общем Product Guide')
    @pytest.mark.parametrize('product_type', ['Vneshnii', 'Vnutrennii'])
    def test_add_sub_action_product_guide(self, rest_internal_client, product_type):
        action_ids = self.create_sub_action(rest_internal_client)
        main_action_id, sub_action_id = action_ids[0], action_ids[1]

        with allure.step(f'Проверяем, что вложенный шаг отображается на вкладке {product_type}'):
            action = [i for i in self.get_all_steps(rest_internal_client, product_type)[0]['actions'] if
                      i['id'] == main_action_id][0]
            assert action['subActions'], 'Вложенных шагов нет'
            assert any(
                i['id'] == sub_action_id for i in action['subActions']), 'Нужный вложенный шаг не добавился к главному'

        self.delete_action(rest_internal_client, main_action_id)
        with allure.step('Проверяем, что шага по этому айди больше нет'):
            self.get_action_404(rest_internal_client, main_action_id), 'Шаг есть'

    @allure.title('Создание вложенного шага PG / Отображение в таблице шагов в админке')
    def test_add_sub_action_admin_table(self, rest_internal_client):
        action_ids = self.create_sub_action(rest_internal_client)
        main_action_id, sub_action_id = action_ids[0], action_ids[1]

        with allure.step('Проверяем, что в админке отображается наличие вложенных шагов'):
            assert self.get_actions_list(rest_internal_client)[0]['actions'][-1]['hasSubAction'], 'Отметки нет'
        self.delete_action(rest_internal_client, main_action_id)
        with allure.step('Проверяем, что шага по этому айди больше нет'):
            self.get_action_404(rest_internal_client, main_action_id), 'Шаг есть'

    @allure.title('Смена активности у вложенного шага при создании')
    @pytest.mark.parametrize('is_active', [True, False])
    def test_add_sub_action_activity(self, rest_internal_client, is_active):
        action_ids = self.create_sub_action(rest_internal_client, params={'isActive': is_active})
        main_action_id, sub_action_id = action_ids[0], action_ids[1]

        with allure.step('Проверяем, что активность у шага как при создании'):
            assert self.get_action(rest_internal_client, sub_action_id)['isActive'] is is_active, 'Активность не та'
        with allure.step('Проверяем, что вложенный шаг отображается на странице продукта согласно активности'):
            action = \
                [i for i in self.get_active_actions(rest_internal_client, 'BI_60')['actions'][0]['actions'] if
                 i['id'] == main_action_id][0]
            assert is_active is any(
                i['id'] == sub_action_id for i in action['subActions']), 'Шаг отображается не согласно активности'

        self.delete_action(rest_internal_client, main_action_id)
        with allure.step('Проверяем, что шага по этому айди больше нет'):
            self.get_action_404(rest_internal_client, main_action_id), 'Шаг есть'

    @allure.title('Смена активности у вложенного шага через апишку')
    @pytest.mark.parametrize('is_active', [True, False])
    def test_add_sub_action_activity_api(self, rest_internal_client, is_active):
        action_ids = self.create_sub_action(rest_internal_client, params={'isActive': is_active})
        main_action_id, sub_action_id = action_ids[0], action_ids[1]

        self.change_step_activity(rest_internal_client, sub_action_id)

        with allure.step('Проверяем, что активность вложенного шага изменилась'):
            assert self.get_action(rest_internal_client, sub_action_id)[
                       'isActive'] is not is_active, 'Активность не сменилась'

        self.delete_action(rest_internal_client, main_action_id)
        with allure.step('Проверяем, что шага по этому айди больше нет'):
            self.get_action_404(rest_internal_client, main_action_id), 'Шаг есть'

    @allure.title('Невалидное создание вложенного шага PG / Добавление группы')
    def test_add_sub_action_invalid_group(self, rest_internal_client):
        with allure.step('Создаем обычный шаг'):
            main_action_id = self.create_action(rest_internal_client,
                                                self.get_guide_data(
                                                    group_name=['abfe6e2a-b86c-49e2-990b-2d07e6087c31']))
        with allure.step('Создаем вложенный шаг'):
            self.create_invalid_action_400(rest_internal_client, self.get_guide_data(
                params={'groups': ['abfe6e2a-b86c-49e2-990b-2d07e6087c31'], 'filter': [],
                        'mainActionId': main_action_id}))

        self.delete_action(rest_internal_client, main_action_id)
        with allure.step('Проверяем, что шага по этому айди больше нет'):
            self.get_action_404(rest_internal_client, main_action_id), 'Шаг есть'

    @allure.title('Невалидное создание вложенного шага PG / Добавление фильтра')
    def test_add_sub_action_invalid_filter(self, rest_internal_client):
        with allure.step('Создаем обычный шаг'):
            main_action_id = self.create_action(rest_internal_client,
                                                self.get_guide_data(
                                                    group_name=['abfe6e2a-b86c-49e2-990b-2d07e6087c31']))
        with allure.step('Создаем вложенный шаг'):
            self.create_invalid_action_400(rest_internal_client,
                                           self.get_guide_data(params={'groups': [], 'mainActionId': main_action_id}))

        self.delete_action(rest_internal_client, main_action_id)
        with allure.step('Проверяем, что шага по этому айди больше нет'):
            self.get_action_404(rest_internal_client, main_action_id), 'Шаг есть'

    @allure.title('Невалидное создание вложенного шага PG / Без id главного шага')
    def test_add_sub_action_invalid_main_step(self, rest_internal_client):
        with allure.step('Создаем обычный шаг'):
            main_action_id = self.create_action(rest_internal_client,
                                                self.get_guide_data(
                                                    group_name=['abfe6e2a-b86c-49e2-990b-2d07e6087c31']))
        with allure.step('Создаем вложенный шаг'):
            self.create_invalid_action_400(rest_internal_client, self.get_guide_data(
                params={'groups': [], 'filter': [],
                        'mainActionId': ''}))

        self.delete_action(rest_internal_client, main_action_id)
        with allure.step('Проверяем, что шага по этому айди больше нет'):
            self.get_action_404(rest_internal_client, main_action_id), 'Шаг есть'

    @allure.title('Свап вложенных шагов PG')
    @pytest.mark.parametrize("id_from, id_to", ([1, 2], [1, 2]))
    def test_swap_sub_actions(self, rest_internal_client, id_from, id_to):
        with allure.step('Создаем обычный шаг'):
            main_action_id = self.create_action(rest_internal_client,
                                                self.get_guide_data(
                                                    group_name=['abfe6e2a-b86c-49e2-990b-2d07e6087c31']))
        with allure.step('Создаем 3 вложенных шага'):
            id_s = [self.create_action(rest_internal_client,
                                       self.get_guide_data(
                                           params={'groups': [], 'filter': [], 'mainActionId': main_action_id})) for _
                    in
                    range(3)]
        id_1 = id_s[id_from]
        id_2 = id_s[id_to]
        self.swap_guides(rest_internal_client, {'id': id_1, 'groupID': main_action_id, 'toID': id_2})

        with allure.step('Проверяем, что шаги поменялись местами'):
            after_swap = [i['id'] for i in self.get_action(rest_internal_client, main_action_id)['subActions']]
            assert after_swap[id_from] == id_2 and after_swap[id_to] == id_1, 'Шаги не поменялись местами'

        self.delete_action(rest_internal_client, main_action_id)
        with allure.step('Проверяем, что шага по этому айди больше нет'):
            self.get_action_404(rest_internal_client, main_action_id), 'Шаг есть'

    @allure.title('Количество строк в excel PG по типам продукта')
    @allure.issue('https://jira.mts.ru/browse/PPI-2790', 'PPInfo - Выгрузка в Excel содержимого PG')
    @pytest.mark.excel
    @pytest.mark.parametrize('product_type', ['Vneshnii', 'Vnutrennii'])
    def test_count_of_rows_in_pg_excel_by_type(self, rest_internal_client, product_type, clear_excel):

        excel = self.get_excel_pg_by_type(rest_internal_client, product_type)
        for sheet, count_rows in zip(excel.sheetnames,
                                     self.count_all_steps_by_type(rest_internal_client, product_type)):
            with allure.step(f'Проверяем количество строк в икселе на листе {sheet}'):
                assert excel[
                           sheet].max_row - 1 == count_rows, f'В икселе {sheet} количество строк не совпадает с кол-вом строк на строкнице'

    @allure.title('Количество строк в excel PG по BI коду продукта')
    @allure.issue('https://jira.mts.ru/browse/PPI-2790', 'PPInfo - Выгрузка в Excel содержимого PG')
    @pytest.mark.excel
    @pytest.mark.parametrize('bi_code', ['BI_60', 'BI_3060', 'BI_271', 'BI_1883'])
    def test_count_of_rows_in_pg_excel_by_bi_code(self, rest_internal_client, bi_code, clear_excel):

        excel = self.get_excel_pg_by_bi_code(rest_internal_client, bi_code)
        for sheet, count_rows in zip(excel.sheetnames, self.count_all_steps_by_bi_code(rest_internal_client, bi_code)):
            with allure.step(f'Проверяем количество строк в икселе на листе {sheet}'):
                assert excel[
                           sheet].max_row - 1 == count_rows, f'В икселе {sheet} количество строк не совпадает с кол-вом строк на странице'

    @allure.title('Создание шага с меткой Для PO')
    @allure.issue('https://jira.mts.ru/browse/PPI-2907', 'PPInfo - Добавление отметок в шаги PG: PO, Tech lead')
    @pytest.mark.parametrize('for_po', [True, False])
    @pytest.mark.parametrize('for_cto', [False, True])
    def test_add_action_for_po_and_cto(self, rest_internal_client, for_po, for_cto):
        with allure.step('Создаем обычный шаг'):
            main_action_id = self.create_action(rest_internal_client,
                                                self.get_guide_data(
                                                    params={'for_po': for_po, 'for_cto': for_cto,
                                                            'groups': ['abfe6e2a-b86c-49e2-990b-2d07e6087c31']}))
        if for_po:
            assert self.get_action(rest_internal_client, main_action_id)['for_po'], 'Метка для ПО не применилась'
        if for_cto:
            assert self.get_action(rest_internal_client, main_action_id)['for_cto'], 'Метка для СТО не применилась'

        self.delete_action(rest_internal_client, main_action_id)
        with allure.step('Проверяем, что шага по этому айди больше нет'):
            self.get_action_404(rest_internal_client, main_action_id), 'Шаг есть'

    @allure.title('Создание шага с меткой Для PO и проверка его на стр продукта')
    @allure.issue('https://jira.mts.ru/browse/PPI-2907', 'PPInfo - Добавление отметок в шаги PG: PO, Tech lead')
    @pytest.mark.parametrize('for_po', [True, False])
    @pytest.mark.parametrize('for_cto', [False, True])
    def test_action_for_po_and_cto_on_product_page(self, rest_internal_client, for_po, for_cto):
        with allure.step('Создаем обычный шаг'):
            main_action_id = self.create_action(rest_internal_client,
                                                self.get_guide_data(
                                                    params={'for_po': for_po, 'for_cto': for_cto, 'isActive': True,
                                                            'groups': ['abfe6e2a-b86c-49e2-990b-2d07e6087c31']}))

        actions = self.get_active_actions(rest_internal_client, 'BI_60')['actions']
        for i in actions:
            if i['groupName'] == 'Разработка концепции':
                for ac in i['actions']:
                    if ac['id'] == main_action_id and for_po:
                        assert ac['for_po'], 'Метка для ПО не применилась'
                    if ac['id'] == main_action_id and for_cto:
                        assert ac['for_cto'], 'Метка для СТО не применилась'

        self.delete_action(rest_internal_client, main_action_id)
        with allure.step('Проверяем, что шага по этому айди больше нет'):
            self.get_action_404(rest_internal_client, main_action_id), 'Шаг есть'

    @allure.title('Создание шага с меткой Для PO и проверка его на стр общего ПГ')
    @allure.issue('https://jira.mts.ru/browse/PPI-2907', 'PPInfo - Добавление отметок в шаги PG: PO, Tech lead')
    @pytest.mark.parametrize('for_po', [True, False])
    @pytest.mark.parametrize('for_cto', [False, True])
    def test_action_for_po_and_cto_on_all_pg(self, rest_internal_client, for_po, for_cto):
        with allure.step('Создаем обычный шаг'):
            main_action_id = self.create_action(rest_internal_client,
                                                self.get_guide_data(
                                                    params={'for_po': for_po, 'for_cto': for_cto, 'isActive': True,
                                                            'groups': ['abfe6e2a-b86c-49e2-990b-2d07e6087c31']}))

        actions = self.get_all_steps(rest_internal_client, 'Vneshnii')
        for i in actions:
            if i['groupName'] == 'Разработка концепции':
                for ac in i['actions']:
                    if ac['id'] == main_action_id and for_po:
                        assert ac['for_po'], 'Метка для ПО не применилась'
                    if ac['id'] == main_action_id and for_cto:
                        assert ac['for_cto'], 'Метка для СТО не применилась'

        self.delete_action(rest_internal_client, main_action_id)
        with allure.step('Проверяем, что шага по этому айди больше нет'):
            self.get_action_404(rest_internal_client, main_action_id), 'Шаг есть'

    @allure.title('Создание Вложенного шага с меткой Для PO и проверка его на стр общего ПГ')
    @allure.issue('https://jira.mts.ru/browse/PPI-2907', 'PPInfo - Добавление отметок в шаги PG: PO, Tech lead')
    @pytest.mark.parametrize('for_po', [True, False])
    @pytest.mark.parametrize('for_cto', [False, True])
    def test_sub_action_for_po_and_cto_on_all_pg(self, rest_internal_client, for_po, for_cto):
        main_action, sub_action = self.create_sub_action(rest_internal_client, for_po=True, for_cto=True)
        actions = self.get_all_steps(rest_internal_client, 'Vneshnii')
        for i in actions:
            if i['groupName'] == 'Разработка концепции':
                for ac in i['actions']:
                    if ac['id'] == main_action:
                        assert not ac['for_po'], 'Метка для ПО не применилась'
                        assert not ac['for_cto'], 'Метка для СТО не применилась'
                        for sub_action in ac['subActions']:
                            if sub_action['id'] == sub_action:
                                assert sub_action['for_po'], 'Метка для ПО не применилась'

        self.delete_action(rest_internal_client, main_action)
        with allure.step('Проверяем, что шага по этому айди больше нет'):
            self.get_action_404(rest_internal_client, main_action), 'Шаг есть'

    @allure.title('Создание Вложенного шага с меткой Для PO и проверка его на стр продукта')
    @allure.issue('https://jira.mts.ru/browse/PPI-2907', 'PPInfo - Добавление отметок в шаги PG: PO, Tech lead')
    @pytest.mark.parametrize('for_po', [True, False])
    @pytest.mark.parametrize('for_cto', [False, True])
    def test_sub_action_for_po_and_cto_on_product_page(self, rest_internal_client, for_po, for_cto):
        main_action, sub_action = self.create_sub_action(rest_internal_client, for_po=True, for_cto=True)
        actions = self.get_active_actions(rest_internal_client, 'BI_60')['actions']
        for i in actions:
            if i['groupName'] == 'Разработка концепции':
                for ac in i['actions']:
                    if ac['id'] == main_action:
                        assert not ac['for_po'], 'Метка для ПО не применилась'
                        assert not ac['for_cto'], 'Метка для СТО не применилась'
                        for sub_action in ac['subActions']:
                            if sub_action['id'] == sub_action:
                                assert sub_action['for_po'], 'Метка для ПО не применилась'

        self.delete_action(rest_internal_client, main_action)
        with allure.step('Проверяем, что шага по этому айди больше нет'):
            self.get_action_404(rest_internal_client, main_action), 'Шаг есть'

    @allure.title('Создание Вложенного шага с меткой Для PO и проверка его на стр продукта')
    @allure.issue('https://jira.mts.ru/browse/PPI-2907', 'PPInfo - Добавление отметок в шаги PG: PO, Tech lead')
    @pytest.mark.parametrize('for_po', [True, False])
    @pytest.mark.parametrize('for_cto', [False, True])
    def test_sub_action_for_po_and_cto_only_main_product_page(self, rest_internal_client, for_po, for_cto):
        main_action, sub_action = self.create_sub_action(rest_internal_client)

        self.patch_action(rest_internal_client, main_action,
                          self.get_guide_data({'isActive': True, 'for_cto': for_cto, 'for_po': for_po,
                                               'groups': ['abfe6e2a-b86c-49e2-990b-2d07e6087c31']}))

        actions = self.get_active_actions(rest_internal_client, 'BI_60')['actions']
        for i in actions:
            if i['groupName'] == 'Разработка концепции':
                for ac in i['actions']:
                    if ac['id'] == main_action and for_po:
                        assert ac['for_po'], 'Метка для ПО не применилась'
                        assert not ac['subActions'][0]['for_po']
                    if ac['id'] == main_action and for_cto:
                        assert ac['for_cto'], 'Метка для СТО не применилась'
                        assert not ac['subActions'][0]['for_cto']

        self.delete_action(rest_internal_client, main_action)
        with allure.step('Проверяем, что шага по этому айди больше нет'):
            self.get_action_404(rest_internal_client, main_action), 'Шаг есть'

    @allure.title(
        'Если метка для ПО и метка для СТО стоит у основного шага, то она не должна автоматически применяться к вложенному шагу')
    @allure.issue('https://jira.mts.ru/browse/PPI-2907', 'PPInfo - Добавление отметок в шаги PG: PO, Tech lead')
    @pytest.mark.parametrize('for_po', [True, False])
    @pytest.mark.parametrize('for_cto', [False, True])
    def test_sub_action_for_po_and_cto_only_main_all_pg(self, rest_internal_client, for_po, for_cto):
        main_action, sub_action = self.create_sub_action(rest_internal_client)

        self.patch_action(rest_internal_client, main_action,
                          self.get_guide_data({'isActive': True, 'for_cto': for_cto, 'for_po': for_po,
                                               'groups': ['abfe6e2a-b86c-49e2-990b-2d07e6087c31']}))

        actions = self.get_all_steps(rest_internal_client, 'Vneshnii')
        for i in actions:
            if i['groupName'] == 'Разработка концепции':
                for ac in i['actions']:
                    if ac['id'] == main_action and for_po:
                        assert ac['for_po'], 'Метка для ПО не применилась'
                        assert not ac['subActions'][0]['for_po']
                    if ac['id'] == main_action and for_cto:
                        assert ac['for_cto'], 'Метка для СТО не применилась'
                        assert not ac['subActions'][0]['for_cto']

        self.delete_action(rest_internal_client, main_action)
        with allure.step('Проверяем, что шага по этому айди больше нет'):
            self.get_action_404(rest_internal_client, main_action), 'Шаг есть'

    @allure.title('Создание основного шага с длительностью')
    @allure.issue('https://jira.mts.ru/browse/PPI-3302', 'PPInfo - Отображать длительность шагов в PG')
    @pytest.mark.parametrize('duration', [0, 5, 100, 1000])
    def test_create_action_with_duration(self, rest_internal_client, duration):

        main_action = self.create_action(rest_internal_client,
                                         self.get_guide_data(params={'isActive': True, 'duration': duration}))
        assert self.get_action(rest_internal_client, main_action)['duration'] == duration, 'Изменения не сохранились'

        assert [action['duration'] for action in
                self.get_active_actions(rest_internal_client, 'BI_60')['actions'][-1]['actions'] if
                action['id'] == main_action][0] == duration, 'Длительность шага не передается в ПГ на странице продукта'

        assert [action['duration'] for action in self.get_all_steps(rest_internal_client, 'Vneshnii')[-1]['actions'] if
                action['id'] == main_action][
                   0] == duration, 'Длительность шага не передается в ПГ на страницу общего ПГ'

    @allure.title('Создание вложенного шага с длительностью')
    @allure.issue('https://jira.mts.ru/browse/PPI-3302', 'PPInfo - Отображать длительность шагов в PG')
    @pytest.mark.parametrize('duration', [0, 5, 100, 1000])
    def test_create_sub_action_with_duration(self, rest_internal_client, duration):

        main_action, sub_action = self.create_sub_action(rest_internal_client,
                                                         params={'isActive': True, 'duration': duration})

        for ac in self.get_action(rest_internal_client, main_action)['subActions']:
            if ac['id'] == sub_action:
                assert ac['duration'] == duration, 'Изменения не сохранились'

        for ac in self.get_active_actions(rest_internal_client, 'BI_60')['actions'][-1]['actions']:
            if ac['id'] == sub_action:
                assert ac['duration'] == duration, 'Длительность шага не передается в ПГ на странице продукта'

        for ac in self.get_all_steps(rest_internal_client, 'Vneshnii')[-1]['actions']:
            if ac['id'] == sub_action:
                assert ac['duration'] == duration, 'Длительность шага не передается в ПГ на страницу общего ПГ'

    @allure.title('Создание основного шага с тегами')
    @allure.issue('https://jira.mts.ru/browse/PPI-3304', 'PPInfo - Поиск по тэгам шагов в разделе Product Guide')
    def test_create_action_with_tags(self, rest_internal_client):

        main_action = self.create_action(rest_internal_client,
                                         self.get_guide_data(params={'isActive': True, 'tags': ['тэг 1', 'тег 2']}))
        assert self.get_action(rest_internal_client, main_action)['tags'] == ['тэг 1',
                                                                              'тег 2'], 'Изменения не сохранились'

        assert \
        [action['tags'] for action in self.get_active_actions(rest_internal_client, 'BI_60')['actions'][-1]['actions']
         if
         action['id'] == main_action][0] == ['тэг 1',
                                             'тег 2'], 'Теги шага не передается в ПГ на странице продукта'

        assert [action['tags'] for action in self.get_all_steps(rest_internal_client, 'Vneshnii')[-1]['actions'] if
                action['id'] == main_action][
                   0] == ['тэг 1', 'тег 2'], 'Теги шага не передается в ПГ на страницу общего ПГ'

    @allure.title('Создание вложенного шага с тегами')
    @allure.issue('https://jira.mts.ru/browse/PPI-3304', 'PPInfo - Поиск по тэгам шагов в разделе Product Guide')
    def test_create_sub_action_with_tags(self, rest_internal_client):

        main_action, sub_action = self.create_sub_action(rest_internal_client,
                                                         params={'isActive': True, 'tags': ['тэг 1', 'тег 2']})

        for ac in self.get_action(rest_internal_client, main_action)['subActions']:
            if ac['id'] == sub_action:
                assert ac['tags'] == ['тэг 1', 'тег 2'], 'Изменения не сохранились'

        for ac in self.get_active_actions(rest_internal_client, 'BI_60')['actions'][-1]['actions']:
            if ac['id'] == sub_action:
                assert ac['tags'] == ['тэг 1', 'тег 2'], 'Длительность шага не передается в ПГ на странице продукта'

        for ac in self.get_all_steps(rest_internal_client, 'Vneshnii')[-1]['actions']:
            if ac['id'] == sub_action:
                assert ac['tags'] == ['тэг 1', 'тег 2'], 'Длительность шага не передается в ПГ на страницу общего ПГ'

    @allure.issue('https://jira.mts.ru/browse/PPI-3231',
                  'PPInfo - Иллюстрация процессов шагов PG с помощью схемы процесса')
    @allure.title('Добавление шага с ссылкой на схему')
    @pytest.mark.parametrize('group_id',
                             [['abfe6e2a-b86c-49e2-990b-2d07e6087c31'], ['76ed0eb2-e889-4b2b-80be-60b46007285e'],
                              ['83e92cfe-1257-49f5-80c8-5b953bcdb3a3'], ['3cb9b512-af19-4aca-b2ec-84a4bd1209ed']])
    def test_create_guide_with_schemas(self, rest_internal_client, group_id):
        action_id = self.create_action(rest_internal_client, self.get_guide_data({'schemeLink': 'Ссылка на схему'}))
        with allure.step('Проверяем, что такой шаг создался'):
            assert self.get_action(rest_internal_client, action_id), 'Шаг не создался'

        with allure.step('Проверяем, что файл записался в шаг'):
            assert self.get_action(rest_internal_client, action_id)[
                       "schemeLink"] == 'Ссылка на схему', 'Ссылка не добавилась'

        self.delete_action(rest_internal_client, action_id)
        with allure.step('Проверяем, что шага по этому айди больше нет'):
            self.get_action_404(rest_internal_client, action_id), 'Шаг есть'
