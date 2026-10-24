import allure
import pytest

from API.models.delegation.delegation import Delegation
from API.models.notification.notification import Notifications


@pytest.mark.api
@pytest.mark.notification
@allure.feature("Нотификации")
@pytest.mark.usefixtures('clear_db_notifications')
class TestNotificationDelegation(Notifications):
    @allure.title("Нотификация / Делегирование / Получение")
    def test_notification_delegation_get(self, ppinfo_client, rest_internal_client):
        with allure.step("Выдаем права на делегирование"):
            self.remove_delegation(ppinfo_client, rest_internal_client)
            self.delete_mailing_from_db('pb')
            self.add_delegation(ppinfo_client)

        emails = self.get_bodies_mailing_from_db('pb')

        recipients = sorted([sorted(mail['to']) for mail in emails], key=lambda lst: (len(lst), lst))
        subjects = sorted([mail['templateMeta']['subject'] for mail in emails],
                          key=lambda subject: (len(subject), subject))

        assert len(recipients) == 2, f'Письма не отправлены\n {recipients}'

        assert subjects[
                   0] == f'Вы делегировали права на редактирование продукта «1_Не трогать, для АТ, делегирование del»', f'У письма некорректный заголовок, сейчас заголовок - ={emails[0]["templateMeta"]["subject"]}'

        assert subjects[
                   1] == f'Вам делегировали права на редактирование продукта «1_Не трогать, для АТ, делегирование del»', f'У письма некорректный заголовок, сейчас заголовок - ={emails[1]["templateMeta"]["subject"]}'

        assert recipients[0] == [
            'aikostrov1@mts.ru'], f'Получатели письма из группы информирования не совпадают с ожидаемыми \n {recipients[0]}'

        assert recipients[1] == [
            'ddsvetov1@mts.ru'], f'Получатели письма из группы информирования не совпадают с ожидаемыми \n {recipients[0]}'

        assert self.get_count_mailing_from_db('ntf') == 4 or 2, (
            f'По данному операции должны были отправится 4 писем, а отправилось {self.get_count_mailing_from_db("ntf")} писем: \n'
            'Делегирующему \n'
            'Делеганту \n')

    @allure.title("Нотификация / Делегирование / Окончание")
    def test_notification_delegation_remove(self, ppinfo_client, rest_internal_client):
        with allure.step("Забираем права на делегирование"):
            self.remove_delegation(ppinfo_client, rest_internal_client)
            self.add_delegation(ppinfo_client)
            self.check_presence(rest_internal_client)
            self.delete_mailing_from_db('pb')
            self.remove_delegation(ppinfo_client, rest_internal_client)
            self.check_absence(rest_internal_client)

        emails = self.get_bodies_mailing_from_db('pb')

        recipients = sorted([sorted(mail['to']) for mail in emails], key=lambda lst: (len(lst), lst))
        subjects = sorted([mail['templateMeta']['subject'] for mail in emails],
                          key=lambda subject: (len(subject), subject))

        assert len(recipients) == 2, f'Письма не отправлены\n {recipients}'

        assert subjects[
                   0] == f'Окончание делегирования прав на редактирование продукта «1_Не трогать, для АТ, делегирование del»', f'У письма некорректный заголовок, сейчас заголовок - ={emails[0]["templateMeta"]["subject"]}'

        assert subjects[
                   1] == f'Окончание делегирования прав на редактирование продукта  «1_Не трогать, для АТ, делегирование del»', f'У письма некорректный заголовок, сейчас заголовок - ={emails[1]["templateMeta"]["subject"]}'

        assert recipients[0] == [
            'aikostrov1@mts.ru'], f'Получатели письма из группы информирования не совпадают с ожидаемыми \n {recipients[0]}'

        assert recipients[1] == [
            'ddsvetov1@mts.ru'], f'Получатели письма из группы информирования не совпадают с ожидаемыми \n {recipients[0]}'

        assert self.get_count_mailing_from_db('ntf') == 4 or 2, (
            f'По данному операции должны были отправится 4 писем, а отправилось {self.get_count_mailing_from_db("ntf")} писем: \n'
            'Делегирующему \n'
            'Делеганту \n')
