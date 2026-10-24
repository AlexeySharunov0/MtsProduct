import allure
import pytest

from API.models.notification.notification import Notifications
from API.models.ppinfo.product_v1 import ProductV1


##### Создание продукта
@pytest.mark.api
@pytest.mark.notification
@allure.feature("Нотификации, шаги ПГ при смене статуса/добавлении продукта")
@pytest.mark.usefixtures('clear_db_notifications')
@allure.issue('https://jira.mts.ru/browse/PPI-3646',
              'PPInfo - После смены статуса продукта уведомлять команду о важных шагах из PG (Внутренние продукты)')
@allure.issue('https://jira.mts.ru/browse/PPI-3306',
              'PPInfo - После смены статуса продукта уведомлять команду о важных шагах из PG (Внешние продукты)')
class TestNotificationAdminCreationPG(Notifications):

    @pytest.mark.parametrize("product_type",
                             ["Vneshnii", "Vnutrennii"])
    @pytest.mark.parametrize("status_code", (
            ["Arkhiv", "(PPinfo_status)In_use", "(PPinfo_status)Pilot", "(PPinfo_status)In_progress",
             '(PPinfo_status)Idea_formation', '(PPinfo_status)Waiting_decision']))
    def test_notification_admin_create_product_check_status(self, ppinfo_client, product_type, status_code):
        allure.dynamic.title(f"Шаги PG в нотификации при добавлении продукта админом - {product_type}, {status_code}")
        with allure.step("Создаем продукт админом"):
            gen_name = self.text
            self.create_product(ppinfo_client,
                                self.get_data_for_product_creation(product_type, name=gen_name, status=status_code))

        emails = self.get_bodies_mailing_from_db('pb')

        assert self.get_count_mailing_from_db('ntf') >= 1, "Нотификации не пришли"

        assert emails[0]['templateMeta']['pgLinks'] == self.get_pg_text[product_type][status_code]

    @pytest.mark.parametrize("product_type",
                             ["Vneshnii", "Vnutrennii"])
    @pytest.mark.parametrize("status_code", (
            ["Arkhiv", "(PPinfo_status)In_use", "(PPinfo_status)Pilot", "(PPinfo_status)In_progress",
             '(PPinfo_status)Idea_formation', '(PPinfo_status)Waiting_decision']))
    def test_notification_admin_update_product_check_status(self, ppinfo_client, product_type, status_code):
        allure.dynamic.title(
            f"Шаги PG в нотификации при редактирование продукта админом - {product_type}, {status_code}")
        body = self.get_data_for_admin_update_status(product_type, status_code)
        self.change_product(ppinfo_client, body)

        emails = self.get_bodies_mailing_from_db('pb')

        assert self.get_count_mailing_from_db('ntf') >= 1, "Нотификации не пришли"

        assert emails[0]['templateMeta']['pgLinks'] == self.get_pg_text[product_type][status_code]

    @pytest.mark.parametrize("product_type", ["internal", "external"])
    @pytest.mark.parametrize("status_code", (
            ["Arkhiv", "(PPinfo_status)In_use", "(PPinfo_status)Pilot", "(PPinfo_status)In_progress",
             '(PPinfo_status)Idea_formation', '(PPinfo_status)Waiting_decision']))
    def test_notification_brief_create_product_user(self, ppinfo_client, ppinfo_user_client, pmd_internal_gw_client, product_type, status_code):
        allure.dynamic.title(
            f"Шаги PG в нотификации при создании продукта пользователем - {product_type}, {status_code}")
        with allure.step("Отправляем заявку"):
            name = self.text
            body = self.get_body_for_brief_creation(product_type, name, status=status_code)
            brief_id = self.crete_brief_by_user(ppinfo_user_client, body)
            self.take_to_work(ppinfo_client, brief_id, {"login": "ddsvetov1"})
            self.delete_mailing_from_db('pb')
            self.change_brief_status(ppinfo_client, brief_id, {"status": 'statusApproval'})
            self.delete_product(pmd_internal_gw_client, self.get_brief_by_id(ppinfo_client, brief_id=brief_id)['data'][8:17])

        emails = self.get_bodies_mailing_from_db('pb')

        assert self.get_count_mailing_from_db('ntf') >= 1, "Нотификации не пришли"

        for mail in emails:
            product_type_formated = "Vneshnii" if product_type == "external" else "Vnutrennii"
            assert mail['templateMeta']['pgLinks'] == self.get_pg_text[product_type_formated][status_code]

    @pytest.mark.parametrize("product_type",
                             ["Vneshnii", "Vnutrennii"])
    @pytest.mark.parametrize("status_code", (
            ["Arkhiv", "(PPinfo_status)In_use", "(PPinfo_status)Pilot", "(PPinfo_status)In_progress",
             '(PPinfo_status)Idea_formation', '(PPinfo_status)Waiting_decision']))
    def test_notification_brief_update_product_user(self, ppinfo_client, ppinfo_user_client, product_type, status_code):
        allure.dynamic.title(
            f"Шаги PG в нотификации при редактирование продукта пользователем - {product_type}, {status_code}")
        with allure.step("Отправляем заявку"):
            body = self.get_data_for_user_update_status(status_code, product_type)
            brief_id = self.crete_brief_by_user(ppinfo_user_client, body)
            self.take_to_work(ppinfo_client, brief_id, {"login": "ddsvetov1"})
            self.delete_mailing_from_db('pb')
            self.change_brief_status(ppinfo_client, brief_id, {"status": 'statusApproval'})

        emails = self.get_bodies_mailing_from_db('pb')

        assert self.get_count_mailing_from_db('ntf') >= 1, "Нотификации не пришли"
        for mail in emails:
            assert mail['templateMeta']['pgLinks'] == self.get_pg_text[product_type][status_code]

    @pytest.mark.parametrize("product_type",
                             ["Vneshnii", "Vnutrennii"])
    def test_notification_start_close_admin_update(self, ppinfo_client, product_type):
        allure.dynamic.title(f"Шаги PG в нотификации при инициирование закрытия - {product_type}")
        with allure.step("Отправляем заявку"):
            body = self.get_data_for_admin_update(start_close=True,
                                                  product_code="BI_2875" if product_type == 'Vneshnii' else "BI_2929")
            self.change_product(ppinfo_client, body)

        emails = self.get_bodies_mailing_from_db('pb')

        assert self.get_count_mailing_from_db('ntf') >= 1, "Нотификации не пришли"

        for mail in emails:
            assert mail['templateMeta']['pgLinks'] == self.get_pg_text[product_type]['init_close']

    @allure.title('debug pg noti')
    def test1(self):

        pass

        # gen_name = self.text
        # self.create_product(self.get_data_for_product_creation("Vnutrennii", name=gen_name, status="(PPinfo_status)Pilot"))

        # body = self.get_data_for_admin_update_status("Vneshnii", "(PPinfo_status)Out_of_use")
        # self.change_product(body)

        # name = self.text
        # body = self.get_body_for_brief_creation("Vneshnii", name, status="(PPinfo_status)Idea_formation")
        # brief_id = self.crete_brief_by_user(body)
        # self.take_to_work(brief_id, {"login": "ddsvetov1"})
        # self.delete_mailing_from_db('pb')
        # self.change_brief_status(brief_id, {"status": 'statusApproval'})

        # body = self.get_data_for_user_update_status("Vneshnii", "(PPinfo_status)Pilot")
        # brief_id = self.crete_brief_by_user(body)
        # self.take_to_work(brief_id, {"login": "ddsvetov1"})
        # self.delete_mailing_from_db('pb')
        # self.change_brief_status(brief_id, {"status": 'statusApproval'})

        # body = self.get_data_for_admin_update(start_close=True,
        #                                       product_code="BI_2875")
        # self.change_product(body)
