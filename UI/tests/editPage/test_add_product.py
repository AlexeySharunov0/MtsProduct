import time

import allure
import pytest

from UI.data.assertions_data import ProductsAsserts as assertions
from UI.tests.editPage.conftest import add_replace_page, user_add_replace_page


@pytest.mark.ui
@allure.feature("Заявки")
@allure.feature("Создание продукта")
class TestUserAddProduct:
    @allure.title('Шаги на странице добавления продукта / Страница выбора типа продукта')
    @allure.issue('https://jira.mts.ru/browse/PPI-1466',
                  'PPInfo - Блок "Шаги добавления продукта" - Добавление шага 1 и 2')
    def test_steps_on_add_page_is_visible(self, user_add_replace_page):
        with allure.step('Проверяем, что на странице выбора типа продукта отображены шаги'):
            assert user_add_replace_page.steps.is_visible(), 'На странице выбора типа продукта отображены шаги'
        with allure.step('Проверяем, что значком (галочкой) не отмечен пока никакой шаг'):
            assert user_add_replace_page.check_mark.are_not_visible(), 'Один из шагов отмечен галочкой'

    @allure.title('Шаги на странице добавления продукта / Страница заполнения заявки')
    @allure.issue('https://jira.mts.ru/browse/PPI-1466',
                  'PPInfo - Блок "Шаги добавления продукта" - Добавление шага 1 и 2')
    @pytest.mark.parametrize('product_type', ['commercial', 'internal'])
    def test_steps_on_add_page_form(self, user_add_replace_page, product_type):
        user_add_replace_page.start_work(product_type)
        with allure.step('Проверяем, что на странице добавления продукта отображены шаги'):
            assert user_add_replace_page.steps.is_visible(), 'Шагов нет'
        with allure.step('Проверяем, что первый шаг отмечен галочкой'):
            assert user_add_replace_page.check_step_marks(
                user_add_replace_page.check_mark[0], 'accept'), 'Первый шаг не отмечен галочкой'
        with allure.step('Проверяем, что значком отмечен только первый шаг'):
            assert user_add_replace_page.check_mark.count() == 1, 'Значком помечены больше или меньше 1 шага'

    @allure.title('Ссылка на FAQ отображена')
    @allure.issue('https://jira.mts.ru/browse/PPI-2534', 'PPInfo - Обновить ссылку на FAQ')
    def test_go_to_faq(self, user_add_replace_page):
        with allure.step('Проверяет урл в кнопке FAQ'):
            assert user_add_replace_page.faq.get_attribute('href') == assertions.faq_link, 'Ссылка не совпадает'

    @allure.title("Корректная отправка заявки на создание внешнего/внутреннего продукта обычным пользователем")
    @allure.issue('https://jira.mts.ru/browse/PPI-1466',
                  'PPInfo - Блок "Шаги добавления продукта" - Добавление шага 1 и 2')
    @allure.issue('https://jira.mts.ru/browse/PPI-2171', 'Блок "Шаги добавления продукта" - Добавление шага 3')
    @pytest.mark.parametrize('product_type', ['commercial', 'internal'])
    def test_add_product_user(self, user_add_replace_page, product_type):
        user_add_replace_page.start_work(product_type)
        user_add_replace_page.fill_required_fields()
        with allure.step('Проверяем, что 2 шага отмечены как пройденные'):
            assert user_add_replace_page.check_mark.count() == 2, 'Галочкой помечены больше или меньше 2 шагов'
            assert all(
                user_add_replace_page.check_step_marks(user_add_replace_page.check_mark.get_items()[i], 'accept') for i
                in
                range(0, 2)), 'Первые 2 шага не отмечены как пройденные'
        with allure.step('Отправляем заявку на модерацию'):
            user_add_replace_page.go_button.click()
            user_add_replace_page.wait_force(2)
        with allure.step('Проверяем, что 3 шага отмечены как пройденные'):
            assert user_add_replace_page.check_mark.count() == 3, 'Значком помечены меньше 3 шагов'
            assert all(
                user_add_replace_page.check_step_marks(user_add_replace_page.check_mark.get_items()[i], 'accept') for i
                in
                range(0, 2)), 'Первые 2 шага не отмечены как пройденные'
            assert user_add_replace_page.check_step_marks(user_add_replace_page.check_mark.get_items()[-1],
                                                          'registered'), 'Третий шаг не отмечен как зарегестрирован'
        with allure.step('Проверяем, что заявка зарегистрирована'):
            assert user_add_replace_page.status_info.get_text() == 'Заявка зарегистрирована', f'У заявки статус: {user_add_replace_page.status_info.get_text()}'

    @allure.title("Отправление заявки пользователем на создание продукта и одобрение админом")
    @pytest.mark.parametrize('product_type', ['commercial', 'internal'])
    def test_add_product_user_full_cycle_accept(self, user_add_replace_page, product_type):
        user_add_replace_page.start_work(product_type)
        user_add_replace_page.fill_required_fields()
        with allure.step('Отправляем заявку на модерацию'):
            user_add_replace_page.go_button.click()
        with allure.step('Ждем пока появится аллерт о том, что заявка зарегистрирована'):
            user_add_replace_page.status_info.is_visible()
        url = user_add_replace_page.url
        user_add_replace_page.login_admin()
        with allure.step('Заходим в заявку'):
            user_add_replace_page.get_page(url)
        with allure.step('Берем заявку в работу'):
            user_add_replace_page.take_to_work.click()
        with allure.step('Одобряем заявку'):
            user_add_replace_page.save_doc.click()
        time.sleep(2)

        with allure.step('Проверяем, что заявка выполнилась'):
            assert user_add_replace_page.status_info.get_text() == 'Заявка выполнена', f'У заявки статус: {user_add_replace_page.status_info.get_text()}'

        with allure.step('Переходим на страницу продукта'):
            user_add_replace_page.refresh()
            user_add_replace_page.link_to_product_in_brief.click()
        user_add_replace_page.delete_product()

        user_add_replace_page.login_user()
        user_add_replace_page.get_page(url)
        user_add_replace_page.wait()
        with allure.step('Проверяем, что 3 шага отмечены как пройденные'):
            assert user_add_replace_page.check_mark.count() == 3, 'Значком помечены меньше 3 шагов'
            assert all(
                user_add_replace_page.check_step_marks(user_add_replace_page.check_mark.get_items()[i], 'accept') for i
                in
                range(0, 3)), 'Все шаги не отмечены как пройденные'

    @allure.title("Шаги на странице добавления продукта / Страница заявки / Заявка в работе")
    @allure.issue('https://jira.mts.ru/browse/PPI-2171', 'Блок "Шаги добавления продукта" - Добавление шага 3')
    @pytest.mark.parametrize('product_type', ['commercial', 'internal'])
    def test_steps_brief_in_work(self, user_add_replace_page, product_type):
        user_add_replace_page.start_work(product_type)
        user_add_replace_page.fill_required_fields()
        with allure.step('Отправляем заявку на модерацию'):
            user_add_replace_page.go_button.click()
            user_add_replace_page.wait_force(2)
            user_add_replace_page.refresh()
        url = user_add_replace_page.url
        user_add_replace_page.login_admin()
        with allure.step('Заходим в заявку'):
            user_add_replace_page.get_page(url)
        with allure.step('Берем заявку в работу'):
            user_add_replace_page.take_to_work.click()
        user_add_replace_page.login_user()
        user_add_replace_page.get_page(url)
        with allure.step('Проверяем, что 3 шага отмечены как пройденные'):
            user_add_replace_page.wait()
            assert user_add_replace_page.check_mark.count() == 3, 'Значком помечены меньше 3 шагов'
            assert all(
                user_add_replace_page.check_step_marks(user_add_replace_page.check_mark.get_items()[i], 'accept') for i
                in
                range(0, 2)), 'Первые 2 шага не отмечены как пройденные'
            assert user_add_replace_page.check_step_marks(user_add_replace_page.check_mark.get_items()[-1],
                                                          'in_work'), 'Третий шаг не отмечен как в работе'

    @allure.title("Отправление заявки пользователем на создание продукта и отклонение админом")
    @allure.issue('https://jira.mts.ru/browse/PPI-2171', 'Блок "Шаги добавления продукта" - Добавление шага 3')
    @pytest.mark.parametrize('product_type', ['commercial', 'internal'])
    def test_add_product_user_full_cycle_reject(self, user_add_replace_page, product_type):
        user_add_replace_page.start_work(product_type)
        user_add_replace_page.fill_required_fields()
        with allure.step('Отправляем заявку на модерацию'):
            user_add_replace_page.go_button.click()
        with allure.step('Ждем пока появится аллерт о том, что заявка зарегистрирована'):
            user_add_replace_page.status_info.is_visible()
        url = user_add_replace_page.url
        user_add_replace_page.login_admin()
        with allure.step('Заходим в заявку'):
            user_add_replace_page.get_page(url)
        with allure.step('Берем заявку в работу'):
            user_add_replace_page.take_to_work.click()
        with allure.step('Отклоняем заявку'):
            user_add_replace_page.reject.click()

        with allure.step('Проверяем, что заявка отклонена'):
            assert user_add_replace_page.status_info.get_text() == 'Заявка отклонена', f'У заявки статус: {user_add_replace_page.status_info.get_text()}'

        user_add_replace_page.login_user()
        user_add_replace_page.get_page(url)
        with allure.step('Проверяем, что 3 шага отмечены как пройденные'):
            assert user_add_replace_page.check_mark.count() == 3, 'Значком помечены меньше 3 шагов'
            assert all(
                user_add_replace_page.check_step_marks(user_add_replace_page.check_mark.get_items()[i], 'accept') for i
                in
                range(0, 2)), 'Первые 2 шага не отмечены как пройденные'
            assert user_add_replace_page.check_step_marks(user_add_replace_page.check_mark.get_items()[-1],
                                                          'deny'), 'Третий шаг не отмечен как в работе'

    @allure.title("Отправление заявки пользователем на создание продукта и одобрение админом с редактированием")
    @pytest.mark.parametrize('product_type', ['commercial', 'internal'])
    def test_add_internal_user_add_input(self, user_add_replace_page, product_type):
        user_add_replace_page.start_work(product_type)
        user_add_replace_page.fill_required_fields()
        with allure.step('Отправляем заявку на модерацию'):
            user_add_replace_page.go_button.click()
        with allure.step('Ждем пока появится аллерт о том, что заявка зарегистрирована'):
            user_add_replace_page.status_info.is_visible()
        url = user_add_replace_page.url
        user_add_replace_page.login_admin()
        with allure.step('Заходим в заявку'):
            user_add_replace_page.get_page(url)
        with allure.step('Берем заявку в работу'):
            user_add_replace_page.take_to_work.click()
        with allure.step('Открываем меню редактирования админа'):
            user_add_replace_page.toggle_replace_admin.click()
        with allure.step('Редактируем имя продукта'):
            user_add_replace_page.text_input(user_add_replace_page.input_name_replace_admin_toggle)
        with allure.step('Одобряем заявку'):
            user_add_replace_page.save_doc.click()

        with allure.step('Проверяем, что заявка выполнилась'):
            user_add_replace_page.wait_force(2)
            assert user_add_replace_page.status_info.get_text() == 'Заявка выполнена', f'У заявки статус: {user_add_replace_page.status_info.get_text()}'

        with allure.step('Переходим на страницу продукта'):
            user_add_replace_page.refresh()
            user_add_replace_page.link_to_product_in_brief.click()
        user_add_replace_page.delete_product()

    @allure.title("Если редактируется только атрибут С модерацией, то кнопка называется Отправить на модерацию")
    @allure.issue('https://jira.mts.ru/browse/PPI-3073', 'PPInfo - Кнопки Записать или Отправить на модерацию')
    def test_moder_button(self, user_2_add_replace_page):
        user_2_add_replace_page.get_page('https://stage.prodboard.mts.ru/product/BI_2062/main')
        user_2_add_replace_page.edit_button.click()
        user_2_add_replace_page.delete_edit.click()
        user_2_add_replace_page.edit_button.click()
        user_2_add_replace_page.PPinfo_web_app_replace.click()
        user_2_add_replace_page.input_replace.click()
        user_2_add_replace_page.first_value.click()
        user_2_add_replace_page.replace.click()

        assert user_2_add_replace_page.moder_button.is_clickable()

    @allure.title("Если редактируется только атрибут Без модерации, то кнопка называется Записать")
    @allure.issue('https://jira.mts.ru/browse/PPI-3073', 'PPInfo - Кнопки Записать или Отправить на модерацию')
    def test_save_button(self, user_2_add_replace_page):
        user_2_add_replace_page.get_page('https://stage.prodboard.mts.ru/product/BI_2062/main')
        user_2_add_replace_page.edit_button.click()
        user_2_add_replace_page.delete_edit.click()
        user_2_add_replace_page.edit_button.click()
        user_2_add_replace_page.gr_PPInfo_product_block.click()
        user_2_add_replace_page.input_replace.click()
        user_2_add_replace_page.first_value.click()
        user_2_add_replace_page.replace.click()

        assert user_2_add_replace_page.save_button_replace.is_clickable()


@pytest.mark.ui
@allure.feature("Создание продукта")
class TestAdminAddProduct:

    @allure.title("Создание продукта админом (только обязательные поля)")
    @pytest.mark.parametrize('product_type', ['commercial', 'internal'])
    def test_add_product_admin(self, add_replace_page, product_type):
        add_replace_page.start_work(product_type)
        add_replace_page.fill_required_fields()
        with allure.step('Добавляем продукт'):
            add_replace_page.save_button.click()
            add_replace_page.header.is_visible()
        with allure.step('Проверяем, что мы оказались на странице продукта'):
            url = add_replace_page.url
            assert url.startswith('https://stage.prodboard.mts.ru/product/BI_'), f'Ссылка другая: {url}'
        add_replace_page.delete_product()

    @allure.title("Создание продукта админом (поля даты)")
    @pytest.mark.parametrize('product_type', ['commercial', 'internal'])
    def test_add_product_date_admin(self, add_replace_page, product_type):
        add_replace_page.start_work(product_type)
        add_replace_page.fill_required_fields()
        with allure.step('Нажимаем кнопку "Показать еще"'):
            add_replace_page.show_all_button.click()
        add_replace_page.fill_all_fields('time', to_remove=['Дата создания'])
        with allure.step('Добавляем продукт'):
            add_replace_page.save_button.click()
            add_replace_page.header.is_visible()
        with allure.step('Проверяем, что мы оказались на странице продукта'):
            url = add_replace_page.url
            assert url.startswith('https://stage.prodboard.mts.ru/product/BI_'), f'Ссылка другая: {url}'
        add_replace_page.delete_product()

    @allure.title("Отклонение/Одобрение заявки админом")
    @pytest.mark.parametrize('brief_status', ['Заявка отклонена', 'Заявка выполнена'])
    def test_admin_work_with_brief(self, add_replace_page, brief_status):
        with allure.step('Заходим в заявки'):
            add_replace_page.fio.click()
            add_replace_page.briefs.click()
        with allure.step('Заходим в первую открытую заявку'):
            add_replace_page.link_first_brief.click()
        with allure.step('Проверяем, что у заявки статус Зарегистрирована'):
            assert add_replace_page.status_info.get_text() == 'Заявка зарегистрирована', 'Статус не тот'
        with allure.step('Берем заявку в работу'):
            add_replace_page.take_to_work.click()
        with allure.step('Проверяем, что у заявки статус В работе'):
            assert add_replace_page.status_info.get_text() == 'Заявка в работе', 'Статус не тот'
        if brief_status == 'Заявка выполнена':
            with allure.step('Одобряем заявку'):
                add_replace_page.save_doc.click()
        else:
            with allure.step('Отклоняем заявку'):
                add_replace_page.reject.click()
        with allure.step(f'Проверяем, что у заявки статус {brief_status}'):
            add_replace_page.wait_force(2)
            assert add_replace_page.status_info.get_text() == brief_status, 'Статус не тот'


@pytest.mark.ui
@pytest.mark.notification
@allure.feature('Нотификации')
class TestNotificationsInAddProductAdmin:
    @allure.title("Проверка переключателя уведомлений на странице создания продукта ")
    @pytest.mark.parametrize('product_type', ['commercial', 'internal'])
    def test_notification_toggle_on_create_product_page(self, add_replace_page, product_type):
        add_replace_page.start_work(product_type)
        with allure.step('Проверяем, что тогл информирования включен по умолчанию'):
            assert add_replace_page.notification_toggle.is_checked(), 'Тогл выключен'
        with allure.step('Жмем на тогл'):
            add_replace_page.notification_toggle.click()
        with allure.step('Проверяем, что тогл информирования выключен'):
            assert not add_replace_page.notification_toggle.is_checked(), 'Тогл включен'

    @allure.title("Проверка переключателя уведомлений на странице заявки")
    @allure.issue('https://jira.mts.ru/browse/CAKF-1354', 'Нет возможности отключить информирование при записи заявки')
    def test_notification_toggle_on_brief_page(self, add_replace_page):
        with allure.step('Заходим в заявки'):
            add_replace_page.fio.click()
            add_replace_page.briefs.click()
        with allure.step('Заходим в первую открытую заявку'):
            add_replace_page.link_first_brief.click()
        with allure.step('Берем заявку в работу'):
            add_replace_page.take_to_work.click()
        with allure.step('Проверяем, что тогл информирования включен по умолчанию'):
            assert add_replace_page.notification_toggle_in_brief.is_checked(), 'Тогл выключен'
        with allure.step('Жмем на тогл'):
            add_replace_page.notification_toggle_in_brief.click()
        with allure.step('Проверяем, что тогл информирования выключен'):
            assert not add_replace_page.notification_toggle_in_brief.is_checked(), 'Тогл включен'

    @allure.title('Поиск доп.сотрудников по логину')
    @allure.issue('https://jira.mts.ru/browse/CAKF-1373', 'Не выполняется поиск по доп.сотрудникам')
    @pytest.mark.parametrize('product_type', ['commercial', 'internal'])
    def test_additional_user_login_input(self, add_replace_page, product_type):
        add_replace_page.start_work(product_type)
        login = "sa0000prodbpmuser1"

        add_replace_page.find_user(add_replace_page.employee_product_owner, login)
        assert add_replace_page.employee_product_owner.get_text() == 'Дани Светов'

    @allure.title('Поиск доп.сотрудников по имени')
    @allure.issue('https://jira.mts.ru/browse/CAKF-1373', 'Не выполняется поиск по доп.сотрудникам')
    @pytest.mark.parametrize('product_type', ['commercial', 'internal'])
    def test_additional_user_name_input(self, add_replace_page, product_type):
        add_replace_page.start_work(product_type)
        login = "Технический Юзер Второй"

        add_replace_page.find_user(add_replace_page.employee_product_owner, login)
        assert add_replace_page.employee_product_owner.get_text() == 'Технический Юзер Второй'
