import allure
import pytest

from API.models.notification.notification import Notifications

NAME = "Тест Notification (название не менять)"


@pytest.mark.api
@pytest.mark.notification
@allure.feature("Нотификации")
@pytest.mark.usefixtures('clear_db_notifications')
@allure.issue('https://jira.mts.ru/browse/PPI-3849',
              'PPInfo - Уведомлять группу сотрудников о закрытии продукта')
class TestNotificationCloseGroup(Notifications):

    ####### Группы информирования по закрытию
    @allure.title(
        "Нотификация группе информирования по закрытию / Админ / Редактирование продукта")
    @pytest.mark.parametrize('product_type', ['Vneshnii', 'Vnutrennii'])
    def test_notification_closed_admin_update_accept_inform(self, ppinfo_client, product_type):
        with allure.step("Отправляем заявку"):
            body = self.get_data_for_admin_update_status(product_type=product_type,
                                                         status_attribute_code='(PPinfo_status)In_use')
            self.change_product(ppinfo_client, body)

            self.delete_mailing_from_db('pb')

            body = self.get_data_for_admin_update_status(product_type=product_type, status_attribute_code='Arkhiv')
            self.change_product(ppinfo_client, body)

        emails = self.get_bodies_mailing_from_db('pb')

        recipients = sorted([sorted(mail['to']) for mail in emails], key=lambda lst: (len(lst), lst))

        assert len(recipients) == 6, f'Письма не отправлены\n {recipients}'

        expected_recipients = ['ddsvetov1@mts.ru', 'ganekrasov@mts.ru'] if product_type == 'Vneshnii' else [
            'a.y.smirnov@mgts.ru', 'ddsvetov1@mts.ru']

        assert recipients[-1] == expected_recipients, f'Админ не получили письмо \n {recipients[0]}'

        assert self.get_count_mailing_from_db('ntf') == 11, (
            f'По данному операции должны были отправится 11 писем, а отправилось {self.get_count_mailing_from_db("ntf")} писем: \n'
            'Админу об Инициировании закрытия\n'
            'Инициатор и группа информирования  об Инициировании закрытия\n')
