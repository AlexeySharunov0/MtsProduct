from typing import Any

import allure
import psycopg2

from API.data.employee import EmployeeList, Users, GetUser, Employee, UserLogin
from API.utils.DBcm import UseDataBase
from API.utils.generate import Gen

HOST = 'https://stage.prodboard.example.com'


class RestEmployeeUrls:
    """
    https://stage.prodboard.example.com/user-service/swagger/rest/index.html#/
    """
    # Получение списка доп. сотрудников
    EMPLOYEE_LIST = 'v1/employee'

    # Создание нового доп. сотрудника 
    CREATE_EMPLOYEE = 'v1/employee'

    # Редактирование данных о доп. сотрудниках
    PATCH_EMPLOYEE = 'v1/employee'

    # Получение данных сотрудника по логину
    GET_EMPLOYEE_BY_LOGIN = 'v1/employee/{}'

    # Удаление доп. сотрудника по логину
    DELETE_EMPLOYEE_BY_LOGIN = 'v1/employee/{}'

    # Поиск сотрудников при смене руководства продукта
    SEARCH_EMPLOYEE = 'v1/user/search'

    # Поиск сотрудника по логину в руководстве продукта
    SEARCH_EMPLOYEE_BY_LOGIN = 'v1/user/{}'

    # Получение данных текущего пользователя
    USER = 'v1/user'


class RestEmployee(RestEmployeeUrls):

    @allure.step('Заполняем данные для кастомного пользователя')
    def get_user(self, params: dict[str, str]) -> dict[str, str]:
        data = {'login': 'qwe',
                'firstName': 'qwe',
                'middleName': 'qwe',
                'lastName': 'qwe',
                'position': 'qwe',
                'mobilePhone': 'qwe',
                'internalPhone': 'qwe',
                'email': 'qwe@example.com',
                'department': 'qwe',
                'company': 'qwe',
                'pulseLink': 'qwe'}
        data.update(params)
        return data

    @property
    def text(self) -> str:
        return 'test' + Gen.generate_text(7).replace(' ', '')

    @allure.step('Получение списка доп юзеров')
    def get_employee_list(self, client) -> dict[str, Any]:
        response = client.get(self.EMPLOYEE_LIST)

        EmployeeList(**response)

        return response

    @allure.step('Получение доп юзера по логину')
    def get_employee_by_login(self, client, login: str) -> dict[str, Any]:
        response = client.get(self.GET_EMPLOYEE_BY_LOGIN.format(login))

        Employee(**response)

        return response

    @allure.step('Создание доп юзера')
    def create_employee(self, client, data: dict[str, Any]) -> None:
        client.post(self.CREATE_EMPLOYEE, json=data, raw_format=True)

    @allure.step('Создание доп юзера с ошибкой')
    def error_create_employee(self, client, data: dict[str, Any]) -> None:
        client.post(self.CREATE_EMPLOYEE, json=data, raw_format=True, expected_status_code=400)

    @allure.step('Редактирование доп юзера')
    def patch_employee(self, client, data: dict[str, Any]) -> None:
        client.patch(self.PATCH_EMPLOYEE, json=data, raw_format=True)

    @allure.step('Редактирование доп юзера с ошибкой')
    def error_patch_employee(self, client, data: dict[str, Any]) -> None:
        client.patch(self.PATCH_EMPLOYEE, json=data, raw_format=True, expected_status_code=400)

    @allure.step('Удаление доп юзера')
    def delete_employee(self, client, login: str) -> None:
        client.delete(self.DELETE_EMPLOYEE_BY_LOGIN.format(login))

    @allure.step('Поиск сотрудников')
    def search_employee(self, client, params: dict[str, Any]) -> dict[str, Any]:
        response = client.get(self.SEARCH_EMPLOYEE, params=params)

        Users(**response)

        return response

    @allure.step('Поиск сотрудников по логину')
    def search_employee_by_login(self, client, login: str) -> dict[str, Any]:
        response = client.get(self.SEARCH_EMPLOYEE_BY_LOGIN.format(login))

        UserLogin(**response)

        return response

    @allure.step('Поиск сотрудников по несуществующему логину')
    def search_employee_by_login_error(self, client, login: str):
        client.get(self.SEARCH_EMPLOYEE_BY_LOGIN.format(login), raw_format=True, expected_status_code=404)

    @allure.step('Получение инфы о юзере')
    def get_user_info(self, client) -> dict[str, Any]:
        with allure.step('Получаем инфу о юзере'):
            response = client.get(self.USER)
            GetUser(**response)
            return response

    @allure.step('Получение логинов пользователей с причиной отсутствия')
    def get_employee_with_absence(self) -> list[str]:

        with UseDataBase() as cursor:
            try:
                cursor.execute("""SELECT login, first_name, last_name, middle_name, cluster, is_fired, email, type_absence, date_end_absence
                                    FROM pmd.employee
                                    where type_absence IS NOT NULL""")
                return [product[0] for product in cursor.fetchall()]
            except psycopg2.OperationalError as e:
                print('Не удалось выполнить запрос', e)
