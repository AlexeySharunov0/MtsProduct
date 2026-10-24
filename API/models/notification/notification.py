import json
import time
from typing import Dict, Any
from urllib.parse import urljoin

import allure
import psycopg2
import requests
from psycopg2 import DatabaseError

from API.models.delegation.delegation import Delegation
from API.models.pmd.internal_product_v1 import InternalV1Product
from API.models.ppinfo.brief import Brief
from API.utils.DBcm import UseDataBase
from API.utils.generate import Gen
from API.utils.headers import mailhog_headers
from API.utils.helpers import assert_status_code

headers = mailhog_headers

MAILHOG_HOST = "https://mailhog-stage.prodboard.example.com"


class MailHogUrls:
    MESSAGES = urljoin(MAILHOG_HOST, "/api/v2/messages")

    MESSAGE_BY_ID = urljoin(MAILHOG_HOST, "/api/v1/messages/{}")

    DELETE = urljoin(MAILHOG_HOST, "/api/v1/messages/")

    SEARCH = urljoin(MAILHOG_HOST, '/api/v2/search')


class Notifications(MailHogUrls, Brief, Delegation, InternalV1Product):
    params_mail = dict(headers=headers, verify=False, timeout=20)

    @property
    def text(self) -> str:
        return Gen.generate_text(7) + 'test'

    @allure.step("Получаем body для заявки на создание продукта")
    def get_body_for_brief_creation(self, product_type: str, name: str, notification: bool = True,
                                    status: str = 'Arkhiv') -> Dict[str, Any]:
        with allure.step(f"Создаем {product_type} продукт"):
            if product_type == "external":
                data = {
                    "type": "createProduct",
                    "data":
                        "{\"name\":"
                        f"\"{name}\","
                        "\"description\":\"qweqweqwe\",\"attributes\":[{\"id\":\"PPinfo_status\",\"values\":[{"
                        f"\"code\":\"{status}\","
                        f"\"value\":\"{self.get_statuses()[status]}\""
                        "}]},{\"id\":\"PPinfo_web_app\",\"values\":[{\"code\":\"(PPinfo_spravochnik_webapp)WEBNO\",\"value\":\"App\"}]},{\"id\":\"PPInfo_product_block\",\"values\":[{\"code\":\"(PPInfo_spravochniK_block)AI_block\",\"value\":\"AI\"}]},{\"id\":\"PPinfo_MTS_Brand\",\"values\":[{\"code\":\"(PPinfo_MTSBrand)MTSBrand_yes\",\"value\":\"Да\"}]},{\"id\":\"PPinfo_mvp\",\"values\":[{\"code\":\"(PPinfo_mvp)MVPYes\",\"value\":\"Да\"}]},{\"id\":\"PPinfo_resolution\",\"values\":[{\"value\":\"qweqweqwe\",\"code\":\"qweqweqwe\"}]},{\"id\":\"PPInfo_type_develop\",\"values\":[{\"code\":\"(PPInfo_spravoch_type)Vendor\",\"value\":\"Вендорская\"}]},{\"id\":\"employee_product_owner\",\"values\":[{\"code\":\"service_user\",\"value\":\"Технический Админ Сергеевич\"}]},{\"id\":\"PPinfo_konkurent\",\"values\":[{\"value\":\"qweqwe\",\"code\":\"qweqwe\"}]},{\"id\":\"PPInfo_Monetization\",\"values\":[{\"value\":\"qweqwe\",\"code\":\"qweqwe\"}]},{\"id\":\"PPinfo_product_problem\",\"values\":[{\"value\":\"qweqweqwe\",\"code\":\"qweqweqwe\"}]},{\"id\":\"PPinfo_product_aim\",\"values\":[{\"value\":\"qweqweqwe\",\"code\":\"qweqweqwe\"}]},{\"id\":\"PPinfo_market_sign\",\"values\":[{\"code\":\"(PPinfo_market_sign)MS_yes\",\"value\":\"Есть товарный знак\"}]},{\"id\":\"PPinfo_values\",\"values\":[{\"value\":\"qweqweqwe\",\"code\":\"qweqweqwe\"}]},{\"id\":\"PPinfo_category_product\",\"values\":[{\"code\":\"(PPInfo_category_spravochnik)Other\",\"value\":\"Другое\"}]},{\"id\":\"PPinfo_market\",\"values\":[{\"code\":\"(PPinfo_market)B2B\",\"value\":\"B2B\"},{\"code\":\"(PPinfo_market)B2C\",\"value\":\"B2C\"}]}],\"type\":\"Vneshnii\"}"
                }
            else:
                data = {
                    "type": "createProduct",
                    "data":
                        "{\"name\":"
                        f"\"{name}\","
                        "\"description\":\"sadfasdf\",\"attributes\":[{\"id\":\"PPinfo_status\",\"values\":[{"
                        f"\"code\":\"{status}\","
                        f"\"value\":\"{self.get_statuses()[status]}\""
                        "}]},{\"id\":\"employee_product_owner\",\"values\":[{\"code\":\"service_user\",\"value\":\"Технический Админ Сергеевич\"}]},{\"id\":\"PPinfo_web_app\",\"values\":[{\"code\":\"(PPinfo_spravochnik_webapp)WEBNO\",\"value\":\"App\"}]},{\"id\":\"PPInfo_type_develop\",\"values\":[{\"code\":\"(PPInfo_spravoch_type)Vendor\",\"value\":\"Вендорская\"}]},{\"id\":\"PPinfo_fix_HFM\",\"values\":[{\"code\":\"(PPinfo_Fix_HFM_voc)PPInfo_Fix_HFM\",\"value\":\"FIX\"}]}],\"type\":\"Vnutrennii\"}"
                }
            if notification:
                data["data"] = data["data"][:-1] + ",\"notification\": true}"
            return data

    @allure.step("Получаем body для заявки на создание продукта со всеми ролями")
    def get_body_for_brief_all_roles(self, name: str, notification: bool = True) -> Dict[str, Any]:
        data = {
            "type": "createProduct",
            "data":
                "{\"name\":"
                f"\"{name}\","
                "\"description\":\"qweqweqwe\",\"attributes\":[{\"id\": \"PPinfo_status\", \"values\": [{\"code\": \"Arkhiv\", \"value\": \"Архив\"}]}, {\"id\": \"employee_product_owner\", \"values\": [{\"code\": \"zimina\", \"value\": \"Зимина Ольга Николаевна\", \"compatibility\": true}]}, {\"id\": \"employee_business_owner\", \"values\": [{\"code\": \"milapshin2\", \"value\": \"Лапшин Максим Игоревич\", \"compatibility\": false}]}, {\"id\": \"employee_tech_lead\", \"values\": [{\"code\": \"aastrunin\", \"value\": \"Струнина Анна Александровна\", \"compatibility\": false}]}, {\"id\": \"employee_chief_PO\", \"values\": [{\"code\": \"nolesnikov\", \"value\": \"Лесникова Наталья Олеговна\", \"compatibility\": false}]}, {\"id\": \"PPinfo_category_product\", \"values\": [{\"code\": \"(PPInfo_category_spravochnik)Other\", \"value\": \"Другое\"}]}, {\"id\": \"employee_sponsor\", \"values\": [{\"code\": \"mifadeeva\", \"value\": \"Фадеева Мария Ивановна\", \"compatibility\": false}]}], \"type\":\"Vneshnii\"}"
        }
        if notification:
            data["data"] = data["data"][:-1] + ",\"notification\": true}"
        return data

    @allure.step("Получаем body для заявки на редактирование продукта")
    def get_body_for_brief_update(self, notification: bool = True) -> Dict[str, Any]:
        description = self.text
        data = {
            "type": "updateProduct",
            "data": "{\"id\":\"BI_22315\",\"attributes\":[{\"id\":\"Identifikator_SOL\",\"values\":[{\"code\":\"777\",\"value\":\"777\"}]}],"
                    f"\"description\":\"{description}\"}}"
        }
        if notification:
            data["data"] = data["data"][:-1] + ",\"notification\": true}"
        return data

    @allure.step("Получаем body для заявки на редактирование продукта иниц.закрытие")
    def get_body_for_brief_update_start_close(self, notification: bool = True) -> Dict[str, Any]:
        data = {
            "type": "updateProduct",
            "data": "{\"id\":\"BI_22315\",\"attributes\":[{\"id\":\"PPinfo_start_close\",\"values\":[{\"code\":\"(PPinfo_spravochnik_start_close)Yes\",\"value\":\"Да\"}]}]}"
        }
        if notification:
            data["data"] = data["data"][:-1] + ",\"notification\": true}"
        return data

    @allure.step("Получаем body для заявки на редактирование продукта кастомная группа")
    def get_body_for_brief_update_custom(self, notification: bool = True) -> Dict[str, Any]:
        data = {
            "type": "updateProduct",
            "data": "{\"id\":\"BI_9855\",\"attributes\":[{\"id\":\"Identifikator_SOL\",\"values\":[{\"code\":\"777\",\"value\":\"777\"}]}]}"
        }
        if notification:
            data["data"] = data["data"][:-1] + ",\"notification\": true}"
        return data

    @allure.step("Получение даты для заявки с документом")
    def get_data_for_doc_brief(self, notification: bool = True) -> Dict[str, Any]:
        data = {
            'data': '{"name":"test_brief","description":"","accessType":"public","code":"BI_22315","productId":"BI_22315","type":"document"}',
            'type': 'addDocument'
        }

        if notification:
            data["data"] = data["data"][:-1] + ",\"notification\": true}"
        return data

    @allure.step("Получение даты для создания продукта со всеми ролями")
    def get_data_all_roles(self, name: str, product_type: str, notification: bool = True) -> Dict[str, Any]:
        return {
            "name": name or self.text,
            "description": "i'll be deleted :(",
            "attributes": [
                {
                    "id": "PPinfo_status",
                    "values": [
                        {
                            "value": "Arkhiv"
                        }
                    ]
                },
                {
                    "id": "PPinfo_category_product",
                    "values": [
                        {
                            "value": "(PPInfo_category_spravochnik)Other"
                        }
                    ]
                },
                {
                    "id": "employee_product_owner",
                    "values": [
                        {
                            "value": "Зимина Ольга Николаевна (zimina)",
                            'code': "zimina"
                        }
                    ]
                },
                {
                    "id": "employee_business_owner",
                    "values": [
                        {
                            "value": "Лапшин Максим Игоревич (milapshin2)",
                            'code': "milapshin2"
                        }
                    ]
                },
                {
                    "id": "employee_tech_lead",
                    "values": [
                        {
                            "value": "Струнина Анна Александровна (aastrunin)",
                            'code': "aastrunin"
                        }
                    ]
                },
                {
                    "id": "employee_chief_PO",
                    "values": [
                        {
                            "value": "Лесникова Наталья Олеговна (nolesnikov)",
                            'code': "nolesnikov"
                        }
                    ]
                },
                {
                    "id": "employee_sponsor",
                    "values": [
                        {
                            "value": "Фадеева Мария Ивановна (mifadeeva)",
                            'code': "mifadeeva"
                        }
                    ]
                }
            ],
            "type": product_type,
            "notification": notification
        }

    @allure.step("Получение даты для заявки с документом")
    def get_data_for_admin_update(self, notification: bool = True, start_close: bool = False,
                                  product_code: str = 'BI_22315') -> Dict[str, Any]:
        data = {"id": product_code,
                "attributes": [{"id": "Identifikator_SOL", "values": [{"code": "777", "value": "777"}]}],
                'notification': notification,
                'type': ''}
        if start_close:
            data.update({'attributes': [{'id': "PPinfo_start_close",
                                         'values': [{'code': "(PPinfo_spravochnik_start_close)Yes", 'value': "Да"}]}]})
        return data

    def get_statuses(self) -> Dict[str, Any]:
        statuses = {
            'Arkhiv': 'Архив',
            '(PPinfo_status)In_use': 'Запущен в КЭ',
            '(PPinfo_status)Waiting_decision': 'Ожидание решения',
            '(PPinfo_status)Pilot': 'Пилот',
            '(PPinfo_status)In_progress': 'Разработка',
            '(PPinfo_status)Idea_formation': 'Формирование идеи'
        }
        return statuses

    @allure.step("Получение даты для изменения статуса")
    def get_data_for_admin_update_status(self, product_type, status_attribute_code: str) -> Dict[str, Any]:

        data = {
            "id": "BI_2875" if product_type == 'Vneshnii' else "BI_2929",
            "attributes": [
                {
                    "id": "PPinfo_status",
                    "values": [
                        {
                            "code": status_attribute_code,
                            "value": self.get_statuses()[status_attribute_code]
                        }
                    ]
                }
            ],
            "notification": True,
            "type": product_type
        }
        return data

    @allure.step("Получение даты для изменения статуса")
    def get_data_for_user_update_status(self, status_attribute_code: str, product_type: str) -> Dict[str, Any]:

        data = {
            "type": "updateProduct",
            "data": json.dumps({
                "id": "BI_2875" if product_type == 'Vneshnii' else "BI_2929",
                "attributes": [
                    {
                        "id": "PPinfo_status",
                        "values": [
                            {
                                "code": status_attribute_code,
                                "value": self.get_statuses()[status_attribute_code]
                            }
                        ]
                    }
                ]
            })
        }
        return data

    @allure.step('Получение даты для нотификации по кураторам')
    def get_data_for_curator(self, values: list, product_code: str = 'BI_22315') -> Dict[str, Any]:
        data = {"id": product_code,
                "attributes": [{"id": "INTEGRATION_Cluster",
                                "values": [{"code": values[0], "value": values[1]}] if values else []}] or [],
                'notification': True,
                'type': 'Vnutrennii'}
        return data

    @allure.step('Получение даты для нотификации по смене руководителя')
    def get_data_for_change_po(self, po: str, product_code: str = 'BI_22315') -> Dict[str, Any]:

        ivanova = {"code": "aaivanov23", "value": "Иванов Александр Александрович", "compatibility": False,
                   "company": "МТС"}

        zimina = {"code": "zimina", "value": "Зимина Ольга Николаевна", "compatibility": True, "company": "МТС"}

        data = {"id": product_code,
                "attributes": [{"id": "employee_product_owner",
                                "values": [ivanova if po.lower() == 'иванова' else zimina]}], "notification": True,
                "type": "Vnutrennii"}
        return data

    @allure.step("Очищаем почту")
    def delete_all_messages(self) -> None:
        response = requests.delete(self.DELETE, **self.params_mail)

        assert_status_code(response)

    @allure.step("Удаляем продукт")
    def delete_product_notification(self, client_delete, client_brief, brief_id: str) -> None:
        product_code = self.get_brief_by_id(client_brief, brief_id=brief_id)['data'][8:17]
        self.delete_product(client_delete, bi=product_code)

    @allure.title("Включаем/Отключаем атрибут в настройках")
    def change_attr_in_settings(self, client, enable: bool) -> None:
        for tag in ['cpoSender', 'poSender', 'ctoSender']:
            if enable:
                try:
                    self.add_attr(client, 'EXTRA_ProductDescription', tag)
                    self.add_attr(client, "Identifikator_SOL", tag)
                    self.add_attr(client, "PPInfo_Doc_Public", tag)
                    self.add_attr(client, "PPInfo_Doc_ByChannel", tag)
                except AssertionError:
                    pass
            else:
                try:
                    self.delete_attr(client, 'EXTRA_ProductDescription', tag)
                    self.delete_attr(client, tag, "Identifikator_SOL")
                    self.delete_attr(client, tag, "PPInfo_Doc_Public")
                    self.delete_attr(client, tag, "PPInfo_Doc_ByChannel")
                except AssertionError:
                    pass

    @allure.title("Устанавливаем дефолтные настройки")
    def set_default_settings(self, client):

        # админ - pymaslenkov@example.com
        users = self.get_tag_info(client, 'PoolSender')['users']
        for user in users:
            self.delete_user(client, 'PoolSender', user['login'])
        self.add_user(client, {'login': 'pymaslenkov', 'tagId': 'PoolSender', 'type': 'user'})

        # внешний продукт - svkurochkin@example.com
        users = self.get_tag_info(client, 'CreateProductCommercial')['users']
        for user in users:
            self.delete_user(client, 'CreateProductCommercial', user['login'])
        self.add_user(client, {'login': 'svkurochkin', 'tagId': 'CreateProductCommercial', 'type': 'user'})

        # внутренний продукт - itismailov@example.com
        users = self.get_tag_info(client, 'CreateProductInternal')['users']
        for user in users:
            self.delete_user(client, 'CreateProductInternal', user['login'])
        self.add_user(client, {'login': 'itismailov', 'tagId': 'CreateProductInternal', 'type': 'user'})

        # иниц закрытие - sskopytin@example.com, ysgurkov1@example.com
        users = self.get_tag_info(client, 'closeProductCommercial')['users']
        for user in users:
            self.delete_user(client, 'closeProductCommercial', user['login'])
        self.add_user(client, {'login': 'sskopytin', 'tagId': 'closeProductCommercial', 'type': 'user'})
        self.add_user(client, {'login': 'ysgurkov1', 'tagId': 'closeProductCommercial', 'type': 'user'})

        # уведомления о создании для руководства
        for attr_id in ['employee_sponsor', 'employee_business_owner', 'employee_tech_lead', 'employee_chief_PO',
                        'employee_product_owner']:
            try:
                self.add_attr(client, attr_id, "CreateProductOwner")
            except AssertionError:
                pass

        # информирование о редактировании для руководства
        for tag in ['cpoSender', 'poSender', 'ctoSender']:
            try:
                self.add_attr(client, "Identifikator_SOL", tag)
                self.add_attr(client, "PPInfo_Doc_Public", tag)
                self.add_attr(client, "PPInfo_Doc_ByChannel", tag)
            except AssertionError:
                pass

        # кастомная группа
        users = self.get_tag_info(client, '1eaab495-95b7-4d97-b315-6fc3ec7b24a3')['users']
        for user in users:
            self.delete_user(client, '1eaab495-95b7-4d97-b315-6fc3ec7b24a3', user['login'])
        self.add_user(client, {'login': 'snkondratyev', 'tagId': '1eaab495-95b7-4d97-b315-6fc3ec7b24a3', 'type': 'user'})

        for tag in ['ec71dbdf-442f-4853-a7e4-8580a80485f1', 'f81359b8-b03c-4e90-9f1d-74674163f12a']:
            try:
                self.add_attr(client, "Identifikator_SOL", tag)
                self.add_attr(client, "PPInfo_Doc_Public", tag)
                self.add_attr(client, "PPInfo_Doc_ByChannel", tag)
            except AssertionError:
                pass

    @allure.step('Удаление рассылки из базы данных')
    def delete_mailing_from_db(self, database: str) -> None:
        """
        Удаление всех сообщений о письмах из базы данных
        """
        query_config = {
            'pmd': 'delete from pmd.message_outbox',
            'ntf': 'delete from ntf.email_history',
            'pb': 'delete from pb.message_outbox'
        }

        if database not in query_config:
            raise ValueError(f"Неизвестная база данных: {database}")

        query = query_config[database]

        try:
            with UseDataBase(database) as cursor:
                cursor.execute(query)
        except psycopg2.OperationalError as e:
            raise DatabaseError(f"Не удалось выполнить запрос для базы данных {database}: {e}")

    @allure.step('Получение количества писем, которые поступили на отправку из базы данных')
    def get_count_mailing_from_db(self, database: str) -> int:
        """
        Получение количества писем, которые поступили на отправку.

        Args:
            database: Название базы данных для выполнения запроса.

        Returns:
            Количество писем в виде числа.

        Raises:
            ValueError: Если передано неизвестное название базы данных.
            DatabaseError: Если не удалось выполнить запрос к базе данных.
        """
        query_config = {
            'pmd': 'SELECT * FROM pmd.message_outbox',
            'ntf': 'SELECT * FROM ntf.email_history',
            'pb': 'SELECT * FROM pb.message_outbox'
        }
        if database == 'ntf':
            time.sleep(15)

        if database not in query_config:
            raise ValueError(f"Неизвестная база данных: {database}")

        query = query_config[database]

        try:
            with UseDataBase(database) as cursor:
                cursor.execute(query)
                return len(cursor.fetchall())
        except psycopg2.OperationalError as e:
            raise DatabaseError(f"Не удалось выполнить запрос для базы данных {database}: {e}")

    @allure.step('Получение списка тел писем, которые поступили на отправку из базы данных')
    def get_bodies_mailing_from_db(self, database: str) -> list:
        """
        Берем все письма и получаем из них содержимое.

        Args:
            database: Название базы данных для выполнения запроса.

        Returns:
            Список тел писем.

        Raises:
            ValueError: Если передано неизвестное название базы данных.
            DatabaseError: Если не удалось выполнить запрос к базе данных.
        """
        query_config = {
            'pmd': 'SELECT * FROM pmd.message_outbox',
            'ntf': 'SELECT * FROM ntf.email_history',
            'pb': 'SELECT * FROM pb.message_outbox'
        }

        if database not in query_config:
            raise ValueError(f"Неизвестная база данных: {database}")

        query = query_config[database]

        try:
            with UseDataBase(database) as cursor:
                cursor.execute(query)
                # Предполагается, что тело письма находится во втором столбце
                return [record[1] for record in cursor.fetchall()]
        except psycopg2.OperationalError as e:
            raise DatabaseError(f"Не удалось выполнить запрос для базы данных {database}: {e}")

    @allure.step('Отправка заявки на добавление документа')
    def send_brief_to_add_document(self, ppinfo_user_api_client, brief_client_admin, brief_status: str,
                                   notification: bool = True) -> str:
        """
        Отправляет заявку на добавление документа, берет ее в работу и согласовывает/отклоняет.

        Args:
            brief_status : Статус, который необходимо установить для заявки на добавление документа. Тут может быть или Согласовано или отклонено
            notification : Флаг, указывающий, следует ли отправлять уведомление.
                                           По умолчанию True.

        Returns:
            str: Номер заявки на добавление документа в формате строки со знаком №.
        """
        body = self.get_data_for_doc_brief(notification=notification)
        brief_id = self.post_brief_doc_user(ppinfo_user_api_client, body=body)
        self.take_to_work(brief_client_admin, brief_id, {"login": "admin_user"})
        self.delete_mailing_from_db('pb')
        self.change_brief_status(brief_client_admin, brief_id, {"status": brief_status})

        return "№ " + self.get_brief_by_id(brief_client_admin, brief_id)["number"]

    @allure.step('Отправка заявки на добавление продукта')
    def send_brief_to_add_product(self, client_delete, client_brief_admin, client_brief_user, brief_status: str,
                                  product_type: str, notification: bool = True,
                                  body: dict = None) -> tuple:
        """
        Отправляет заявку на добавление продукта, берет ее в работу и согласовывает/отклоняет.

        Args:
            brief_status : Статус, который необходимо установить для заявки на добавление продукта. Тут может быть или Согласовано или отклонено
            product_type : Тип продукта
            notification : Флаг, указывающий, следует ли отправлять уведомление. По умолчанию True.
            body : Тело заявки

        Returns:
            str: Номер заявки на добавление документа в формате строки со знаком №.
        """
        name = self.text
        if body is None:
            body = self.get_body_for_brief_creation(product_type, name, notification=notification)
        brief_id = self.crete_brief_by_user(client_brief_user, body)
        self.take_to_work(client_brief_admin, brief_id, {"login": "admin_user"})
        self.delete_mailing_from_db('pb')
        self.change_brief_status(client_brief_admin, brief_id, {"status": brief_status})

        if brief_status == 'statusApproval':
            self.delete_product_notification(client_delete, client_brief_admin, brief_id)

        return "№ " + self.get_brief_by_id(client_brief_admin, brief_id)["number"], name

    @allure.step('Отправка заявки на редактирование продукта')
    def send_brief_to_replace_product(self, brief_client_admin, brief_client_user, brief_status: str,
                                      body: dict = None) -> str:
        """
        Отправляет заявку на редактирование продукта, берет ее в работу и согласовывает/отклоняет.

        Args:
            brief_status : Статус, который необходимо установить для заявки на редактирование продукта. Тут может быть или Согласовано или отклонено
            body : Тело заявки

        Returns:
            str: Номер заявки на добавление документа в формате строки со знаком №.
        """
        brief_id = self.crete_brief_by_user(brief_client_user, body)
        self.take_to_work(brief_client_admin, brief_id, {"login": "admin_user"})
        self.delete_mailing_from_db('pb')
        self.change_brief_status(brief_client_admin, brief_id, {"status": brief_status})

        return "№ " + self.get_brief_by_id(brief_client_admin, brief_id)["number"]

    @property
    def get_pg_text(self) -> dict:
        """
        Получение ссылок ПГ которые должны быть в нотификации о смене статуса и инициировано закрытие
        Returns:
            Весь список, а в тестах уже надо выбрать нужное
        """
        data = {
            "Vneshnii": {
                "Arkhiv": None,
                "(PPinfo_status)In_use": [
                    'https://product.example.com/product-guide/Vneshnii/%D0%A0%D0%B0%D0%B7%D0%B2%D0%B8%D1%82%D0%B8%D0%B5%20%D0%BF%D1%80%D0%BE%D0%B4%D1%83%D0%BA%D1%82%D0%B0',
                    'https://product.example.com/product-guide/Vneshnii/%D0%A0%D0%B0%D0%B7%D0%B2%D0%B8%D1%82%D0%B8%D0%B5%20%D0%BF%D1%80%D0%BE%D0%B4%D1%83%D0%BA%D1%82%D0%B0?step=85a9065b-fe33-42dc-85f7-9abc24c89add',
                    'https://product.example.com/product-guide/Vneshnii/%D0%A0%D0%B0%D0%B7%D0%B2%D0%B8%D1%82%D0%B8%D0%B5%20%D0%BF%D1%80%D0%BE%D0%B4%D1%83%D0%BA%D1%82%D0%B0?step=cdb27d13-5aa3-4386-b002-2c021b49bee7',
                    'https://product.example.com/product-guide/Vneshnii/%D0%A0%D0%B0%D0%B7%D0%B2%D0%B8%D1%82%D0%B8%D0%B5%20%D0%BF%D1%80%D0%BE%D0%B4%D1%83%D0%BA%D1%82%D0%B0?step=57ac7562-7fa2-4f8c-ab3b-baa7bbe5dabe',
                    'https://product.example.com/product-guide/Vneshnii/%D0%A0%D0%B0%D0%B7%D0%B2%D0%B8%D1%82%D0%B8%D0%B5%20%D0%BF%D1%80%D0%BE%D0%B4%D1%83%D0%BA%D1%82%D0%B0?step=a1d8cf9a-1b50-4270-92a7-83b31056e154',
                    'https://product.example.com/product-guide/Vneshnii/%D0%A0%D0%B0%D0%B7%D0%B2%D0%B8%D1%82%D0%B8%D0%B5%20%D0%BF%D1%80%D0%BE%D0%B4%D1%83%D0%BA%D1%82%D0%B0?step=42162155-9f6a-4d1e-9de0-9a57728cf94b',
                    'https://product.example.com/product-guide/Vneshnii/%D0%A0%D0%B0%D0%B7%D0%B2%D0%B8%D1%82%D0%B8%D0%B5%20%D0%BF%D1%80%D0%BE%D0%B4%D1%83%D0%BA%D1%82%D0%B0?step=5490ffaa-47b5-4483-8a1c-57fc0229a389',
                    'https://product.example.com/product-guide/Vneshnii/%D0%97%D0%B0%D0%BA%D1%80%D1%8B%D1%82%D0%B8%D0%B5%20%D0%BF%D1%80%D0%BE%D0%B4%D1%83%D0%BA%D1%82%D0%B0',
                    'https://product.example.com/product-guide/Vneshnii/%D0%A0%D0%B0%D0%B7%D0%B2%D0%B8%D1%82%D0%B8%D0%B5%20%D0%BF%D1%80%D0%BE%D0%B4%D1%83%D0%BA%D1%82%D0%B0'],
                "(PPinfo_status)Pilot": [
                    'https://product.example.com/product-guide/Vneshnii/%D0%A0%D0%B0%D0%B7%D0%B2%D0%B8%D1%82%D0%B8%D0%B5%20%D0%BF%D1%80%D0%BE%D0%B4%D1%83%D0%BA%D1%82%D0%B0',
                    'https://product.example.com/product-guide/Vneshnii/%D0%A0%D0%B0%D0%B7%D1%80%D0%B0%D0%B1%D0%BE%D1%82%D0%BA%D0%B0%20%D0%B8%20%D0%B7%D0%B0%D0%BF%D1%83%D1%81%D0%BA%20MVP?step=40cb21d7-ecdd-4db1-ac9a-7a4db8fe04ec',
                    'https://product.example.com/product-guide/Vneshnii/%D0%A0%D0%B0%D0%B7%D0%B2%D0%B8%D1%82%D0%B8%D0%B5%20%D0%BF%D1%80%D0%BE%D0%B4%D1%83%D0%BA%D1%82%D0%B0?step=20299c45-b327-4ff7-93f0-acc6c4cfc8e5',
                    'https://product.example.com/product-guide/Vneshnii/%D0%A0%D0%B0%D0%B7%D0%B2%D0%B8%D1%82%D0%B8%D0%B5%20%D0%BF%D1%80%D0%BE%D0%B4%D1%83%D0%BA%D1%82%D0%B0?step=42162155-9f6a-4d1e-9de0-9a57728cf94b',
                    'https://product.example.com/product-guide/Vneshnii/%D0%A0%D0%B0%D0%B7%D0%B2%D0%B8%D1%82%D0%B8%D0%B5%20%D0%BF%D1%80%D0%BE%D0%B4%D1%83%D0%BA%D1%82%D0%B0?step=5490ffaa-47b5-4483-8a1c-57fc0229a389',
                    'https://product.example.com/product-guide/Vneshnii/%D0%A0%D0%B0%D0%B7%D0%B2%D0%B8%D1%82%D0%B8%D0%B5%20%D0%BF%D1%80%D0%BE%D0%B4%D1%83%D0%BA%D1%82%D0%B0?step=87ad325b-8a85-4eb1-b64c-82042e2912b1',
                    'https://product.example.com/product-guide/Vneshnii/%D0%A0%D0%B0%D0%B7%D0%B2%D0%B8%D1%82%D0%B8%D0%B5%20%D0%BF%D1%80%D0%BE%D0%B4%D1%83%D0%BA%D1%82%D0%B0'],
                "(PPinfo_status)In_progress": [
                    'https://product.example.com/product-guide/Vneshnii/%D0%A0%D0%B0%D0%B7%D1%80%D0%B0%D0%B1%D0%BE%D1%82%D0%BA%D0%B0%20%D0%B8%20%D0%B7%D0%B0%D0%BF%D1%83%D1%81%D0%BA%20MVP',
                    'https://product.example.com/product-guide/Vneshnii/%D0%A0%D0%B0%D0%B7%D1%80%D0%B0%D0%B1%D0%BE%D1%82%D0%BA%D0%B0%20%D0%B8%20%D0%B7%D0%B0%D0%BF%D1%83%D1%81%D0%BA%20MVP?step=ede7ec9d-5a7b-4326-9859-a866f28f62b6',
                    'https://product.example.com/product-guide/Vneshnii/%D0%A0%D0%B0%D0%B7%D1%80%D0%B0%D0%B1%D0%BE%D1%82%D0%BA%D0%B0%20%D0%B8%20%D0%B7%D0%B0%D0%BF%D1%83%D1%81%D0%BA%20MVP?step=2affd307-a6c5-4fd3-a1c7-fe4ec8791d7f',
                    'https://product.example.com/product-guide/Vneshnii/%D0%A0%D0%B0%D0%B7%D1%80%D0%B0%D0%B1%D0%BE%D1%82%D0%BA%D0%B0%20%D0%B8%20%D0%B7%D0%B0%D0%BF%D1%83%D1%81%D0%BA%20MVP?step=ef5fb4a9-64f0-4220-aff9-114c052374ad',
                    'https://product.example.com/product-guide/Vneshnii/%D0%A0%D0%B0%D0%B7%D1%80%D0%B0%D0%B1%D0%BE%D1%82%D0%BA%D0%B0%20%D0%B8%20%D0%B7%D0%B0%D0%BF%D1%83%D1%81%D0%BA%20MVP?step=8202ab25-7ee4-4315-a2b9-12f5703a468a',
                    'https://product.example.com/product-guide/Vneshnii/%D0%A0%D0%B0%D0%B7%D1%80%D0%B0%D0%B1%D0%BE%D1%82%D0%BA%D0%B0%20%D0%B8%20%D0%B7%D0%B0%D0%BF%D1%83%D1%81%D0%BA%20MVP?step=b7316c03-0226-4c73-9fd9-37fc3b263bfe',
                    'https://product.example.com/product-guide/Vneshnii/%D0%A0%D0%B0%D0%B7%D1%80%D0%B0%D0%B1%D0%BE%D1%82%D0%BA%D0%B0%20%D0%B8%20%D0%B7%D0%B0%D0%BF%D1%83%D1%81%D0%BA%20MVP?step=f79d225b-2e5f-4518-b5df-14afdbcaf7b1',
                    'https://product.example.com/product-guide/Vneshnii/%D0%A0%D0%B0%D0%B7%D1%80%D0%B0%D0%B1%D0%BE%D1%82%D0%BA%D0%B0%20%D0%B8%20%D0%B7%D0%B0%D0%BF%D1%83%D1%81%D0%BA%20MVP'],
                "(PPinfo_status)Idea_formation": ['https://product.example.com/product-guide/Vneshnii',
                                                  'https://product.example.com/product-guide/Vneshnii/%D0%A0%D0%B0%D0%B7%D1%80%D0%B0%D0%B1%D0%BE%D1%82%D0%BA%D0%B0%20%D0%BA%D0%BE%D0%BD%D1%86%D0%B5%D0%BF%D1%86%D0%B8%D0%B8?step=dffca5fe-3849-406f-9045-71b0b8cf0670',
                                                  'https://product.example.com/product-guide/Vneshnii/%D0%A0%D0%B0%D0%B7%D1%80%D0%B0%D0%B1%D0%BE%D1%82%D0%BA%D0%B0%20%D0%BA%D0%BE%D0%BD%D1%86%D0%B5%D0%BF%D1%86%D0%B8%D0%B8?step=a07b856b-4f68-4a01-8f52-2da67c8058ee',
                                                  'https://product.example.com/product-guide/Vneshnii/%D0%A0%D0%B0%D0%B7%D1%80%D0%B0%D0%B1%D0%BE%D1%82%D0%BA%D0%B0%20%D0%B8%20%D0%B7%D0%B0%D0%BF%D1%83%D1%81%D0%BA%20MVP?step=7a073fdc-e684-408a-81d4-7863de42218d',
                                                  'https://product.example.com/product-guide/Vneshnii/%D0%A0%D0%B0%D0%B7%D1%80%D0%B0%D0%B1%D0%BE%D1%82%D0%BA%D0%B0%20%D0%B8%20%D0%B7%D0%B0%D0%BF%D1%83%D1%81%D0%BA%20MVP?step=51f49497-cf5a-4b81-8d5d-64213b167e02',
                                                  'https://product.example.com/product-guide/Vneshnii/%D0%A0%D0%B0%D0%B7%D1%80%D0%B0%D0%B1%D0%BE%D1%82%D0%BA%D0%B0%20%D0%B8%20%D0%B7%D0%B0%D0%BF%D1%83%D1%81%D0%BA%20MVP?step=b682f6ad-6ef6-4e16-9b7b-7c460be9d45c',
                                                  'https://product.example.com/product-guide/Vneshnii'],
                "(PPinfo_status)Waiting_decision": None,
                "init_close": [
                    'https://product.example.com/product-guide/Vneshnii/%D0%97%D0%B0%D0%BA%D1%80%D1%8B%D1%82%D0%B8%D0%B5%20%D0%BF%D1%80%D0%BE%D0%B4%D1%83%D0%BA%D1%82%D0%B0',
                    'https://product.example.com/product-guide/Vneshnii/%D0%97%D0%B0%D0%BA%D1%80%D1%8B%D1%82%D0%B8%D0%B5%20%D0%BF%D1%80%D0%BE%D0%B4%D1%83%D0%BA%D1%82%D0%B0?step=9c1f449f-efe7-4990-ab14-43416c0f2a6e',
                    'https://product.example.com/product-guide/Vneshnii/%D0%97%D0%B0%D0%BA%D1%80%D1%8B%D1%82%D0%B8%D0%B5%20%D0%BF%D1%80%D0%BE%D0%B4%D1%83%D0%BA%D1%82%D0%B0?step=be8e4f70-b82c-4de7-956a-0c98d7ada631',
                    'https://product.example.com/product-guide/Vneshnii/%D0%97%D0%B0%D0%BA%D1%80%D1%8B%D1%82%D0%B8%D0%B5%20%D0%BF%D1%80%D0%BE%D0%B4%D1%83%D0%BA%D1%82%D0%B0?step=45ca963f-22a0-4008-80ad-01aee7ad13c3',
                    'https://product.example.com/product-guide/Vneshnii/%D0%97%D0%B0%D0%BA%D1%80%D1%8B%D1%82%D0%B8%D0%B5%20%D0%BF%D1%80%D0%BE%D0%B4%D1%83%D0%BA%D1%82%D0%B0?step=fa7236e1-28c1-4472-aa95-507a1296ff28',
                    'https://product.example.com/product-guide/Vneshnii/%D0%97%D0%B0%D0%BA%D1%80%D1%8B%D1%82%D0%B8%D0%B5%20%D0%BF%D1%80%D0%BE%D0%B4%D1%83%D0%BA%D1%82%D0%B0?step=e6f4ad22-70ce-4e53-99a6-5abb69117175',
                    'https://product.example.com/product-guide/Vneshnii/%D0%97%D0%B0%D0%BA%D1%80%D1%8B%D1%82%D0%B8%D0%B5%20%D0%BF%D1%80%D0%BE%D0%B4%D1%83%D0%BA%D1%82%D0%B0']
            },
            "Vnutrennii": {
                "Arkhiv": None,
                "(PPinfo_status)In_use": [
                    'https://product.example.com/product-guide/Vnutrennii/%D0%A0%D0%B0%D0%B7%D0%B2%D0%B8%D1%82%D0%B8%D0%B5%20%D0%BF%D1%80%D0%BE%D0%B4%D1%83%D0%BA%D1%82%D0%B0',
                    'https://product.example.com/product-guide/Vnutrennii/%D0%A0%D0%B0%D0%B7%D0%B2%D0%B8%D1%82%D0%B8%D0%B5%20%D0%BF%D1%80%D0%BE%D0%B4%D1%83%D0%BA%D1%82%D0%B0?step=20299c45-b327-4ff7-93f0-acc6c4cfc8e5',
                    'https://product.example.com/product-guide/Vnutrennii/%D0%A0%D0%B0%D0%B7%D0%B2%D0%B8%D1%82%D0%B8%D0%B5%20%D0%BF%D1%80%D0%BE%D0%B4%D1%83%D0%BA%D1%82%D0%B0?step=42162155-9f6a-4d1e-9de0-9a57728cf94b',
                    'https://product.example.com/product-guide/Vnutrennii/%D0%A0%D0%B0%D0%B7%D0%B2%D0%B8%D1%82%D0%B8%D0%B5%20%D0%BF%D1%80%D0%BE%D0%B4%D1%83%D0%BA%D1%82%D0%B0?step=faead2f0-5203-4241-9739-1b1cd3eca5c3',
                    'https://product.example.com/product-guide/Vnutrennii/%D0%97%D0%B0%D0%BA%D1%80%D1%8B%D1%82%D0%B8%D0%B5%20%D0%BF%D1%80%D0%BE%D0%B4%D1%83%D0%BA%D1%82%D0%B0',
                    'https://product.example.com/product-guide/Vnutrennii/%D0%A0%D0%B0%D0%B7%D0%B2%D0%B8%D1%82%D0%B8%D0%B5%20%D0%BF%D1%80%D0%BE%D0%B4%D1%83%D0%BA%D1%82%D0%B0'],
                "(PPinfo_status)Pilot": [
                    'https://product.example.com/product-guide/Vnutrennii/%D0%A0%D0%B0%D0%B7%D0%B2%D0%B8%D1%82%D0%B8%D0%B5%20%D0%BF%D1%80%D0%BE%D0%B4%D1%83%D0%BA%D1%82%D0%B0',
                    'https://product.example.com/product-guide/Vnutrennii/%D0%A0%D0%B0%D0%B7%D1%80%D0%B0%D0%B1%D0%BE%D1%82%D0%BA%D0%B0%20%D0%B8%20%D0%B7%D0%B0%D0%BF%D1%83%D1%81%D0%BA%20MVP?step=40cb21d7-ecdd-4db1-ac9a-7a4db8fe04ec',
                    'https://product.example.com/product-guide/Vnutrennii/%D0%A0%D0%B0%D0%B7%D0%B2%D0%B8%D1%82%D0%B8%D0%B5%20%D0%BF%D1%80%D0%BE%D0%B4%D1%83%D0%BA%D1%82%D0%B0?step=20299c45-b327-4ff7-93f0-acc6c4cfc8e5',
                    'https://product.example.com/product-guide/Vnutrennii/%D0%A0%D0%B0%D0%B7%D0%B2%D0%B8%D1%82%D0%B8%D0%B5%20%D0%BF%D1%80%D0%BE%D0%B4%D1%83%D0%BA%D1%82%D0%B0?step=42162155-9f6a-4d1e-9de0-9a57728cf94b',
                    'https://product.example.com/product-guide/Vnutrennii/%D0%A0%D0%B0%D0%B7%D0%B2%D0%B8%D1%82%D0%B8%D0%B5%20%D0%BF%D1%80%D0%BE%D0%B4%D1%83%D0%BA%D1%82%D0%B0?step=faead2f0-5203-4241-9739-1b1cd3eca5c3',
                    'https://product.example.com/product-guide/Vnutrennii/%D0%A0%D0%B0%D0%B7%D0%B2%D0%B8%D1%82%D0%B8%D0%B5%20%D0%BF%D1%80%D0%BE%D0%B4%D1%83%D0%BA%D1%82%D0%B0?step=920cc94d-d12a-4895-b431-a0d9a2daab25',
                    'https://product.example.com/product-guide/Vnutrennii/%D0%A0%D0%B0%D0%B7%D0%B2%D0%B8%D1%82%D0%B8%D0%B5%20%D0%BF%D1%80%D0%BE%D0%B4%D1%83%D0%BA%D1%82%D0%B0'],
                "(PPinfo_status)In_progress": [
                    'https://product.example.com/product-guide/Vnutrennii/%D0%A0%D0%B0%D0%B7%D1%80%D0%B0%D0%B1%D0%BE%D1%82%D0%BA%D0%B0%20%D0%B8%20%D0%B7%D0%B0%D0%BF%D1%83%D1%81%D0%BA%20MVP',
                    'https://product.example.com/product-guide/Vnutrennii/%D0%A0%D0%B0%D0%B7%D1%80%D0%B0%D0%B1%D0%BE%D1%82%D0%BA%D0%B0%20%D0%B8%20%D0%B7%D0%B0%D0%BF%D1%83%D1%81%D0%BA%20MVP?step=ef5fb4a9-64f0-4220-aff9-114c052374ad',
                    'https://product.example.com/product-guide/Vnutrennii/%D0%A0%D0%B0%D0%B7%D1%80%D0%B0%D0%B1%D0%BE%D1%82%D0%BA%D0%B0%20%D0%B8%20%D0%B7%D0%B0%D0%BF%D1%83%D1%81%D0%BA%20MVP?step=cf9c5cb5-c209-48e6-8f0c-72cca59400d3',
                    'https://product.example.com/product-guide/Vnutrennii/%D0%A0%D0%B0%D0%B7%D1%80%D0%B0%D0%B1%D0%BE%D1%82%D0%BA%D0%B0%20%D0%B8%20%D0%B7%D0%B0%D0%BF%D1%83%D1%81%D0%BA%20MVP?step=eeb007d0-13f9-428d-a391-b78c5626cd30',
                    'https://product.example.com/product-guide/Vnutrennii/%D0%A0%D0%B0%D0%B7%D1%80%D0%B0%D0%B1%D0%BE%D1%82%D0%BA%D0%B0%20%D0%B8%20%D0%B7%D0%B0%D0%BF%D1%83%D1%81%D0%BA%20MVP?step=8202ab25-7ee4-4315-a2b9-12f5703a468a',
                    'https://product.example.com/product-guide/Vnutrennii/%D0%A0%D0%B0%D0%B7%D1%80%D0%B0%D0%B1%D0%BE%D1%82%D0%BA%D0%B0%20%D0%B8%20%D0%B7%D0%B0%D0%BF%D1%83%D1%81%D0%BA%20MVP?step=b7316c03-0226-4c73-9fd9-37fc3b263bfe',
                    'https://product.example.com/product-guide/Vnutrennii/%D0%A0%D0%B0%D0%B7%D1%80%D0%B0%D0%B1%D0%BE%D1%82%D0%BA%D0%B0%20%D0%B8%20%D0%B7%D0%B0%D0%BF%D1%83%D1%81%D0%BA%20MVP?step=f79d225b-2e5f-4518-b5df-14afdbcaf7b1',
                    'https://product.example.com/product-guide/Vnutrennii/%D0%A0%D0%B0%D0%B7%D1%80%D0%B0%D0%B1%D0%BE%D1%82%D0%BA%D0%B0%20%D0%B8%20%D0%B7%D0%B0%D0%BF%D1%83%D1%81%D0%BA%20MVP'],
                "(PPinfo_status)Idea_formation": [
                    'https://product.example.com/product-guide/Vnutrennii/%D0%A0%D0%B0%D0%B7%D1%80%D0%B0%D0%B1%D0%BE%D1%82%D0%BA%D0%B0%20%D0%B8%20%D0%B7%D0%B0%D0%BF%D1%83%D1%81%D0%BA%20MVP',
                    'https://product.example.com/product-guide/Vnutrennii/%D0%A0%D0%B0%D0%B7%D1%80%D0%B0%D0%B1%D0%BE%D1%82%D0%BA%D0%B0%20%D0%BA%D0%BE%D0%BD%D1%86%D0%B5%D0%BF%D1%86%D0%B8%D0%B8?step=dffca5fe-3849-406f-9045-71b0b8cf0670',
                    'https://product.example.com/product-guide/Vnutrennii?step=a07b856b-4f68-4a01-8f52-2da67c8058ee',
                    'https://product.example.com/product-guide/Vnutrennii/%D0%A0%D0%B0%D0%B7%D1%80%D0%B0%D0%B1%D0%BE%D1%82%D0%BA%D0%B0%20%D0%B8%20%D0%B7%D0%B0%D0%BF%D1%83%D1%81%D0%BA%20MVP?step=b14cccae-bdb9-45c7-8930-034ddc107d0f',
                    'https://product.example.com/product-guide/Vnutrennii/%D0%A0%D0%B0%D0%B7%D1%80%D0%B0%D0%B1%D0%BE%D1%82%D0%BA%D0%B0%20%D0%B8%20%D0%B7%D0%B0%D0%BF%D1%83%D1%81%D0%BA%20MVP?step=37ad7720-d582-441b-abf2-c0c16ab480ee',
                    'https://product.example.com/product-guide/Vnutrennii/%D0%A0%D0%B0%D0%B7%D1%80%D0%B0%D0%B1%D0%BE%D1%82%D0%BA%D0%B0%20%D0%B8%20%D0%B7%D0%B0%D0%BF%D1%83%D1%81%D0%BA%20MVP?step=b682f6ad-6ef6-4e16-9b7b-7c460be9d45c',
                    'https://product.example.com/product-guide/Vnutrennii/%D0%A0%D0%B0%D0%B7%D1%80%D0%B0%D0%B1%D0%BE%D1%82%D0%BA%D0%B0%20%D0%B8%20%D0%B7%D0%B0%D0%BF%D1%83%D1%81%D0%BA%20MVP'],
                "(PPinfo_status)Waiting_decision": None,
                "init_close": [
                    'https://product.example.com/product-guide/Vnutrennii/%D0%97%D0%B0%D0%BA%D1%80%D1%8B%D1%82%D0%B8%D0%B5%20%D0%BF%D1%80%D0%BE%D0%B4%D1%83%D0%BA%D1%82%D0%B0',
                    'https://product.example.com/product-guide/Vnutrennii/%D0%97%D0%B0%D0%BA%D1%80%D1%8B%D1%82%D0%B8%D0%B5%20%D0%BF%D1%80%D0%BE%D0%B4%D1%83%D0%BA%D1%82%D0%B0?step=6cb06385-29d2-42db-9dda-06d136fbd7bd',
                    'https://product.example.com/product-guide/Vnutrennii/%D0%97%D0%B0%D0%BA%D1%80%D1%8B%D1%82%D0%B8%D0%B5%20%D0%BF%D1%80%D0%BE%D0%B4%D1%83%D0%BA%D1%82%D0%B0?step=be8e4f70-b82c-4de7-956a-0c98d7ada631',
                    'https://product.example.com/product-guide/Vnutrennii/%D0%97%D0%B0%D0%BA%D1%80%D1%8B%D1%82%D0%B8%D0%B5%20%D0%BF%D1%80%D0%BE%D0%B4%D1%83%D0%BA%D1%82%D0%B0?step=fa7236e1-28c1-4472-aa95-507a1296ff28',
                    'https://product.example.com/product-guide/Vnutrennii/%D0%97%D0%B0%D0%BA%D1%80%D1%8B%D1%82%D0%B8%D0%B5%20%D0%BF%D1%80%D0%BE%D0%B4%D1%83%D0%BA%D1%82%D0%B0?step=e6f4ad22-70ce-4e53-99a6-5abb69117175',
                    'https://product.example.com/product-guide/Vnutrennii/%D0%97%D0%B0%D0%BA%D1%80%D1%8B%D1%82%D0%B8%D0%B5%20%D0%BF%D1%80%D0%BE%D0%B4%D1%83%D0%BA%D1%82%D0%B0']
            }
        }

        return data
