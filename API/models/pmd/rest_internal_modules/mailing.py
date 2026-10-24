import warnings
from datetime import datetime
from typing import Any

import allure
import openpyxl

from API.models.employee.rest import RestEmployee
from API.models.notification.notification import Notifications
from API.models.ppinfo.product_v2 import ProductV2

warnings.filterwarnings("ignore", message="numpy.dtype size changed")

HOST = 'https://stage.prodboard.example.com'


class MailingUrls:
    """
    https://stage.prodboard.example.com/pmd/swagger/rest/internal/index.html#/
    """

    # MAILING

    # Получение Excel результаты по рассылке
    GET_MAILING_EXCEL = 'v1/mailing/excel'

    # Запуск рассылки по продуктам
    SEND_MAILING = 'v1/mailing/send/{}'

    # Запрос активности кнопки в настройках
    IS_ACTIVE_BUTTON = 'v1/mailing/{}'


class Mailing(MailingUrls, Notifications, ProductV2, RestEmployee):

    @allure.step('Получение Excel результатам по рассылки')
    def get_mailing_excel(self, client) -> openpyxl.Workbook.active:
        """
        Получение Excel результатов по рассылки
        Returns:
            Excel преобразованные в DataFrame
        """
        response = client.get(self.GET_MAILING_EXCEL, raw_format=True)

        with open('filename_excel.xlsx', 'wb') as f:
            f.write(response.content)

        xls = 'filename_excel.xlsx'

        wb = openpyxl.load_workbook(xls)
        sheet = wb.active

        return sheet

    @allure.step('Запуск рассылки')
    def send_mailing(self, client, product_type: str) -> dict[str, Any]:
        """
        Запускает рассылку, как правило, всегда будет не работать, потому что стоит лимит на запуск рассылки (не более 1 раза в 7 дней).
        Returns:
            Ответ от сервера, где можно получить текст ошибки
        """
        skip_limit = {
            'skipLimit': False
        }
        response = client.post(self.SEND_MAILING.format(product_type), json=skip_limit, expected_status_code=400)

        return response

    @allure.step('Запуск рассылки с пропуском лимита')
    def send_mailing_with_skip_limit(self, client, product_type: str) -> None:
        """
        Запускает рассылку с пропуском лимита. Рассылка начнется, даже если она уже запускалась в течение 7 дней
        """
        skip_limit = {
            'skipLimit': True
        }
        client.post(self.SEND_MAILING.format(product_type), json=skip_limit, raw_format=True)

    @allure.step('Получение количества писем, которые поступили на отправку')
    def get_count_mailing(self, client, product_type: str):
        """
        Получение количества писем, которые поступили на отправку
        Returns:
            Количество писем в виде числа
        """
        self.delete_mailing_from_db('pmd')

        self.send_mailing_with_skip_limit(client, product_type)

        self.get_count_mailing_from_db('pmd')

    @allure.step('Получение тела письма по продукту BI_2064')
    def get_body_mailing_bi_2064_from_db(self, client) -> dict[str, Any]:
        """
        Получение тела письма по продукту BI_2064
        Returns:
            Тело письма
        """
        self.delete_mailing_from_db('pmd')

        self.send_mailing_with_skip_limit(client)

        current_message = None
        for message in self.get_bodies_mailing_from_db():
            if 'https://stage.prodboard.example.com/product/BI_2064/main' in str(message):
                current_message = message
                break

        return current_message

    @allure.step('Получение информации о кнопке запуска рассылки в настройках')
    def get_button_info(self, client, product_type: str):
        response = client.get(self.IS_ACTIVE_BUTTON.format(product_type))

        return response

    @allure.step('Получение информации о значение атрибута со странице продукта по его коду')
    def get_value_by_attribute_code_from_product(self, client, product_code: str, attribute_name: str) -> str | list | datetime:
        """
        Получение значения атрибута по его коду со странице продукта
        Args:
            product_code: Код продукта
            attribute_name: Код атрибута
        Returns:
            Значение атрибута
        """
        info_about_product = self.get_info_by_product_code(client, product_code)
        if attribute_name == 'Описание продукта':
            return info_about_product['description']['value']
        elif attribute_name == 'Название продукта':
            return info_about_product['name']['value']
        else:
            for attr in info_about_product['hidingAttributes']:
                if attr['name'] == attribute_name:
                    if attr['values']:
                        if len(attr['values']) == 1 and attr['type'] == 'link':
                            return [value['code'] for value in attr['values']][0]
                        elif len(attr['values']) == 1 and attr['type'] == 'time':
                            return \
                                [datetime.strptime(value['value'], '%Y-%m-%dT%H:%M:%S.%fZ').strftime('%d.%m.%Y') for
                                 value
                                 in attr['values']][0]
                        elif len(attr['values']) == 1:
                            return [value['value'] for value in attr['values']][0]
                        return ', '.join([value['value'] for value in attr['values']])
                    else:
                        return '—'

    @allure.step('Получение ПО и СТО со страници продукта')
    def get_po_and_cto_from_product(self, client, client_ppinfo, product_code: str) -> dict:
        """
        Получение ПО и СТО со страници продукта для соответвия информации с нотификацией
        Args:
            client: Клиент сервиса пользователей
            product_code: Код продукта
        Returns:
            Словарь состоящий из ПО и СТО
        """
        info_about_product = self.get_info_by_product_code(client_ppinfo, product_code)
        result = {}
        for attr in info_about_product['users']:
            if attr['id'] == 'employee_product_owner' and attr['users']:
                try:
                    result.update({'po': self.search_employee_by_login(client, attr['users'][0]['login'])['email']})
                except Exception:
                    pass
                    # result.update({'po': attr['users'][0]['login'] + '@example.com'})
            if attr['id'] == 'employee_tech_lead' and attr['users']:
                try:
                    result.update({'cto': self.search_employee_by_login(client, attr['users'][0]['login'])['email']})
                except Exception:
                    pass
                    # result.update({'cto': attr['users'][0]['login'] + '@example.com'})

        return result

    @allure.step('Проверка легетимности отправки письма по продукту')
    def checking_the_legitimacy_of_sending(self, client_ppinfo, product_code: str) -> bool:
        """
        Получаем на вход код продукта и проверяем, удален ли он, не находится ли он в архиве и не является ли он банковским
        Args:
            product_code: Код продукта
        Returns:
            Если продукт прошел валидацию и не является удаленным/архивным/банковским то возвращаем True, иначе возращаем False
        """
        info_about_product = self.get_info_by_product_code(client_ppinfo, product_code)
        is_deleted = info_about_product['reasonDeletion'] is not None
        is_archived = info_about_product['status']['code'] == '(PPinfo_status)Out_of_use' and \
                      info_about_product['status']['code'] == '(PPinfo_status)Canceled'
        is_bank = False
        for attr in info_about_product['hidingAttributes']:
            if attr['id'] == 'PPinfo_category_product' and attr['values']:
                if attr['values'][0]['code'] == '(PPInfo_category_spravochnik)Bank':
                    is_bank = True

        return not is_deleted and not is_archived and not is_bank
