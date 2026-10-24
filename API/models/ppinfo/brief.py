from typing import Any

import allure

from API.data.ppinfo import Briefs, StatusesBrief, BriefById, UserBriefs
from API.utils.generate import Gen

HOST = 'https://stage.prodboard.example.com'


class BriefUrls:
    """
    https://stage.prodboard.example.com/ppinfo/swagger/brief/index.html#/
    """

    # Получение заявок от лица пользователя
    GET_BRIEFS_USER = 'v2/brief'

    # Получение всех заявок
    GET_BRIEFS = 'v1/brief'

    # Создание заявки
    CREATE_BRIEF = 'v1/brief'

    # Получение статусов по заявкам
    STATUSES = 'v1/brief/statuses'

    # Сохранение комментария для администратора или пользователя
    COMMENT = 'v1/brief/{}/comment'

    # Взятие заявки в работу
    EMPLOYEE = 'v1/brief/{}/employee'

    # Согласование/отклонение заявки
    CHANGE_STATUS = 'v1/brief/{}/status'

    # Получение конкретного брифа по ID
    GET_BRIEF_BY_ID = 'v1/brief/{}'

    # Изменение заявки по id
    PATCH_BRIEF_BY_ID = 'v1/brief/{}'


class Brief(BriefUrls):

    @property
    def text(self) -> str:
        return Gen.generate_text(7) + 'test'

    @property
    def initiator_data(self):
        return {
            'type': 'comment_initiator',
            'comment': 'qwe_initiator'
        }

    @property
    def executor_data(self):
        return {
            'type': 'comment_executor',
            'comment': 'qwe_executor'
        }

    def attr_storage_brief(self, bi_code: str = 'BI_3266'):
        return {
            #### Создание продуктов
            'create_external_product': '{"name":'
                                       f'"{self.text}",'
                                       "\"description\":\"qweqweqwe\",\"attributes\":[{\"id\":\"PPinfo_category_product\",\"values\":[{\"value\":\"(PPInfo_category_spravochnik)Other\"}]},{\"id\":\"PPinfo_status\",\"values\":[{\"value\":\"Arkhiv\"}]},{\"id\":\"employee_chief_PO\",\"values\":[{\"code\":\"admin_user\",\"value\":\"Фамилия Имя Отчество\"}]},{\"id\":\"employee_product_owner\",\"values\":[{\"code\":\"admin_user\",\"value\":\"Фамилия Имя Отчество\"}]},{\"id\":\"PPinfo_web_app\",\"values\":[{\"value\":\"(PPinfo_spravochnik_webapp)WEBNO\"}]},{\"id\":\"PPInfo_product_block\",\"values\":[{\"value\":\"(PPInfo_spravochniK_block)ECO_block\"}]},{\"id\":\"PPinfo_MTS_Brand\",\"values\":[{\"value\":\"(PPinfo_MTSBrand)MTSBrand_no\"}]},{\"id\":\"PPinfo_mvp\",\"values\":[{\"value\":\"(PPinfo_mvp)MVPNo\"}]},{\"id\":\"PPinfo_konkurent\",\"values\":[{\"value\":\"net 1233\"}]},{\"id\":\"PPInfo_Monetization\",\"values\":[{\"value\":\"net 1233\"}]},{\"id\":\"PPinfo_product_problem\",\"values\":[{\"value\":\"net 1233\"}]},{\"id\":\"PPinfo_product_aim\",\"values\":[{\"value\":\"net 1233\"}]},{\"id\":\"PPinfo_resolution\",\"values\":[{\"value\":\"net 1233\"}]},{\"id\":\"PPinfo_market\",\"values\":[{\"value\":\"(PPinfo_market)B2C\"}]},{\"id\":\"PPInfo_type_develop\",\"values\":[{\"value\":\"(PPInfo_spravoch_type)Vendor\"}]},{\"id\":\"PPinfo_market_sign\",\"values\":[{\"value\":\"(PPinfo_market_sign)MS_No\"}]},{\"id\":\"PPinfo_values\",\"values\":[{\"value\":\"net 1233\"}]}],\"type\":\"Vneshnii\"}",
            'create_internal_product': '{"name":'
                                       f'"{self.text}",'
                                       "\"description\":\"sadfasdf\",\"attributes\":[{\"id\":\"employee_product_owner\",\"values\":[{\"code\":\"admin_user\",\"value\":\"Фамилия Имя Отчество\",\"compatibility\":false}]},{\"id\":\"PPinfo_web_app\",\"values\":[{\"value\":\"(PPinfo_spravochnik_webapp)WEBNO\"}]},{\"id\":\"PPinfo_fix_HFM\",\"values\":[{\"value\":\"(PPinfo_Fix_HFM_voc)PPInfo_Fix_HFM\"}]},{\"id\":\"PPinfo_status\",\"values\":[{\"value\":\"(PPinfo_status)Idea_formation\"}]},{\"id\":\"PPInfo_type_develop\",\"values\":[{\"value\":\"(PPInfo_spravoch_type)Own_Vendor\"}]}],\"type\":\"Vnutrennii\"}",
            #### Строки
            "string_add": f"{{\"id\":\"{bi_code}\",\"attributes\":[{{\"id\":\"PPInfo_showcase\",\"values\":"
                          f"[{{\"value\":"
                          f"\"test\""
                          f"}}]}}]}}",
            "string_replace": f"{{\"id\":\"{bi_code}\",\"attributes\":[{{\"id\":\"PPInfo_showcase\",\"values\":"
                              f"[{{\"value\": "
                              f"\"test2\""
                              f"}}]}}]}}",
            "string_remove": f"{{\"id\":\"{bi_code}\",\"attributes\":[{{\"id\":\"PPInfo_showcase\",\"values\":[]}}]}}",
            #### Мэниселект
            "manyselect_add": f"{{\"id\":\"{bi_code}\",\"attributes\":[{{\"id\":\"PPinfo_StructuralProductType1\",\"values\":[{{\"code\":\"(PPInfo_spravochnic_Structural)Main\",\"value\":\"Основной\"}}]}}]}}",
            "manyselect_replace": f"{{\"id\":\"{bi_code}\",\"attributes\":[{{\"id\":\"PPinfo_StructuralProductType1\",\"values\":[{{\"code\":\"(PPInfo_spravochnic_Structural)Atomic\",\"value\":\"Атомарный\"}}]}}]}}",
            "manyselect_remove": f"{{\"id\":\"{bi_code}\",\"attributes\":[{{\"id\":\"PPinfo_StructuralProductType1\",\"values\":[]}}]}}",

            #### Дата
            "date_add": f"{{\"id\":\"{bi_code}\",\"attributes\":[{{\"id\":\"PPinfo_start_close_date\",\"values\":[{{\"code\":\"2024-01-23T03:00:00Z\",\"value\":\"2023-09-20T03:00:00Z\"}}]}}]}}",
            "date_replace": f"{{\"id\":\"{bi_code}\",\"attributes\":[{{\"id\":\"PPinfo_start_close_date\",\"values\":[{{\"code\":\"2024-01-24T03:00:00Z\",\"value\":\"2023-09-21T03:00:00Z\"}}]}}]}}",
            "date_remove": f"{{\"id\":\"{bi_code}\",\"attributes\":[{{\"id\":\"PPinfo_start_close_date\",\"values\":[]}}]}}",

            #### Число
            "num_add": f"{{\"id\":\"{bi_code}\",\"attributes\":[{{\"id\":\"Identifikator_SOL\",\"values\":[{{\"code\":\"666\",\"value\":\"666\"}}]}}]}}",
            "num_replace": f"{{\"id\":\"{bi_code}\",\"attributes\":[{{\"id\":\"Identifikator_SOL\",\"values\":[{{\"code\":\"777\",\"value\":\"777\"}}]}}]}}",
            "num_remove": f"{{\"id\":\"{bi_code}\",\"attributes\":[{{\"id\":\"Identifikator_SOL\",\"values\":[]}}]}}",
            #### Юзер
            "user_add": f"{{\"id\":\"{bi_code}\",\"attributes\":[{{\"id\":\"employee_business_owner\",\"values\":[{{\"code\":\"admin_user\",\"value\":\"Светов Даниил Дмитриевич\"}}]}}]}}",
            "user_replace": f"{{\"id\":\"{bi_code}\",\"attributes\":[{{\"id\":\"employee_business_owner\",\"values\":[{{\"code\":\"aigladyshev\",\"value\":\"Фамилия Имя Отчество\"}}]}}]}}",
            "user_remove": f"{{\"id\":\"{bi_code}\",\"attributes\":[{{\"id\":\"employee_business_owner\",\"values\":[]}}]}}",

            #### Множество
            "multi_add": f"{{\"id\":\"{bi_code}\",\"attributes\":[{{\"id\":\"Mnozhestvo\",\"values\":[{{\"code\":\"Vtoroi\",\"value\":\"Второй\"}},{{\"code\":\"Pervyi\",\"value\":\"Первый\"}},{{\"code\":\"Tretii\",\"value\":\"Третий\"}}]}}]}}",
            "multi_replace": f"{{\"id\":\"{bi_code}\",\"attributes\":[{{\"id\":\"Mnozhestvo\",\"values\":[{{\"code\":\"Vtoroi\",\"value\":\"Второй\"}}]}}]}}",
            "multi_remove": f"{{\"id\":\"{bi_code}\",\"attributes\":[{{\"id\":\"Mnozhestvo\",\"values\":[]}}]}}",

            #### Мультиюзер
            "multiuser_add": f"{{\"id\":\"{bi_code}\",\"attributes\":[{{\"id\":\"Rukovoditel_etogo_balagana\",\"values\":[{{\"code\":\"pymaslenkov\",\"value\":\"Масленков Павел Юрьевич\"}},{{\"code\":\"admin_user\",\"value\":\"Светов Даниил Дмитриевич\"}},{{\"code\":\"regular_user\",\"value\":\"Костров Алексей Игоревич\"}}]}}]}}",
            "multiuser_replace_minus": f"{{\"id\":\"{bi_code}\",\"attributes\":[{{\"id\":\"Rukovoditel_etogo_balagana\",\"values\":[{{\"code\":\"pymaslenkov\",\"value\":\"Масленков Павел Юрьевич\"}},{{\"code\":\"admin_user\",\"value\":\"Светов Даниил Дмитриевич\"}}]}}]}}",
            "multiuser_replace_plus": f"{{\"id\":\"{bi_code}\",\"attributes\":[{{\"id\":\"Rukovoditel_etogo_balagana\",\"values\":[{{\"code\":\"pymaslenkov\",\"value\":\"Масленков Павел Юрьевич\"}},{{\"code\":\"admin_user\",\"value\":\"Светов Даниил Дмитриевич\"}},{{\"code\":\"regular_user\",\"value\":\"Костров Алексей Игоревич\"}}]}}]}}",
            "multiuser_remove": f"{{\"id\":\"{bi_code}\",\"attributes\":[{{\"id\":\"Rukovoditel_etogo_balagana\",\"values\":[]}}]}}",

            #### ОдинПродукт
            "product_add": f"{{\"id\":\"{bi_code}\",\"attributes\":[{{\"id\":\"Odin_produkt\",\"values\":[{{\"code\":\"BI_60\",\"value\":\"МТС Маркетолог\"}}]}}]}}",
            "product_replace": f"{{\"id\":\"{bi_code}\",\"attributes\":[{{\"id\":\"Odin_produkt\",\"values\":[{{\"code\":\"BI_25\",\"value\":\"Kaspersky Security для МТС\"}}]}}]}}",
            "product_remove": f"{{\"id\":\"{bi_code}\",\"attributes\":[{{\"id\":\"Odin_produkt\",\"values\":[]}}]}}",

            #### МультиПродукт
            "multiproduct_add": f"{{\"id\":\"{bi_code}\",\"attributes\":[{{\"id\":\"Mnogo_produktov\",\"values\":[{{\"code\":\"BI_270\",\"value\":\"GPS-Трекер с МТС Поиск\"}},{{\"code\":\"BI_25\",\"value\":\"Kaspersky Security для МТС\"}},{{\"code\":\"BI_1901\",\"value\":\"Весь МТС\"}},{{\"code\":\"BI_1972\",\"value\":\"Весь МТС Полный дом\"}}]}}]}}",
            "multiproduct_replace_minus": f"{{\"id\":\"{bi_code}\",\"attributes\":[{{\"id\":\"Mnogo_produktov\",\"values\":[{{\"code\":\"BI_1972\",\"value\":\"Весь МТС Полный дом\"}},{{\"code\":\"BI_270\",\"value\":\"GPS-Трекер с МТС Поиск\"}},{{\"code\":\"BI_25\",\"value\":\"Kaspersky Security для МТС\"}}]}}]}}",
            "multiproduct_replace_plus": f"{{\"id\":\"{bi_code}\",\"attributes\":[{{\"id\":\"Mnogo_produktov\",\"values\":[{{\"code\":\"BI_25\",\"value\":\"Kaspersky Security для МТС\"}},{{\"code\":\"BI_1972\",\"value\":\"Весь МТС Полный дом\"}},{{\"code\":\"BI_270\",\"value\":\"GPS-Трекер с МТС Поиск\"}},{{\"code\":\"BI_1984\",\"value\":\"МТС Маркетолог. Скоринг\"}}]}}]}}",
            "multiproduct_remove": f"{{\"id\":\"{bi_code}\",\"attributes\":[{{\"id\":\"Mnogo_produktov\",\"values\":[]}}]}}",

            #### МультиСсылка
            "multilink_add": f"{{\"id\":\"{bi_code}\",\"attributes\":[{{\"id\":\"Test_mnozh_ssylki\",\"values\":[{{\"code\":\"Линк1\",\"value\":\"Название ссылки1\"}},{{\"value\":\"Название ссылки2\",\"code\":\"Линк2\"}}]}}]}}",
            "multilink_replace_minus": f"{{\"id\":\"{bi_code}\",\"attributes\":[{{\"id\":\"Test_mnozh_ssylki\",\"values\":[{{\"code\":\"Линк1\",\"value\":\"Название ссылки1\"}}]}}]}}",
            "multilink_replace_plus": f"{{\"id\":\"{bi_code}\",\"attributes\":[{{\"id\":\"Test_mnozh_ssylki\",\"values\":[{{\"code\":\"Линк1\",\"value\":\"Название ссылки1\"}},{{\"value\":\"Название ссылки2\",\"code\":\"Линк2\"}}]}}]}}",
            "multilink_remove": f"{{\"id\":\"{bi_code}\",\"attributes\":[{{\"id\":\"Test_mnozh_ssylki\",\"values\":[]}}]}}",

            #### Многострочный текст
            "multistring_add": f"{{\"id\":\"{bi_code}\",\"attributes\":[{{\"id\":\"PPinfo_resolution\",\"values\":[{{\"value\":\"test\"}}]}}]}}",
            "multistring_replace": f"{{\"id\":\"{bi_code}\",\"attributes\":[{{\"id\":\"PPinfo_resolution\",\"values\":[{{\"value\":\"test2\"}}]}}]}}",
            "multistring_remove": f"{{\"id\":\"{bi_code}\",\"attributes\":[{{\"id\":\"PPinfo_resolution\",\"values\":[]}}]}}",

            #### Ссылка
            "link_add": f"{{\"id\":\"{bi_code}\",\"attributes\":[{{\"id\":\"PPInfo_site_landing\",\"values\":[{{\"code\":\"https://cashback.example.com\",\"value\":\"\"}}]}}]}}",
            "link_replace": f"{{\"id\":\"{bi_code}\",\"attributes\":[{{\"id\":\"PPInfo_site_landing\",\"values\":[{{\"code\":\"https://stage.prodboard.example.com/product/BI_42/main\",\"value\":\"\"}}]}}]}}",
            "link_remove": f"{{\"id\":\"{bi_code}\",\"attributes\":[{{\"id\":\"PPInfo_site_landing\",\"values\":[]}}]}}",

            #### Основной проект
            "main_project_jira_add": f"{{\"id\":\"{bi_code}\",\"attributes\":[{{\"id\":\"Osnovnoi_proekt_Jira\",\"values\":[{{\"code\":\"https://jira.example.com/browse/GB\",\"value\":\"Гетблоггер (GB)\"}}]}}]}}",
            "main_project_jira_product_replace": f"{{\"id\":\"{bi_code}\",\"attributes\":[{{\"id\":\"Osnovnoi_proekt_Jira\",\"values\":[{{\"code\":\"https://jira.example.com/browse/PN\",\"value\":\"Партнерская сеть МТС (PN)\"}}]}}]}}",
            "main_project_jira_product_remove": f"{{\"id\":\"{bi_code}\",\"attributes\":[{{\"id\":\"Osnovnoi_proekt_Jira\",\"values\":[]}}]}}",

        }

    @allure.step('Получение параметров для get_briefs')
    def get_briefs_params(self, new_params: dict[str, Any] | None = None) -> dict[str, Any]:
        params = {
            'offset': "0",
            'limit': "10",
            'status': "statusPublished",
            'isOwned': True
        }
        if new_params:
            params.update(new_params)

        return params

    @allure.step("Получение data для цикла")
    def get_briefs_body(self, type_of_data: str, action: str = "updateProduct", bi_code: str | None = None) -> dict[
        str, Any]:
        data = self.attr_storage_brief(bi_code)[type_of_data] if bi_code else self.attr_storage_brief()[type_of_data]
        boby = {"type": action,
                "data": data}
        return boby

    @allure.step('Получение заявок от лица пользователя')
    def get_briefs_user(self, client) -> dict[str, Any]:
        response = client.get(self.GET_BRIEFS_USER)

        UserBriefs(**response)

        return response

    @allure.step('Получение заявок')
    def get_briefs(self, client, params: dict[str, Any]) -> dict[str, Any]:
        response = client.get(self.GET_BRIEFS, params=params)

        Briefs(**response)

        return response

    @allure.step('Создание заявки админом')
    def crete_brief_by_admin(self, client, data: dict[str, Any]) -> str:
        response = client.post(self.CREATE_BRIEF, json=data)

        return response['id']

    @allure.step('Создание заявки обычным пользователем')
    def crete_brief_by_user(self, client, data: dict[str, Any]) -> str:
        response = client.post(self.CREATE_BRIEF, json=data)

        return response['id']

    @allure.step('Создание заявки обычным пользователем без прав')
    def crete_brief_by_user_403(self, client, data: dict[str, Any]) -> None:
        client.post(self.CREATE_BRIEF, json=data, expected_status_code=403)

    @allure.step('Получение счетчиков по статусам')
    def get_statuses_count(self, client) -> dict[str, Any]:
        response = client.get(self.STATUSES)

        StatusesBrief(**response)

        return response

    @allure.step('Создание комментария')
    def put_comment(self, client, brief_id: str, comment_data: dict[str, Any]) -> None:
        client.put(self.COMMENT.format(brief_id), json=comment_data)

    @allure.step('Взятие в работу')
    def take_to_work(self, client, brief_id: str, employee_data: dict[str, Any]) -> None:
        client.patch(self.EMPLOYEE.format(brief_id), json=employee_data)

    @allure.step('Согласование/отклонение заявки')
    def change_brief_status(self, client, brief_id: str, status_data: dict[str, Any]) -> None:
        client.patch(self.CHANGE_STATUS.format(brief_id), json=status_data)

    @allure.step('Получение информации о заявке по id')
    def get_brief_by_id(self, client, brief_id: str) -> dict[str, Any]:
        response = client.get(self.GET_BRIEF_BY_ID.format(brief_id))

        BriefById(**response)

        return response

    @allure.step('Изменение заявки по id')
    def patch_brief_by_id(self, client, brief_id: str, brief_data: dict[str, Any]) -> None:
        client.patch(self.PATCH_BRIEF_BY_ID.format(brief_id), json=brief_data)

    @allure.step('Согласование заявки')
    def approval(self, client, brief_id):
        status = {
            'status': 'statusApproval'
        }

        self.change_brief_status(client, brief_id, status)

    @allure.step('Отклонение заявки')
    def declined(self, client, brief_id):
        status = {
            'status': 'statusDeclined'
        }

        self.change_brief_status(client, brief_id, status)

    @allure.title('Полный цикл работы над заявкой')
    def full_cycle(self, client_admin, client_user, data: dict[str, Any], status_str: str) -> None:

        login = {'login': 'admin_user'}
        status = {'status': status_str}

        brief_id = self.crete_brief_by_user(client_user, data)

        self.take_to_work(client_admin, brief_id, login)
        with allure.step(f'Меняем статус заявки на {status_str}'):
            self.change_brief_status(client_admin, brief_id, status)

        with allure.step('Проверяем, что статус заявки поменялся'):
            if status_str == 'statusDeclined':
                assert self.get_brief_by_id(client_admin, brief_id)[
                           'status'] == 'statusDeclined', f'Текущий статус: {self.get_brief_by_id(client_admin, brief_id)["status"]}'
            else:
                assert self.get_brief_by_id(client_admin, brief_id)[
                           'status'] == 'statusDone', f'Текущий статус: {self.get_brief_by_id(client_admin, brief_id)["status"]}'

    @allure.step('Создание заявки и взятие её в работу')
    def create_brief_and_take_to_work(self, client_admin, client_user) -> str:
        body = self.get_briefs_body('string_add')

        login = {
            'login': 'admin_user'
        }

        brief_id = self.crete_brief_by_user(client_user, body)

        self.take_to_work(client_admin, brief_id, login)

        return brief_id
