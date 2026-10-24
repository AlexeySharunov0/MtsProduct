import warnings

import allure
import pytest

from API.models.pmd.rest_internal_modules.curators import Curators

warnings.filterwarnings('ignore', message='numpy.dtype size changed')


### CURATORS
@pytest.mark.api
@allure.feature('Кураторы')
@allure.issue('https://jira.mts.ru/browse/PPI-2523',
              'PPInfo - Backend - Создать API для раздела "Кураторы по кластерам"')
class TestCurators(Curators):
    @allure.title('Получение списка всех атрибутов типа Вычисляемый сотрудник')
    def test_get_all_curator_attributes(self, rest_internal_client):
        assert all(i for i in self.get_all_curator_attributes(rest_internal_client)), 'Пустой ответ'

    @allure.title('Получение всех кураторов по id')
    @pytest.mark.parametrize('attr_id',
                             ['83adfce2-5067-4196-b8ce-1f347a2fd1e9', '817de6f9-19b2-4cea-af9a-1ad48d439ed1'])
    def test_get_all_curator_attributes(self, rest_internal_client, attr_id):
        curator_list = self.get_all_curators_by_id(rest_internal_client, attr_id)
        with allure.step('Проверяем, что кластера пришли'):
            assert curator_list, 'Пустой ответ'

        with allure.step('Проверяем, что есть хотя бы один сотрудник'):
            assert any(i['curators'] for i in curator_list), f'В атрибуте {attr_id} нет ни одного сотрудника'

    @allure.title('Получение всех кураторов по невалидному id')
    @pytest.mark.parametrize('attr_id', ['12345', 'привет'])
    def test_get_all_curator_attributes_by_invalid_id(self, rest_internal_client, attr_id):
        self.get_all_curators_by_id_invalid(rest_internal_client, attr_id)

    @allure.title('Добавление кураторов в атрибут с мультивыбором')
    @pytest.mark.parametrize('login',
                             ['ddsvetov1', 'bachuk', ['asnikiforov1', 'ddsvetov1']])
    @pytest.mark.parametrize('value_id',
                             ['ac8cc879-4240-4108-ba0f-ebefb6190c6a', '518db5ba-3c31-4472-a2ca-adb4462dfeb4',
                              '6c88211f-8833-42e8-8eb1-4ec6916f6201'])
    def test_add_curator_multi(self, rest_internal_client, login, value_id):
        with allure.step('Добавляем сотрудника'):
            response = self.change_curators(rest_internal_client, login,
                                            attribute_id='83adfce2-5067-4196-b8ce-1f347a2fd1e9',
                                            value_id=value_id)
        with allure.step('Проверяем, что сотрудники изменились'):
            required_curators = [i['curators'] for i in response if i['valueID'] == value_id][0]
            required_logins = [i['login'] for i in required_curators]

            assert all(i in login or i == login for i in required_logins), 'Изменения не применились'

    @allure.title('Удаление кураторов в атрибуте с мультивыбором')
    @pytest.mark.parametrize('value_id',
                             ['69f0835d-23bb-444c-9461-8d901fa06418', '518db5ba-3c31-4472-a2ca-adb4462dfeb4',
                              '6c88211f-8833-42e8-8eb1-4ec6916f6201'])
    def test_delete_curator_multi(self, rest_internal_client, value_id):
        with allure.step('Добавляем сотрудника'):
            self.change_curators(rest_internal_client, 'asnikiforov1',
                                 attribute_id='83adfce2-5067-4196-b8ce-1f347a2fd1e9',
                                 value_id=value_id)

        with allure.step('Удаляем сотрудника'):
            response = self.change_curators(rest_internal_client, [],
                                            attribute_id='83adfce2-5067-4196-b8ce-1f347a2fd1e9',
                                            value_id=value_id)

        with allure.step('Проверяем, что сотрудники удалились'):
            assert not [i['curators'] for i in response if i['valueID'] == value_id][0], 'Сотрудники не удалились'

    @allure.title('Добавление куратора в атрибут с единичным выбором')
    @pytest.mark.parametrize('login',
                             ['ddsvetov1', 'bachuk'])
    @pytest.mark.parametrize('value_id',
                             ['ac8cc879-4240-4108-ba0f-ebefb6190c6a', '518db5ba-3c31-4472-a2ca-adb4462dfeb4',
                              '6c88211f-8833-42e8-8eb1-4ec6916f6201'])
    def test_add_curator_only(self, rest_internal_client, login, value_id):
        with allure.step('Добавляем сотрудника'):
            response = self.change_curators(rest_internal_client, login,
                                            attribute_id='817de6f9-19b2-4cea-af9a-1ad48d439ed1',
                                            value_id=value_id)
        with allure.step('Проверяем, что сотрудники изменились'):
            required_curators = [i['curators'] for i in response if i['valueID'] == value_id][0]
            required_logins = [i['login'] for i in required_curators]

            assert all(i in login or i == login for i in required_logins), 'Изменения не применились'

    @allure.title('Удаление куратора в атрибуте с единичным выбором')
    @pytest.mark.parametrize('value_id',
                             ['ac8cc879-4240-4108-ba0f-ebefb6190c6a', '518db5ba-3c31-4472-a2ca-adb4462dfeb4',
                              '6c88211f-8833-42e8-8eb1-4ec6916f6201'])
    def test_delete_curator_only(self, rest_internal_client, value_id):
        with allure.step('Добавляем сотрудника'):
            self.change_curators(rest_internal_client, 'asnikiforov1',
                                 attribute_id='817de6f9-19b2-4cea-af9a-1ad48d439ed1',
                                 value_id=value_id)

        with allure.step('Удаляем сотрудника'):
            response = self.change_curators(rest_internal_client, [],
                                            attribute_id='817de6f9-19b2-4cea-af9a-1ad48d439ed1',
                                            value_id=value_id)

        with allure.step('Проверяем, что сотрудники удалились'):
            assert not [i['curators'] for i in response if i['valueID'] == value_id][0], 'Сотрудники не удалились'

    @allure.title('Невалидное добавление нескольких кураторов в атрибут с единичным выбором')
    @pytest.mark.skip('Вроде как сказал что кураторы не могут быть единичными атрибутами, только множественными')
    @pytest.mark.parametrize('value_id',
                             ['ac8cc879-4240-4108-ba0f-ebefb6190c6a', '518db5ba-3c31-4472-a2ca-adb4462dfeb4',
                              '6c88211f-8833-42e8-8eb1-4ec6916f6201'])
    def test_add_curator_only_invalid(self, rest_internal_client, value_id):
        with allure.step('Добавляем сотрудника'):
            self.change_curators_invalid(rest_internal_client, ['asnikiforov1', 'ddsvetov1'],
                                         attribute_id='817de6f9-19b2-4cea-af9a-1ad48d439ed1',
                                         value_id=value_id)

    @allure.title('Невалидное добавление куратора в несуществующий кластер')
    @pytest.mark.parametrize('value_id',
                             ['привет', '123',
                              '6c88211f-8833-42e8-8eb1-4ec6916o6201'])
    def test_add_curator_invalid_id(self, rest_internal_client, value_id):
        with allure.step('Добавляем сотрудника'):
            self.change_curators_invalid(rest_internal_client, 'asnikiforov1',
                                         attribute_id='817de6f9-19b2-4cea-af9a-1ad48d439ed1',
                                         value_id=value_id)

    @allure.title('Невалидное добавление куратора в несуществующий атрибут')
    @pytest.mark.parametrize('attr_id',
                             ['привет', '123',
                              '6c88211f-8833-42e8-8eb1-4ec6916o6201'])
    def test_add_curator_invalid_attr_id(self, rest_internal_client, attr_id):
        with allure.step('Добавляем сотрудника'):
            self.change_curators_invalid(rest_internal_client, 'asnikiforov1',
                                         attribute_id=attr_id,
                                         value_id='6c88211f-8833-42e8-8eb1-4ec6916f6201')

    @allure.title('Проверяем, что изменение одного кластера не влияет на другие')
    @pytest.mark.parametrize('attr_id',
                             ['817de6f9-19b2-4cea-af9a-1ad48d439ed1', '83adfce2-5067-4196-b8ce-1f347a2fd1e9'])
    def test_clusters_no_affect(self, rest_internal_client, attr_id):
        clusters_before = self.get_all_curators_by_id(rest_internal_client, attr_id)
        clusters_after = self.change_curators(rest_internal_client, 'asnikiforov1',
                                              attribute_id=attr_id,
                                              value_id='69f0835d-23bb-444c-9461-8d901fa06418')
        assert clusters_after[1:] == clusters_before[1:], 'Кластеры, которые не менялись изменились'

    @allure.title('Проверяем, что изменение одного атрибута не влияет на другие')
    @pytest.mark.parametrize(['attr_1', 'attr_2'],
                             [['817de6f9-19b2-4cea-af9a-1ad48d439ed1', '83adfce2-5067-4196-b8ce-1f347a2fd1e9'],
                              ['83adfce2-5067-4196-b8ce-1f347a2fd1e9', '817de6f9-19b2-4cea-af9a-1ad48d439ed1']])
    def test_attributes_curators_no_affect(self, rest_internal_client, attr_1, attr_2):
        attribute_first = self.change_curators(rest_internal_client, 'asnikiforov1',
                                               attribute_id=attr_1,
                                               value_id='69f0835d-23bb-444c-9461-8d901fa06418')
        attribute_second = self.change_curators(rest_internal_client, 'ddsvetov1',
                                                attribute_id=attr_2,
                                                value_id='69f0835d-23bb-444c-9461-8d901fa06418')

        with allure.step('Проверяем, что в первом атрибуте непустой кластер'):
            assert attribute_first[0]['curators'], 'В первом атрибуте пропали сотрудники'

        with allure.step('Проверяем, что во втором атрибуте непустой кластер'):
            assert attribute_second[0]['curators'], 'Во втором атрибуте пропали сотрудники'

        with allure.step('Проверяем, что в атрибутах разные кластера'):
            assert attribute_first[0] != attribute_second[1], 'У атрибутов одинаковые кластера'

    @allure.title('В иксель по кураторам указаны все кластера')
    @allure.issue('https://jira.mts.ru/browse/PPI-2862', 'PPInfo - Выгрузка кураторов в Excel')
    def test_count_clusters_in_excel(self, rest_internal_client, clear_excel):

        clusters = self.get_all_curators_by_id(rest_internal_client, 'd5bd183d-28d7-46a0-8422-69c2830015c1')
        clusters_names = [i['name'] for i in clusters if i['isActive']]

        ex = self.get_curators_excel(rest_internal_client)
        clusters_names_from_excel = []
        for row in ex.iter_cols(min_row=2, min_col=2, max_col=2, max_row=ex.max_row):
            for cell in row:
                clusters_names_from_excel.append(cell.value)

        assert len(clusters_names) == len(
            set(clusters_names_from_excel)), 'Количество кластеров в икселе и на странице сайта не совпадает'

    @allure.title('В иксель по кураторам указаны все атрибуты с типом куратор')
    @allure.issue('https://jira.mts.ru/browse/PPI-2862', 'PPInfo - Выгрузка кураторов в Excel')
    def test_count_curators_in_excel(self, rest_internal_client, clear_excel):

        curators = self.get_all_curator_attributes(rest_internal_client)
        curators_names = [i['name'] for i in curators]

        ex = self.get_curators_excel(rest_internal_client)
        curators_names_from_excel = []
        for row in ex.iter_cols(min_row=2, min_col=1, max_col=1, max_row=ex.max_row):
            for cell in row:
                curators_names_from_excel.append(cell.value)

        assert len(curators_names) == len(
            set(curators_names_from_excel)), 'Количество кураторов в икселе и на странице сайта не совпадает'

    @allure.title('Столбец ФИО и email не пустые')
    @allure.issue('https://jira.mts.ru/browse/PPI-2862', 'PPInfo - Выгрузка кураторов в Excel')
    def test_fio_column_not_empty(self, rest_internal_client, clear_excel):

        ex = self.get_curators_excel(rest_internal_client)

        fio = []

        for row in ex.iter_cols(min_row=2, min_col=3, max_col=4, max_row=ex.max_row):
            for cell in row:
                if cell.value not in (None, ' '):
                    fio.append(cell.value)

        assert len(fio) >= 2, 'Столбец ФИО и email не пустые'

        assert len(fio) % 2 == 0, 'Кол-во ФИО соответствует кол-ву email'
