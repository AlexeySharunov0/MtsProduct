import allure
import pytest

from API.models.employee.rest import RestEmployee


@pytest.mark.api
@allure.feature('Юзеры')
class TestRestEmployee(RestEmployee):

    @allure.title('Получение списка доп юзеров')
    def test_get_employee_list(self, user_service_client):
        self.get_employee_list(user_service_client)

    @allure.title('Поиск сотрудников по fullname')
    @pytest.mark.parametrize('limit', ['1', '5', '10'])
    @pytest.mark.parametrize('query', ['Фамилия', 'Иванов', 'Петров', 'Технический'])
    def test_search_employees_by_fullname(self, user_service_client, limit, query):
        params = {'limit': limit, 'query': query}
        result = self.search_employee(user_service_client, params)['users']
        print(result)

        with allure.step('Проверяем, что запрос вернул непустой ответ'):
            assert result, 'Пришел пустой ответ'

        assert all(query.lower() in user['fullName'].lower() for user in
                   result), 'Поисковая выдача не соответствует запросу'

        with allure.step('Проверяем, что количество результатов не превышает limit'):
            assert len(result) <= int(limit), f'Ожидалось не более {limit} результатов, но получили {len(result)}'

    @allure.title('Поиск доп. сотрудников по login')
    @pytest.mark.parametrize('limit', ['1', '5', '10'])
    @pytest.mark.parametrize('query', ['hehehe', 'ddsvetov1', 'aikostrov1'])  # hehehe - доп юзер
    def test_search_employees_by_login(self, user_service_client, limit, query):
        params = {'limit': limit, 'query': query}
        result = self.search_employee(user_service_client, params)['users']

        with allure.step('Проверяем, что запрос вернул непустой ответ'):
            assert result, 'Пришел пустой ответ'

        assert all(query.lower() in user['login'].lower() for user in
                   result), 'Поисковая выдача не соответствует запросу'

        with allure.step('Проверяем, что количество результатов не превышает limit'):
            assert len(result) <= int(limit), f'Ожидалось не более {limit} результатов, но получили {len(result)}'

    @allure.title('Поиск сотрудников с пробелом в начале')
    @allure.issue('https://jira.mts.ru/browse/PPI-2450', 'PPInfo - Обрезать пробелы в начале поиска сотрудников', )
    @pytest.mark.parametrize('query', ['   Светов', ' sa0000ddsvetov1', ' hehehe'])
    def test_search_employees_with_space_in_beginning(self, user_service_client, query):
        params_with_spaces = {'limit': 20, 'query': query}
        params_trimmed = {'limit': 20, 'query': query.strip()}

        with allure.step('Делаем запрос с пробелами в начале'):
            result_with_spaces = self.search_employee(
                user_service_client, params_with_spaces
            )['users']
            assert result_with_spaces, 'Пользователи не нашлись с пробелами в начале'

        with allure.step('Делаем запрос без пробелов в начале'):
            result_trimmed = self.search_employee(user_service_client, params_trimmed)[
                'users'
            ]
            assert result_trimmed, 'Пользователи не нашлись без пробелов'

        with allure.step('Сравниваем результаты двух запросов'):
            assert (
                    result_with_spaces == result_trimmed
            ), 'Результаты поиска с пробелами и без пробелов не совпадают'

    @allure.title('Провеска юр лица у сотрудников')
    @allure.issue('https://jira.mts.ru/browse/PPI-2912',
                  'PPInfo - Отображать юр. лицо при выборе в атрибуте сотрудника', )
    @pytest.mark.parametrize(
        'query, company',
        [
            ('ddsvetov1', 'МВС'),
            ('Светов Даниил Дмитриевич', 'МВС'),
            ('svku', 'МТС'),
            ('Курочкин Сергей', 'МТС'),
        ],
    )
    def test_search_employees_with_tab(self, user_service_client, query, company):
        params = {'limit': 20, 'query': query}
        with allure.step('Проверяем, что пользователи нашлись'):
            assert self.search_employee(user_service_client, params)['users'][0][
                       'company'] == company, 'У пользователя некорректный юр адрес'

    @allure.title('Поиск сотрудников по логину')
    @pytest.mark.parametrize(
        'login',
        [
            'ddsvetov1',
            'aikostrov1',
            'pymaslenkov',
            'sa0000ppinfouser1',
            'o.vorobyeva',
            'user-with.all_signs123',
        ],
    )
    def test_search_employee_by_login(self, user_service_client, login):
        result = self.search_employee_by_login(user_service_client, login)

        with allure.step('Проверяем, что логин в ответе совпадает с искомым'):
            assert result['login'].lower() == login.lower(), f'Ожидался логин {login}, но получен {result["login"]}'

    @allure.title('Поиск сотрудников по несуществующему логину')
    @pytest.mark.parametrize(
        'login', ['1', 'йцуйцуйцуйцк', 'DROP DATABASE', '버그가 없습니다']
    )
    def test_search_employee_by_login_error(self, user_service_client, login):
        self.search_employee_by_login_error(user_service_client, login)

    @allure.title('Проверка совместимости сотрудников при выборе руководителя продукта через поиск')
    @allure.issue('https://jira.mts.ru/browse/PPI-1080', 'PPInfo - Отображать совместительство по сотруднику')
    @pytest.mark.parametrize('query', ['svku', 'iartemova'])
    def test_get_user_in_search_compatibility(self, user_service_client, query):
        params = {'limit': '5', 'query': query}
        result = self.search_employee(user_service_client, params)['users']

        assert all(user['compatibility'] for user in result), "У пользователя не отображается совместительство"

        with allure.step('Проверяем, что количество результатов не превышает limit'):
            assert len(result) <= int(
                params['limit']), f'Ожидалось не более {params["limit"]} результатов, но получили {len(result)}'

    @allure.title('Проверка того, что пользователь уволен')
    @pytest.mark.parametrize('query', ['bachuk', 'oamatveyev'])
    def test_get_user_in_search_fired(self, user_service_client, query):
        result = self.search_employee_by_login(user_service_client, query)
        with allure.step('Проверяем, что пользователь уволен'):
            assert result['isFired']

    @allure.title('Проверка, что уволенные сотрудники не находятся через ФИО')
    @pytest.mark.parametrize('limit', ['10'])
    @pytest.mark.parametrize('query', ['Авраменко Иван Константинович', 'Алешкин Рамиль'])
    def test_search_employees_fired(self, user_service_client, limit, query):
        params = {'limit': limit, 'query': query}
        result = self.search_employee(user_service_client, params)['users']

        with allure.step('Проверяем, что запрос вернул пустой ответ'):
            assert not result, 'Пришел пустой ответ'

    @allure.title('Создание, проверка и удаление доп. юзера')
    def test_create_employee(self, user_service_client):
        test_login = self.text
        data = self.get_user({'login': test_login, 'email': f'{test_login}@mts.ru'})

        self.create_employee(user_service_client, data)
        employee = self.get_employee_by_login(user_service_client, test_login)
        self.delete_employee(user_service_client, test_login)

        with allure.step('Проверяем, что логин в ответе соответствует ожидаемому'):
            assert employee['login'] == test_login, f'Ожидался логин {test_login}, но получен {employee["login"]}'

    @allure.title('Создание доп. юзера с отсутствующим обязательным полем: {missing_field}')
    @pytest.mark.parametrize('missing_field', ['login', 'firstName', 'lastName', 'email'])
    def test_create_employee_missing_required_field(self, user_service_client, missing_field):
        login = self.text
        data = self.get_user({'login': login})
        data[missing_field] = ''
        self.error_create_employee(user_service_client, data)

    @allure.title('Редактирование доп юзера')
    def test_patch_employee(self, user_service_client):
        test_login = self.text
        data = self.get_user({'login': test_login})

        self.create_employee(user_service_client, data)

        with allure.step('Проверяем, что пользователь создался'):
            self.get_employee_by_login(user_service_client, test_login)

        data = self.get_user({'login': test_login, 'firstName': 'qwe1'})

        self.patch_employee(user_service_client, data)

        with allure.step('Проверяем, что пользователь отредактирован'):
            assert self.get_employee_by_login(user_service_client, test_login)['firstName'] == 'qwe1'

        self.delete_employee(user_service_client, test_login)

    @allure.title('Редактирование логина у доп юзера')
    def test_patch_employee_login_error(self, user_service_client):
        test_login = self.text
        data = self.get_user({'login': test_login})

        self.create_employee(user_service_client, data)

        with allure.step('Проверяем, что пользователь создался'):
            self.get_employee_by_login(user_service_client, test_login)

        data = self.get_user({'login': test_login + '1', 'firstName': 'qwe1'})

        self.error_patch_employee(user_service_client, data)

        self.delete_employee(user_service_client, test_login)

    @allure.title('Получение информации о юзере')
    def test_get_user_info(self, user_service_client):
        self.get_user_info(user_service_client)

    @allure.title('Проверка, что возвращаются допустимые типы отсутствия у сотрудников')
    def test_employee_absence_types_are_valid(self, user_service_client):
        valid_types = {'absence', 'vacation', 'businessTrip'}

        logins = self.get_employee_with_absence()


        for login in logins:
            response = self.search_employee_by_login(user_service_client, login)
            type_absence = response['absence']['absenceType']
            assert type_absence in valid_types, f'У сотрудника {login} неверный type_absence: {type_absence}'

    @allure.title('Проверка отображения списка продуктов и ролей сотрудника')
    @allure.issue("https://jira.mts.ru/browse/PPI-4612", "PPInfo - В карточке продукта в Руководстве у сотрудника отображать его роли на других продуктах")
    @pytest.mark.parametrize(
        'test_login',
        [
            'ddsvetov1',
            'pymaslenkov',
            'sa0000ppinfouser2'
        ]
    )
    def test_employee_product_roles_display(self, user_service_client, test_login):
        with allure.step(f'Запрашиваем данные по сотруднику с логином {test_login}'):
            employee_products = self.search_employee_by_login(user_service_client, test_login)['products']


        with allure.step('Проверяем, что список продуктов и ролей существует'):
            assert employee_products, f'В ответе для логина {test_login} отсутствуют данные о продуктах и ролях.'

        with allure.step('Проверяем, что в списке присутствуют только разрешенные роли (CPO, PO, Tech Lead)'):
            allowed_roles = ['CPO', 'PO', 'Tech Lead']

            for item in employee_products:
                product_roles = [role.strip() for role in item['roles'].split(',')]

                for role in product_roles:
                    assert role in allowed_roles, f"Обнаружена недопустимая роль '{role}' для логина {test_login}"

    @allure.title('Проверка порядка ролей (CPO, PO, Tech Lead)')
    @allure.issue("https://jira.mts.ru/browse/PPI-4612","PPInfo - В карточке продукта в Руководстве у сотрудника отображать его роли на других продуктах")
    @pytest.mark.parametrize(
        'test_login',
        [
            'ddsvetov1',
            'sa0000ppinfouser2',
            'pymaslenkov'
        ]
    )
    def test_employee_roles_order(self, user_service_client, test_login):

        with allure.step(f'Запрашиваем данные по сотруднику с логином {test_login}'):
            employee_products = self.search_employee_by_login(user_service_client, test_login)['products']

        assert employee_products, f'В ответе для логина {test_login} нет данных о продуктах.'

        expected_order = ['CPO', 'PO', 'Tech Lead']

        with allure.step('Проверяем, что роли в каждом продукте отсортированы по ожидаемому порядку'):
            for item in employee_products:
                product_roles = [role.strip() for role in item['roles'].split(',')]

                sorted_product_roles = sorted(product_roles, key=lambda role: expected_order.index(role) if role in expected_order else len(expected_order))

                assert product_roles == sorted_product_roles, (
                    f"Роли для продукта '{item['name']}' расположены неверно. "
                    f"Ожидаемый порядок: {sorted_product_roles}, полученный: {product_roles}."
                )
