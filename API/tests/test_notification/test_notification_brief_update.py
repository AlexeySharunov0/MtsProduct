import allure
import pytest

from API.models.notification.notification import Notifications

NAME = "Тест Notification (название не менять)"


@pytest.mark.api
@pytest.mark.notification
@allure.feature("Нотификации")
@pytest.mark.usefixtures('clear_db_notifications')
class TestNotificationBriefUpdate(Notifications):

    @allure.title("Нотификация / Заявка / Редактирование / Отправка заявки")
    def test_notification_brief_update_send(self, ppinfo_client, ppinfo_user_client):
        self.set_default_settings(ppinfo_client)
        with allure.step("Отправляем заявку"):
            body = self.get_body_for_brief_update()
            brief_id = self.crete_brief_by_user(ppinfo_user_client, body)
            number = "№ " + self.get_brief_by_id(ppinfo_client, brief_id)["number"]

        emails = self.get_bodies_mailing_from_db('pb')

        recipients = sorted([sorted(mail['to']) for mail in emails], key=lambda lst: (len(lst), lst))
        subjects = sorted([mail['templateMeta']['subject'] for mail in emails],
                          key=lambda subject: (len(subject), subject))

        assert len(recipients) == 2, f'Письма не отправлены\n {recipients}'

        assert recipients[0] == ['aikostrov1@mts.ru'], f'Инициатор не получили письмо \n {recipients[0]}'

        assert recipients[1] == ['pymaslenkov@mts.ru'], f'Админ не получили письмо \n {recipients[1]}'

        assert subjects[
                   0] == f'Вам направлена заявка {number} на редактирование продукта «{NAME}»', f'У письма некорректный заголовок, сейчас заголовок - ={emails[0]["templateMeta"]["subject"]}'

        assert subjects[
                   1] == f'Заявка  {number} на редактирование продукта «{NAME}»  отправлена на модерацию', f'У письма некорректный заголовок, сейчас заголовок - ={emails[0]["templateMeta"]["subject"]}'

        assert self.get_count_mailing_from_db('ntf') == 2, (
            f'По данному операции должны были отправится 2 писем, а отправилось {self.get_count_mailing_from_db("ntf")} писем: \n'
            'Админу о получении заявки\n'
            'Инициатору об отправке заявки\n')

    @allure.title("Нотификация / Заявка / Редактирование продукта / Взятие в работу")
    def test_notification_brief_update_take_to_work(self, ppinfo_client, ppinfo_user_client):
        with allure.step("Отправляем заявку"):
            body = self.get_body_for_brief_update()
            brief_id = self.crete_brief_by_user(ppinfo_user_client, body)
            number = "№ " + self.get_brief_by_id(ppinfo_client, brief_id)["number"]
            self.delete_mailing_from_db('pb')
            self.take_to_work(ppinfo_client, brief_id, {"login": "asnikiforov1"})

        emails = self.get_bodies_mailing_from_db('pb')

        recipients = sorted([sorted(mail['to']) for mail in emails], key=lambda lst: (len(lst), lst))
        subjects = sorted([mail['templateMeta']['subject'] for mail in emails],
                          key=lambda subject: (len(subject), subject))

        assert len(recipients) == 2, f'Письма не отправлены\n {recipients}'

        assert recipients[0] == ['aikostrov1@mts.ru'], f'Инициатор не получили письмо \n {recipients[0]}'

        assert recipients[1] == ['pymaslenkov@mts.ru'], f'Админ не получили письмо \n {recipients[1]}'

        assert subjects[
                   0] == f'Заявка {number} на редактирование продукта «{NAME}» — взята в работу', f'У письма некорректный заголовок, сейчас заголовок - ={emails[0]["templateMeta"]["subject"]}'

        assert subjects[
                   1] == f'Заявка {number} на редактирование продукта «{NAME}» — взята в работу', f'У письма некорректный заголовок, сейчас заголовок - ={emails[0]["templateMeta"]["subject"]}'

        assert self.get_count_mailing_from_db('ntf') == 4, (
            f'По данному операции должны были отправится 4 писем, а отправилось {self.get_count_mailing_from_db("ntf")} писем: \n'
            'Админу о получении заявки\n'
            'Инициатору об отправке заявки\n'
            'Админу о взятии заявки в работу\n'
            'Инициатору о взятии заявки в работу\n')

    @allure.title("Нотификация / Заявка / Редактирование продукта / Принятие с информированием")
    def test_notification_brief_update_accept_inform(self, ppinfo_client, ppinfo_user_client):

        self.send_brief_to_replace_product(ppinfo_client, ppinfo_user_client, 'statusApproval',
                                           body=self.get_body_for_brief_update())

        emails = self.get_bodies_mailing_from_db('pb')

        recipients = sorted([sorted(mail['to']) for mail in emails], key=lambda lst: (len(lst), lst))
        subjects = sorted([mail['templateMeta']['subject'] for mail in emails],
                          key=lambda subject: (len(subject), subject))

        assert len(recipients) == 6, f'Письма не отправлены\n {recipients}'

        assert recipients[0] == ['aastrunin@mts.ru'], f'ПО не получили письмо \n {recipients[0]}'

        assert recipients[1] == ['aikostrov1@mts.ru'], f'Инициатор не получили письмо \n {recipients[1]}'

        assert recipients[2] == ['nolesnikov@mts.ru'], f'СПО не получили письмо \n {recipients[2]}'

        assert recipients[3] == ['pymaslenkov@mts.ru'], f'Админ не получили письмо \n {recipients[3]}'

        assert recipients[4] == ['snkondratyev@mts.ru'], f'Группа информирования не получили письмо \n {recipients[4]}'

        assert recipients[5] == ['zimina@mts.ru'], f'БО не получили письмо \n {recipients[5]}'

        for subject in subjects:
            assert subject == f'Продукт «{NAME}» отредактирован', f'У письма некорректный заголовок, сейчас заголовок - ={emails[0]["templateMeta"]["subject"]}'

        assert self.get_count_mailing_from_db('ntf') == 10, (
            f'По данному операции должны были отправится 10 писем, а отправилось {self.get_count_mailing_from_db("ntf")} писем: \n'
            'Админу о получении заявки\n'
            'Инициатору об отправке заявки\n'
            'Админу о взятии заявки в работу\n'
            'Инициатору о взятии заявки в работу\n'
            'Админу редактирование продукта\n'
            'СПО редактирование продукта\n'
            'ПО редактирование продукта\n'
            'БО редактирование продукта\n'
            'Инициатор редактирование продукта\n'
            'Группе информированияредактирование продукта\n')

    @allure.title("Нотификация / Заявка / Редактирование продукта / Отклонение с информированием")
    def test_notification_brief_update_deny_inform(self, ppinfo_client, ppinfo_user_client):

        self.send_brief_to_replace_product(ppinfo_client, ppinfo_user_client, 'statusDeclined',
                                           body=self.get_body_for_brief_update())

        emails = self.get_bodies_mailing_from_db('pb')

        recipients = sorted([sorted(mail['to']) for mail in emails], key=lambda lst: (len(lst), lst))

        assert len(recipients) == 2, f'Письма не отправлены\n {recipients}'

        assert recipients[0] == ['aikostrov1@mts.ru'], f'Инициатор не получили письмо \n {recipients[0]}'

        assert recipients[1] == ['pymaslenkov@mts.ru'], f'Инициатор не получили письмо \n {recipients[1]}'

        assert self.get_count_mailing_from_db('ntf') == 6, (
            f'По данному операции должны были отправится 6 писем, а отправилось {self.get_count_mailing_from_db("ntf")} писем: \n'
            'Админу о получении заявки\n'
            'Инициатору об отправке заявки\n'
            'Админу о взятии заявки в работу\n'
            'Инициатору о взятии заявки в работу\n'
            'Админу редактирование продукта\n'
            'Инициатор редактирование продукта\n')

    @allure.title("Нотификация / Заявка / Редактирование продукта / Принятие без информирования")
    @allure.issue('https://jira.mts.ru/browse/PPI-2314',
                  'PPinfo - Не приходит нотификация админу при принятии заявки с отключенным информированием')
    def test_notification_brief_update_accept_no_inform(self, ppinfo_client, ppinfo_user_client):

        self.send_brief_to_replace_product(ppinfo_client, ppinfo_user_client, 'statusApproval',
                                           body=self.get_body_for_brief_update(notification=False))

        emails = self.get_bodies_mailing_from_db('pb')

        recipients = sorted([sorted(mail['to']) for mail in emails], key=lambda lst: (len(lst), lst))

        assert len(recipients) == 2, f'Письма не отправлены\n {recipients}'

        assert recipients[0] == ['aikostrov1@mts.ru'], f'Инициатор не получили письмо \n {recipients[0]}'

        assert recipients[1] == ['pymaslenkov@mts.ru'], f'Инициатор не получили письмо \n {recipients[1]}'

        assert self.get_count_mailing_from_db('ntf') == 6, (
            f'По данному операции должны были отправится 6 писем, а отправилось {self.get_count_mailing_from_db("ntf")} писем: \n'
            'Админу о получении заявки\n'
            'Инициатору об отправке заявки\n'
            'Админу о взятии заявки в работу\n'
            'Инициатору о взятии заявки в работу\n'
            'Админу редактирование продукта\n'
            'Инициатор редактирование продукта\n')

    @allure.title("Нотификация / Заявка / Редактирование продукта / Отклонение без информирования")
    def test_notification_brief_update_deny_no_inform(self, ppinfo_client, ppinfo_user_client):

        self.send_brief_to_replace_product(ppinfo_client, ppinfo_user_client, 'statusDeclined',
                                           body=self.get_body_for_brief_update(notification=False))

        emails = self.get_bodies_mailing_from_db('pb')

        recipients = sorted([sorted(mail['to']) for mail in emails], key=lambda lst: (len(lst), lst))

        assert len(recipients) == 2, f'Письма не отправлены\n {recipients}'

        assert recipients[0] == ['aikostrov1@mts.ru'], f'Инициатор не получили письмо \n {recipients[0]}'

        assert recipients[1] == ['pymaslenkov@mts.ru'], f'Инициатор не получили письмо \n {recipients[1]}'

        assert self.get_count_mailing_from_db('ntf') == 6, (
            f'По данному операции должны были отправится 6 писем, а отправилось {self.get_count_mailing_from_db("ntf")} писем: \n'
            'Админу о получении заявки\n'
            'Инициатору об отправке заявки\n'
            'Админу о взятии заявки в работу\n'
            'Инициатору о взятии заявки в работу\n'
            'Админу редактирование продукта\n'
            'Инициатор редактирование продукта\n')

    @allure.title("Нотификация / Автосогласование / Редактирование продукта / Принятие с информированием")
    def test_notification_brief_auto_update_accept_inform(self, ppinfo_client):
        with allure.step("Отправляем заявку"):
            body = self.get_body_for_brief_update()
            self.crete_brief_by_admin(ppinfo_client, body)

        emails = self.get_bodies_mailing_from_db('pb')

        recipients = sorted([sorted(mail['to']) for mail in emails], key=lambda lst: (len(lst), lst))

        assert len(recipients) == 6, f'Письма не отправлены\n {recipients}'

        assert recipients[0] == ['aastrunin@mts.ru'], f'СТО не получили письмо \n {recipients[0]}'

        assert recipients[1] == ['ddsvetov1@mts.ru'], f'Согласующий не получили письмо \n {recipients[1]}'

        assert recipients[2] == ['nolesnikov@mts.ru'], f'СПО не получили письмо \n {recipients[2]}'

        assert recipients[3] == ['pymaslenkov@mts.ru'], f'Админ не получили письмо \n {recipients[3]}'

        assert recipients[4] == ['snkondratyev@mts.ru'], f'Инициатор не получили письмо \n {recipients[4]}'

        assert recipients[5] == ['zimina@mts.ru'], f'Группа информирования не получили письмо \n {recipients[5]}'

        assert self.get_count_mailing_from_db('ntf') == 6, (
            f'По данному операции должны были отправится 6 писем, а отправилось {self.get_count_mailing_from_db("ntf")} писем: \n'
            'Админу редактирование продукта\n'
            'СПО редактирование продукта\n'
            'ПО редактирование продукта\n'
            'БО редактирование продукта\n'
            'Инициатор редактирование продукта\n'
            'Группе информирования редактирование продукта\n')

    @allure.title("Нотификация / Автосогласование / Редактирование продукта / Принятие без информирования")
    @allure.issue('https://jira.mts.ru/browse/PPI-2314',
                  'PPinfo - Не приходит нотификация админу при принятии заявки с отключенным информированием')
    def test_notification_brief_auto_update_accept_no_inform(self, ppinfo_client):
        with allure.step("Отправляем заявку"):
            body = self.get_body_for_brief_update(notification=False)
            self.crete_brief_by_admin(ppinfo_client, body)

        emails = self.get_bodies_mailing_from_db('pb')

        recipients = sorted([sorted(mail['to']) for mail in emails], key=lambda lst: (len(lst), lst))

        assert len(recipients) == 2, f'Письма не отправлены\n {recipients}'

        assert recipients[0] == ['ddsvetov1@mts.ru'], f'Инициатор не получили письмо \n {recipients[0]}'

        assert recipients[1] == ['pymaslenkov@mts.ru'], f'Админ не получили письмо \n {recipients[1]}'

        assert self.get_count_mailing_from_db('ntf') == 2, (
            f'По данному операции должны были отправится 2 писем, а отправилось {self.get_count_mailing_from_db("ntf")} писем: \n'
            'Админу редактирование продукта\n'
            'Инициатор редактирование продукта\n')

    ####### Уведомления руководству
    @allure.title("Нотификация рук-ву / Заявка / Редактирование продукта / Принятие с информированием")
    @allure.issue('https://jira.mts.ru/browse/PPI-2323',
                  'PPinfo - Не приходит нотификация руководству при редактировании атрибутов')
    @pytest.mark.parametrize('auto_accept', [True, False])
    def test_notification_users_brief_update_accept_inform(self, ppinfo_client, ppinfo_user_client, auto_accept):
        with allure.step("Отправляем заявку"):
            self.change_attr_in_settings(ppinfo_client, enable=True)
            body = self.get_body_for_brief_update()
            if auto_accept:
                with allure.step('Заявка на автосогласовании'):
                    self.crete_brief_by_admin(ppinfo_client, body)
            else:
                self.send_brief_to_replace_product(ppinfo_client, ppinfo_user_client, 'statusApproval',
                                                   body=body)

        emails = self.get_bodies_mailing_from_db('pb')

        recipients = sorted([sorted(mail['to']) for mail in emails], key=lambda lst: (len(lst), lst))

        print(recipients)

        assert len(recipients) == 6, f'Письма не отправлены\n {recipients}'

        assert recipients[0] == ['aastrunin@mts.ru'], f'СТО не получили письмо \n {recipients[0]}'

        assert recipients[1] == ['ddsvetov1@mts.ru'] if auto_accept else [
            'aikostrov1@mts.ru'], f'Согласующий не получили письмо \n {recipients[1]}'

        assert recipients[2] == ['nolesnikov@mts.ru'], f'СПО не получили письмо \n {recipients[2]}'

        assert recipients[3] == ['pymaslenkov@mts.ru'], f'Админ не получили письмо \n {recipients[3]}'

        assert recipients[4] == ['snkondratyev@mts.ru'], f'Инициатор не получили письмо \n {recipients[4]}'

        assert recipients[5] == ['zimina@mts.ru'], f'Группа информирования не получили письмо \n {recipients[5]}'

        assert self.get_count_mailing_from_db('ntf') == 6 if auto_accept else 10, (
            f'По данному операции должны были отправится 6 или 10 писем, а отправилось {self.get_count_mailing_from_db("ntf")} писем: \n'
            'Админу редактирование продукта\n'
            'СПО редактирование продукта\n'
            'ПО редактирование продукта\n'
            'БО редактирование продукта\n'
            'Инициатор редактирование продукта\n'
            'Группе информирования редактирование продукта\n')

    @allure.title("Нотификация рук-ву / Заявка / Редактирование продукта/Принятие с информированием/Атрибут отключен")
    def test_notification_users_brief_update_accept_inform_no_attr(self, ppinfo_client, ppinfo_user_client):

        self.change_attr_in_settings(ppinfo_client, enable=False)

        self.send_brief_to_replace_product(ppinfo_client, ppinfo_user_client, 'statusApproval',
                                           body=self.get_body_for_brief_update())

        emails = self.get_bodies_mailing_from_db('pb')

        recipients = sorted([sorted(mail['to']) for mail in emails], key=lambda lst: (len(lst), lst))

        assert len(recipients) == 6, f'Письма не отправлены\n {recipients}'

        assert recipients[0] == ['aastrunin@mts.ru'], f'СТО не получили письмо \n {recipients[0]}'

        assert recipients[1] == ['aikostrov1@mts.ru'], f'Согласующий не получили письмо \n {recipients[1]}'

        assert recipients[2] == ['nolesnikov@mts.ru'], f'СПО не получили письмо \n {recipients[2]}'

        assert recipients[3] == ['pymaslenkov@mts.ru'], f'Админ не получили письмо \n {recipients[3]}'

        assert recipients[4] == ['snkondratyev@mts.ru'], f'Инициатор не получили письмо \n {recipients[4]}'

        assert recipients[5] == ['zimina@mts.ru'], f'Группа информирования не получили письмо \n {recipients[5]}'

        assert self.get_count_mailing_from_db('ntf') == 10, (
            f'По данному операции должны были отправится 10 писем, а отправилось {self.get_count_mailing_from_db("ntf")} писем: \n'
            'Админу редактирование продукта\n'
            'СПО редактирование продукта\n'
            'ПО редактирование продукта\n'
            'БО редактирование продукта\n'
            'Инициатор редактирование продукта\n'
            'Группе информирования редактирование продукта\n')

    @allure.title("Нотификация рук-ву / Заявка / Редактирование продукта / Отклонение с информированием")
    def test_notification_users_brief_update_deny_inform(self, ppinfo_client, ppinfo_user_client):

        self.send_brief_to_replace_product(ppinfo_client, ppinfo_user_client, 'statusDeclined',
                                           body=self.get_body_for_brief_update())

        emails = self.get_bodies_mailing_from_db('pb')

        recipients = sorted([sorted(mail['to']) for mail in emails], key=lambda lst: (len(lst), lst))

        assert len(recipients) == 2, f'Письма не отправлены\n {recipients}'

        assert recipients[0] == ['aikostrov1@mts.ru'], f'Инициатор не получили письмо \n {recipients[0]}'

        assert recipients[1] == ['pymaslenkov@mts.ru'], f'Админ не получили письмо \n {recipients[1]}'

        assert self.get_count_mailing_from_db('ntf') == 6, (
            f'По данному операции должны были отправится 6 писем, а отправилось {self.get_count_mailing_from_db("ntf")} писем: \n'
            'Админу о получении заявки\n'
            'Инициатору об отправке заявки\n'
            'Админу о взятии заявки в работу\n'
            'Инициатору о взятии заявки в работу\n'
            'Админу о добавлении продукта\n'
            'Инициатору о добавлении продукта\n'
        )

    @allure.title("Нотификация рук-ву / Заявка / Редактирование продукта / Принятие без информирования")
    @pytest.mark.parametrize('auto_accept', [True, False])
    def test_notification_users_brief_update_accept_no_inform(self, ppinfo_client, ppinfo_user_client, auto_accept):
        with allure.step("Отправляем заявку"):
            body = self.get_body_for_brief_update(notification=False)
            if auto_accept:
                with allure.step('Заявка на автосогласовании'):
                    self.crete_brief_by_admin(ppinfo_client, body)
            else:
                self.send_brief_to_replace_product(ppinfo_client, ppinfo_user_client, 'statusApproval', body=body)

        emails = self.get_bodies_mailing_from_db('pb')

        recipients = sorted([sorted(mail['to']) for mail in emails], key=lambda lst: (len(lst), lst))

        assert len(recipients) == 2, f'Письма не отправлены\n {recipients}'

        assert recipients[0] == ['ddsvetov1@mts.ru'] if auto_accept else [
            'aikostrov1@mts.ru'], f'Инициатор не получили письмо \n {recipients[0]}'

        assert recipients[1] == ['pymaslenkov@mts.ru'], f'Админ не получили письмо \n {recipients[1]}'

        assert self.get_count_mailing_from_db('ntf') == 2 if auto_accept else 8, (
            f'По данному операции должны были отправится 2 или 8 писем, а отправилось {self.get_count_mailing_from_db("ntf")} писем: \n'
            'Админу о получении заявки\n'
            'Инициатору об отправке заявки\n'
            'Админу о взятии заявки в работу\n'
            'Инициатору о взятии заявки в работу\n'
            'Админу о добавлении продукта\n'
            'Инициатору о добавлении продукта\n'
        )

    @allure.title("Нотификация рук-ву/ Заявка / Редактирование продукта / Отклонение без информирования")
    def test_notification_users_brief_update_deny_no_inform(self, ppinfo_client, ppinfo_user_client):

        self.send_brief_to_replace_product(ppinfo_client, ppinfo_user_client, 'statusDeclined',
                                           body=self.get_body_for_brief_update(notification=False))

        emails = self.get_bodies_mailing_from_db('pb')

        recipients = sorted([sorted(mail['to']) for mail in emails], key=lambda lst: (len(lst), lst))

        assert len(recipients) == 2, f'Письма не отправлены\n {recipients}'

        assert recipients[0] == ['aikostrov1@mts.ru'], f'Инициатор не получили письмо \n {recipients[0]}'

        assert recipients[1] == ['pymaslenkov@mts.ru'], f'Админ не получили письмо \n {recipients[1]}'

        assert self.get_count_mailing_from_db('ntf') == 6, (
            f'По данному операции должны были отправится 6 писем, а отправилось {self.get_count_mailing_from_db("ntf")} писем: \n'
            'Админу о получении заявки\n'
            'Инициатору об отправке заявки\n'
            'Админу о взятии заявки в работу\n'
            'Инициатору о взятии заявки в работу\n'
            'Админу о добавлении продукта\n'
            'Инициатору о добавлении продукта\n'
        )

    ####### Уведомления группе иниц. закрытие
    @allure.title("Нотификация иниц. закрытие / Заявка / Редактирование продукта / Принятие с информированием")
    @allure.issue('https://jira.mts.ru/browse/PPI-2326',
                  'PPinfo - Нет нотификации группе заинтересованной в иницированно закрытие')
    @pytest.mark.parametrize('auto_accept', [True, False])
    def test_notification_start_close_brief_update_accept_inform(self, ppinfo_client, ppinfo_user_client, auto_accept):
        with allure.step("Отправляем заявку"):
            body = self.get_body_for_brief_update_start_close()
            if auto_accept:
                with allure.step('Заявка на автосогласовании'):
                    self.crete_brief_by_admin(ppinfo_client, body)
            else:
                self.send_brief_to_replace_product(ppinfo_client, ppinfo_user_client, 'statusApproval',
                                                   body=body)

        emails = self.get_bodies_mailing_from_db('pb')

        recipients = sorted([sorted(mail['to']) for mail in emails], key=lambda lst: (len(lst), lst))

        assert len(recipients) == 3, f'Письма не отправлены\n {recipients}'

        assert recipients[0] == ['ddsvetov1@mts.ru'] if auto_accept else [
            'aikostrov1@mts.ru'], f'Инициатор не получили письмо \n {recipients[0]}'

        assert recipients[1] == ['pymaslenkov@mts.ru'], f'Админ не получили письмо \n {recipients[1]}'

        assert recipients[2] == ['ddsvetov1@mts.ru', 'sskopytin@mts.ru',
                                 'ysgurkov1@mts.ru'], f'Админ не получили письмо \n {recipients[2]}'

        assert self.get_count_mailing_from_db('ntf') == 3 if auto_accept else 10, (
            f'По данному операции должны были отправится 3 или 10 писем, а отправилось {self.get_count_mailing_from_db("ntf")} писем: \n'
            'Админу о получении заявки\n'
            'Инициатору об отправке заявки\n'
            'Админу о взятии заявки в работу\n'
            'Инициатору о взятии заявки в работу\n'
            'Админу о добавлении продукта\n'
            'Инициатору о добавлении продукта\n'
        )

    @allure.title("Нотификация иниц. закрытие / Заявка / Редактирование продукта / Отклонение с информированием")
    def test_notification_start_close_brief_update_deny_inform(self, ppinfo_client, ppinfo_user_client):

        self.send_brief_to_replace_product(ppinfo_client, ppinfo_user_client, 'statusDeclined',
                                           body=self.get_body_for_brief_update())

        emails = self.get_bodies_mailing_from_db('pb')

        recipients = sorted([sorted(mail['to']) for mail in emails], key=lambda lst: (len(lst), lst))

        assert len(recipients) == 2, f'Письма не отправлены\n {recipients}'

        assert recipients[0] == ['aikostrov1@mts.ru'], f'Инициатор не получили письмо \n {recipients[0]}'

        assert recipients[1] == ['pymaslenkov@mts.ru'], f'Админ не получили письмо \n {recipients[1]}'

        assert self.get_count_mailing_from_db('ntf') == 6, (
            f'По данному операции должны были отправится 6 писем, а отправилось {self.get_count_mailing_from_db("ntf")} писем: \n'
            'Админу о получении заявки\n'
            'Инициатору об отправке заявки\n'
            'Админу о взятии заявки в работу\n'
            'Инициатору о взятии заявки в работу\n'
            'Админу о добавлении продукта\n'
            'Инициатору о добавлении продукта\n'
        )

    @allure.title("Нотификация иниц. закрытие / Заявка / Редактирование продукта / Принятие без информирования")
    @pytest.mark.parametrize('auto_accept', [True, False])
    def test_notification_start_close_brief_update_accept_no_inform(self, ppinfo_client, ppinfo_user_client,
                                                                    auto_accept):
        with allure.step("Отправляем заявку"):
            body = self.get_body_for_brief_update(notification=False)
            if auto_accept:
                with allure.step('Заявка на автосогласовании'):
                    self.crete_brief_by_admin(ppinfo_client, body)
            else:
                self.send_brief_to_replace_product(ppinfo_client, ppinfo_user_client, 'statusApproval',
                                                   body=body)

        emails = self.get_bodies_mailing_from_db('pb')

        recipients = sorted([sorted(mail['to']) for mail in emails], key=lambda lst: (len(lst), lst))

        assert len(recipients) == 2, f'Письма не отправлены\n {recipients}'

        assert recipients[0] == ['ddsvetov1@mts.ru'] if auto_accept else [
            'aikostrov1@mts.ru'], f'Инициатор не получили письмо \n {recipients[0]}'

        assert recipients[1] == ['pymaslenkov@mts.ru'], f'Админ не получили письмо \n {recipients[1]}'

        assert self.get_count_mailing_from_db('ntf') == 2 if auto_accept else 10, (
            f'По данному операции должны были отправится 2 или 10 писем, а отправилось {self.get_count_mailing_from_db("ntf")} писем: \n'
            'Админу о получении заявки\n'
            'Инициатору об отправке заявки\n'
            'Админу о взятии заявки в работу\n'
            'Инициатору о взятии заявки в работу\n'
            'Админу о добавлении продукта\n'
            'Инициатору о добавлении продукта\n'
        )

    @allure.title("Нотификация иниц. закрытие/ Заявка / Редактирование продукта / Отклонение без информирования")
    def test_notification_start_close_brief_update_deny_no_inform(self, ppinfo_client, ppinfo_user_client):
        self.send_brief_to_replace_product(ppinfo_client, ppinfo_user_client, 'statusDeclined',
                                           body=self.get_body_for_brief_update(notification=False))

        emails = self.get_bodies_mailing_from_db('pb')

        recipients = sorted([sorted(mail['to']) for mail in emails], key=lambda lst: (len(lst), lst))

        assert len(recipients) == 2, f'Письма не отправлены\n {recipients}'

        assert recipients[0] == ['aikostrov1@mts.ru'], f'Инициатор не получили письмо \n {recipients[0]}'

        assert recipients[1] == ['pymaslenkov@mts.ru'], f'Админ не получили письмо \n {recipients[1]}'

        assert self.get_count_mailing_from_db('ntf') == 6, (
            f'По данному операции должны были отправится 6 писем, а отправилось {self.get_count_mailing_from_db("ntf")} писем: \n'
            'Админу о получении заявки\n'
            'Инициатору об отправке заявки\n'
            'Админу о взятии заявки в работу\n'
            'Инициатору о взятии заявки в работу\n'
            'Админу о добавлении продукта\n'
            'Инициатору о добавлении продукта\n'
        )

    ####### Кастомная группа
    @allure.title("Нотификация кастомной группе / Заявка / Редактирование продукта / Принятие с информированием")
    @pytest.mark.parametrize('auto_accept', [True, False])
    @pytest.mark.parametrize('product_type, key_word', [['external', 'Notification'], ['internal', 'manual']])
    def test_notification_custom_group_brief_update_accept_inform(self, ppinfo_client, ppinfo_user_client, product_type,
                                                                  key_word, auto_accept):
        with allure.step("Отправляем заявку"):
            body = self.get_body_for_brief_update() if product_type == 'external' else self.get_body_for_brief_update_custom()
            if auto_accept:
                with allure.step('Заявка на автосогласовании'):
                    self.crete_brief_by_admin(ppinfo_client, body)
            else:
                brief_id = self.crete_brief_by_user(ppinfo_user_client, body)
                self.take_to_work(ppinfo_client, brief_id, {"login": "asnikiforov1"})
                self.delete_mailing_from_db('pb')
                self.change_brief_status(ppinfo_client, brief_id, {"status": "statusApproval"})

        emails = self.get_bodies_mailing_from_db('pb')

        recipients = sorted([sorted(mail['to']) for mail in emails], key=lambda lst: (len(lst), lst))

        with allure.step(f"Проверяем, что кастомная группа получили корректное письмо для типа {product_type}"):
            flattened_list = [email for sublist in recipients for email in sublist]
            assert 'snkondratyev@mts.ru' in flattened_list, 'Кастоманая группа не получили сообщение'

    @allure.title("Нотификация кастомной группе / Заявка / Редактирование продукта / Отклонение с информированием")
    @pytest.mark.parametrize('product_type, key_word', [['external', 'Notification'], ['internal', 'manual']])
    def test_notification_custom_group_brief_update_deny_inform(self, ppinfo_client, ppinfo_user_client, product_type,
                                                                key_word):
        with allure.step("Отправляем заявку"):
            body = self.get_body_for_brief_update() if product_type == 'external' else self.get_body_for_brief_update_custom()
            brief_id = self.crete_brief_by_user(ppinfo_user_client, body)
            self.take_to_work(ppinfo_client, brief_id, {"login": "asnikiforov1"})
            self.delete_mailing_from_db('pb')
            self.change_brief_status(ppinfo_client, brief_id, {"status": "statusDeclined"})

        emails = self.get_bodies_mailing_from_db('pb')

        recipients = sorted([sorted(mail['to']) for mail in emails], key=lambda lst: (len(lst), lst))

        with allure.step(f"Проверяем, что кастомная группа получили корректное письмо для типа {product_type}"):
            assert 'snkondratyev@mts.ru' not in recipients, 'Катомная группа получили сообщение, хотя не должны были'

    @allure.title("Нотификация кастомной группе / Заявка / Редактирование продукта / Принятие без информирования")
    @pytest.mark.parametrize('auto_accept', [True, False])
    @pytest.mark.parametrize('product_type, key_word', [['external', 'Notification'], ['internal', 'manual']])
    def test_notification_custom_group_brief_update_accept_no_inform(self, ppinfo_client, ppinfo_user_client,
                                                                     product_type, key_word, auto_accept):
        with allure.step("Отправляем заявку"):
            body = self.get_body_for_brief_update(
                notification=False) if product_type == 'external' else self.get_body_for_brief_update_custom(
                notification=False)
            if auto_accept:
                with allure.step('Заявка на автосогласовании'):
                    self.delete_mailing_from_db('pb')
                    self.crete_brief_by_admin(ppinfo_client, body)
            else:
                brief_id = self.crete_brief_by_user(ppinfo_user_client, body)
                self.take_to_work(ppinfo_client, brief_id, {"login": "asnikiforov1"})
                self.delete_mailing_from_db('pb')
                self.change_brief_status(ppinfo_client, brief_id, {"status": "statusApproval"})

        emails = self.get_bodies_mailing_from_db('pb')

        recipients = sorted([sorted(mail['to']) for mail in emails], key=lambda lst: (len(lst), lst))

        with allure.step(f"Проверяем, что кастомная группа получили корректное письмо для типа {product_type}"):
            assert 'snkondratyev@mts.ru' not in recipients, 'Катомная группа получили сообщение, хотя не должны были'

    @allure.title("Нотификация кастомной группе/ Заявка / Редактирование продукта / Отклонение без информирования")
    @pytest.mark.parametrize('product_type, key_word', [['external', 'Notification'], ['internal', 'manual']])
    def test_notification_custom_group_brief_update_deny_no_inform(self, ppinfo_client, ppinfo_user_client,
                                                                   product_type, key_word):
        with allure.step("Отправляем заявку"):
            body = self.get_body_for_brief_update(
                notification=False) if product_type == 'external' else self.get_body_for_brief_update_custom(
                notification=False)
            brief_id = self.crete_brief_by_user(ppinfo_user_client, body)
            self.take_to_work(ppinfo_client, brief_id, {"login": "asnikiforov1"})
            self.delete_mailing_from_db('pb')
            self.change_brief_status(ppinfo_client, brief_id, {"status": "statusDeclined"})

        emails = self.get_bodies_mailing_from_db('pb')

        recipients = sorted([sorted(mail['to']) for mail in emails], key=lambda lst: (len(lst), lst))

        with allure.step(f"Проверяем, что кастомная группа получили корректное письмо для типа {product_type}"):
            assert 'snkondratyev@mts.ru' not in recipients, 'Катомная группа получили сообщение, хотя не должны были'
