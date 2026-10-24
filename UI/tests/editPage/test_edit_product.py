import allure
import pytest

from API.utils.generate import Gen


@pytest.mark.ui
@allure.feature("Редактирование продукта")
class TestAdminEditProduct:
    @allure.title(f"Редактирование атрибута ссылки админом")
    @pytest.mark.parametrize('add_replace_page', ['https://stage.prodboard.mts.ru/product/BI_2062/main'], indirect=True)
    def test_replace_external_admin_link(self, add_replace_page):
        text = add_replace_page.public_links.get_attributes('href')
        add_replace_page.edit_button.click()
        add_replace_page.delete_edit.click()
        add_replace_page.edit_button.click()
        add_replace_page.show_all.click()
        add_replace_page.PPInfo_Public_Description_replace.click()
        add_replace_page.replace_input("string", add_replace_page.input_replace_string)
        add_replace_page.replace.click()
        add_replace_page.save.click()
        add_replace_page.wait()
        assert add_replace_page.public_links[0].get_attribute('href') != text

    @allure.title(f"Добавление и удаление атрибута-селект админом")
    @pytest.mark.parametrize("metod", ["add", "remove"])
    @pytest.mark.parametrize('add_replace_page', ['https://stage.prodboard.mts.ru/product/BI_2062/main'], indirect=True)
    def test_replace_external_admin_manyselect(self, add_replace_page, metod):
        add_replace_page.edit_button.click()
        add_replace_page.delete_edit.click()
        add_replace_page.edit_button.click()
        add_replace_page.scroll_page_down(600)
        text = add_replace_page.PPinfo_web_app_field.get_text()
        add_replace_page.PPinfo_web_app_replace.click()
        add_replace_page.replace_input("many select", add_replace_page.input_replace)
        add_replace_page.replace.click()
        add_replace_page.save.click()
        add_replace_page.wait_force(2)
        add_replace_page.edit_button.click()
        add_replace_page.scroll_page_down(300)
        assert add_replace_page.PPinfo_web_app_field.get_text() != text

    @allure.title(f"Редактирование атомарного продукта админом")
    @pytest.mark.parametrize('add_replace_page', ['https://stage.prodboard.mts.ru/product/BI_3266/main'], indirect=True)
    def test_replace_atomic_admin(self, add_replace_page):
        add_replace_page.edit_button.click()
        add_replace_page.delete_edit.click()
        add_replace_page.edit_button.click()
        text = add_replace_page.public_links.get_attributes('href')
        add_replace_page.show_all.click()
        add_replace_page.PPInfo_Public_Description_replace.click()
        add_replace_page.input_in_modal.fill('https://' + Gen.generate_text(7))
        add_replace_page.replace.click()
        add_replace_page.save.click()
        add_replace_page.wait_force(2)
        add_replace_page.edit_button.click()
        assert add_replace_page.public_links.get_attributes('href') != text


@allure.feature('Заявки')
@allure.feature('Добавление документов')
@pytest.mark.ui
class TestAddDocsUser:

    @allure.title("Отправка заявки на добавление документа пользователем")
    @allure.issue('https://jira.mts.ru/browse/PPI-154', 'PPInfo - Снекбар с кнопкой после создания заявки')
    def test_add_docs_user(self, user_add_replace_page):
        user_add_replace_page.add_doc()

    @allure.title("Отправка заявки на добавление документа пользователем и согласование/отклонение ее админом")
    @allure.issue('https://jira.mts.ru/browse/PPI-154', 'PPInfo - Снекбар с кнопкой после создания заявки')
    @pytest.mark.parametrize('brief_status', ['Заявка отклонена', 'Заявка выполнена'])
    def test_add_docs_user_full_cycle(self, user_add_replace_page, brief_status):
        user_add_replace_page.add_doc()
        url = user_add_replace_page.url
        user_add_replace_page.login_admin()
        with allure.step('Заходим в заявку админом'):
            user_add_replace_page.get_page(url)
        with allure.step('Берем заявку в работу'):
            user_add_replace_page.take_to_work.click()
            user_add_replace_page.save_doc.is_visible()
        with allure.step('Проверяем, что заявка в работе'):
            assert 'Заявка в работе' in user_add_replace_page.status_info.get_text(), 'Статус не тот'
        if brief_status == 'Заявка выполнена':
            with allure.step('Одобряем заявку'):
                user_add_replace_page.save_doc.click()
        else:
            with allure.step('Отклоняем заявку'):
                user_add_replace_page.reject.click()
        with allure.step(f'Проверяем, что у заявки статус {brief_status}'):
            user_add_replace_page.wait_force(1)
            assert user_add_replace_page.status_info.get_text() == brief_status, 'Статус не тот'

    @allure.title("Отправка заявки на добавление ссылки пользователем")
    @allure.issue('https://jira.mts.ru/browse/PPI-154', 'PPInfo - Снекбар с кнопкой после создания заявки')
    def test_add_links_user(self, user_add_replace_page):
        user_add_replace_page.add_link()

    @allure.title("Отправка заявки на ссылки документа пользователем и согласование/отклонение ее админом")
    @allure.issue('https://jira.mts.ru/browse/PPI-154', 'PPInfo - Снекбар с кнопкой после создания заявки')
    @pytest.mark.parametrize('brief_status', ['Заявка отклонена', 'Заявка выполнена'])
    def test_add_links_user_full_cycle(self, user_add_replace_page, brief_status):
        user_add_replace_page.add_link()
        url = user_add_replace_page.url
        user_add_replace_page.login_admin()
        with allure.step('Заходим в заявку админом'):
            user_add_replace_page.get_page(url)
        with allure.step('Берем заявку в работу'):
            user_add_replace_page.take_to_work.click()
            user_add_replace_page.save.is_visible()
        with allure.step('Проверяем, что заявка в работе'):
            assert 'Заявка в работе' in user_add_replace_page.status_info.get_text(), 'Статус не тот'
        if brief_status == 'Заявка выполнена':
            with allure.step('Одобряем заявку'):
                user_add_replace_page.save_doc.click()
        else:
            with allure.step('Отклоняем заявку'):
                user_add_replace_page.reject.click()
        with allure.step(f'Проверяем, что у заявки статус {brief_status}'):
            assert user_add_replace_page.status_info.get_text() == brief_status, 'Статус не тот'

    @allure.title("На жизненном цикле есть кнопка редактирования")
    @allure.issue('https://jira.mts.ru/browse/PPI-3297', 'PPInfo - Редактирование статусов в прогресс-баре')
    def test_edit_life_cycle(self, user_add_replace_page):

        user_add_replace_page.get_page('https://stage.prodboard.mts.ru/product/BI_2064/main')
        user_add_replace_page.edit_button.click()

        assert user_add_replace_page.edit_button_lc.is_visible(), 'На жизненном цикле пользователю не отображена кнопка редактирования'
