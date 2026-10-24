import allure
import pytest

from UI.data.assertions_data import ProductsAsserts as assertions
from UI.tests.editPage.conftest import add_replace_page
from UI.tests.productPage.conftest import product_page as page
from UI.tests.productPage.conftest import product_page_user_1 as page_user


@pytest.mark.ui
@allure.feature("Страница продукта")
class TestMainInfo:
    # Отображение основных блоков -------------------------------------------------------------------------------------
    @allure.title("Проверка отображения основных блоков на странице продукта / Блок лого и названия")
    def test_main_page_check_block_logo_and_name(self, page):
        with allure.step("Проверяем корректное отображения лого"):
            assert page.product_logo.is_visible(), 'Лого нет'
            assert page.product_logo.is_clickable(), 'На лого нельзя нажать'
        with allure.step("Проверяем корректное отображение названия"):
            assert page.product_name.is_visible(), 'Названия нет'
            assert page.product_name.is_clickable(), 'На название нельзя нажать'
            assert page.product_name.get_text(), 'Название пустое'
        with allure.step('Проверяем корректное отображение кнопки избранного'):
            assert page.add_to_favorite_button.is_visible(), 'Кнопки Добавить в избранное нет'
            assert page.add_to_favorite_button.is_clickable(), 'На кнопку нельзя нажать'

    @allure.title("Проверка отображения основных блоков на странице продукта / Блок кодов продукта")
    @allure.issue('https://jira.mts.ru/browse/PPI-498', 'PPInfo - Отображать код Oracle вместе с кодом BI')
    def test_main_page_check_block_codes(self, page):
        with allure.step("Проверяем корректное отображения кодов продукта"):
            assert page.product_code.is_visible(), 'Блока с кодами продукта нет'
            assert page.product_code.get_text() == "Код продукта Oracle MAAS ID продукта МТС Product BI_60", 'В блоке кода другой текст'

    @allure.title("Проверка отображения основных блоков на странице продукта / Блок чипсов свойств и действий")
    def test_main_page_check_block_chips_and_actions(self, page):
        with allure.step("Проверяем корректное отображения блока чипсов"):
            assert page.product_chips_property.is_visible(), 'Блока с чипсами свойств нет'
        with allure.step("Проверяем корректное отображение кнопки 'Задать вопрос'"):
            assert page.ask_questions_button.is_visible(), 'Кнопка не отображается'
            assert page.ask_questions_button.is_clickable(), 'Кнопку нельзя нажать'
            assert page.ask_questions_button.get_text() == 'ЗАДАТЬ ВОПРОС ПО ПРОДУКТУ', 'Текст на кнопке не тот'

    @allure.title("Проверка отображения основных блоков на странице продукта / Блок меню слева с табами")
    def test_main_page_check_block_tab_menu(self, page):
        with allure.step("Проверяем корректное отображения блока табов"):
            assert page.product_sidebar.is_visible(), 'Блока с табами нет'
        tab_list = [page.main_info_tab, page.atomic_tab, page.metrics_tab,
                    page.project_tab, page.software_tab,
                    page.docs_tab, page.product_guide_tab]
        for tab in tab_list:
            with allure.step(f'Проверяем наличие таба {tab.get_attribute("id")}'):
                assert tab.is_visible(), 'Таба нет'
                assert tab.is_clickable(), 'На таб нельзя нажать'

    @allure.title("Проверка отображения основных блоков на странице продукта / Основные заголовки")
    def test_main_page_check_block_main_headers(self, page):
        with allure.step("Проверяем корректное отображения хедера Основная информация"):
            assert page.main_info_header.is_visible(), 'Хедера нет'
            assert page.main_info_header.get_text() == 'Основная информация', 'Текст не тот'
        with allure.step("Проверяем корректное отображения хедера Свойства"):
            assert page.properties_header.is_visible(), 'Хедера нет'
            assert page.properties_header.get_text() == 'Свойства', 'Текст не тот'

    @allure.title("Проверка отображения основных блоков на странице продукта / Прогрессбар")
    def test_main_page_check_block_lifecycle(self, page):
        with allure.step("Проверяем корректное отображения прогрессбара"):
            assert page.lifecycle.is_visible(), 'Прогрессбара нет'
        with allure.step('Проверяем отображение основных статусов'):
            statuses = [page.idea_formation_status, page.in_work_status, page.pilot_status,
                        page.in_use_status,
                        page.out_of_use_status]
            for status in statuses:
                with allure.step(f'Проверяем отображение статуса {status.get_text()}'):
                    assert status.is_visible(), 'Статуса нет на прогрессбаре'

    @allure.title("Проверка отображения основных блоков на странице продукта / Блок описания")
    def test_main_page_check_block_description(self, page):
        with allure.step("Проверяем корректное отображения блока описания"):
            assert page.description_block.is_visible(), 'Блока с описанием нет'
            assert page.description_block.get_text(), 'Текста описания нет'
        with allure.step("Проверяем корректное отображение блока действий"):
            assert page.actions_under_description.is_visible(), 'Блока действий нет'

    @allure.title("Проверка отображения основных блоков на странице продукта / Блок руководства")
    def test_main_page_check_block_owners(self, page):
        with allure.step("Проверяем корректное отображение заголовка"):
            assert page.owners_header.is_visible(), 'Заголовка нет'
        with allure.step("Проверяем корректное отображения блока"):
            assert page.owners_block.is_visible(), 'Блока нет'

    @allure.title("Проверка отображения основных блоков на странице продукта / Блок Полезные ссылки и действия")
    def test_main_page_check_block_useful_links(self, page):
        with allure.step("Проверяем корректное отображение заголовка"):
            assert page.useful_links_header.is_visible(), 'Заголовка нет'
        with allure.step("Проверяем корректное отображения блока"):
            assert page.useful_links_block.is_visible(), 'Блока нет'

    @allure.title("Проверка отображения основных блоков на странице продукта / Блок Оценок")
    def test_main_page_check_block_rating(self, page):
        with allure.step("Проверяем корректное отображение заголовка"):
            assert page.rating_header.is_visible(), 'Заголовка нет'
        with allure.step("Проверяем корректное отображения блока"):
            assert page.rating_block.is_visible(), 'Блока нет'

    @allure.title("Проверка отображения основных блоков на странице продукта / Блок Действия")
    def test_main_page_check_block_actions(self, page):
        with allure.step("Проверяем корректное отображение заголовка"):
            assert page.actions_header.is_visible(), 'Заголовка нет'
        with allure.step("Проверяем корректное отображения блока"):
            assert page.actions_block.is_visible(), 'Блока нет'

    @allure.title("Проверка отображения основных блоков на странице продукта / Блок Цикл Финансирования")
    @allure.issue('https://jira.mts.ru/browse/PPI-2466', 'PPInfo - Frontend - Добавить блок "Цикл финансирования"')
    def test_main_page_check_block_financing(self, page):
        with allure.step("Проверяем корректное отображение заголовка"):
            assert page.financing_header.is_visible(), 'Заголовка нет'
        with allure.step("Проверяем корректное отображения блока"):
            assert page.financing_block.is_visible(), 'Блока нет'

    @allure.title("Проверка отображения основных блоков на странице продукта / Горизонтальные табы")
    def test_main_page_check_block_horizontal_tabs(self, page):
        with allure.step("Проверяем корректное отображение табов"):
            assert page.tabs_horizontal.is_visible(), 'Табов нет'

    @allure.title("Проверка отображения основных блоков на странице продукта / Блок Атрибутов")
    def test_main_page_check_block_attributes(self, page):
        with allure.step("Проверяем корректное отображение таблицы атрибутов"):
            assert page.attributes_block.is_visible(), 'таблицы нет'

    @allure.title("Проверка отображения основных блоков на странице продукта / Блок Связанных продуктов")
    def test_main_page_check_block_related(self, page):
        with allure.step("Проверяем корректное отображение связанных продуктов"):
            assert page.related_product.is_visible(), 'Связанных продуктов нет'

    @allure.title("Проверка отображения основных блоков на странице продукта / Кнопка Показать все свойства ")
    def test_main_page_check_block_related(self, page):
        with allure.step("Проверяем корректное отображение кнопки"):
            assert page.show_other_button.is_visible(), 'Кнопки нет'
            assert page.show_other_button.is_clickable(), 'На кнопку нельзя нажать'
        with allure.step("Жмем на кнопку"):
            page.show_other_button.click()
        with allure.step("Проверяем, что текстовка изменилась"):
            page.show_other_button.is_not_visible(), 'Текстовка не изменилась'
            page.hide_other_button.is_visible(), 'Кнопка не изменилась'
        with allure.step("Жмем на кнопку еще раз"):
            page.hide_other_button.click()
        with allure.step("Проверяем, что текстовка изменилась"):
            page.show_other_button.is_visible(), 'Текстовка не изменилась'
            page.hide_other_button.is_not_visible(), 'Кнопка не изменилась'

    @allure.title("Проверка отображения основных блоков на странице продукта / Блок кнопок редактирования")
    def test_main_page_check_block_edit_buttons(self, page):
        with allure.step("Проверяем корректное отображение блока кнопок"):
            assert page.edit_product_block.is_visible(), 'Кнопки нет'
        with allure.step("Проверяем корректное отображение кнопки Редактировать"):
            assert page.edit_button.is_visible(), 'Кнопки нет'
            assert page.edit_button.is_clickable(), 'На кнопку нельзя нажать'
        with allure.step("Проверяем корректное отображение кнопки Удалить"):
            assert page.delete_button.is_visible(), 'Кнопки нет'
            assert page.delete_button.is_clickable(), 'На кнопку нельзя нажать'

    # Сотрудники ----------------------------------------------------------------------------------------------------
    @allure.title("Корректное отображение ФИО руководства  в карточке сотрудника на стр продукта")
    def test_owners_name(self, page):
        with allure.step("Проверяем, что ФИО отображается корректно"):
            assert page.owners_text.is_visible(), 'ФИО нет'
            assert page.owners_text.get_text(), 'ФИО пустое'
            assert page.owners_text.is_clickable(), 'На ФИО нельзя нажать'

    @allure.title("Корректное отображение карточки уволенного сотрудника на странице продукта")
    @pytest.mark.parametrize('page', ['https://stage.prodboard.mts.ru/product/BI_311/main'], indirect=True)
    def test_fired_owner(self, page: page):
        with allure.step('Жмем на ФИО уволенного сотрудника'):
            page.fired_user_haritonov.click()
        with allure.step("Проверяем, что чипс 'Уволен' отображается"):
            assert page.fired_status.is_visible(), 'Чипса нет'

    @allure.title("Отображение карточки сотрудника при клике по ФИО")
    def test_user_card(self, page):
        with allure.step("Жмем на пользователя Зимина"):
            page.user_zimina.click()
        with allure.step("Проверяем, что появилась карточка сотрудника"):
            assert page.user_card.is_visible(), 'Карточки сотрудника нет'
        with allure.step("Проверяем, что мобильный телефон отображается корректно"):
            assert page.mobile_number.is_visible(), 'Телефона нет'
            if page.mobile_number.get_text() != '—':
                assert page.mobile_number.is_clickable(), 'На мобильный телефон нельзя нажать'
        with allure.step("Проверяем, что почта отображается корректно"):
            assert page.email_card.is_visible(), 'Почты нет'
            assert page.email_card.is_clickable(), 'На почту нельзя нажать'
            assert page.email_card.get_text(), 'Почта пустая'
        with allure.step("Проверяем, что блок орг. структуры отображается корректно"):
            assert page.org_block.is_visible(), 'Блока со структурой нет'
            assert page.org_block.get_text(), 'Блок орг структуры пустой'
        with allure.step("Проверяем, что ссылка на пульс корректная"):
            assert page.pulse_link.is_visible(), 'Ссылки на пульс нет'
            assert page.pulse_link.get_attribute(
                "href") == 'https://newportal.mts.ru/my/Person.aspx?accountname=ADMSK%5Czimina', 'Ссылка не та'
        with allure.step("Жмем на ФИО еще раз"):
            page.user_zimina.click()
        with allure.step('Проверяем, что карточка пропала'):
            assert page.user_card.is_not_visible(), 'Карточка не пропала'

    @allure.title("Корректное отображение уволенного сотрудника в атрибутах")
    @allure.issue('https://jira.mts.ru/browse/PPI-1860', 'PPInfo - Отображение уволенных сотрудников в свойствах')
    @pytest.mark.parametrize('page', ['https://stage.prodboard.mts.ru/product/BI_311/main'], indirect=True)
    def test_fired_user_in_attributes(self, page: page):
        with allure.step("Жмем Показать еще"):
            page.show_other_button.click()
        with allure.step('Проверяем, что уволенный юзер отображается серым цветом'):
            assert 'userFired' in page.po_attribute.get_attribute(
                'class'), 'Пользователь не отображен серым цветом'
        with allure.step('Жмем по уволенному сотруднику'):
            page.po_attribute.click()
        with allure.step('Проверяем, что чипс Уволен есть'):
            assert page.fired_status.is_visible(), 'Чипса нет'

    # Удаление ---------------------------------------------------------------------------------------
    @allure.title('При наличии у продукта атомарных продуктов его невозможно удалить')
    @allure.issue('https://jira.mts.ru/browse/PPI-183', 'PPInfo - Проверка на наличие атомарных продуктов при удалении')
    def test_cant_delete_with_atomic(self, page):
        with allure.step('Нажимаем кнопку Удалить'):
            page.delete_button.click()
        with allure.step('Проверяем что появилась модалка о невозможности удаления'):
            assert page.cant_delete.is_visible(), 'Окна с предупреждением не появилось'
            assert page.cant_delete_text.get_text() == 'Чтобы удалить этот продукт, удалите или отвяжите все его атомарные продукты.', 'Текст не тот'
            assert page.cant_delete_go_to_atomic.is_clickable(), 'На ссылку нельзя нажать'
        with allure.step("Проверяем, что кнопку Удалить нельзя нажать"):
            assert not page.cant_delete_button.is_clickable(), 'На кнопку можно нажать'
        with allure.step('В тосте есть переход к атомарным продуктом, переходим по кнопку'):
            page.cant_delete_go_to_atomic.click()
        with allure.step('Проверяем что мы находимся на странице атомарных продуктов МТС Маркетолога'):
            assert page.url == 'https://stage.prodboard.mts.ru/product/BI_60/atomic', 'Мы не перешли на страницу атомарных'

    @allure.title("Проверяем корректное отображение модалки при удалении продукта")
    @pytest.mark.parametrize('page', ['https://stage.prodboard.mts.ru/product/BI_229/main'], indirect=True)
    def test_check_modal_delete(self, page: page):
        page.publish_product()
        with allure.step("Жмем на кнопку Удалить"):
            page.delete_button.click()
        with allure.step("Проверяем, что модальное окно появилось"):
            page.delete_product_modal_window.is_visible(), 'Модалки не появилось'

    @allure.title("Проверяем корректную работу радио кнопок в модалке при удалении продукта")
    @pytest.mark.parametrize('page', ['https://stage.prodboard.mts.ru/product/BI_229/main'], indirect=True)
    def test_check_modal_delete_radio_buttons(self, page: page):
        page.publish_product()
        with allure.step("Жмем на кнопку Удалить"):
            page.delete_button.click()

        assert page.radio_buttons.are_visible(), 'Кнопки нет'
        assert page.radio_buttons.are_clickable(), 'На кнопку нельзя нажать'
        for i in range(page.radio_buttons.count()):
            page.radio_buttons[i].click()
            page.radio_buttons[i].is_checked()
            assert page.radio_buttons[i].is_checked(), 'Кнопка не выделилась'

    @allure.title("Проверка корректной работы инпута удаления и кнопки в модалке")
    @pytest.mark.parametrize('page', ['https://stage.prodboard.mts.ru/product/BI_229/main'], indirect=True)
    def test_check_modal_input_and_button(self, page: page):
        page.publish_product()
        with allure.step("Жмем на кнопку Удалить"):
            page.delete_button.click()
        with allure.step("Проверяем, что кнопка Удалить в модалке выключена"):
            assert page.delete_in_modal_button.is_disabled(), 'Кнопка не выключена'
            assert page.delete_in_modal_button.is_not_clickable(), 'На кнопку можно нажать'
        with allure.step("Вводим текст в инпут удаления"):
            page.reason_deleted_input.fill('тест123')
        with allure.step("Проверяем, что кнопка Удалить активировалась"):
            assert page.delete_in_modal_button.is_not_disabled(), 'Кнопка выключена'
            assert page.delete_in_modal_button.is_clickable(), 'На кнопку нельзя нажать'

    @allure.title("Проверяем удаление продукта")
    def test_check_delete_product(self, page: page, add_replace_page):
        page.get_page('https://stage.prodboard.mts.ru/product/BI_229/main')
        page.publish_product()
        add_replace_page.delete_product()
        with allure.step("Проверяем, что модалка пропала"):
            assert page.delete_product_modal_window.is_not_visible(), 'Модалка не пропала'
        with allure.step("Проверяем, что появился чипс Удален"):
            assert page.deleted_chips.is_visible(), 'Чипса нет'
        with allure.step("Проверяем, что кнопки удаления и редактирования пропали"):
            assert page.edit_button.is_not_visible(), 'Кнопка редактирования не пропала'
            assert page.delete_button.is_not_visible(), 'Кнопка удаления не пропала'
        with allure.step("Проверяем, что появилась кнопка Опубликовать"):
            assert page.get_back_from_dead_button.is_visible(), 'Кнопки нет'

        page.publish_product()

    @allure.title("Проверяем восстановление продукта")
    def test_check_recover_product(self, page: page, add_replace_page):
        page.get_page('https://stage.prodboard.mts.ru/product/BI_229/main')
        page.publish_product()
        add_replace_page.delete_product()
        page.publish_product()
        with allure.step("Проверяем, что кнопки удаления и редактирования появились"):
            assert page.edit_button.is_visible(), 'Кнопка редактирования не появилась'
            assert page.delete_button.is_visible(), 'Кнопка удаления не появилась'
        with allure.step("Проверяем, что появилась кнопка Опубликовать"):
            assert page.get_back_from_dead_button.is_not_visible(), 'Кнопка не пропала'
        with allure.step("Проверяем, что пропал чипс Удален"):
            assert page.deleted_chips.is_not_visible(), 'Чипс не пропал'

    # Прочее ----------------------------------------------------------------------------------------------------------
    @allure.title("Проверка работы горизонтальных табов")
    def test_horizontal_tabs(self, page):
        prev_text = ''
        for i in range(page.pp_tabs.count()):
            with allure.step(f'Проверяем таб {page.pp_tabs[i].get_text()}'):
                with allure.step("Проверяем кликабельность таба"):
                    assert page.pp_tabs[i].is_clickable(), f'На таб нельзя нажать'
                with allure.step('Жмем на таб'):
                    page.pp_tabs[i].click()
                with allure.step('Проверяем, что таб выделился'):
                    assert page.pp_tabs[i].is_selected(), 'Таб не выделился'
                with allure.step('Проверяем, что таблица атрибутов поменялась'):
                    assert page.pp_tabs[i].get_text() != prev_text, 'Атрибут не сменился после переключения таба'
                    prev_text = page.pp_tabs[i].get_text()

    @allure.title("Корректное отображение конца срока финансирования на прогрессбаре")
    @pytest.mark.parametrize('page', ['https://stage.prodboard.mts.ru/product/BI_1661/main'], indirect=True)
    def test_lifecycle_pilot_date_fin(self, page: page):
        with allure.step("Проверяем, что прогрессбар есть"):
            assert page.lifecycle.is_visible(), 'Прогрессбара нет'
        with allure.step('Проверяем корректное отображение конца финансирования'):
            assert page.fin_close_on_progressbar.is_visible(), 'Конец финансирования не отображается'
            assert page.fin_close_on_progressbar.get_text() == 'Конец финансирования 30.08.22', 'Текст не тот'

    @allure.title("Корректное отображение ссылки на SOL на странице родительского продукта")
    @allure.issue("https://jira.mts.ru/browse/PPI-324", "PPInfo - Автоматизировать получение ссылки на SOL")
    def test_sol_link(self, page):
        link_value = page.sol_link.get_attribute('href')
        with allure.step('Проверяем корректность отображения ссылки на SOl'):
            assert page.sol_link.is_visible(), 'Ссылки на сол нет'
            assert page.sol_link.is_clickable(), 'Нельзя нажать на ссылку'
            assert link_value == "https://dev.sol.mts.ru/new/products/code/BI_60", 'Ссылка не та'

    @allure.title(
        "Проверка корректной сортировки ключевых свойств на странице внешнего/внутреннего продукта при ее обновлении")
    @pytest.mark.parametrize('page', assertions.linkToInternalAndExternal, indirect=True)
    def test_reload_key_prop_ex(self, page):
        key_props_before_refresh = page.key_prop.get_texts()
        with allure.step('Обновляем страницу'):
            page.refresh()
        with allure.step("Проверяем, что после обновления страницы ключевые свойства остались неизменными"):
            assert page.key_prop.get_texts() == key_props_before_refresh, 'Порядок свойств изменился'

    @allure.title('Пустые оценки не отображаются на странице продукта')
    @allure.issue('PPInfo - Не отображать пустой блок "Оценки"', 'https://jira.mts.ru/browse/PPI-464')
    @pytest.mark.parametrize('page', ['https://stage.prodboard.mts.ru/product/BI_1323/main'], indirect=True)
    def test_empty_rating_not_visible(self, page: page):
        with allure.step('Блок оценок не отображается'):
            assert page.rait.is_not_visible(), 'Пустой блок оценок отображается'

    @allure.title("Проверяем работу кнопку Добавить в избранное")
    def test_check_fav_button(self, page):
        if page.delete_from_favorite_button.is_visible():
            with allure.step("Удаляем продукт из избранного если он там есть"):
                page.delete_from_favorite_button.click()
        current_counter = int(page.favorite_counter.get_text())
        with allure.step("Жмем на кнопку Добавить в избранное"):
            page.add_to_favorite_button.click()
        with allure.step("Проверяем, что каунтер в избранном увеличился на 1"):
            assert int(page.favorite_counter.get_text()) == current_counter + 1, 'Каунтер не изменился'
        with allure.step("Проверяем, что кнопка Избранного изменилась"):
            assert page.add_to_favorite_button.is_not_visible(), 'Кнопка добавить не пропала'
            assert page.delete_from_favorite_button.is_visible(), 'Кнопка удалить не появилась'

        current_counter = int(page.favorite_counter.get_text())
        with allure.step("Жмем на кнопку Удалить из избранного"):
            page.delete_from_favorite_button.click()
        with allure.step("Проверяем, что каунтер в избранном уменьшился на 1"):
            assert int(page.favorite_counter.get_text()) == current_counter - 1, 'Каунтер не изменился'
        with allure.step("Проверяем, что кнопка Избранного изменилась"):
            assert page.add_to_favorite_button.is_visible(), 'Кнопка добавить не появилась'
            assert page.delete_from_favorite_button.is_not_visible(), 'Кнопка удалить не пропала'

    @allure.title(f"У архивных продуктов имеется вслывашка об архивность и банер рядом с названием ")
    @allure.issue('https://jira.mts.ru/browse/PPI-2705', 'PPInfo - Доработка отображения архивных продуктов')
    def test_is_product_really_archived(self, page):
        assert page.is_archived_toast.is_not_visible(), 'Тост об архивность продукт отображается у активного продукта'
        assert page.is_archived_text.is_not_visible(), 'Текст об архивности продукт отображается у активного продукта'

        page.get_page('https://stage.prodboard.mts.ru/product/BI_271/main')
        assert page.is_archived_toast.is_visible(), 'Тост об архивность продукт не отображается'
        assert page.is_archived_text.is_visible(), 'Текст об архивности продукт не отображается'

    @allure.title(f"Атрибуты тех зрелости отображены на станице продукта")
    @allure.issue('https://jira.mts.ru/browse/PPI-2898', 'PPInfo - Техзрелость продукта')
    @pytest.mark.parametrize('page', ['https://stage.prodboard.mts.ru/product/BI_42/main'], indirect=True)
    @pytest.mark.skip(reason='Переехало в здоровье')
    def test_tm_attr_visible(self, page: page):

        assert page.index_tm.get_text() == '3.37', 'Текст индекса товара не отображается'
        assert page.tma_complete_date.get_text() == '17.10.2024', 'Текст даты прохождения тех зрелости не отображается'

    @allure.title('Атрибут Ссылка в Selfe кликабельный')
    @allure.issue('https://jira.mts.ru/browse/PPI-3294', 'PPInfo - Отображение ссылки на карточку в SelfE')
    @pytest.mark.skip(reason='Переехало в здоровье')
    def test_selfe_attr_clickable(self, page):

        assert page.selfe.is_visible()
        assert page.selfe.is_clickable()
        link = page.selfe.get_attribute('href')
        assert link == 'https://selfe.mts.ru/surveys/result/personal-survey?personalSurveyId=95186', 'Ссылка на Selfe неверная'

    @allure.title('В режиме редактирования чипсы видны каранаши')
    @allure.issue('https://jira.mts.ru/browse/PPI-4372', 'PPInfo - Редактирование скрытых атрибутов контролёром направления бизнеса и админом (чипсы)')
    def test_editable_chips(self, page):

        page.edit_button.click()
        assert page.edit_in_chips.are_visible(), 'Карандаши в чипсах не видны после нажатия на кнопку редактирования'




    # TODO Сделай когда опишу Settings
    # @allure.title("Настройки чипсов на странице внешнего продукта")
    # @pytest.mark.parametrize("delayed_product_page", assertions_data.ProductsAsserts.linkToExternalProduct,
    #                          indirect=True)
    # def test_external_keyproperties(self, product_commercial_page, delayed_product_page):
    #     product_commercial_page.ext_key_prop_tab.click()
    #     product_commercial_page.wait_page_loaded()
    #     checked_toggles = product_commercial_page.is_checked.get_text()
    #     draggable_titles = [draggable.split("\n")[-1] for draggable in
    #                         product_commercial_page.draggable_titles.get_text()]
    #
    #     product_page = delayed_product_page()
    #     product_page.wait_page_loaded()
    #     key_props = product_page.key_prop.get_text()
    #
    #     print(draggable_titles)
    #     print(checked_toggles)
    #     print(key_props)
    #
    #     assert set(checked_toggles) == set(draggable_titles)
    #     assert len(key_props) == len(draggable_titles)
    #
    # @allure.title("Настройки чипсов на странице внутреннего продукта")
    # @pytest.mark.parametrize("delayed_product_page", assertions_data.ProductsAsserts.linkToInternalProduct,
    #                          indirect=True)
    # def test_internal_keyproperties(self, delayed_product_page, product_internal_page):
    #     product_internal_page.int_key_prop_tab.click()
    #     product_internal_page.wait_page_loaded()
    #     checked_toggles = product_internal_page.is_checked.get_text()
    #     draggable_titles = [draggable.split("\n")[-1] for draggable in
    #                         product_internal_page.draggable_titles.get_text()]
    #
    #     product_page = delayed_product_page()
    #     product_page.wait_page_loaded()
    #     key_props = product_page.key_prop.get_text()
    #
    #     print(draggable_titles)
    #     print(checked_toggles)
    #     print(key_props)
    #
    #     assert set(checked_toggles) == set(draggable_titles)
    #     assert len(key_props) == len(draggable_titles)


@pytest.mark.ui
class TestMainPageTechUser:

    @allure.title(f"Проверка невозможности редактирования продукта пользователю без админских прав")
    def test_replace_not_visible(self, page_user):
        with allure.step('Проверяем, что блок кнопок редактирования не отображается'):
            page_user.edit_product_block.click()
            assert page_user.edit_product_block_user_modal.is_visible(), 'Пользователю не высветилось модальное окно'

    @allure.title("Проверка, что пользователь из руководства может редактировать продукт")
    @pytest.mark.parametrize('page_user', ['https://stage.prodboard.mts.ru/product/BI_2062/main'],
                             indirect=True)
    def test_edit_owner_user(self, page_user: page_user):
        assert page_user.edit_product_block.is_visible(), 'Блока с кнопками нет'
        assert page_user.edit_button.is_clickable(), 'На кпопку редакитровать нельзя нажать'

    @allure.issue('https://jira.mts.ru/browse/PPI-3459',
                  'PPInfo - Отображение актуальности данных на странице продукта')
    @allure.title('Проверка, что пользователю отображается дата последнего изменения атрибута')
    def test_updated_at_for_user_main(self, page_user):
        assert page_user.date_with_tooltip.is_visible(), 'Нет даты обновления атрибутов'
        assert page_user.date_with_tooltip.is_clickable(), 'Объект не кликабельный'

    @allure.issue('https://jira.mts.ru/browse/PPI-3459',
                  'PPInfo - Отображение актуальности данных на странице продукта')
    @allure.title('Проверка, что пользователю отображается дата последнего изменения в разделе Атомарные')
    def test_updated_at_for_user_atomic(self, page_user):
        page_user.atomic_tab.click()
        assert page_user.date_with_tooltip.is_visible(), 'Нет даты обновления атрибутов'
        assert page_user.date_with_tooltip.is_clickable(), 'Объект не кликабельный'

    @allure.issue('https://jira.mts.ru/browse/PPI-3459',
                  'PPInfo - Отображение актуальности данных на странице продукта')
    @allure.title('Проверка, что пользователю отображается дата последнего изменения в разделе Документы')
    def test_updated_at_for_user_docs(self, page_user):
        page_user.docs_tab.click()
        assert page_user.date_with_tooltip.is_visible(), 'Нет даты обновления атрибутов'
        assert page_user.date_with_tooltip.is_clickable(), 'Объект не кликабельный'

    @allure.issue('https://jira.mts.ru/browse/PPI-3459',
                  'PPInfo - Отображение актуальности данных на странице продукта')
    @allure.title('Проверка, что пользователю отображается дата последнего изменения в разделе ПГ')
    def test_updated_at_for_user_pg(self, page_user):
        page_user.product_guide_tab.click()
        assert page_user.date_with_tooltip.is_visible(), 'Нет даты обновления атрибутов'
        assert page_user.date_with_tooltip.is_clickable(), 'Объект не кликабельный'

    @allure.issue('https://jira.mts.ru/browse/PPI-3566',
                  'PPInfo - Сделать понятным для пользователя, к кому обратиться для актуализации свойств продукта')
    @allure.title('Проверка, что пользователю без прав на редактирование отображается модалка')
    def test_edit_from_user_view(self, page_user):
        assert page_user.edit_button.is_visible()
        assert page_user.edit_button.is_clickable()

        page_user.edit_button.click()

        assert page_user.user_modal.is_visible()


    @allure.title('При клике на кнопку редактирования у архивных продуктов открывается')
    @allure.issue('https://jira.mts.ru/browse/PPI-4205',
                  'PPInfo - Кнопка "Редактировать" в карточке продукта в статусе Архив')
    @pytest.mark.parametrize('page_user', ['https://stage.prodboard.mts.ru/product/BI_52750/main'],
                             indirect=True)
    def test_edit_button_on_archived(self, page_user: page_user):

        page_user.call_admin_button.click()

        assert page_user.user_modal.is_visible, 'Модалка оповещения пользователей не появилась'

