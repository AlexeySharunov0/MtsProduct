import allure
import pytest

from API.models.notification.notification import Notifications


@pytest.mark.api
@pytest.mark.notification
@allure.feature("Нотификации")
@pytest.mark.usefixtures('clear_db_notifications')
class TestNotificationBriefCreation(Notifications):

    @allure.title("Нотификация / Заявка / Создание внешнего/внутреннего продукта / Отправка заявки")
    @pytest.mark.parametrize("product_type", ["external", "internal"])
    def test_notification_brief_create_product_send(self, product_type, ppinfo_client, ppinfo_user_client):
        self.set_default_settings(ppinfo_client)
        with allure.step("Отправляем заявку"):
            name = self.text
            body = self.get_body_for_brief_creation(product_type, name)
            brief_id = self.crete_brief_by_user(ppinfo_user_client, body)
            number = " № " + self.get_brief_by_id(ppinfo_client, brief_id)["number"]

        emails = self.get_bodies_mailing_from_db('pb')

        recipients = sorted([sorted(mail['to']) for mail in emails], key=lambda lst: (len(lst), lst))
        subjects = sorted([mail['templateMeta']['subject'] for mail in emails],
                          key=lambda subject: (len(subject), subject))

        assert len(recipients) == 2, f'Письма не отправлены\n {recipients}'

        assert recipients[0] == ['aikostrov1@mts.ru'], f'Инициатор не получили письмо \n {recipients[0]}'

        assert recipients[1] == ['pymaslenkov@mts.ru'], f'Админ не получили письмо \n {recipients[1]}'

        assert subjects[
                   0] == f'Вам направлена заявка{number} на создание продукта «{name}»', f'У письма некорректный заголовок, сейчас заголовок - ={emails[0]["templateMeta"]["subject"]}'

        assert subjects[
                   1] == f'Заявка {number} на создание продукта «{name}»  отправлена на модерацию', f'У письма некорректный заголовок, сейчас заголовок - ={emails[0]["templateMeta"]["subject"]}'

        assert self.get_count_mailing_from_db('ntf') == 2, (f'По данному операции должны были отправится 2 писем, а отправилось {self.get_count_mailing_from_db("ntf")} писем: \n'
                                                            'Админу о получении заявки\n'
                                                            'Инициатору об отправке заявки\n')

    @allure.title("Нотификация / Заявка / Создание внешнего/внутреннего продукта / Взятие в работу")
    @pytest.mark.parametrize("product_type", ["internal", "external"])
    def test_notification_brief_create_product_take_to_work(self, product_type, ppinfo_client, ppinfo_user_client):
        with allure.step("Отправляем заявку"):
            name = self.text
            body = self.get_body_for_brief_creation(product_type, name)
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
                   0] == f'Заявка {number} на создание продукта «{name}» — взята в работу', f'У письма некорректный заголовок, сейчас заголовок - ={emails[0]["templateMeta"]["subject"]}'

        assert subjects[
                   1] == f'Заявка {number} на создание продукта «{name}» — взята в работу', f'У письма некорректный заголовок, сейчас заголовок - ={emails[0]["templateMeta"]["subject"]}'

        assert self.get_count_mailing_from_db('ntf') == 4, (f'По данному операции должны были отправится 4 писем, а отправилось {self.get_count_mailing_from_db("ntf")} писем: \n'
                                                            'Админу о получении заявки\n'
                                                            'Инициатору об отправке заявки\n'
                                                            'Админу о взятии заявки в работу\n'
                                                            'Инициатору о взятии заявки в работу\n')

    @allure.title("Нотификация / Заявка / Создание внешнего/внутреннего продукта / Принятие с информированием")
    @pytest.mark.parametrize("product_type, mail",
                             [["internal", "itismailov@mts.ru"], ["external", "svkurochkin@mts.ru"]])
    def test_notification_brief_create_product_accept_inform(self, pmd_internal_gw_client, ppinfo_client, ppinfo_user_client, product_type, mail):

        number_and_name = self.send_brief_to_add_product(pmd_internal_gw_client, ppinfo_client, ppinfo_user_client, 'statusApproval', product_type)

        emails = self.get_bodies_mailing_from_db('pb')

        recipients = sorted([sorted(mail['to']) for mail in emails], key=lambda lst: (len(lst), lst))
        subjects = sorted([mail['templateMeta']['subject'] for mail in emails],
                          key=lambda subject: (len(subject), subject))

        assert len(recipients) == 2, f'Письма не отправлены\n {recipients}'

        assert recipients[0] == ['ddsvetov1@mts.ru',
                                 'pymaslenkov@mts.ru'], f'Админ и согласующий не получили письмо \n {recipients[0]}'

        assert recipients[1] == sorted(['aikostrov1@mts.ru', 'sa0000ppinfouser1@nts.ru'] + [
            mail]), f'Инициатор, ПО и группа информирования не получили письмо \n {recipients[1]}'

        assert subjects[
                   0] == f'Добавлен продукт «{number_and_name[1]}» в статусе «Архив»', f'У письма некорректный заголовок, сейчас заголовок - ={subjects[0]}'

        assert subjects[
                   1] == f'Добавлен продукт «{number_and_name[1]}» в статусе «Архив»', f'У письма некорректный заголовок, сейчас заголовок - ={subjects[1]}'

        assert self.get_count_mailing_from_db('ntf') == 7, (f'По данному операции должны были отправится 7 писем, а отправилось {self.get_count_mailing_from_db("ntf")} писем: \n'
                                                            'Админу о получении заявки\n'
                                                            'Инициатору об отправке заявки\n'
                                                            'Админу о взятии заявки в работу\n'
                                                            'Инициатору о взятии заявки в работу\n'
                                                            'Админу и согласующему о добавлении продукта\n'
                                                            'Инициатору, группе информирования и ПО о добавлении продукта\n'
                                                            'ПО об удалении продукта\n')

    @allure.title("Нотификация / Заявка / Создание внешнего/внутреннего продукта / Отклонение с информированием")
    @pytest.mark.parametrize("product_type, mail",
                             [["internal", "asnikiforov1@mts.ru"], ["external", "svkurochkin@mts.ru"]])
    def test_notification_brief_create_product_deny_inform(self, pmd_internal_gw_client, ppinfo_client, ppinfo_user_client, product_type, mail):
        number_and_name = self.send_brief_to_add_product(pmd_internal_gw_client, ppinfo_client, ppinfo_user_client, 'statusDeclined', product_type)

        emails = self.get_bodies_mailing_from_db('pb')

        recipients = sorted([sorted(mail['to']) for mail in emails], key=lambda lst: (len(lst), lst))
        subjects = sorted([mail['templateMeta']['subject'] for mail in emails],
                          key=lambda subject: (len(subject), subject))

        print(recipients)

        assert len(recipients) == 2, f'Письма не отправлены\n {recipients}'

        assert recipients[0] == ['aikostrov1@mts.ru'], f'Инициатор не получили письмо \n {recipients[0]}'

        assert recipients[1] == ['pymaslenkov@mts.ru'], f'Админ не получили письмо \n {recipients[1]}'
        assert subjects[
                   0] == f'Заявка {number_and_name[0]} на создание продукта «{number_and_name[1]}» отклонена', f'У письма некорректный заголовок, сейчас заголовок - ={subjects[0]}'

        assert subjects[
                   1] == f'Заявка {number_and_name[0]} на создание продукта «{number_and_name[1]}» отклонена', f'У письма некорректный заголовок, сейчас заголовок - ={subjects[1]}'

        assert self.get_count_mailing_from_db('ntf') == 6, (f'По данному операции должны были отправится 6 писем, а отправилось {self.get_count_mailing_from_db("ntf")} писем: \n'
                                                            'Админу о получении заявки\n'
                                                            'Инициатору об отправке заявки\n'
                                                            'Админу о взятии заявки в работу\n'
                                                            'Инициатору о взятии заявки в работу\n'
                                                            'Админу о добавлении продукта\n'
                                                            'Инициатору о добавлении продукта\n')

    @allure.title("Нотификация / Заявка / Создание внешнего/внутреннего продукта / Принятие без информирования")
    @pytest.mark.parametrize("product_type, mail",
                             [["internal", "asnikiforov1@mts.ru"], ["external", "svkurochkin@mts.ru"]])
    @allure.issue('https://jira.mts.ru/browse/PPI-2314',
                  'PPinfo - Не приходит нотификация админу при принятии заявки с отключенным информированием')
    def test_notification_brief_create_product_accept_no_inform(self, pmd_internal_gw_client, ppinfo_client, ppinfo_user_client, product_type, mail):
        number_and_name = self.send_brief_to_add_product(pmd_internal_gw_client, ppinfo_client, ppinfo_user_client, 'statusApproval', product_type, notification=False)

        emails = self.get_bodies_mailing_from_db('pb')

        recipients = sorted([sorted(mail['to']) for mail in emails], key=lambda lst: (len(lst), lst))
        subjects = sorted([mail['templateMeta']['subject'] for mail in emails],
                          key=lambda subject: (len(subject), subject))

        assert len(recipients) == 2, f'Письма не отправлены\n {recipients}'

        assert recipients[0] == ['aikostrov1@mts.ru'], f'Инициатор не получили письмо \n {recipients[0]}'

        assert recipients[1] == ['ddsvetov1@mts.ru',
                                 'pymaslenkov@mts.ru'], f'Админ и согласующий не получили письмо \n {recipients[1]}'

        assert subjects[
                   0] == f'Добавлен продукт «{number_and_name[1]}» в статусе «Архив»', f'У письма некорректный заголовок, сейчас заголовок - ={subjects[0]}'

        assert subjects[
                   1] == f'Добавлен продукт «{number_and_name[1]}» в статусе «Архив»', f'У письма некорректный заголовок, сейчас заголовок - ={subjects[1]}'

        assert self.get_count_mailing_from_db('ntf') == 7, (f'По данному операции должны были отправится 7 писем, а отправилось {self.get_count_mailing_from_db("ntf")} писем: \n'
                                                            'Админу о получении заявки\n'
                                                            'Инициатору об отправке заявки\n'
                                                            'Админу о взятии заявки в работу\n'
                                                            'Инициатору о взятии заявки в работу\n'
                                                            'Админу и согласующему о добавлении продукта\n'
                                                            'Инициатору, группе информирования и ПО о добавлении продукта\n'
                                                            'ПО об удалении продукта\n')

    @allure.title("Нотификация / Заявка / Создание внешнего/внутреннего продукта / Отклонение без информирования")
    @pytest.mark.parametrize("product_type, mail",
                             [["internal", "asnikiforov1@mts.ru"], ["external", "svkurochkin@mts.ru"]])
    def test_notification_brief_create_product_deny_no_inform(self, pmd_internal_gw_client, ppinfo_client, ppinfo_user_client, product_type, mail):
        number_and_name = self.send_brief_to_add_product(pmd_internal_gw_client, ppinfo_client, ppinfo_user_client, 'statusDeclined', product_type, notification=False)

        emails = self.get_bodies_mailing_from_db('pb')

        recipients = sorted([sorted(mail['to']) for mail in emails], key=lambda lst: (len(lst), lst))
        subjects = sorted([mail['templateMeta']['subject'] for mail in emails],
                          key=lambda subject: (len(subject), subject))

        assert len(recipients) == 2, f'Письма не отправлены\n {recipients}'

        assert recipients[0] == ['aikostrov1@mts.ru'], f'Инициатор не получили письмо \n {recipients[0]}'

        assert recipients[1] == ['pymaslenkov@mts.ru'], f'Админ и согласующий не получили письмо \n {recipients[1]}'

        assert subjects[
                   0] == f'Заявка {number_and_name[0]} на создание продукта «{number_and_name[1]}» отклонена', f'У письма некорректный заголовок, сейчас заголовок - ={subjects[0]}'

        assert subjects[
                   1] == f'Заявка {number_and_name[0]} на создание продукта «{number_and_name[1]}» отклонена', f'У письма некорректный заголовок, сейчас заголовок - ={subjects[1]}'

        assert self.get_count_mailing_from_db('ntf') == 6, (f'По данному операции должны были отправится 6 писем, а отправилось {self.get_count_mailing_from_db("ntf")} писем: \n'
                                                            'Админу о получении заявки\n'
                                                            'Инициатору об отправке заявки\n'
                                                            'Админу о взятии заявки в работу\n'
                                                            'Инициатору о взятии заявки в работу\n'
                                                            'Админу и согласующему о добавлении продукта\n'
                                                            'Инициатору, группе информирования и ПО о добавлении продукта\n')

    #### Проверка информирования ролей
    @allure.title("Нотификация рук-ву / Заявка / Создание продукта / Принятие с информированием")
    def test_notification_users_brief_create_product_accept_inform(self, pmd_internal_gw_client, ppinfo_client, ppinfo_user_client):
        name = self.text
        self.send_brief_to_add_product(pmd_internal_gw_client, ppinfo_client, ppinfo_user_client, 'statusApproval', 'Vneshnii',
                                                         body=self.get_body_for_brief_all_roles(name))

        emails = self.get_bodies_mailing_from_db('pb')

        recipients = sorted([sorted(mail['to']) for mail in emails], key=lambda lst: (len(lst), lst))
        subjects = sorted([mail['templateMeta']['subject'] for mail in emails],
                          key=lambda subject: (len(subject), subject))

        assert len(recipients) == 2, f'Письма не отправлены\n {recipients}'

        assert recipients[0] == ['ddsvetov1@mts.ru',
                                 'pymaslenkov@mts.ru'], f'Админ и согласующий не получили письмо \n {recipients[0]}'

        assert recipients[1] == ['aastrunin@mts.ru', 'aikostrov1@mts.ru', 'mifadeeva@mts.ru', 'milapshin2@mts.ru',
                                 'nolesnikov@mts.ru', 'svkurochkin@mts.ru',
                                 'zimina@mts.ru'], f'ПО, СПО, СТО, ВП, БО и группа информирования не получили письмо \n {recipients[1]}'

        assert subjects[
                   0] == f'Добавлен продукт «{name}» в статусе «Архив»', f'У письма некорректный заголовок, сейчас заголовок - ={subjects[0]}'

        assert subjects[
                   1] == f'Добавлен продукт «{name}» в статусе «Архив»', f'У письма некорректный заголовок, сейчас заголовок - ={subjects[1]}'

        assert self.get_count_mailing_from_db('ntf') == 7, (f'По данному операции должны были отправится 7 писем, а отправилось {self.get_count_mailing_from_db("ntf")} писем: \n'
                                                            'Админу о получении заявки\n'
                                                            'Инициатору об отправке заявки\n'
                                                            'Админу о взятии заявки в работу\n'
                                                            'Инициатору о взятии заявки в работу\n'
                                                            'Админу и инициатору о добавлении документа\n'
                                                            'Руководству о добавлении документа\n'
                                                            'ПО об удалении продукта\n'
                                                            )

    @allure.title("Нотификация рук-ву / Заявка / Создание продукта / Отклонение с информированием")
    def test_notification_users_brief_create_product_deny_inform(self, pmd_internal_gw_client, ppinfo_client, ppinfo_user_client):
        name = self.text
        self.send_brief_to_add_product(pmd_internal_gw_client, ppinfo_client, ppinfo_user_client, 'statusDeclined', 'Vneshnii', body=self.get_body_for_brief_all_roles(name))

        emails = self.get_bodies_mailing_from_db('pb')

        recipients = sorted([sorted(mail['to']) for mail in emails], key=lambda lst: (len(lst), lst))

        assert len(recipients) == 2, f'Письма не отправлены\n {recipients}'

        assert recipients[0] == ['aikostrov1@mts.ru'], f'Инициатор не получили письмо \n {recipients[0]}'

        assert recipients[1] == ['pymaslenkov@mts.ru'], f'Админ не получили письмо \n {recipients[1]}'

        assert self.get_count_mailing_from_db('ntf') == 6, (f'По данному операции должны были отправится 6 писем, а отправилось {self.get_count_mailing_from_db("ntf")} писем: \n'
                                                            'Админу о получении заявки\n'
                                                            'Инициатору об отправке заявки\n'
                                                            'Админу о взятии заявки в работу\n'
                                                            'Инициатору о взятии заявки в работу\n'
                                                            'Админу об отклонении заявки\n'
                                                            'Инициатору об отклонении заявки\n'
                                                            )

    @allure.title("Нотификация рук-ву / Заявка / Создание продукта / Принятие без информирования")
    def test_notification_users_brief_create_product_accept_no_inform(self, pmd_internal_gw_client, ppinfo_client, ppinfo_user_client):
        name = self.text
        self.send_brief_to_add_product(pmd_internal_gw_client, ppinfo_client, ppinfo_user_client, 'statusApproval', 'Vneshnii',
                                       body=self.get_body_for_brief_all_roles(name, notification=False))

        emails = self.get_bodies_mailing_from_db('pb')

        recipients = sorted([sorted(mail['to']) for mail in emails], key=lambda lst: (len(lst), lst))

        assert len(recipients) == 2, f'Письма не отправлены\n {recipients}'

        assert recipients[0] == ['aikostrov1@mts.ru'], f'Админ и согласующий не получили письмо \n {recipients[0]}'

        assert recipients[1] == ['ddsvetov1@mts.ru',
                                 'pymaslenkov@mts.ru'], f'Инициатор не получили письмо \n {recipients[1]}'

        assert self.get_count_mailing_from_db('ntf') == 7, (f'По данному операции должны были отправится 7 писем, а отправилось {self.get_count_mailing_from_db("ntf")} писем: \n'
                                                            'Админу о получении заявки\n'
                                                            'Инициатору об отправке заявки\n'
                                                            'Админу о взятии заявки в работу\n'
                                                            'Инициатору о взятии заявки в работу\n'
                                                            'Админу о добавлении продукта\n'
                                                            'Инициатору о добавлении продукта\n'
                                                            'ПО об удалении продукта\n')

    @allure.title("Нотификация рук-ву/ Заявка / Создание продукта / Отклонение без информирования")
    def test_notification_users_brief_create_product_deny_no_inform(self, pmd_internal_gw_client, ppinfo_client, ppinfo_user_client):
        name = self.text
        self.send_brief_to_add_product(pmd_internal_gw_client, ppinfo_client, ppinfo_user_client, 'statusDeclined', 'Vneshnii',
                                       body=self.get_body_for_brief_all_roles(name, notification=False))

        emails = self.get_bodies_mailing_from_db('pb')

        recipients = sorted([sorted(mail['to']) for mail in emails], key=lambda lst: (len(lst), lst))

        assert len(recipients) == 2, f'Письма не отправлены\n {recipients}'

        assert recipients[0] == ['aikostrov1@mts.ru'], f'Админ и согласующий не получили письмо \n {recipients[0]}'

        assert recipients[1] == ['pymaslenkov@mts.ru'], f'Инициатор не получили письмо \n {recipients[1]}'

        assert self.get_count_mailing_from_db('ntf') == 6, (f'По данному операции должны были отправится 6 писем, а отправилось {self.get_count_mailing_from_db("ntf")} писем: \n'
                                                            'Админу о получении заявки\n'
                                                            'Инициатору об отправке заявки\n'
                                                            'Админу о взятии заявки в работу\n'
                                                            'Инициатору о взятии заявки в работу\n'
                                                            'Админу об отклонении заявки\n'
                                                            'Инициатору об отклонении заявки\n'
                                                            )
