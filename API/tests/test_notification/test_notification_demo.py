import json

import allure
import pytest

from API.models.pmd.rest_internal_modules.demo import Demo
from API.models.notification.notification import Notifications


@pytest.mark.api
@pytest.mark.notification
@allure.feature("Нотификации")
@pytest.mark.usefixtures('clear_db_notifications')
class TestNotificationDemo(Demo, Notifications):

    @allure.title("Нотификации / Создание заявки на добавление демо")
    def test_notification_create_brief_by_user(self, ppinfo_client, rest_internal_user_client):
        with allure.step("Создание заявки на добавление демо"):
            brief_id = self.create_demo_user(rest_internal_user_client, self.get_demo_data())['briefID']
            brief_info = self.get_brief_by_id(ppinfo_client, brief_id)

        emails = self.get_bodies_mailing_from_db('pb')

        recipients = sorted([sorted(mail['to']) for mail in emails], key=lambda lst: (len(lst), lst))
        subjects = sorted([mail['templateMeta']['subject'] for mail in emails],
                          key=lambda subject: (len(subject), subject))

        assert len(recipients) == 2, f'Письма не отправлены\n {recipients}'

        assert subjects[
                   0] == f'Вам направлена заявка № {brief_info["number"]} на добавление демо', f'У письма некорректный заголовок, сейчас заголовок - ={emails[0]["templateMeta"]["subject"]}'

        assert subjects[
                   1] == f'Заявка  № {brief_info["number"]} на добавление демо  отправлена на модерацию', f'У письма некорректный заголовок, сейчас заголовок - ={emails[1]["templateMeta"]["subject"]}'

        assert recipients[0] == [
            'aikostrov1@mts.ru'], f'Получатели письма из группы информирования не совпадают с ожидаемыми \n {recipients[0]}'

        assert recipients[1] == [
            'pymaslenkov@mts.ru'], f'Получатели письма из группы информирования не совпадают с ожидаемыми \n {recipients[0]}'

        assert self.get_count_mailing_from_db('ntf') == 2, (
            f'По данному операции должны были отправится 4 писем, а отправилось {self.get_count_mailing_from_db("ntf")} писем: \n'
            'Админу \n'
            'Инициатору \n')


    @allure.title("Нотификации / Создание заявки на добавление демо и взятие ее в работу")
    def test_notification_create_brief_by_user_and_take_to_work(self, ppinfo_client, rest_internal_user_client):
        with allure.step("Создание заявки на добавление демо и взятие ее в работу"):
            brief_id = self.create_demo_user(rest_internal_user_client, self.get_demo_data())['briefID']
            brief_info = self.get_brief_by_id(ppinfo_client, brief_id)
            self.delete_mailing_from_db('pb')
            self.take_to_work(ppinfo_client, brief_id, {"login": "ddsvetov1"})

        emails = self.get_bodies_mailing_from_db('pb')

        recipients = sorted([sorted(mail['to']) for mail in emails], key=lambda lst: (len(lst), lst))
        subjects = sorted([mail['templateMeta']['subject'] for mail in emails],
                          key=lambda subject: (len(subject), subject))

        assert len(recipients) == 2, f'Письма не отправлены\n {recipients}'

        assert subjects[
                   0] == f'Заявка № {brief_info["number"]} на добавление демо — взята в работу', f'У письма некорректный заголовок, сейчас заголовок - ={emails[0]["templateMeta"]["subject"]}'

        assert subjects[
                   1] == f'Заявка № {brief_info["number"]} на добавление демо — взята в работу', f'У письма некорректный заголовок, сейчас заголовок - ={emails[1]["templateMeta"]["subject"]}'

        assert recipients[0] == [
            'aikostrov1@mts.ru'], f'Получатели письма из группы информирования не совпадают с ожидаемыми \n {recipients[0]}'

        assert recipients[1] == [
            'pymaslenkov@mts.ru'], f'Получатели письма из группы информирования не совпадают с ожидаемыми \n {recipients[0]}'

        assert self.get_count_mailing_from_db('ntf') == 4, (
            f'По данному операции должны были отправится 4 писем, а отправилось {self.get_count_mailing_from_db("ntf")} писем: \n'
            'Админу \n'
            'Инициатору \n')

    @allure.title("Нотификации / Согласование заявки на добавление демо")
    def test_notification_full_brief_add_accepted(self, ppinfo_client, rest_internal_user_client):
        with allure.step("Создание заявки, взятие ее в работу и согласование"):
            brief_id = self.create_demo_user(rest_internal_user_client, self.get_demo_data())['briefID']
            brief_info = self.get_brief_by_id(ppinfo_client, brief_id)
            self.take_to_work(ppinfo_client, brief_id, {"login": "ddsvetov1"})
            self.delete_mailing_from_db('pb')
            self.approval(ppinfo_client, brief_id)


        emails = self.get_bodies_mailing_from_db('pb')

        recipients = sorted([sorted(mail['to']) for mail in emails], key=lambda lst: (len(lst), lst))
        subjects = sorted([mail['templateMeta']['subject'] for mail in emails],
                          key=lambda subject: (len(subject), subject))

        assert len(recipients) == 1, f'Письма не отправлены\n {recipients}'

        assert subjects[
                   0] == f'Заявка № {brief_info["number"]} на добавление демо выполнена', f'У письма некорректный заголовок, сейчас заголовок - ={emails[0]["templateMeta"]["subject"]}'


        assert recipients[0] == [
            'aikostrov1@mts.ru'], f'Получатели письма из группы информирования не совпадают с ожидаемыми \n {recipients[0]}'


        assert self.get_count_mailing_from_db('ntf') == 5, (
            f'По данному операции должны были отправится 4 писем, а отправилось {self.get_count_mailing_from_db("ntf")} писем: \n'
            'Делегирующему \n'
            'Делеганту \n')

    @allure.title("Нотификации / СОтклонение заявки на добавление демо")
    def test_notification_full_brief_add_declined(self, ppinfo_client, rest_internal_user_client):
        with allure.step("Создание заявки, взятие ее в работу и отклонение"):
            brief_id = self.create_demo_user(rest_internal_user_client, self.get_demo_data())['briefID']
            brief_info = self.get_brief_by_id(ppinfo_client, brief_id)
            self.take_to_work(ppinfo_client, brief_id, {"login": "ddsvetov1"})
            self.delete_mailing_from_db('pb')
            self.declined(ppinfo_client, brief_id)

        emails = self.get_bodies_mailing_from_db('pb')

        recipients = sorted([sorted(mail['to']) for mail in emails], key=lambda lst: (len(lst), lst))
        subjects = sorted([mail['templateMeta']['subject'] for mail in emails],
                          key=lambda subject: (len(subject), subject))

        assert len(recipients) == 2, f'Письма не отправлены\n {recipients}'

        assert subjects[
                   0] == f'Заявка № {brief_info["number"]} на добавление демо отклонена', f'У письма некорректный заголовок, сейчас заголовок - ={emails[0]["templateMeta"]["subject"]}'

        assert subjects[
                   1] == f'Заявка № {brief_info["number"]} на добавление демо отклонена', f'У письма некорректный заголовок, сейчас заголовок - ={emails[1]["templateMeta"]["subject"]}'

        assert recipients[0] == [
            'aikostrov1@mts.ru'], f'Получатели письма из группы информирования не совпадают с ожидаемыми \n {recipients[0]}'

        assert recipients[1] == [
            'pymaslenkov@mts.ru'], f'Получатели письма из группы информирования не совпадают с ожидаемыми \n {recipients[0]}'

        assert self.get_count_mailing_from_db('ntf') == 6, (
            f'По данному операции должны были отправится 4 писем, а отправилось {self.get_count_mailing_from_db("ntf")} писем: \n'
            'Админу \n'
            'Инициатору \n')


    @allure.title("Нотификации / Отклонение заявки на добавление демо")
    def test_notification_full_brief_delete_accepted(self, ppinfo_client, rest_internal_client, rest_internal_user_client):
        with allure.step("Создание заявки, взятие ее в работу и отклонение"):
            demo_id = self.create_demo(rest_internal_client, self.get_demo_data())['demoID']

            brief_id = self.delete_demo_user(rest_internal_user_client, demo_id)
            brief_info = self.get_brief_by_id(ppinfo_client, brief_id)

            self.take_to_work(ppinfo_client, brief_id, {"login": "ddsvetov1"})

            self.delete_mailing_from_db('pb')


            self.approval(ppinfo_client, brief_id)

        emails = self.get_bodies_mailing_from_db('pb')

        recipients = sorted([sorted(mail['to']) for mail in emails], key=lambda lst: (len(lst), lst))
        subjects = sorted([mail['templateMeta']['subject'] for mail in emails],
                          key=lambda subject: (len(subject), subject))

        assert len(recipients) == 1, f'Письма не отправлены\n {recipients}'

        assert subjects[
                   0] == f'Заявка № {brief_info["number"]} на удаление демо выполнена', f'У письма некорректный заголовок, сейчас заголовок - ={emails[0]["templateMeta"]["subject"]}'


        assert recipients[0] == [
            'aikostrov1@mts.ru'], f'Получатели письма из группы информирования не совпадают с ожидаемыми \n {recipients[0]}'


        assert self.get_count_mailing_from_db('ntf') == 5, (
            f'По данному операции должны были отправится 5 писем, а отправилось {self.get_count_mailing_from_db("ntf")} писем: \n'
            'Админу \n'
            'Инициатору \n')

    @allure.title("Нотификации / Отклонение заявки на добавление демо")
    def test_notification_full_brief_delete_declined(self, ppinfo_client, rest_internal_client, rest_internal_user_client):
        with allure.step("Создание заявки, взятие ее в работу и отклонение"):
            demo_id = self.create_demo(rest_internal_client, self.get_demo_data())['demoID']

            brief_id = self.delete_demo_user(rest_internal_user_client, demo_id)
            brief_info = self.get_brief_by_id(ppinfo_client, brief_id)

            self.take_to_work(ppinfo_client, brief_id, {"login": "ddsvetov1"})

            self.delete_mailing_from_db('pb')


            self.declined(ppinfo_client, brief_id)

        emails = self.get_bodies_mailing_from_db('pb')

        recipients = sorted([sorted(mail['to']) for mail in emails], key=lambda lst: (len(lst), lst))
        subjects = sorted([mail['templateMeta']['subject'] for mail in emails],
                          key=lambda subject: (len(subject), subject))

        assert len(recipients) == 2, f'Письма не отправлены\n {recipients}'

        assert subjects[
                   0] == f'Заявка № {brief_info["number"]} на удаление демо отклонена', f'У письма некорректный заголовок, сейчас заголовок - ={emails[0]["templateMeta"]["subject"]}'

        assert subjects[
                   1] == f'Заявка № {brief_info["number"]} на удаление демо отклонена', f'У письма некорректный заголовок, сейчас заголовок - ={emails[1]["templateMeta"]["subject"]}'

        assert recipients[0] == [
            'aikostrov1@mts.ru'], f'Получатели письма из группы информирования не совпадают с ожидаемыми \n {recipients[0]}'

        assert recipients[1] == [
            'pymaslenkov@mts.ru'], f'Получатели письма из группы информирования не совпадают с ожидаемыми \n {recipients[0]}'


        assert self.get_count_mailing_from_db('ntf') == 6, (
            f'По данному операции должны были отправится 5 писем, а отправилось {self.get_count_mailing_from_db("ntf")} писем: \n'
            'Админу \n'
            'Инициатору \n')


    @allure.title("Нотификации / Отклонение заявки на добавление демо")
    def test_notification_full_brief_patche_accepted(self, ppinfo_client, rest_internal_client, rest_internal_user_client):
        with allure.step("Создание заявки, взятие ее в работу и отклонение"):

            demo_id = self.create_demo(rest_internal_client, self.get_demo_data())['demoID']
            demos_id = []

            for quarter in self.get_demos(rest_internal_client):
                for demo in quarter['demos']:
                    demos_id.append(demo['id'])

            assert demo_id in demos_id, 'Демо удалилось, хотя не должно было'

            brief_id = self.patch_demo_user(rest_internal_user_client, demo_id,
                                            self.get_demo_data(name='test_name_patched',
                                                               description='test_description_patched',
                                                               link='test_link_patched'))

            brief_info = self.get_brief_by_id(ppinfo_client, brief_id)


            self.take_to_work(ppinfo_client, brief_id, {"login": "ddsvetov1"})

            self.delete_mailing_from_db('pb')

            self.approval(ppinfo_client, brief_id)

        emails = self.get_bodies_mailing_from_db('pb')

        recipients = sorted([sorted(mail['to']) for mail in emails], key=lambda lst: (len(lst), lst))
        subjects = sorted([mail['templateMeta']['subject'] for mail in emails],
                          key=lambda subject: (len(subject), subject))

        assert len(recipients) == 1, f'Письма не отправлены\n {recipients}'

        assert subjects[
                   0] == f'Заявка № {brief_info["number"]} на редактирование демо выполнена', f'У письма некорректный заголовок, сейчас заголовок - ={emails[0]["templateMeta"]["subject"]}'


        assert recipients[0] == [
            'aikostrov1@mts.ru'], f'Получатели письма из группы информирования не совпадают с ожидаемыми \n {recipients[0]}'


        assert self.get_count_mailing_from_db('ntf') == 5, (
            f'По данному операции должны были отправится 5 писем, а отправилось {self.get_count_mailing_from_db("ntf")} писем: \n'
            'Админу \n'
            'Инициатору \n')


    @allure.title("Нотификации / Проверка всех полей")
    def test_notification_full_brief_all_field(self, ppinfo_client, rest_internal_client, rest_internal_user_client):
        with allure.step("Создание заявки, взятие ее в работу и согласование"):
            file_id1 = self.add_file(rest_internal_client, 'test2', '.xlsx')

            brief_id = self.create_demo_user(rest_internal_user_client, self.get_demo_data(other={'files': [file_id1], 'linkedProducts': ['BI_3266']}))['briefID']
            brief_info = self.get_brief_by_id(ppinfo_client, brief_id)
            self.take_to_work(ppinfo_client, brief_id, {"login": "ddsvetov1"})
            self.delete_mailing_from_db('pb')
            self.approval(ppinfo_client, brief_id)

        emails = self.get_bodies_mailing_from_db('pb')
        attributes = emails[0]['templateMeta']['createAttributes']

        for attr in attributes:

            if attr['name'] == 'Название':
                assert attr['value'] == json.loads(brief_info["data"])['name']

            if attr['name'] == 'Материалы':
                file_link = json.loads(brief_info["data"])['files'][0]['id']
                assert attr['value'] == f'<a style="word-break: break-all;" href="https://stage.prodboard.mts.ru/pmd/internal/rest/api/v1/demo/file/{file_link}" title="test2.xlsx">test2.xlsx</a>'


            if attr['name'] == 'Связанные продукты':
                assert attr['value'] == '<a href="https://stage.prodboard.mts.ru/product/BI_3266/main" title="Не трогать (продукт для автотестов)">Не трогать (продукт для автотестов)</a>'

            if attr['name'] == 'Ссылка на демо':
                assert attr['value'] == f'<a style="word-break: break-all;" href="{json.loads(brief_info["data"])["link"]}" title="test_name">test_name</a>'


            if attr['name'] == 'Описание':
                assert attr['value'] == 'test_description'

            if attr['name'] == 'Категория':
                assert attr['value'] == 'Открытое демо'

            if attr['name'] == 'Дата проведения':
                assert attr['value'] == '09.01.2025'

