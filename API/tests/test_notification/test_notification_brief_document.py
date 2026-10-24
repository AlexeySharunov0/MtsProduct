import allure
import pytest

from API.models.notification.notification import Notifications

NAME = "Тест Notification (название не менять)"


@pytest.mark.api
@pytest.mark.notification
@allure.feature("Нотификации")
@pytest.mark.usefixtures('clear_db_notifications')
class TestNotificationBriefDocument(Notifications):

    @allure.title("Нотификация / Заявка / Добавление документа / Отправка заявки")
    def test_notification_brief_document_send(self, ppinfo_user_api_client, ppinfo_client, ppinfo_user_client):
        self.set_default_settings(ppinfo_client)
        with allure.step("Отправляем заявку"):
            body = self.get_data_for_doc_brief()
            brief_id = self.post_brief_doc_user(ppinfo_user_api_client, body=body)
            number = "№ " + self.get_brief_by_id(ppinfo_client, brief_id)["number"]

        emails = self.get_bodies_mailing_from_db('pb')

        recipients = sorted([sorted(mail['to']) for mail in emails], key=lambda lst: (len(lst), lst))
        subjects = sorted([mail['templateMeta']['subject'] for mail in emails],
                          key=lambda subject: (len(subject), subject))

        assert len(recipients) == 2, f'Письма не отправлены\n {recipients}'

        assert recipients[0] == ['aikostrov1@mts.ru'], f'Инициатор не получили письмо \n {recipients[0]}'

        assert recipients[1] == ['pymaslenkov@mts.ru'], f'Админ не получили письмо \n {recipients[1]}'

        assert subjects[
                   0] == f'Вам направлена заявка {number} на добавление документа в продукт «{NAME}»', f'У письма некорректный заголовок, сейчас заголовок - ={emails[0]["templateMeta"]["subject"]}'

        assert subjects[
                   1] == f'Заявка  {number} на добавление документа в продукт «{NAME}»  отправлена на модерацию', f'У письма некорректный заголовок, сейчас заголовок - ={emails[0]["templateMeta"]["subject"]}'

        assert self.get_count_mailing_from_db('ntf') == 2, (f'По данному операции должны были отправится 7 писем, а отправилось {self.get_count_mailing_from_db("ntf")} писем: \n'
                                                            'Админу о получении заявки\n'
                                                            'Инициатору об отправке заявки\n')

    @allure.title("Нотификация / Заявка / Добавление документа / Взятие в работу")
    def test_notification_brief_document_take_to_work(self, ppinfo_user_api_client, ppinfo_client):
        with allure.step("Отправляем заявку"):
            body = self.get_data_for_doc_brief()
            brief_id = self.post_brief_doc_user(ppinfo_user_api_client, body=body)
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
                   0] == f'Заявка {number} на добавление документа в продукт «{NAME}» — взята в работу', f'У письма некорректный заголовок, сейчас заголовок - ={emails[0]["templateMeta"]["subject"]}'

        assert subjects[
                   1] == f'Заявка {number} на добавление документа в продукт «{NAME}» — взята в работу', f'У письма некорректный заголовок, сейчас заголовок - ={emails[0]["templateMeta"]["subject"]}'

        assert self.get_count_mailing_from_db('ntf') == 4, (f'По данному операции должны были отправится 7 писем, а отправилось {self.get_count_mailing_from_db("ntf")} писем: \n'
                                                            'Админу о получении заявки\n'
                                                            'Инициатору об отправке заявки\n'
                                                            'Админу о взятии заявки в работу\n'
                                                            'Инициатору о взятии заявки в работу\n')

    @allure.title("Нотификация / Заявка / Добавление документа / Принятие с информированием")
    @allure.issue("https://jira.mts.ru/browse/PPI-2329",
                  "PPInfo - Перепутаны текстовки в названиях писем в нотификациях при добавлении документа")
    def test_notification_brief_document_accept_inform(self, ppinfo_user_api_client, ppinfo_client):
        number = self.send_brief_to_add_document(ppinfo_user_api_client, ppinfo_client, 'statusApproval')
        emails = self.get_bodies_mailing_from_db('pb')

        recipients = sorted([sorted(mail['to']) for mail in emails], key=lambda lst: (len(lst), lst))
        subjects = sorted([mail['templateMeta']['subject'] for mail in emails],
                          key=lambda subject: (len(subject), subject))

        assert len(recipients) == 3, f'Письма не отправлены\n {recipients}'

        assert recipients[0] == ['aikostrov1@mts.ru'], f'Инициатор не получили письмо \n {recipients[0]}'

        assert recipients[1] == ['pymaslenkov@mts.ru'], f'Админ не получили письмо \n {recipients[1]}'

        assert recipients[2] == ['aastrunin@mts.ru', 'nolesnikov@mts.ru',
                                 'zimina@mts.ru'], f'Админ не получили письмо \n {recipients[2]}'

        assert subjects[
                   0] == f'В продукт «{NAME}» добавлен документ', f'У письма некорректный заголовок, сейчас заголовок - ={subjects[0]}'

        assert subjects[
                   1] == f'Заявка {number} на добавление документа в продукт «{NAME}» принята', f'У письма некорректный заголовок, сейчас заголовок - ={subjects[1]}'

        assert subjects[
                   2] == f'Ваша заявка {number} на добавление документа в продукт «{NAME}» принята', f'У письма некорректный заголовок, сейчас заголовок - ={subjects[2]}'

        assert self.get_count_mailing_from_db('ntf') == 7, (f'По данному операции должны были отправится 7 писем, а отправилось {self.get_count_mailing_from_db("ntf")} писем: \n'
                                                            'Админу о получении заявки\n'
                                                            'Инициатору об отправке заявки\n'
                                                            'Админу о взятии заявки в работу\n'
                                                            'Инициатору о взятии заявки в работу\n'
                                                            'Админу о добавлении документа\n'
                                                            'Инициатору о добавлении документа\n'
                                                            'Руководству о добавлении документа\n'
                                                            )

    @allure.title("Нотификация / Заявка / Добавление документа / Отклонение с информированием")
    def test_notification_brief_document_deny_inform(self, ppinfo_user_api_client, ppinfo_client):
        number = self.send_brief_to_add_document(ppinfo_user_api_client, ppinfo_client, 'statusDeclined')
        emails = self.get_bodies_mailing_from_db('pb')

        recipients = sorted([sorted(mail['to']) for mail in emails], key=lambda lst: (len(lst), lst))
        subjects = sorted([mail['templateMeta']['subject'] for mail in emails],
                          key=lambda subject: (len(subject), subject))

        assert len(recipients) == 2, f'Письма не отправлены\n {recipients}'

        assert recipients[0] == ['aikostrov1@mts.ru'], f'Инициатор не получили письмо \n {recipients[0]}'

        assert recipients[1] == ['pymaslenkov@mts.ru'], f'Админ не получили письмо \n {recipients[1]}'
        assert subjects[
                   0] == f'Заявка {number} на добавление документа в продукт «{NAME}» отклонена', f'У письма некорректный заголовок, сейчас заголовок - ={subjects[0]}'

        assert subjects[
                   1] == f'Заявка {number} на добавление документа в продукт «{NAME}» отклонена', f'У письма некорректный заголовок, сейчас заголовок - ={subjects[1]}'

        assert self.get_count_mailing_from_db('ntf') == 6, (f'По данному операции должны были отправится 7 писем, а отправилось {self.get_count_mailing_from_db("ntf")} писем: \n'
                                                            'Админу о получении заявки\n'
                                                            'Инициатору об отправке заявки\n'
                                                            'Админу о взятии заявки в работу\n'
                                                            'Инициатору о взятии заявки в работу\n'
                                                            'Админу об отклонении заявки\n'
                                                            'Инициатору об отклонении заявки\n')

    @allure.title("Нотификация / Заявка / Добавление документа / Принятие без информирования")
    @allure.issue('https://jira.mts.ru/browse/PPI-2314',
                  'PPinfo - Не приходит нотификация админу при принятии заявки с отключенным информированием')
    def test_notification_brief_document_accept_no_inform(self, ppinfo_user_api_client, ppinfo_client):
        number = self.send_brief_to_add_document(ppinfo_user_api_client, ppinfo_client, 'statusApproval', notification=False)
        emails = self.get_bodies_mailing_from_db('pb')

        recipients = sorted([sorted(mail['to']) for mail in emails], key=lambda lst: (len(lst), lst))
        subjects = sorted([mail['templateMeta']['subject'] for mail in emails],
                          key=lambda subject: (len(subject), subject))

        assert len(recipients) == 1, f'Письма не отправлены\n {recipients}'

        assert recipients[0] == ['aikostrov1@mts.ru'], f'Инициатор не получили письмо \n {recipients[0]}'

        assert subjects[
                   0] == f'Ваша заявка {number} на добавление документа в продукт «{NAME}» принята', f'У письма некорректный заголовок, сейчас заголовок - ={subjects[0]}'

        assert self.get_count_mailing_from_db('ntf') == 5, (f'По данному операции должны были отправится 7 писем, а отправилось {self.get_count_mailing_from_db("ntf")} писем: \n'
                                                            'Админу о получении заявки\n'
                                                            'Инициатору об отправке заявки\n'
                                                            'Админу о взятии заявки в работу\n'
                                                            'Инициатору о взятии заявки в работу\n'
                                                            'Инициатору о добавлении документа\n')

    @allure.title("Нотификация / Заявка / Добавление документа / Отклонение без информирования")
    def test_notification_brief_document_deny_no_inform(self, ppinfo_user_api_client, ppinfo_client):
        number = self.send_brief_to_add_document(ppinfo_user_api_client, ppinfo_client, 'statusDeclined', notification=False)

        emails = self.get_bodies_mailing_from_db('pb')

        recipients = sorted([sorted(mail['to']) for mail in emails], key=lambda lst: (len(lst), lst))
        subjects = sorted([mail['templateMeta']['subject'] for mail in emails],
                          key=lambda subject: (len(subject), subject))

        assert len(recipients) == 2, f'Письма не отправлены\n {recipients}'

        assert recipients[0] == ['aikostrov1@mts.ru'], f'Инициатор не получили письмо \n {recipients[0]}'

        assert recipients[1] == ['pymaslenkov@mts.ru'], f'Админ не получили письмо \n {recipients[1]}'
        assert subjects[
                   0] == f'Заявка {number} на добавление документа в продукт «{NAME}» отклонена', f'У письма некорректный заголовок, сейчас заголовок - ={subjects[0]}'

        assert subjects[
                   1] == f'Заявка {number} на добавление документа в продукт «{NAME}» отклонена', f'У письма некорректный заголовок, сейчас заголовок - ={subjects[1]}'

        assert self.get_count_mailing_from_db('ntf') == 6, (f'По данному операции должны были отправится 7 писем, а отправилось {self.get_count_mailing_from_db("ntf")} писем: \n'
                                                            'Админу о получении заявки\n'
                                                            'Инициатору об отправке заявки\n'
                                                            'Админу о взятии заявки в работу\n'
                                                            'Инициатору о взятии заявки в работу\n'
                                                            'Админу об отклонении заявки\n'
                                                            'Инициатору об отклонении заявки\n')

    ####### Уведомления руководству
    @allure.title("Нотификация рук-ву / Заявка / Добавление документа / Принятие с информированием")
    @allure.issue('https://jira.mts.ru/browse/PPI-2330',
                  'PPinfo - Не приходит нотификация руководству при добавлении документа')
    def test_notification_users_brief_document_accept_inform(self, ppinfo_user_api_client, ppinfo_client):
        self.change_attr_in_settings(ppinfo_client, enable=True)
        self.send_brief_to_add_document(ppinfo_user_api_client, ppinfo_client, 'statusApproval')
        emails = self.get_bodies_mailing_from_db('pb')

        recipients = sorted([sorted(mail['to']) for mail in emails], key=lambda lst: (len(lst), lst))
        subjects = sorted([mail['templateMeta']['subject'] for mail in emails],
                          key=lambda subject: (len(subject), subject))

        assert len(recipients) == 3, f'Письма не отправлены\n {recipients}'

        assert recipients[2] == ['aastrunin@mts.ru', 'nolesnikov@mts.ru',
                                 'zimina@mts.ru'], f'Админ не получили письмо \n {recipients[2]}'

        assert subjects[
                   0] == f'В продукт «{NAME}» добавлен документ', f'У письма некорректный заголовок, сейчас заголовок - ={subjects[0]}'

        assert self.get_count_mailing_from_db('ntf') == 7, (f'По данному операции должны были отправится 7 писем, а отправилось {self.get_count_mailing_from_db("ntf")} писем: \n'
                                                            'Админу о получении заявки\n'
                                                            'Инициатору об отправке заявки\n'
                                                            'Админу о взятии заявки в работу\n'
                                                            'Инициатору о взятии заявки в работу\n'
                                                            'Админу о добавлении документа\n'
                                                            'Инициатору о добавлении документа\n'
                                                            'Руководству о добавлении документа\n'
                                                            )

    @allure.title("Нотификация рук-ву / Заявка / Добавление документа/Принятие с информированием/Атрибут отключен")
    def test_notification_users_brief_document_accept_inform_no_attr(self, ppinfo_user_api_client, ppinfo_client):
        self.change_attr_in_settings(ppinfo_client, enable=False)
        self.send_brief_to_add_document(ppinfo_user_api_client, ppinfo_client, 'statusApproval')
        emails = self.get_bodies_mailing_from_db('pb')

        recipients = sorted([sorted(mail['to']) for mail in emails], key=lambda lst: (len(lst), lst))
        subjects = sorted([mail['templateMeta']['subject'] for mail in emails],
                          key=lambda subject: (len(subject), subject))

        assert len(recipients) == 3, f'Письма не отправлены\n {recipients}'

        assert recipients[2] == ['aastrunin@mts.ru', 'nolesnikov@mts.ru',
                                 'zimina@mts.ru'], f'Админ не получили письмо \n {recipients[2]}'

        assert subjects[
                   0] == f'В продукт «{NAME}» добавлен документ', f'У письма некорректный заголовок, сейчас заголовок - ={subjects[0]}'

        assert self.get_count_mailing_from_db('ntf') == 7, (f'По данному операции должны были отправится 7 писем, а отправилось {self.get_count_mailing_from_db("ntf")} писем: \n'
                                                            'Админу о получении заявки\n'
                                                            'Инициатору об отправке заявки\n'
                                                            'Админу о взятии заявки в работу\n'
                                                            'Инициатору о взятии заявки в работу\n'
                                                            'Админу о добавлении документа\n'
                                                            'Инициатору о добавлении документа\n'
                                                            'Руководству о добавлении документа\n'
                                                            )

    @allure.title("Нотификация рук-ву / Заявка / Добавление документа / Отклонение с информированием")
    def test_notification_users_brief_document_deny_inform(self, ppinfo_user_api_client, ppinfo_client):
        self.send_brief_to_add_document(ppinfo_user_api_client, ppinfo_client, 'statusDeclined')

        emails = self.get_bodies_mailing_from_db('pb')

        recipients = sorted([sorted(mail['to']) for mail in emails], key=lambda lst: (len(lst), lst))

        assert len(recipients) == 2, f'Письма не отправлены\n {recipients}'

        assert recipients[1] != ['aastrunin@mts.ru', 'nolesnikov@mts.ru',
                                 'zimina@mts.ru'] and recipients[0] != ['aastrunin@mts.ru', 'nolesnikov@mts.ru',
                                                                          'zimina@mts.ru'], f'Руководство получило письмо \n {recipients}'

    @allure.title("Нотификация рук-ву / Заявка / Добавление документа / Принятие без информирования")
    def test_notification_users_brief_document_accept_no_inform(self, ppinfo_user_api_client, ppinfo_client):
        self.send_brief_to_add_document(ppinfo_user_api_client, ppinfo_client, 'statusApproval', notification=False)

        emails = self.get_bodies_mailing_from_db('pb')

        recipients = sorted([sorted(mail['to']) for mail in emails], key=lambda lst: (len(lst), lst))

        assert len(recipients) == 1, f'Письма не отправлены\n {recipients}'

        assert recipients[0] != ['aastrunin@mts.ru', 'nolesnikov@mts.ru',
                                 'zimina@mts.ru'], f'Руководство получило письмо \n {recipients}'

    @allure.title("Нотификация рук-ву/ Заявка / Добавление документа / Отклонение без информирования")
    def test_notification_users_brief_document_deny_no_inform(self, ppinfo_user_api_client, ppinfo_client):
        self.send_brief_to_add_document(ppinfo_user_api_client, ppinfo_client, 'statusDeclined', notification=False)

        emails = self.get_bodies_mailing_from_db('pb')

        recipients = sorted([sorted(mail['to']) for mail in emails], key=lambda lst: (len(lst), lst))

        assert len(recipients) == 2, f'Письма не отправлены\n {recipients}'

        assert recipients[1] != ['aastrunin@mts.ru', 'nolesnikov@mts.ru',
                                 'zimina@mts.ru'] and recipients[0] != ['aastrunin@mts.ru', 'nolesnikov@mts.ru',
                                                                          'zimina@mts.ru'], f'Руководство получило письмо \n {recipients}'
