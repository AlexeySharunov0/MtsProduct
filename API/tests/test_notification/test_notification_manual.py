import allure
import pytest

from API.models.criticality_class.criticality_class import CriticalityClass
from API.models.delegation.delegation import Delegation
from API.models.pmd.rest_internal_modules.actions import Actions
from API.models.pmd.rest_internal_modules.curators import Curators
from API.models.ppinfo.product_v1 import ProductV1
from API.utils.notificion_links import NotificationLinks as links
from API.models.notification.notification import Notifications


# ------------------------------------------------ Создание через заявку -----------------------------------------------
@pytest.mark.manual
@pytest.mark.notification
@allure.feature("Нотификации")
class TestManualNotificationBriefCreation(Notifications):


    @allure.title("Ручная проверка нотификации / Заявка / Создание продукта / Отправка заявки")
    @pytest.mark.parametrize("product_type", ["external", "internal"])
    def test_manual_notification_brief_create_product_send(self, ppinfo_client, ppinfo_user_client, product_type):
        self.delete_all_messages()
        with allure.step("Отправляем заявку"):
            name = self.text
            body = self.get_body_for_brief_creation(product_type, name)
            brief_id = self.crete_brief_by_user(ppinfo_user_client, body)
            number = " № " + self.get_brief_by_id(ppinfo_client, brief_id)["number"]

        allure.attach(links.product_creation, name='Создание продукта')
        with allure.step('Проверяем письмо инициатору aikostrov@mts.ru'):
            with allure.step(
                    f'Ищем письмо [Ваша заявка{number} на создание продукта «{name}» отправлена на модерацию]'):
                pass
            with allure.step('Общие проверки'):
                with allure.step('Баннер кликабельный, соответствует теме письма, ведет на product.mts.ru'):
                    pass
                with allure.step(f'Кнопка открыть заявку ведет на https://stage.prodboard.mts.ru/brief/{brief_id}'):
                    pass
                with allure.step('Проверить, что все элементы отображаются корректно'):
                    pass
            with allure.step('Проверяем основной блок'):
                with allure.step('Название жирное, совпадает с темой письма'):
                    pass
                with allure.step('Проверяем заполнение полей в соответствии с Создание #1'):
                    pass

        with allure.step('Проверяем письмо админу pymaslenkov@mts.ru'):
            with allure.step(f'Ищем письмо [Вам направлена заявка{number} на создание продукта «{name}»]'):
                pass
            with allure.step('Общие проверки'):
                with allure.step('Баннер кликабельный, соответствует теме письма, ведет на product.mts.ru'):
                    pass
                with allure.step(f'Кнопка открыть заявку ведет на https://stage.prodboard.mts.ru/brief/{brief_id}'):
                    pass
                with allure.step('Проверить, что все элементы отображаются корректно'):
                    pass
            with allure.step('Проверяем основной блок'):
                with allure.step('Название жирное, совпадает с темой письма'):
                    pass
                with allure.step('Проверяем заполнение полей в соответствии с Создание #2'):
                    pass
            with allure.step('Проверяем Блок свойств'):
                with allure.step('Проверяем заполнение полей в соответствии с Создание #2'):
                    pass

    @allure.title("Ручная проверка нотификации / Заявка / Создание продукта / Взятие в работу")
    @pytest.mark.parametrize("product_type", ["internal", "external"])
    def test_manual_notification_brief_create_product_take_to_work(self, ppinfo_client, ppinfo_user_client, product_type):
        self.delete_all_messages()
        with allure.step("Отправляем заявку"):
            name = self.text
            body = self.get_body_for_brief_creation(product_type, name)
            brief_id = self.crete_brief_by_user(ppinfo_user_client, body)
            number = "№ " + self.get_brief_by_id(ppinfo_client, brief_id)["number"]
            self.take_to_work(ppinfo_client, brief_id, {"login": "asnikiforov1"})

        allure.attach(links.product_creation, name='Создание продукта')
        with allure.step('Проверяем письмо инициатору aikostrov@mts.ru'):
            with allure.step(
                    f'Ищем письмо [Ваша заявка {number} на создание продукта «{name}» — взята в работу]'):
                pass
            with allure.step('Общие проверки'):
                with allure.step('Баннер кликабельный, соответствует теме письма, ведет на product.mts.ru'):
                    pass
                with allure.step(f'Кнопка открыть заявку ведет на https://stage.prodboard.mts.ru/brief/{brief_id}'):
                    pass
                with allure.step('Проверить, что все элементы отображаются корректно'):
                    pass
            with allure.step('Проверяем основной блок'):
                with allure.step('Название жирное, совпадает с темой письма'):
                    pass
                with allure.step('Проверяем заполнение полей в соответствии с Создание #3'):
                    pass
                with allure.step('Модератор кликабельный, при клике переходим в почту с предзаполненным адресатом'):
                    pass

        with allure.step('Проверяем письмо админу pymaslenkov@mts.ru'):
            with allure.step(f'Ищем письмо [Заявка {number} на создание продукта «{name}» — взята в работу»]'):
                pass
            with allure.step('Общие проверки'):
                with allure.step('Баннер кликабельный, соответствует теме письма, ведет на product.mts.ru'):
                    pass
                with allure.step(f'Кнопка открыть заявку ведет на https://stage.prodboard.mts.ru/brief/{brief_id}'):
                    pass
                with allure.step('Проверить, что все элементы отображаются корректно'):
                    pass
            with allure.step('Проверяем основной блок'):
                with allure.step('Название жирное, совпадает с темой письма'):
                    pass
                with allure.step('Проверяем заполнение полей в соответствии с Создание #4'):
                    pass
                with allure.step('Модератор кликабельный, при клике переходим в почту с предзаполненным адресатом'):
                    pass

    @allure.title("Ручная проверка нотификации / Заявка / Создание продукта / Принятие заявки")
    @pytest.mark.parametrize("product_type, mail",
                             [["internal", "asnikiforov1@mts.ru"], ["external", "svkurochkin@mts.ru"]])
    def test_manual_notification_brief_create_product_accept_inform(self, pmd_internal_gw_client, ppinfo_client, ppinfo_user_client, product_type, mail):
        with allure.step("Отправляем заявку"):
            name = self.text
            body = self.get_body_for_brief_creation(product_type, name)
            brief_id = self.crete_brief_by_user(ppinfo_user_client, body)
            self.take_to_work(ppinfo_client, brief_id, {"login": "asnikiforov1"})
            self.change_brief_status(ppinfo_client, brief_id, {"status": "statusApproval"})

        self.delete_product_notification(pmd_internal_gw_client, ppinfo_client, brief_id)

        allure.attach(links.product_creation, name='Создание продукта')
        with allure.step(
                f'Проверяем письмо aikostrov@mts.ru, {mail}, sa000ppinfouser@nts.ru (инициатор, группа информирования, рук-во в составе)'):
            with allure.step(
                    f'Ищем письмо [Продукт «{name}» создан в статусе «Выведен из КЭ»]'):
                pass
            with allure.step('Общие проверки'):
                with allure.step('Баннер кликабельный, соответствует теме письма, ведет на product.mts.ru'):
                    pass
                with allure.step('Кнопка Открыть продукт ведет на страницу продукта'):
                    pass
                with allure.step('Проверить, что все элементы отображаются корректно'):
                    pass
            with allure.step('Проверяем основной блок'):
                with allure.step('Название жирное, название продукта кликабельное и ведет на страницу продукта'):
                    pass
                with allure.step('Проверяем заполнение полей в соответствии с Создание #7'):
                    pass

        with allure.step('Проверяем письмо админу pymaslenkov@mts.ru и модератору ddsvetov1@mts.ru'):
            with allure.step(f'Ищем письмо [Продукт «{name}» создан в статусе «Выведен из КЭ»]'):
                pass
            with allure.step('Общие проверки'):
                with allure.step('Баннер кликабельный, соответствует теме письма, ведет на product.mts.ru'):
                    pass
                with allure.step('Кнопка Открыть продукт ведет на страницу продукта'):
                    pass
                with allure.step('Проверить, что все элементы отображаются корректно'):
                    pass
            with allure.step('Проверяем основной блок'):
                with allure.step('Название жирное, название продукта кликабельное и ведет на страницу продукта'):
                    pass
                with allure.step('Проверяем заполнение полей в соответствии с Создание #8/9'):
                    pass

    @allure.title("Ручная проверка нотификации / Заявка / Создание продукта / Отклонение заявки")
    @pytest.mark.parametrize("product_type, mail",
                             [["internal", "asnikiforov1@mts.ru"], ["external", "svkurochkin@mts.ru"]])
    def test_manual_notification_brief_create_product_deny_inform(self, ppinfo_client, ppinfo_user_client, product_type, mail):
        self.delete_all_messages()
        with allure.step("Отправляем заявку"):
            name = self.text
            body = self.get_body_for_brief_creation(product_type, name)
            brief_id = self.crete_brief_by_user(ppinfo_user_client, body)
            number = "№ " + self.get_brief_by_id(ppinfo_client, brief_id)["number"]
            self.take_to_work(ppinfo_client, brief_id, {"login": "asnikiforov1"})
            self.change_brief_status(ppinfo_client, brief_id, {"status": "statusDeclined"})

        allure.attach(links.product_creation, name='Создание продукта')
        with allure.step('Проверяем письмо инициатору aikostrov@mts.ru'):
            with allure.step(
                    f'Ищем письмо [Ваша заявка {number} на создание продукта «{name}» отклонена]'):
                pass
            with allure.step('Общие проверки'):
                with allure.step('Баннер кликабельный, соответствует теме письма, ведет на product.mts.ru'):
                    pass
                with allure.step(f'Кнопка открыть заявку ведет на https://stage.prodboard.mts.ru/brief/{brief_id}'):
                    pass
                with allure.step('Проверить, что все элементы отображаются корректно'):
                    pass
            with allure.step('Проверяем основной блок'):
                with allure.step('Название жирное, совпадает с темой письма'):
                    pass
                with allure.step('Проверяем заполнение полей в соответствии с Создание #5'):
                    pass
                with allure.step('Модератор кликабельный, при клике переходим в почту с предзаполненным адресатом'):
                    pass

        with allure.step('Проверяем письмо админу pymaslenkov@mts.ru'):
            with allure.step(f'Ищем письмо [Заявка {number} на создание продукта «{name}» отклонена»]'):
                pass
            with allure.step('Общие проверки'):
                with allure.step('Баннер кликабельный, соответствует теме письма, ведет на product.mts.ru'):
                    pass
                with allure.step(f'Кнопка открыть заявку ведет на https://stage.prodboard.mts.ru/brief/{brief_id}'):
                    pass
                with allure.step('Проверить, что все элементы отображаются корректно'):
                    pass
            with allure.step('Проверяем основной блок'):
                with allure.step('Название жирное, совпадает с темой письма'):
                    pass
                with allure.step('Проверяем заполнение полей в соответствии с Создание #6'):
                    pass
                with allure.step('Модератор кликабельный, при клике переходим в почту с предзаполненным адресатом'):
                    pass


# -------------------------------------------------- Создание админом --------------------------------------------------
@allure.feature("Нотификации")
@pytest.mark.manual
class TestManualNotificationAdminCreation(Notifications):
    @allure.title("Ручная проверка нотификации / Админ / Создание продукта")
    @pytest.mark.parametrize("product_type, mail",
                             [["Vnutrennii", "asnikiforov1@mts.ru"], ["Vneshnii", "svkurochkin@mts.ru"]])
    def test_manual_notification_admin_create_product_accept_inform(self, ppinfo_client, product_type, mail):
        self.delete_all_messages()
        with allure.step("Создаем продукт админом"):
            gen_name = self.text
            self.create_product(ppinfo_client, self.get_data_for_product_creation(product_type, name=gen_name))

        allure.attach(links.product_creation, name='Создание продукта')
        with allure.step(f'Проверяем письмо группе информирования {mail}'):
            with allure.step(
                    f'Ищем письмо [Продукт «{gen_name}» создан в статусе «Выведен из КЭ»]'):
                pass
            with allure.step('Общие проверки'):
                with allure.step('Баннер кликабельный, соответствует теме письма, ведет на product.mts.ru'):
                    pass
                with allure.step('Кнопка Открыть продукт ведет на страницу продукта'):
                    pass
                with allure.step('Проверить, что все элементы отображаются корректно'):
                    pass
            with allure.step('Проверяем основной блок'):
                with allure.step('Название жирное, название продукта кликабельное и ведет на страницу продукта'):
                    pass
                with allure.step('Проверяем заполнение полей в соответствии с Создание #8 (без поля модератор)'):
                    pass

        with allure.step('Проверяем письмо админу pymaslenkov@mts.ru и модератору ddsvetov1@mts.ru'):
            with allure.step(f'Ищем письмо [Продукт «{gen_name}» создан в статусе «Выведен из КЭ»]'):
                pass
            with allure.step('Общие проверки'):
                with allure.step('Баннер кликабельный, соответствует теме письма, ведет на product.mts.ru'):
                    pass
                with allure.step('Кнопка Открыть продукт ведет на страницу продукта'):
                    pass
                with allure.step('Проверить, что все элементы отображаются корректно'):
                    pass
            with allure.step('Проверяем основной блок'):
                with allure.step('Название жирное, название продукта кликабельное и ведет на страницу продукта'):
                    pass
                with allure.step('Проверяем заполнение полей в соответствии с Создание #9 (без поля модератор)'):
                    pass


# ------------------------------------------------- Удаление продукта --------------------------------------------------
@allure.feature("Нотификации")
@pytest.mark.manual
class TestManualNotificationDelete(Notifications):

    @allure.title("Ручная проверка нотификации / Удаление продукта")
    def test_manual_notification_delete(self, pmd_internal_gw_client, ppinfo_client, ppinfo_user_client):
        self.delete_all_messages()
        with allure.step("Отправляем заявку"):
            gen_name = self.text
            body = self.get_body_for_brief_all_roles(gen_name)
            brief_id = self.crete_brief_by_user(ppinfo_user_client, body)
            self.take_to_work(ppinfo_client, brief_id, {"login": "asnikiforov1"})
            self.change_brief_status(ppinfo_client, brief_id, {"status": "statusApproval"})
            self.delete_product_notification(pmd_internal_gw_client, ppinfo_client, brief_id)

        allure.attach(links.product_delete, name='Удаление продукта')
        with allure.step('Проверяем письмо PO zimina@mts.ru и CPO nolesnikov@mts.ru'):
            with allure.step(f'Ищем письмо [Продукт «{gen_name}» удален]'):
                pass
            with allure.step('Общие проверки'):
                with allure.step('Баннер кликабельный, соответствует теме письма, ведет на product.mts.ru'):
                    pass
                with allure.step('Кнопка Открыть продукт ведет на страницу продукта'):
                    pass
                with allure.step('Проверить, что все элементы отображаются корректно'):
                    pass
            with allure.step('Проверяем основной блок'):
                with allure.step('Название жирное, название продукта кликабельное и ведет на страницу продукта'):
                    pass
                with allure.step('Проверяем заполнение полей в соответствии с Удаление #1'):
                    pass


# --------------------------------------------- Редактирование через заявку --------------------------------------------
NAME = "Тест Notification (название не менять)"


@pytest.mark.manual
@pytest.mark.notification
@allure.feature("Нотификации")
class TestManualNotificationBriefUpdate(Notifications):

    @allure.title("Ручная проверка нотификаций / Заявка / Редактирование / Отправка заявки")
    def test_manual_notification_brief_update_send(self, ppinfo_client, ppinfo_user_client):
        self.delete_all_messages()
        with allure.step("Отправляем заявку"):
            body = self.get_body_for_brief_update()
            brief_id = self.crete_brief_by_user(ppinfo_user_client, body)
            number = "№ " + self.get_brief_by_id(ppinfo_client, brief_id)["number"]

        allure.attach(links.product_change, name='Редактирование продукта')
        with allure.step('Проверяем письмо инициатору aikostrov@mts.ru'):
            with allure.step(
                    f'Ищем письмо [Ваша заявка {number} на редактирование продукта «{NAME}» отправлена на модерацию]'):
                pass
            with allure.step('Общие проверки'):
                with allure.step('Баннер кликабельный, соответствует теме письма, ведет на product.mts.ru'):
                    pass
                with allure.step(f'Кнопка открыть заявку ведет на https://stage.prodboard.mts.ru/brief/{brief_id}'):
                    pass
                with allure.step('Проверить, что все элементы отображаются корректно'):
                    pass
            with allure.step('Проверяем основной блок'):
                with allure.step('Название жирное, совпадает с темой письма, название продукта кликабельное'):
                    pass
                with allure.step('Проверяем заполнение полей в соответствии с Редактирование #1'):
                    pass
            with allure.step('Проверяем блок свойств'):
                with allure.step('Проверяем заполнение полей'):
                    pass
                with allure.step('Проверяем наличие стрелочек, старых и новых значений'):
                    pass

        with allure.step('Проверяем письмо админу pymaslenkov@mts.ru'):
            with allure.step(f'Ищем письмо [Вам направлена заявка {number} на редактирование продукта «{NAME}»]'):
                pass
            with allure.step('Общие проверки'):
                with allure.step('Баннер кликабельный, соответствует теме письма, ведет на product.mts.ru'):
                    pass
                with allure.step(f'Кнопка открыть заявку ведет на https://stage.prodboard.mts.ru/brief/{brief_id}'):
                    pass
                with allure.step('Проверить, что все элементы отображаются корректно'):
                    pass
            with allure.step('Проверяем основной блок'):
                with allure.step('Название жирное, совпадает с темой письма, название продукта кликабельное'):
                    pass
                with allure.step('Проверяем заполнение полей в соответствии с Редактирование #3'):
                    pass
            with allure.step('Проверяем блок свойств'):
                with allure.step('Проверяем заполнение полей'):
                    pass
                with allure.step('Проверяем наличие стрелочек, старых и новых значений'):
                    pass

    @allure.title("Ручная проверка нотификаций / Заявка / Редактирование продукта / Взятие в работу")
    def test_manual_notification_brief_update_take_to_work(self, ppinfo_client, ppinfo_user_client):
        self.delete_all_messages()
        with allure.step("Отправляем заявку"):
            body = self.get_body_for_brief_update()
            brief_id = self.crete_brief_by_user(ppinfo_user_client, body)
            number = "№ " + self.get_brief_by_id(ppinfo_client, brief_id)["number"]
            self.take_to_work(ppinfo_client, brief_id, {"login": "asnikiforov1"})

        allure.attach(links.product_change, name='Редактирование продукта')
        with allure.step('Проверяем письмо инициатору aikostrov@mts.ru'):
            with allure.step(
                    f'Ищем письмо [Ваша заявка {number} на редактирование продукта «{NAME}» — взята в работу]'):
                pass
            with allure.step('Общие проверки'):
                with allure.step('Баннер кликабельный, соответствует теме письма, ведет на product.mts.ru'):
                    pass
                with allure.step(f'Кнопка открыть заявку ведет на https://stage.prodboard.mts.ru/brief/{brief_id}'):
                    pass
                with allure.step('Проверить, что все элементы отображаются корректно'):
                    pass
            with allure.step('Проверяем основной блок'):
                with allure.step('Название жирное, совпадает с темой письма, название продукта кликабельное'):
                    pass
                with allure.step('Проверяем заполнение полей в соответствии с Редактирование #3'):
                    pass

        with allure.step('Проверяем письмо админу pymaslenkov@mts.ru'):
            with allure.step(f'Ищем письмо [Заявка {number} на редактирование продукта «{NAME}» — взята в работу]'):
                pass
            with allure.step('Общие проверки'):
                with allure.step('Баннер кликабельный, соответствует теме письма, ведет на product.mts.ru'):
                    pass
                with allure.step(f'Кнопка открыть заявку ведет на https://stage.prodboard.mts.ru/brief/{brief_id}'):
                    pass
                with allure.step('Проверить, что все элементы отображаются корректно'):
                    pass
            with allure.step('Проверяем основной блок'):
                with allure.step('Название жирное, совпадает с темой письма, название продукта кликабельное'):
                    pass
                with allure.step('Проверяем заполнение полей в соответствии с Редактирование #4'):
                    pass

    @allure.title("Ручная проверка нотификаций / Заявка / Редактирование продукта / Принятие заявки")
    def test_manual_notification_brief_update_accept_inform(self, ppinfo_client, ppinfo_user_client):
        self.delete_all_messages()
        with allure.step("Отправляем заявку"):
            body = self.get_body_for_brief_update()
            brief_id = self.crete_brief_by_user(ppinfo_user_client, body)
            self.take_to_work(ppinfo_client, brief_id, {"login": "asnikiforov1"})
            self.change_brief_status(ppinfo_client, brief_id, {"status": "statusApproval"})

        allure.attach(links.product_change, name='Редактирование продукта')
        with allure.step('Проверяем письмо инициатору aikostrov@mts.ru'):
            with allure.step(f'Ищем письмо [Продукт «{NAME}» отредактирован]'):
                pass
            with allure.step('Общие проверки'):
                with allure.step('Баннер кликабельный, соответствует теме письма, ведет на product.mts.ru'):
                    pass
                with allure.step(f'Кнопка открыть заявку ведет на https://stage.prodboard.mts.ru/brief/{brief_id}'):
                    pass
                with allure.step('Проверить, что все элементы отображаются корректно'):
                    pass
            with allure.step('Проверяем основной блок'):
                with allure.step('Название жирное, совпадает с темой письма, название продукта кликабельное'):
                    pass
                with allure.step('Проверяем заполнение полей в соответствии с Редактирование #7'):
                    pass
            with allure.step('Проверяем блок свойств'):
                with allure.step('Проверяем заполнение полей'):
                    pass
                with allure.step('Проверяем наличие стрелочек, старых и новых значений'):
                    pass

        with allure.step('Проверяем письмо админу pymaslenkov@mts.ru'):
            with allure.step(f'Ищем письмо [Продукт «{NAME}» отредактирован]'):
                pass
            with allure.step('Общие проверки'):
                with allure.step('Баннер кликабельный, соответствует теме письма, ведет на product.mts.ru'):
                    pass
                with allure.step(f'Кнопка открыть заявку ведет на https://stage.prodboard.mts.ru/brief/{brief_id}'):
                    pass
                with allure.step('Проверить, что все элементы отображаются корректно'):
                    pass
            with allure.step('Проверяем основной блок'):
                with allure.step('Название жирное, совпадает с темой письма, название продукта кликабельное'):
                    pass
                with allure.step('Проверяем заполнение полей в соответствии с Редактирование #8'):
                    pass
            with allure.step('Проверяем блок свойств'):
                with allure.step('Проверяем заполнение полей'):
                    pass
                with allure.step('Проверяем наличие стрелочек, старых и новых значений'):
                    pass

        with allure.step(
                'Проверяем 3 отдельных письма рук-ву: zimina@mts.ru(PO), nolesnikov@mts.ru(CPO), aastrunin@mts.ru(CTO)'):
            with allure.step(f'Ищем письмо [Продукт «{NAME}» отредактирован]'):
                pass
            with allure.step('Общие проверки'):
                with allure.step('Баннер кликабельный, соответствует теме письма, ведет на product.mts.ru'):
                    pass
                with allure.step(f'Кнопка открыть заявку ведет на https://stage.prodboard.mts.ru/brief/{brief_id}'):
                    pass
                with allure.step('Проверить, что все элементы отображаются корректно'):
                    pass
            with allure.step('Проверяем основной блок'):
                with allure.step('Название жирное, совпадает с темой письма, название продукта кликабельное'):
                    pass
                with allure.step('Проверяем заполнение полей в соответствии с Редактирование #9'):
                    pass
            with allure.step('Проверяем блок свойств'):
                with allure.step('Проверяем заполнение полей'):
                    pass
                with allure.step('Проверяем наличие стрелочек, старых и новых значений'):
                    pass
                with allure.step(
                        'Описание не должно быть в письмах для PO и CTO (предварительно проверить настройки'):
                    pass

        with allure.step('Проверяем письмо группе информирования snkondratyev@mts.ru'):
            with allure.step(f'Ищем письмо [Продукт «{NAME}» отредактирован]'):
                pass
            with allure.step('Общие проверки'):
                with allure.step('Баннер кликабельный, соответствует теме письма, ведет на product.mts.ru'):
                    pass
                with allure.step(f'Кнопка открыть заявку ведет на https://stage.prodboard.mts.ru/brief/{brief_id}'):
                    pass
                with allure.step('Проверить, что все элементы отображаются корректно'):
                    pass
            with allure.step('Проверяем основной блок'):
                with allure.step('Название жирное, совпадает с темой письма, название продукта кликабельное'):
                    pass
                with allure.step('Проверяем заполнение полей в соответствии с Редактирование #10'):
                    pass
            with allure.step('Проверяем блок свойств'):
                with allure.step('Проверяем заполнение полей'):
                    pass
                with allure.step('Проверяем наличие стрелочек, старых и новых значений'):
                    pass

    @allure.title("Ручная проверка нотификаций / Заявка / Редактирование продукта / Отклонение заявки")
    def test_manual_notification_brief_update_deny_inform(self, ppinfo_client, ppinfo_user_client):
        self.delete_all_messages()
        with allure.step("Отправляем заявку"):
            body = self.get_body_for_brief_update()
            brief_id = self.crete_brief_by_user(ppinfo_user_client, body)
            number = "№ " + self.get_brief_by_id(ppinfo_client, brief_id)["number"]
            self.take_to_work(ppinfo_client, brief_id, {"login": "asnikiforov1"})
            self.change_brief_status(ppinfo_client, brief_id, {"status": "statusDeclined"})

        allure.attach(links.product_change, name='Редактирование продукта')
        with allure.step('Проверяем письмо инициатору aikostrov@mts.ru'):
            with allure.step(f'Ищем письмо [Ваша заявка {number} на редактирование продукта «{NAME}» отклонена]'):
                pass
            with allure.step('Общие проверки'):
                with allure.step('Баннер кликабельный, соответствует теме письма, ведет на product.mts.ru'):
                    pass
                with allure.step(f'Кнопка открыть заявку ведет на https://stage.prodboard.mts.ru/brief/{brief_id}'):
                    pass
                with allure.step('Проверить, что все элементы отображаются корректно'):
                    pass
            with allure.step('Проверяем основной блок'):
                with allure.step('Название жирное, совпадает с темой письма, название продукта кликабельное'):
                    pass
                with allure.step('Проверяем заполнение полей в соответствии с Редактирование #5'):
                    pass
            with allure.step('Проверяем блок свойств'):
                with allure.step('Проверяем заполнение полей'):
                    pass
                with allure.step('Проверяем наличие стрелочек, старых и новых значений'):
                    pass

        with allure.step('Проверяем письмо админу pymaslenkov@mts.ru'):
            with allure.step(f'Ищем письмо [Заявка {number} на редактирование продукта «{NAME}» отклонена]'):
                pass
            with allure.step('Общие проверки'):
                with allure.step('Баннер кликабельный, соответствует теме письма, ведет на product.mts.ru'):
                    pass
                with allure.step(f'Кнопка открыть заявку ведет на https://stage.prodboard.mts.ru/brief/{brief_id}'):
                    pass
                with allure.step('Проверить, что все элементы отображаются корректно'):
                    pass
            with allure.step('Проверяем основной блок'):
                with allure.step('Название жирное, совпадает с темой письма, название продукта кликабельное'):
                    pass
                with allure.step('Проверяем заполнение полей в соответствии с Редактирование #6'):
                    pass
            with allure.step('Проверяем блок свойств'):
                with allure.step('Проверяем заполнение полей'):
                    pass
                with allure.step('Проверяем наличие стрелочек, старых и новых значений'):
                    pass

    @allure.title("Ручная проверка нотификации иниц. закрытие / Заявка / Редактирование продукта / Принятие заявки")
    def test_manual_notification_start_close_brief_update_accept_inform(self, ppinfo_client, ppinfo_user_client):
        self.delete_all_messages()
        with allure.step("Отправляем заявку"):
            body = self.get_body_for_brief_update_start_close()
            brief_id = self.crete_brief_by_user(ppinfo_user_client, body)
            self.take_to_work(ppinfo_client, brief_id, {"login": "asnikiforov1"})
            self.change_brief_status(ppinfo_client, brief_id, {"status": "statusApproval"})

        allure.attach(links.product_change, name='Редактирование продукта')
        with allure.step(
                'Проверяем письмо инициатору ddsvetov@mts.ru и группе информ. sskopytin@mts.ru, dpsazonov3@mts.ru'):
            with allure.step(f'Ищем письмо [По продукту «{NAME}» инициировано закрытие]'):
                pass
            with allure.step('Общие проверки'):
                with allure.step('Баннер кликабельный, соответствует теме письма, ведет на product.mts.ru'):
                    pass
                with allure.step(f'Кнопка Открыть продукт ведет на страницу продукта'):
                    pass
                with allure.step('Проверить, что все элементы отображаются корректно'):
                    pass
            with allure.step('Проверяем основной блок'):
                with allure.step('Название жирное, совпадает с темой письма, название продукта кликабельное'):
                    pass
                with allure.step('Проверяем заполнение полей в соответствии с Редактирование #11'):
                    pass
            with allure.step('Проверяем блок свойств'):
                with allure.step('Проверяем заполнение полей'):
                    pass
                with allure.step('Проверяем наличие стрелочек, старых и новых значений'):
                    pass


# --------------------------------------------- Редактирование админом -------------------------------------------------
@pytest.mark.manual
@pytest.mark.notification
@allure.feature("Нотификации")
class TestManualNotificationAdminUpdate(Notifications):
    @allure.title("Ручная проверка нотификации / Админ / Редактирование продукта")
    def test_manual_notification_admin_update_accept_inform(self, ppinfo_client):
        self.delete_all_messages()
        with allure.step("Редактируем продукт"):
            body = self.get_data_for_admin_update()
            self.change_product(ppinfo_client, body)

        allure.attach(links.product_change, name='Редактирование продукта')

        with allure.step('Проверяем письмо админу pymaslenkov@mts.ru'):
            with allure.step(f'Ищем письмо [Продукт «{NAME}» отредактирован]'):
                pass
            with allure.step('Общие проверки'):
                with allure.step('Баннер кликабельный, соответствует теме письма, ведет на product.mts.ru'):
                    pass
                with allure.step(f'Кнопка Открыть продукт ведет на страницу продукта'):
                    pass
                with allure.step('Проверить, что все элементы отображаются корректно'):
                    pass
            with allure.step('Проверяем основной блок'):
                with allure.step('Название жирное, совпадает с темой письма, название продукта кликабельное'):
                    pass
                with allure.step('Проверяем заполнение полей в соответствии с Редактирование #8'):
                    pass
            with allure.step('Проверяем блок свойств'):
                with allure.step('Проверяем заполнение полей'):
                    pass
                with allure.step('Проверяем наличие стрелочек, старых и новых значений'):
                    pass

        with allure.step(
                'Проверяем 3 отдельных письма рук-ву: zimina@mts.ru(PO), nolesnikov@mts.ru(CPO), aastrunin@mts.ru(CTO)'):
            with allure.step(f'Ищем письмо [Продукт «{NAME}» отредактирован]'):
                pass
            with allure.step('Общие проверки'):
                with allure.step('Баннер кликабельный, соответствует теме письма, ведет на product.mts.ru'):
                    pass
                with allure.step(f'Кнопка Открыть продукт ведет на страницу продукта'):
                    pass
                with allure.step('Проверить, что все элементы отображаются корректно'):
                    pass
            with allure.step('Проверяем основной блок'):
                with allure.step('Название жирное, совпадает с темой письма, название продукта кликабельное'):
                    pass
                with allure.step('Проверяем заполнение полей в соответствии с Редактирование #9'):
                    pass
            with allure.step('Проверяем блок свойств'):
                with allure.step('Проверяем заполнение полей'):
                    pass
                with allure.step('Проверяем наличие стрелочек, старых и новых значений'):
                    pass
                with allure.step(
                        'Описание не должно быть в письмах для PO и CTO (предварительно проверить настройки'):
                    pass

        with allure.step('Проверяем письмо группе информирования snkondratyev@mts.ru'):
            with allure.step(f'Ищем письмо [Продукт «{NAME}» отредактирован]'):
                pass
            with allure.step('Общие проверки'):
                with allure.step('Баннер кликабельный, соответствует теме письма, ведет на product.mts.ru'):
                    pass
                with allure.step(f'Кнопка Открыть продукт ведет на страницу продукта'):
                    pass
                with allure.step('Проверить, что все элементы отображаются корректно'):
                    pass
            with allure.step('Проверяем основной блок'):
                with allure.step('Название жирное, совпадает с темой письма, название продукта кликабельное'):
                    pass
                with allure.step('Проверяем заполнение полей в соответствии с Редактирование #10'):
                    pass
            with allure.step('Проверяем блок свойств'):
                with allure.step('Проверяем заполнение полей'):
                    pass
                with allure.step('Проверяем наличие стрелочек, старых и новых значений'):
                    pass


# ----------------------------------------------- Добавление документа -------------------------------------------------
@pytest.mark.manual
@pytest.mark.notification
@allure.feature("Нотификации")
class TestManualNotificationBriefDocument(Notifications):

    @allure.title("Ручная проверка нотификации / Заявка / Добавление документа / Отправка заявки")
    def test_manual_notification_brief_document_send(self, ppinfo_user_api_client, ppinfo_client):
        self.delete_all_messages()
        with allure.step("Отправляем заявку"):
            body = self.get_data_for_doc_brief()
            brief_id = self.post_brief_doc_user(ppinfo_user_api_client, body=body)
            number = "№ " + self.get_brief_by_id(ppinfo_client, brief_id)["number"]

        allure.attach(links.add_document, name='Добавление документа')
        with allure.step('Проверяем письмо инициатору aikostrov@mts.ru'):
            with allure.step(
                    f'Ищем письмо [Ваша заявка {number} на добавление документа в продукт «{NAME}» отправлена на модерацию]'):
                pass
            with allure.step('Общие проверки'):
                with allure.step('Баннер кликабельный, соответствует теме письма, ведет на product.mts.ru'):
                    pass
                with allure.step(f'Кнопка открыть заявку ведет на https://stage.prodboard.mts.ru/brief/{brief_id}'):
                    pass
                with allure.step('Проверить, что все элементы отображаются корректно'):
                    pass
            with allure.step('Проверяем основной блок'):
                with allure.step('Название жирное, совпадает с темой письма, название продукта кликабельное'):
                    pass
                with allure.step('Проверяем заполнение полей в соответствии с Добавление #1'):
                    pass
            with allure.step('Проверяем блок Загруженный документ'):
                with allure.step('Проверяем заполнение полей'):
                    pass
                with allure.step('Проверяем, что документ кликабельный, скачивается'):
                    pass

        with allure.step('Проверяем письмо админу pymaslenkov@mts.ru'):
            with allure.step(
                    f'Ищем письмо [Вам направлена заявка {number} на добавление документа в продукт «{NAME}»]'):
                pass
            with allure.step('Общие проверки'):
                with allure.step('Баннер кликабельный, соответствует теме письма, ведет на product.mts.ru'):
                    pass
                with allure.step(f'Кнопка открыть заявку ведет на https://stage.prodboard.mts.ru/brief/{brief_id}'):
                    pass
                with allure.step('Проверить, что все элементы отображаются корректно'):
                    pass
            with allure.step('Проверяем основной блок'):
                with allure.step('Название жирное, совпадает с темой письма, название продукта кликабельное'):
                    pass
                with allure.step('Проверяем заполнение полей в соответствии с Добавление #5'):
                    pass
            with allure.step('Проверяем блок Загруженный документ'):
                with allure.step('Проверяем заполнение полей'):
                    pass
                with allure.step('Проверяем, что документ кликабельный, скачивается'):
                    pass

    @allure.title("Ручная проверка нотификации / Заявка / Добавление документа / Взятие в работу")
    def test_manual_notification_brief_document_take_to_work(self, ppinfo_user_api_client, ppinfo_client):
        self.delete_all_messages()
        with allure.step("Отправляем заявку"):
            body = self.get_data_for_doc_brief()
            brief_id = self.post_brief_doc_user(ppinfo_user_api_client, body=body)
            number = "№ " + self.get_brief_by_id(ppinfo_client, brief_id)["number"]
            self.take_to_work(ppinfo_client, brief_id, {"login": "asnikiforov1"})

        allure.attach(links.add_document, name='Добавление документа')
        with allure.step('Проверяем письмо инициатору aikostrov@mts.ru'):
            with allure.step(
                    f'Ищем письмо [Ваша заявка {number} на добавление документа в продукт «{NAME}» — взята в работу]'):
                pass
            with allure.step('Общие проверки'):
                with allure.step('Баннер кликабельный, соответствует теме письма, ведет на product.mts.ru'):
                    pass
                with allure.step(f'Кнопка открыть заявку ведет на https://stage.prodboard.mts.ru/brief/{brief_id}'):
                    pass
                with allure.step('Проверить, что все элементы отображаются корректно'):
                    pass
            with allure.step('Проверяем основной блок'):
                with allure.step('Название жирное, совпадает с темой письма, название продукта кликабельное'):
                    pass
                with allure.step('Проверяем заполнение полей в соответствии с Добавление #2'):
                    pass
            with allure.step('Проверяем блок Загруженный документ'):
                with allure.step('Проверяем заполнение полей'):
                    pass
                with allure.step('Проверяем, что документ кликабельный, скачивается'):
                    pass

        with allure.step('Проверяем письмо админу pymaslenkov@mts.ru'):
            with allure.step(
                    f'Ищем письмо [Заявка {number} на добавление документа в продукт «{NAME}» — взята в работу]'):
                pass
            with allure.step('Общие проверки'):
                with allure.step('Баннер кликабельный, соответствует теме письма, ведет на product.mts.ru'):
                    pass
                with allure.step(f'Кнопка открыть заявку ведет на https://stage.prodboard.mts.ru/brief/{brief_id}'):
                    pass
                with allure.step('Проверить, что все элементы отображаются корректно'):
                    pass
            with allure.step('Проверяем основной блок'):
                with allure.step('Название жирное, совпадает с темой письма, название продукта кликабельное'):
                    pass
                with allure.step('Проверяем заполнение полей в соответствии с Добавление #6'):
                    pass
            with allure.step('Проверяем блок Загруженный документ'):
                with allure.step('Проверяем заполнение полей'):
                    pass
                with allure.step('Проверяем, что документ кликабельный, скачивается'):
                    pass

    @allure.title("Ручная проверка нотификации / Заявка / Добавление документа / Принятие заявки")
    def test_manual_notification_brief_document_accept_inform(self, ppinfo_user_api_client, ppinfo_client):
        self.delete_all_messages()
        with allure.step("Отправляем заявку"):
            body = self.get_data_for_doc_brief()
            brief_id = self.post_brief_doc_user(ppinfo_user_api_client, body=body)
            number = "№ " + self.get_brief_by_id(ppinfo_client, brief_id)["number"]
            self.take_to_work(ppinfo_client, brief_id, {"login": "asnikiforov1"})
            self.change_brief_status(ppinfo_client, brief_id, {"status": "statusApproval"})

        allure.attach(links.add_document, name='Добавление документа')
        with allure.step('Проверяем письмо инициатору aikostrov@mts.ru'):
            with allure.step(
                    f'Ищем письмо [Ваша заявка {number} на добавление документа в продукт «{NAME}» принята]'):
                pass
            with allure.step('Общие проверки'):
                with allure.step('Баннер кликабельный, соответствует теме письма, ведет на product.mts.ru'):
                    pass
                with allure.step(f'Кнопка открыть заявку ведет на https://stage.prodboard.mts.ru/brief/{brief_id}'):
                    pass
                with allure.step('Проверить, что все элементы отображаются корректно'):
                    pass
            with allure.step('Проверяем основной блок'):
                with allure.step('Название жирное, совпадает с темой письма, название продукта кликабельное'):
                    pass
                with allure.step('Проверяем заполнение полей в соответствии с Добавление #3'):
                    pass
            with allure.step('Проверяем блок Загруженный документ'):
                with allure.step('Проверяем заполнение полей'):
                    pass
                with allure.step('Проверяем, что документ кликабельный, скачивается'):
                    pass

        with allure.step('Проверяем письмо админу pymaslenkov@mts.ru'):
            with allure.step(
                    f'Ищем письмо [Заявка {number} на добавление документа в продукт «{NAME}» принята]'):
                pass
            with allure.step('Общие проверки'):
                with allure.step('Баннер кликабельный, соответствует теме письма, ведет на product.mts.ru'):
                    pass
                with allure.step(f'Кнопка открыть заявку ведет на https://stage.prodboard.mts.ru/brief/{brief_id}'):
                    pass
                with allure.step('Проверить, что все элементы отображаются корректно'):
                    pass
            with allure.step('Проверяем основной блок'):
                with allure.step('Название жирное, совпадает с темой письма, название продукта кликабельное'):
                    pass
                with allure.step('Проверяем заполнение полей в соответствии с Добавление #8'):
                    pass
            with allure.step('Проверяем блок Загруженный документ'):
                with allure.step('Проверяем заполнение полей'):
                    pass
                with allure.step('Проверяем, что документ кликабельный, скачивается'):
                    pass

        with allure.step('Проверяем письмо группе информирования: zimina@mts.ru, aastrunin@mts.ru, nolesnikov@mts.ru'):
            with allure.step(
                    f'Ищем письмо [В продукт «{NAME}» добавлен документ]'):
                pass
            with allure.step('Общие проверки'):
                with allure.step('Баннер кликабельный, соответствует теме письма, ведет на product.mts.ru'):
                    pass
                with allure.step(f'Кнопка открыть заявку ведет на https://stage.prodboard.mts.ru/brief/{brief_id}'):
                    pass
                with allure.step('Проверить, что все элементы отображаются корректно'):
                    pass
            with allure.step('Проверяем основной блок'):
                with allure.step('Название жирное, совпадает с темой письма, название продукта кликабельное'):
                    pass
                with allure.step('Проверяем заполнение полей в соответствии с Добавление #9'):
                    pass
            with allure.step('Проверяем блок Загруженный документ'):
                with allure.step('Проверяем заполнение полей'):
                    pass
                with allure.step('Проверяем, что документ кликабельный, скачивается'):
                    pass

    @allure.title("Нотификация / Заявка / Добавление документа / Отклонение с информированием")
    def test_manual_notification_brief_document_deny_inform(self, ppinfo_user_api_client, ppinfo_client):
        self.delete_all_messages()
        with allure.step("Отправляем заявку"):
            body = self.get_data_for_doc_brief()
            brief_id = self.post_brief_doc_user(ppinfo_user_api_client, body=body)
            number = "№ " + self.get_brief_by_id(ppinfo_client, brief_id)["number"]
            self.take_to_work(ppinfo_client, brief_id, {"login": "asnikiforov1"})
            self.change_brief_status(ppinfo_client, brief_id, {"status": "statusDeclined"})

        allure.attach(links.add_document, name='Добавление документа')
        with allure.step('Проверяем письмо инициатору aikostrov@mts.ru'):
            with allure.step(
                    f'Ищем письмо [Ваша заявка {number} на добавление документа в продукт «{NAME}» отклонена]'):
                pass
            with allure.step('Общие проверки'):
                with allure.step('Баннер кликабельный, соответствует теме письма, ведет на product.mts.ru'):
                    pass
                with allure.step(f'Кнопка открыть заявку ведет на https://stage.prodboard.mts.ru/brief/{brief_id}'):
                    pass
                with allure.step('Проверить, что все элементы отображаются корректно'):
                    pass
            with allure.step('Проверяем основной блок'):
                with allure.step('Название жирное, совпадает с темой письма, название продукта кликабельное'):
                    pass
                with allure.step('Проверяем заполнение полей в соответствии с Добавление #4'):
                    pass
            with allure.step('Проверяем блок Загруженный документ'):
                with allure.step('Проверяем заполнение полей'):
                    pass
                with allure.step('Проверяем, что документ кликабельный, скачивается'):
                    pass

        with allure.step('Проверяем письмо админу pymaslenkov@mts.ru'):
            with allure.step(
                    f'Ищем письмо [Заявка {number} на добавление документа в продукт «{NAME}» отклонена]'):
                pass
            with allure.step('Общие проверки'):
                with allure.step('Баннер кликабельный, соответствует теме письма, ведет на product.mts.ru'):
                    pass
                with allure.step(f'Кнопка открыть заявку ведет на https://stage.prodboard.mts.ru/brief/{brief_id}'):
                    pass
                with allure.step('Проверить, что все элементы отображаются корректно'):
                    pass
            with allure.step('Проверяем основной блок'):
                with allure.step('Название жирное, совпадает с темой письма, название продукта кликабельное'):
                    pass
                with allure.step('Проверяем заполнение полей в соответствии с Добавление #7'):
                    pass
            with allure.step('Проверяем блок Загруженный документ'):
                with allure.step('Проверяем заполнение полей'):
                    pass
                with allure.step('Проверяем, что документ кликабельный, скачивается'):
                    pass


# ----------------------------------------------- Делегирование --------------------------------------------------------
@pytest.mark.manual
@pytest.mark.notification
@allure.feature("Нотификации")
class TestManualNotificationDelegation(Notifications):
    @allure.title("Ручная проверка нотификаций / Делегирование / Получение")
    def test_manual_notification_delegation_get(self, ppinfo_client, rest_internal_client):
        self.delete_all_messages()
        with allure.step("Выдаем права на делегирование"):
            self.remove_delegation(ppinfo_client, rest_internal_client)
            self.add_delegation(ppinfo_client)

        allure.attach(links.delegation, name='Делегирование')
        with allure.step('Проверяем письмо руководителю ddsvetov1@mts.ru'):
            with allure.step(
                    f'Ищем письмо [Вы делегировали права на редактирование продукта «1_Не трогать, для АТ, делегирование del»]'):
                pass
            with allure.step('Общие проверки'):
                with allure.step('Баннер кликабельный, соответствует теме письма, ведет на product.mts.ru'):
                    pass
                with allure.step(f'Кнопка Открыть продукт ведет на страницу продукта'):
                    pass
                with allure.step('Проверить, что все элементы отображаются корректно'):
                    pass
            with allure.step('Проверяем основной блок'):
                with allure.step('Название жирное, совпадает с темой письма, название продукта кликабельное'):
                    pass
                with allure.step('Проверяем заполнение полей в соответствии с Делегирование #1'):
                    pass

        with allure.step('Проверяем письмо сотруднику, получившему делегирование, aikostrov1@mts.ru'):
            with allure.step(
                    f'Ищем письмо [Вам делегировали права на редактирование продукта «1_Не трогать, для АТ, делегирование del»]'):
                pass
            with allure.step('Общие проверки'):
                with allure.step('Баннер кликабельный, соответствует теме письма, ведет на product.mts.ru'):
                    pass
                with allure.step(f'Кнопка Открыть продукт ведет на страницу продукта'):
                    pass
                with allure.step('Проверить, что все элементы отображаются корректно'):
                    pass
            with allure.step('Проверяем основной блок'):
                with allure.step('Название жирное, совпадает с темой письма, название продукта кликабельное'):
                    pass
                with allure.step('Проверяем заполнение полей в соответствии с Делегирование #2'):
                    pass

    @allure.title("Ручная проверка нотификаций / Делегирование / Окончание")
    def test_manual_notification_delegation_remove(self, ppinfo_client, rest_internal_client):
        self.delete_all_messages()
        with allure.step("Забираем права на делегирование"):
            self.remove_delegation(ppinfo_client, rest_internal_client)
            self.add_delegation(ppinfo_client)
            self.check_presence(rest_internal_client)
            self.remove_delegation(ppinfo_client, rest_internal_client)
            self.check_absence(rest_internal_client)

        allure.attach(links.delegation, name='Делегирование')
        with allure.step('Проверяем письмо руководителю ddsvetov1@mts.ru'):
            with allure.step(
                    f'Ищем письмо [Окончание делегирования прав на редактирование продукта «1_Не трогать, для АТ, делегирование del»]'):
                pass
            with allure.step('Общие проверки'):
                with allure.step('Баннер кликабельный, соответствует теме письма, ведет на product.mts.ru'):
                    pass
                with allure.step(f'Кнопка Открыть продукт ведет на страницу продукта'):
                    pass
                with allure.step('Проверить, что все элементы отображаются корректно'):
                    pass
            with allure.step('Проверяем основной блок'):
                with allure.step('Название жирное, совпадает с темой письма, название продукта кликабельное'):
                    pass
                with allure.step('Проверяем заполнение полей в соответствии с Делегирование #3'):
                    pass

        with allure.step('Проверяем письмо сотруднику, получившему делегирование, aikostrov1@mts.ru'):
            with allure.step(
                    f'Ищем письмо [Окончание делегирования прав на редактирование продукта «1_Не трогать, для АТ, делегирование del»]'):
                pass
            with allure.step('Общие проверки'):
                with allure.step('Баннер кликабельный, соответствует теме письма, ведет на product.mts.ru'):
                    pass
                with allure.step(f'Кнопка Открыть продукт ведет на страницу продукта'):
                    pass
                with allure.step('Проверить, что все элементы отображаются корректно'):
                    pass
            with allure.step('Проверяем основной блок'):
                with allure.step('Название жирное, совпадает с темой письма, название продукта кликабельное'):
                    pass
                with allure.step('Проверяем заполнение полей в соответствии с Делегирование #4'):
                    pass


# ------------------------------------------- Класс критичности --------------------------------------------------------
@pytest.mark.manual
@pytest.mark.notification
@allure.feature("Нотификации")
class TestManualNotificationCriticalityClass(Notifications, CriticalityClass):
    @allure.title("Ручная проверка нотификаций / Класс критичности / Получение сообщения")
    @pytest.mark.parametrize('cc_value', ['Business Critical', 'Business Support', 'Mission Critical'])
    def test_manual_notification_criticality_class(self, rest_external_client, cc_value):
        self.delete_all_messages()
        with allure.step("Отправляем заявку из SD"):
            self.create_criticality_class_message(rest_external_client, self.data_criticality_class({"productCriticalityClass": cc_value}, product_code='BI_22315'))

        allure.attach(links.criticality_class, name='Класс критичности')
        with allure.step('Проверяем письмо админу pymaslenkov@mts.ru'):
            with allure.step(f'Ищем письмо [Обновление класса критичности продукта «{NAME}» из ServiceDesk»]'):
                pass
            with allure.step('Общие проверки'):
                with allure.step('Баннер кликабельный, соответствует теме письма, ведет на product.mts.ru'):
                    pass
                with allure.step('Кнопка Открыть ведет на таблицу изменений свойств продукта'):
                    pass
                with allure.step('Проверить, что все элементы отображаются корректно'):
                    pass
            with allure.step('Проверяем основной блок'):
                with allure.step('Название жирное, совпадает с темой письма'):
                    pass
                with allure.step('Проверяем заполнение полей в соответствии с Класс Критичности #1'):
                    pass
                with allure.step('Гиперссылка ведет на продукт'):
                    pass


# ------------------------------------------- Кураторы ----------------------------------------------------------------
@pytest.mark.manual
@pytest.mark.notification
@allure.feature("Нотификации")
class TestNotificationCurator(Notifications, Actions, Curators):
    @allure.title('Ручная проверка нотификаций / Кураторы / Редактирование кластера')
    @pytest.mark.parametrize(['value_1', 'value_2'],
                             [[['fb3aefaf-ffe5-4836-ba9d-9736a99c0a3e', 'ИТ-кластер \"Финтех\"'],
                               ['f2b8dc4b-90bc-4140-b811-9ba228ad2366',
                                'ИТ-кластер \"Телеком\"']]])
    def test_manual_notification_curator_change(self, ppinfo_client, rest_internal_client, value_1, value_2):
        with allure.step('Устанавливаем кураторов в кластеры'):
            self.change_curators(rest_internal_client, 'pakapustin', attribute_id='04e8b2af-ebbc-40b6-b6cb-2f86863f36af',
                                 value_id=value_1[0])
            self.change_curators(rest_internal_client, 'mvpukhov', attribute_id='04e8b2af-ebbc-40b6-b6cb-2f86863f36af',
                                 value_id=value_2[0])
            body = self.get_data_for_curator(value_1)
            self.change_product(ppinfo_client, body)

        self.delete_all_messages()

        with allure.step('Меняем кластер в продукте'):
            body = self.get_data_for_curator(value_2)
            self.change_product(ppinfo_client, body)

        allure.attach(links.curators, name='Кураторы')
        with allure.step('Проверяем письмо кураторам yakapustin1@mts.ru и mvpukhov@mts.ru'):
            with allure.step(f'Ищем письмо [У продукта «Тест Notification (название не менять)» изменился кластер]'):
                pass
            with allure.step('Общие проверки'):
                with allure.step('Баннер кликабельный, соответствует теме письма, ведет на product.mts.ru'):
                    pass
                with allure.step('Кнопка Открыть продукт ведет на страницу продукта'):
                    pass
                with allure.step('Проверить, что все элементы отображаются корректно'):
                    pass
            with allure.step('Проверяем основной блок'):
                with allure.step('Название жирное, совпадает с темой письма'):
                    pass
                with allure.step('Проверяем заполнение полей в соответствии с Кураторы #1'):
                    pass
                with allure.step('Гиперссылка ведет на продукт'):
                    pass
