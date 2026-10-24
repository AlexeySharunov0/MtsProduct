import allure
import pytest
from requests import HTTPError

from API.models.criticality_class.criticality_class import CriticalityClass
from API.models.notification.notification import Notifications
from API.models.pmd.rest_internal_modules.actions import Actions
from API.models.pmd.rest_internal_modules.curators import Curators
from API.models.ppinfo.product_v1 import ProductV1

NAME = "Тест Notification (название не менять)"


@pytest.mark.api
@pytest.mark.notification
@allure.feature("Нотификации")
@pytest.mark.usefixtures('clear_db_notifications')
@allure.issue('https://jira.mts.ru/browse/PPI-2291',
              'PPInfo - Нотификация при получении класса критичности из SD')
class TestNotificationCriticalityClass(Notifications, CriticalityClass):
    @allure.title("Нотификация / Класс критичности / Получение сообщения")
    @pytest.mark.parametrize('cc_value', ['Business Critical', 'Business Support', 'Mission Critical'])
    def test_notification_criticality_class(self, rest_external_client, cc_value):
        with allure.step("Отправляем заявку из SD"):
            self.create_criticality_class_message(rest_external_client,
                                                  self.data_criticality_class({"productCriticalityClass": cc_value},
                                                                              product_code='BI_22315'))

        with allure.step("Проверяем, что админ получил корректное письмо"):
            emails = self.get_bodies_mailing_from_db('pmd')

            recipients = sorted([sorted(mail['to']) for mail in emails], key=lambda lst: (len(lst), lst))
            subjects = sorted([mail['templateMeta']['subject'] for mail in emails],
                              key=lambda subject: (len(subject), subject))

            assert len(recipients) == 1, f'Письма не отправлены\n {recipients}'
            assert recipients[0] == ['pymaslenkov@mts.ru'], f'Админ не получили письмо \n {recipients[0]}'
            assert subjects[
                       0] == f'Обновление класса критичности продукта «Тест Notification (название не менять)» из ServiceDesk', f'У письма некорректный заголовок, сейчас заголовок - ={emails[0]["templateMeta"]["subject"]}'
            assert self.get_count_mailing_from_db('ntf') == 1, (
                f'По данному операции должны были отправится 7 писем, а отправилось {self.get_count_mailing_from_db("ntf")} писем: \n'
                'Админу о получении сообщение на изменения класса критичности\n')


@pytest.mark.api
@pytest.mark.notification
@allure.feature("Нотификации")
@pytest.mark.usefixtures('clear_db_notifications')
@allure.issue('https://jira.mts.ru/browse/PPI-2360', 'PPInfo - Нотификации кураторам по кластерам')
class TestNotificationCurator(Notifications, Actions, Curators):

    @allure.title('Нотификации / Кураторы / Редактирование кластера / Переход из одного в другой')
    @pytest.mark.parametrize(['value_1', 'value_2'],
                             [[['23f83f41-7b66-4732-9491-0a09e3d3e64a', 'ИТ-кластер \"Финтех\"'],
                               ['3da18dd1-ba07-4a45-8ac7-2c0b644551e1',
                                'ИТ-кластер \"Телеком\"']]])
    def test_notification_curator_change(self, ppinfo_client, rest_internal_client, value_1, value_2):
        with allure.step('Устанавливаем кураторов в кластеры'):
            body = self.get_data_for_curator(value_1)
            self.change_product(ppinfo_client, body)

            self.change_curators(rest_internal_client, 'pakapustin', attribute_id='04e8b2af-ebbc-40b6-b6cb-2f86863f36af',
                                 value_id=value_1[0])
            self.change_curators(rest_internal_client, 'mvpukhov', attribute_id='04e8b2af-ebbc-40b6-b6cb-2f86863f36af',
                                 value_id=value_2[0])

            self.delete_mailing_from_db('pmd')

            body = self.get_data_for_curator(value_2)
            self.change_product(ppinfo_client, body)

        emails = self.get_bodies_mailing_from_db('pmd')

        recipients = [sorted(mail['to']) for mail in emails]
        subjects = [mail['templateMeta']['subject'] for mail in emails]

        assert len(recipients) == 1, f'Письма не отправлены\n {recipients}'

        for subject in subjects:
            assert subject == 'У продукта «Тест Notification (название не менять)» изменился кластер', f'У письма некорректный заголовок, сейчас заголовок - ={emails[0]["templateMeta"]["subject"]}'

        assert recipients[0] == ['maksim.pukhovsky@mts.ru',
                                 'pakapustin@mts.ru'], f'Кураторы по кластерам не получили письмо \n {recipients[0]}'

        assert emails[0]['templateMeta']['updateAttributes'][0][
                   'oldValue'] == 'ИТ-кластер "Финтех"', 'Не отображено старое значение кластера'

        assert emails[0]['templateMeta']['updateAttributes'][0][
                   'newValue'] == 'ИТ-кластер "Телеком"', 'Не отображено новое значение кластера'

    @allure.title('Нотификации / Кураторы / Редактирование кластера / Переход из пустого в новый')
    @pytest.mark.parametrize(['value_1', 'value_2'],
                             [[['23f83f41-7b66-4732-9491-0a09e3d3e64a', 'ИТ-кластер \"Финтех\"'], []]])
    def test_notification_curator_change_from_empty(self, ppinfo_client, rest_internal_client, value_1, value_2):
        with allure.step('Устанавливаем кураторов в кластеры'):
            try:
                body = self.get_data_for_curator(value_2)
                self.change_product(ppinfo_client, body)
            except HTTPError:
                pass

            self.change_curators(rest_internal_client, 'pakapustin', attribute_id='04e8b2af-ebbc-40b6-b6cb-2f86863f36af',
                                 value_id=value_1[0])

            self.delete_mailing_from_db('pmd')

            body = self.get_data_for_curator(value_1)
            self.change_product(ppinfo_client, body)



        emails = self.get_bodies_mailing_from_db('pmd')

        recipients = [sorted(mail['to']) for mail in emails]
        subjects = [mail['templateMeta']['subject'] for mail in emails]

        assert len(recipients) == 1, f'Письма не отправлены\n {recipients}'

        for subject in subjects:
            assert subject == 'У продукта «Тест Notification (название не менять)» изменился кластер', f'У письма некорректный заголовок, сейчас заголовок - ={emails[0]["templateMeta"]["subject"]}'

        assert recipients[0] == ['pakapustin@mts.ru'], f'Кураторы по кластерам не получили письмо \n {recipients[0]}'

        assert emails[0]['templateMeta']['updateAttributes'][0][
                   'oldValue'] == 'Пусто', 'Не отображено старое значение кластера'

        assert emails[0]['templateMeta']['updateAttributes'][0][
                   'newValue'] == 'ИТ-кластер "Финтех"', 'Не отображено новое значение кластера'

    @allure.title('Нотификации / Кураторы / Редактирование кластера / Переход из кластера в пустой')
    @pytest.mark.parametrize(['value_1', 'value_2'],
                             [[['23f83f41-7b66-4732-9491-0a09e3d3e64a', 'ИТ-кластер \"Финтех\"'], []]])
    def test_notification_curator_change_to_empty(self, ppinfo_client, rest_internal_client, value_1, value_2):
        with allure.step('Устанавливаем кураторов в кластеры'):
            body = self.get_data_for_curator(value_1)
            self.change_product(ppinfo_client, body)

            self.delete_mailing_from_db('pmd')
            self.change_curators(rest_internal_client, 'pakapustin', attribute_id='04e8b2af-ebbc-40b6-b6cb-2f86863f36af',
                                 value_id=value_1[0])

            body = self.get_data_for_curator(value_2)
            self.change_product(ppinfo_client, body)


        emails = self.get_bodies_mailing_from_db('pmd')

        recipients = [sorted(mail['to']) for mail in emails]
        subjects = [mail['templateMeta']['subject'] for mail in emails]

        assert len(recipients) == 1, f'Письма не отправлены\n {recipients}'

        for subject in subjects:
            assert subject == 'У продукта «Тест Notification (название не менять)» изменился кластер', f'У письма некорректный заголовок, сейчас заголовок - ={emails[0]["templateMeta"]["subject"]}'

        assert recipients[0] == ['pakapustin@mts.ru'], f'Кураторы по кластерам не получили письмо \n {recipients[0]}'

        assert emails[0]['templateMeta']['updateAttributes'][0][
                   'oldValue'] == 'ИТ-кластер "Финтех"', 'Не отображено старое значение кластера'

        assert emails[0]['templateMeta']['updateAttributes'][0][
                   'newValue'] == 'Пусто', 'Не отображено новое значение кластера'
