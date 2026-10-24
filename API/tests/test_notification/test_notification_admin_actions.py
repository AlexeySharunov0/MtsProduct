import allure
import pytest

from API.models.notification.notification import Notifications


##### Удаление продукта
@pytest.mark.notification
@allure.feature("Нотификации")
@pytest.mark.api
@pytest.mark.usefixtures('clear_db_notifications')
class TestNotificationDelete(Notifications):

    @allure.title("Нотификация / Удаление продукта / Руководство")
    def test_notification_delete_roles(self, pmd_internal_gw_client, ppinfo_client, ppinfo_user_client):
        self.set_default_settings(ppinfo_client)
        with allure.step("Отправляем заявку"):
            gen_name = self.text
            body = self.get_body_for_brief_all_roles(gen_name)
            brief_id = self.crete_brief_by_user(ppinfo_user_client, body)
            self.take_to_work(ppinfo_client, brief_id, {"login": "asnikiforov1"})
            self.change_brief_status(ppinfo_client, brief_id, {"status": "statusApproval"})
            self.delete_mailing_from_db('pmd')
            self.delete_product_notification(pmd_internal_gw_client, ppinfo_client, brief_id)

        mail_addresses = ['zimina@mts.ru', 'nolesnikov@mts.ru']

        emails = self.get_bodies_mailing_from_db('pmd')
        assert len(emails) == 1, 'Сообщение об удалении продукта не сформировано'

        assert emails[0]['to'] == sorted(
            mail_addresses), f'Получатели письма не совпадают с ожидаемыми \n {emails[0]["to"]} != {mail_addresses}'
        assert emails[0]['templateMeta'][
                   'subject'] == f'Продукт «{gen_name}» удален', f'У письма некорректный заголовок, сейчас заголовок - ={emails[0]["templateMeta"]["subject"]}'

        assert self.get_count_mailing_from_db('ntf') == 7, (
            f'По данному операции должны были отправится 7 писем, а отправилось {self.get_count_mailing_from_db("ntf")} писем: \n'
            'Админу об отправке заявки \n'
            'Пользователю об отправке заявки \n'
            'Админу о взятии в работу \n'
            'Пользователю о взятии в работу \n'
            'Админу о согласовании \n'
            'Пользователю о согласовании \n'
            'Об удалении продукта')


##### Создание продукта
@pytest.mark.notification
@pytest.mark.api
@allure.feature("Нотификации")
@pytest.mark.usefixtures('clear_db_notifications')
class TestNotificationAdminCreation(Notifications):
    @allure.title("Нотификация / Админ / Создание внешнего/внутреннего продукта / Принятие с информированием")
    @pytest.mark.parametrize("product_type, mail",
                             [["Vnutrennii", "itismailov@mts.ru"], ["Vneshnii", "svkurochkin@mts.ru"]])
    def test_notification_admin_create_product_accept_inform(self, ppinfo_client, product_type, mail):
        with allure.step("Создаем продукт админом"):
            gen_name = self.text
            self.create_product(ppinfo_client,
                                self.get_data_for_product_creation(product_type, name=gen_name, notification=True))

        emails = self.get_bodies_mailing_from_db('pb')

        recipients = sorted([sorted(mail['to']) for mail in emails], key=len)

        assert len(recipients) == 2, f'Письма не отправлены\n {recipients}'

        assert emails[0]['templateMeta'][
                   'subject'] == f'Добавлен продукт «{gen_name}» в статусе «Архив»', f'У письма некорректный заголовок, сейчас заголовок - ={emails[0]["templateMeta"]["subject"]}'

        assert recipients[0] == ['itismailov@mts.ru'] if product_type == 'Vnutrennii' else [
            'svkurochkin@mts.ru'], f'Получатели письма из группы информирования не совпадают с ожидаемыми \n {recipients[0]}'

        assert recipients[1] == ['ddsvetov1@mts.ru',
                                 'pymaslenkov@mts.ru'], f'Админ и ПО не получили письмо \n {recipients[1]}'

        assert self.get_count_mailing_from_db('ntf') == 2, (
            f'По данному операции должны были отправится 2 писем, а отправилось {self.get_count_mailing_from_db("ntf")} писем: \n'
            'Админу и инициатору о создании продукта \n'
            'Группе информирования о создании продукта \n')

    @allure.title("Нотификация / Админ / Создание внешнего/внутреннего продукта / Принятие без информирования")
    @pytest.mark.parametrize("product_type, mail",
                             [["Vnutrennii", "asnikiforov1@mts.ru"], ["Vneshnii", "svkurochkin@mts.ru"]])
    @allure.issue('https://jira.mts.ru/browse/PPI-2314',
                  'PPinfo - Не приходит нотификация админу при принятии заявки с отключенным информированием')
    def test_notification_admin_create_product_accept_no_inform(self, ppinfo_client, product_type, mail):
        with allure.step("Создаем продукт админом"):
            gen_name = self.text
            self.create_product(ppinfo_client, self.get_data_for_product_creation(product_type, name=gen_name))

        emails = self.get_bodies_mailing_from_db('pb')

        recipients = sorted([sorted(mail['to']) for mail in emails], key=len)

        assert len(recipients) == 1, f'Письмо должно быть одно, а их {len(recipients)}'

        assert recipients[0] == ['ddsvetov1@mts.ru',
                                 'pymaslenkov@mts.ru'], f'Админ и ПО не получили письмо \n {recipients[0]}'

        assert self.get_count_mailing_from_db('ntf') == 1, (
            f'По данному операции должны были отправится 1 писем, а отправилось {self.get_count_mailing_from_db("ntf")} писем: \n'
            'Админу и инициатору о создании продукта \n')

    @allure.title("Нотификация / Админ / Создание внешнего/внутреннего продукта / Проверка статусов")
    @allure.issue('https://jira.mts.ru/browse/PPI-1953', 'PPInfo - Добавить статусы в нотификации на создание продукта')
    @pytest.mark.parametrize("product_type",
                             ["Vnutrennii", "Vneshnii"])
    @pytest.mark.parametrize("status_code, status_name", (
            ["Arkhiv", "Архив"], ["(PPinfo_status)In_use", "Запущен в КЭ"],
            ["(PPinfo_status)Pilot", "Пилот"], ["(PPinfo_status)In_progress", "Разработка"],
            ["(PPinfo_status)Idea_formation", "Формирование идеи"],
            ["(PPinfo_status)Waiting_decision", "Ожидание решения"]))
    def test_notification_admin_create_product_check_status(self, ppinfo_client, product_type, status_code,
                                                            status_name):
        with allure.step("Создаем продукт админом"):
            gen_name = self.text
            self.create_product(ppinfo_client,
                                self.get_data_for_product_creation(product_type, name=gen_name, status=status_code,
                                                                   notification=True))

        emails = self.get_bodies_mailing_from_db('pb')
        assert emails[0]['templateMeta'][
                   'subject'] == f'Добавлен продукт «{gen_name}» в статусе «{status_name}»', f'У письма некорректный заголовок, сейчас заголовок - ={emails[0]["templateMeta"]["subject"]}'

        assert self.get_count_mailing_from_db('ntf') == 2, (
            f'По данному операции должны были отправится 2 писем, а отправилось {self.get_count_mailing_from_db("ntf")} писем: \n'
            'Админу и инициаторуо создании продукта \n'
            'Руководство продукта\n')

    @allure.title("Нотификация рук-ву / Админ / Создание продукта / Принятие с информированием")
    @pytest.mark.parametrize("product_type, mail",
                             [["Vnutrennii", "itismailov@mts.ru"], ["Vneshnii", "svkurochkin@mts.ru"]])
    def test_notification_users_admin_create_product_accept_inform(self, ppinfo_client, product_type, mail):
        with allure.step("Отправляем заявку"):
            gen_name = self.text
            self.create_product(ppinfo_client,
                                self.get_data_all_roles(product_type=product_type, name=gen_name, notification=True))

        emails = self.get_bodies_mailing_from_db('pb')

        recipients = sorted([sorted(mail['to']) for mail in emails], key=len)

        assert len(recipients) == 2, f'Админ и ПО не получили письмо \n {recipients}'

        assert recipients[0] == ['ddsvetov1@mts.ru',
                                 'pymaslenkov@mts.ru'], f'Админ и ПО не получили письмо \n {recipients[0]}'

        assert recipients[1] == sorted(
            ['aastrunin@mts.ru', 'mifadeeva@mts.ru', 'milapshin2@mts.ru', 'nolesnikov@mts.ru', 'zimina@mts.ru'] + [
                mail]), f'Руководство продукта не получили нотификацию \n {recipients[1]}'

        assert self.get_count_mailing_from_db('ntf') == 2, (
            f'По данному операции должны были отправится 2 писем, а отправилось {self.get_count_mailing_from_db("ntf")} писем: \n'
            'Админу и инициатору о создании продукта \n'
            'Руководство продукта и сотрудникам из группы информирования\n')

    @allure.title("Нотификация рук-ву / Админ / Создание продукта / Принятие без информирования")
    @pytest.mark.parametrize("product_type",
                             ["Vnutrennii", "Vneshnii"])
    def test_notification_users_admin_create_product_accept_no_inform(self, ppinfo_client, product_type):
        with allure.step("Отправляем заявку"):
            gen_name = self.text
            self.create_product(ppinfo_client,
                                self.get_data_all_roles(product_type=product_type, name=gen_name, notification=False))

        emails = self.get_bodies_mailing_from_db('pb')

        recipients = sorted([sorted(mail['to']) for mail in emails], key=len)

        assert len(recipients) == 1, f'Админ и ПО не получили письмо \n {recipients}'

        assert recipients[0] == ['ddsvetov1@mts.ru',
                                 'pymaslenkov@mts.ru'], f'Админ и ПО не получили письмо \n {recipients[0]}'

        assert self.get_count_mailing_from_db('ntf') == 1, (
            f'По данному операции должны были отправится 1 писем, а отправилось {self.get_count_mailing_from_db("ntf")} писем: \n'
            'Админу и ПО о создании продукта \n')


NAME = "Тест Notification (название не менять)"


@pytest.mark.last
@pytest.mark.api
@allure.feature("Нотификации")
@pytest.mark.usefixtures('clear_db_notifications')
class TestNotificationAdminUpdate(Notifications):
    @allure.title("Нотификация / Админ / Редактирование продукта / Принятие с информированием")
    def test_notification_admin_update_accept_inform(self, ppinfo_client):
        with allure.step("Отправляем заявку"):
            body = self.get_data_for_admin_update()
            self.change_product(ppinfo_client, body)

        emails = self.get_bodies_mailing_from_db('pb')

        recipients = sorted([sorted(mail['to']) for mail in emails], key=lambda lst: (len(lst), lst))
        subjects = sorted([mail['templateMeta']['subject'] for mail in emails],
                          key=lambda subject: (len(subject), subject))

        assert len(recipients) == 5, f'Письма не отправлены\n {recipients}'

        assert recipients[0] == ['aastrunin@mts.ru'], f'СТО не получили письмо \n {recipients[0]}'
        assert recipients[1] == ['nolesnikov@mts.ru'], f'СПО не получили письмо \n {recipients[0]}'
        assert recipients[2] == ['pymaslenkov@mts.ru'], f'Админне получили письмо \n {recipients[0]}'
        assert recipients[3] == [
            'snkondratyev@mts.ru'], f'Кастомная группа нотификаций  не получили письмо \n {recipients[0]}'
        assert recipients[4] == ['zimina@mts.ru'], f'ПО не получили письмо \n {recipients[0]}'

        for subject in subjects:
            assert subject == f'Продукт «{NAME}» отредактирован', f'Некорректный subject \n {subject}'

    @allure.title("Нотификация / Админ / Редактирование продукта / Принятие без информирования")
    @allure.issue('https://jira.mts.ru/browse/PPI-2314',
                  'PPinfo - Не приходит нотификация админу при принятии заявки с отключенным информированием')
    def test_notification_admin_update_accept_no_inform(self, ppinfo_client):
        with allure.step("Отправляем заявку"):
            body = self.get_data_for_admin_update(notification=False)
            self.change_product(ppinfo_client, body)

        emails = self.get_bodies_mailing_from_db('pb')

        recipients = sorted([sorted(mail['to']) for mail in emails], key=lambda lst: (len(lst), lst))
        subjects = sorted([mail['templateMeta']['subject'] for mail in emails],
                          key=lambda subject: (len(subject), subject))

        assert len(recipients) == 1, f'Письма не отправлены\n {recipients}'

        assert recipients[0] == ['pymaslenkov@mts.ru'], f'Админ не получили письмо \n {recipients[0]}'
        assert subjects[0] == f'Продукт «{NAME}» отредактирован', f'Некорректный subject \n {subjects[0]}'

    ####### Иниц. закрытие
    @allure.title(
        "Нотификация иниц. закрытие / Админ / Редактирование продукта / Принятие с информированием")
    @allure.issue('https://jira.mts.ru/browse/PPI-2326',
                  'PPinfo - Нет нотификации группе заинтересованной в иницированно закрытие')
    def test_notification_start_close_admin_update_accept_inform(self, ppinfo_client):
        with allure.step("Отправляем заявку"):
            body = self.get_data_for_admin_update(start_close=True)
            self.change_product(ppinfo_client, body)

        emails = self.get_bodies_mailing_from_db('pb')

        recipients = sorted([sorted(mail['to']) for mail in emails], key=lambda lst: (len(lst), lst))
        subjects = sorted([mail['templateMeta']['subject'] for mail in emails],
                          key=lambda subject: (len(subject), subject))

        assert len(recipients) == 2, f'Письма не отправлены\n {recipients}'

        assert recipients[0] == ['pymaslenkov@mts.ru'], f'Админ не получили письмо \n {recipients[0]}'
        assert recipients[1] == ['ddsvetov1@mts.ru', 'sskopytin@mts.ru',
                                 'ysgurkov1@mts.ru'], f'Иницаитор (ddsvetov1) и группа информирования по Иниц закрытие не получили письмо \n {recipients[0]}'
        assert subjects[0] == f'Продукт «{NAME}» отредактирован', f'Некорректный subject \n {subjects[0]}'

        assert self.get_count_mailing_from_db('ntf') == 2, (
            f'По данному операции должны были отправится 7 писем, а отправилось {self.get_count_mailing_from_db("ntf")} писем: \n'
            'Админу об Инициировании закрытия\n'
            'Инициатор и группа информирования  об Инициировании закрытия\n')

    @allure.title(
        "Нотификация иниц. закрытие / Админ / Редактирование продукта / Принятие без информирования")
    def test_notification_start_close_admin_update_accept_no_inform(self, ppinfo_client):
        with allure.step("Отправляем заявку"):
            body = self.get_data_for_admin_update(start_close=True, notification=False)
            self.change_product(ppinfo_client, body)

        emails = self.get_bodies_mailing_from_db('pb')

        recipients = sorted([sorted(mail['to']) for mail in emails], key=lambda lst: (len(lst), lst))
        subjects = sorted([mail['templateMeta']['subject'] for mail in emails],
                          key=lambda subject: (len(subject), subject))

        assert len(recipients) == 2, f'Письма не отправлены\n {recipients}'

        assert recipients[0] == [
            'ddsvetov1@mts.ru'], f'Иницаитор (ddsvetov1) по Иниц закрытие не получили письмо \n {recipients[0]}'
        assert recipients[1] == ['pymaslenkov@mts.ru'], f'Админ не получили письмо \n {recipients[0]}'
        assert subjects[0] == f'Продукт «{NAME}» отредактирован', f'Некорректный subject \n {subjects[0]}'

        assert self.get_count_mailing_from_db('ntf') == 2, (
            f'По данному операции должны были отправится 2 писем, а отправилось {self.get_count_mailing_from_db("ntf")} писем: \n'
            'Админу об Инициировании закрытия\n'
            'Инициатор об Инициировании закрытия\n')

    ####### Кастомная группа
    @allure.title(
        "Нотификация кастомной группе / Админ / Редактирование продукта / Принятие с информированием")
    @pytest.mark.parametrize('product_type, key_word', [['external', 'Notification'], ['internal', 'manual']])
    def test_notification_custom_group_admin_update_accept_inform(self, ppinfo_client, product_type, key_word):
        with allure.step("Отправляем заявку"):
            body = self.get_data_for_admin_update() if product_type == 'external' else self.get_data_for_admin_update(
                product_code='BI_9855')
            self.change_product(ppinfo_client, body)

        emails = self.get_bodies_mailing_from_db('pb')

        recipients = sorted([sorted(mail['to']) for mail in emails], key=lambda lst: (len(lst), lst))
        subjects = sorted([mail['templateMeta']['subject'] for mail in emails],
                          key=lambda subject: (len(subject), subject))

        if product_type == 'internal':
            prod_name = 'Внутренний продукт для manual тестоВ'
            assert len(recipients) == 3, f'Письма не отправлены\n {recipients}'

            assert recipients[0] == ['pymaslenkov@mts.ru'], f'Админ не получили письмо \n {recipients[0]}'
            assert recipients[1] == [
                'snkondratyev@mts.ru'], f'Кастомная группа информирования не получили письмо \n {recipients[0]}'
            assert recipients[2] == ['ymshatov@mts.ru'], f'ПО не получили письмо \n {recipients[0]}'

            for subject in subjects:
                assert subject == f'Продукт «{prod_name}» отредактирован', f'Некорректный subject \n {subject}'
        else:
            prod_name = "Тест Notification (название не менять)"
            assert len(recipients) == 5, f'Письма не отправлены\n {recipients}'

            assert recipients[0] == ['aastrunin@mts.ru'], f'СТО не получили письмо \n {recipients[0]}'
            assert recipients[1] == ['nolesnikov@mts.ru'], f'СПО не получили письмо \n {recipients[0]}'
            assert recipients[2] == ['pymaslenkov@mts.ru'], f'Админне получили письмо \n {recipients[0]}'
            assert recipients[3] == [
                'snkondratyev@mts.ru'], f'Кастомная группа нотификаций  не получили письмо \n {recipients[0]}'
            assert recipients[4] == ['zimina@mts.ru'], f'ПО не получили письмо \n {recipients[0]}'

            for subject in subjects:
                assert subject == f'Продукт «{prod_name}» отредактирован', f'Некорректный subject \n {subject}'

    @allure.title(
        "Нотификация кастомной группе / Админ / Редактирование продукта / Принятие без информирования")
    @pytest.mark.parametrize('product_type, key_word', [['external', 'Notification'], ['internal', 'manual']])
    def test_notification_custom_group_admin_update_accept_no_inform(self, ppinfo_client, product_type, key_word):
        with allure.step("Отправляем заявку"):
            body = self.get_data_for_admin_update(
                notification=False) if product_type == 'external' else self.get_data_for_admin_update(
                product_code='BI_9855', notification=False)
            self.change_product(ppinfo_client, body)

        emails = self.get_bodies_mailing_from_db('pb')

        recipients = sorted([sorted(mail['to']) for mail in emails], key=lambda lst: (len(lst), lst))

        assert len(recipients) == 1, f'Письма не отправлены\n {recipients}'
        assert recipients[0] == ['pymaslenkov@mts.ru'], f'Админ не получили письмо \n {recipients[0]}'

    @allure.title(
        "При смене руководителя и новый и старый руководитель получают письмо")
    @allure.issue('https://jira.mts.ru/browse/PPI-4602', 'PPInfo - Информирование при смене нового руководства')
    def test_notification_old_and_new_po(self, ppinfo_client):
        self.delete_mailing_from_db('pb')
        self.change_product(ppinfo_client, self.get_data_for_change_po('иванова'))

        emails = self.get_bodies_mailing_from_db('pb')

        recipients = sorted([sorted(mail['to']) for mail in emails], key=lambda lst: (len(lst), lst))

        assert 'aaivanov23@mts.ru' in sum(recipients, []) and 'zimina@mts.ru' in sum(recipients, [])

        self.delete_mailing_from_db('pb')
        self.change_product(ppinfo_client, self.get_data_for_change_po('зимина'))

        emails = self.get_bodies_mailing_from_db('pb')

        recipients = sorted([sorted(mail['to']) for mail in emails], key=lambda lst: (len(lst), lst))

        assert 'aaivanov23@mts.ru' in sum(recipients, []) and 'zimina@mts.ru' in sum(recipients, [])
