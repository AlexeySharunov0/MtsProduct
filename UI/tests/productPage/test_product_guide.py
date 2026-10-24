import allure
import pytest

from UI.data.assertions_data import ProductsAsserts as assertions
from UI.tests.productPage.conftest import pg_page
from UI.tests.settingsPage.conftest import pg_page as pg_settings_page

@pytest.mark.ui
@allure.feature("Вкладка Product Guide")
class TestProductGuideSchema:
    @allure.title("Проверка кликабельности и отображения таба Product Guide")
    def test_pg_tab_check(self, pg_page):
        with allure.step("Проверяем, что таб есть в боковом меню"):
            assert pg_page.product_guide_tab.is_visible(), 'Таба нет в меню'
        with allure.step('Проверяем, что таб кликабельный'):
            assert pg_page.product_guide_tab.is_clickable(), 'Таб некликабельный'
        with allure.step("Проверяем, что таб отмечен как активный (черный)"):
            assert pg_page.product_guide_tab.get_attribute('class') == 'content', 'Таб окрашен серым'
        with allure.step('Проверяем, что чипс NEW отображается'):
            assert pg_page.new_chips.is_visible(), 'Чипса нет'

    @allure.title("Проверка корректности описание таба Product Guide")
    @allure.issue('https://jira.mts.ru/browse/PPI-1886', 'PPInfo - Пояснения к разделам на странице продукта')
    def test_info_about_tab(self, pg_page):
        with allure.step("Проверяем, что заголовок страницы отображается корректно"):
            assert pg_page.product_guide_header.is_visible(), 'Заголовка нет'
            assert pg_page.product_guide_header.get_text() == 'Product Guide', 'Текст заголовка не совпадает'
        with allure.step("Проверяем, что описание страницы отображается корректно"):
            assert pg_page.tab_description.is_visible(), 'Описания нет'
            assert pg_page.tab_description.get_text() == assertions.product_guide_description, 'Текст описания не совпадает'

    @allure.title("Проверка отображения основных элементов Product Guide / Строка поиска")
    @allure.issue('https://jira.mts.ru/browse/PPI-1910', 'PPInfo - Добавление нумерации действий в Product Guide')
    def test_pg_main_elements_search(self, pg_page):
        with allure.step('Проверяем, что строка поиска отображается'):
            assert pg_page.product_guide_search_line.is_visible(), 'Строки поиска нет'

    @allure.title("Проверка отображения основных элементов Product Guide / Вкладки групп")
    @allure.issue('https://jira.mts.ru/browse/PPI-4020',
                  'PPInfo - Графическое отображение PG')
    def test_pg_main_elements_groups_scheme_mode(self, pg_settings_page, pg_page):
        with allure.step('Проверяем, что вкладки отображается'):
            assert all(
                i.is_visible() for i in pg_page.column_name_in_scheme_mode), 'Часть групп не отображается'
        with allure.step('Проверяем каунтеры на группах'):
            assert all(
                i.is_visible() for i in pg_page.column_counter_in_scheme_mode), 'Каунтеры не видны'
            assert all(int(i.get_text()) >= 0 for i in
                       pg_page.column_counter_in_scheme_mode), 'Каунтеры отрицательные'
        with allure.step('Проверяем, что все вкладки из настроек отображаются'):
            actual_groups = [i.get_text().replace(' ', '').replace('\n', '').lower() for i in
                             pg_page.column_name_in_scheme_mode]
            pg_settings_page.get_page('https://stage.prodboard.mts.ru/lifecycleadmin/current')
            expected_groups = [i.get_text().replace(' ', '').replace('\n', '').lower() for i in
                               pg_settings_page.side_groups]
            assert actual_groups == expected_groups, 'Группы не совпадают'


    @allure.title('При нажатии на шаг в режиме схемы, появляется всплывающее окно')
    @pytest.mark.skip('Разобраться')
    @allure.issue('https://jira.mts.ru/browse/PPI-4020',
                  'PPInfo - Графическое отображение PG')
    def test_side_window(self, pg_page):

        for step in pg_page.steps_pg:
            step.click()
            if sub := pg_page.substep_list.is_visible():
                for substep in pg_page.steps_in_substep_list:
                    substep.click()
                    assert pg_page.side_window_in_scheme_mode.is_visible(), 'Всплывающее окно не появилось'
                    pg_page.schema.click(force=True)
            pg_page.toggle_substeps.click() if sub else pg_page.schema.click(force=True)



@pytest.mark.ui
@allure.feature("Вкладка Product Guide")
class TestProductGuideList:

    @allure.title("Проверка отображения основных элементов Product Guide / Вкладки групп")
    def test_pg_main_elements_groups(self, pg_settings_page, pg_page):
        pg_page.display_mode[1].click()
        with allure.step('Проверяем, что вкладки отображается'):
            assert all(
                i.is_visible() for i in pg_page.product_guide_groups_list), 'Часть групп не отображается'
            assert all(i.is_clickable() for i in pg_page.product_guide_groups_list), 'Часть групп не нажать'
        with allure.step('Проверяем каунтеры на группах'):
            assert all(
                i.is_visible() for i in pg_page.product_guide_group_counters), 'Каунтеры не видны'
            assert all(int(i.get_text()) >= 0 for i in
                       pg_page.product_guide_group_counters), 'Каунтеры отрицательные'
        with allure.step('Проверяем, что все вкладки из настроек отображаются'):
            actual_groups = [i.get_text()[:-2].replace(' ', '').replace('\n', '').lower() for i in
                             pg_page.product_guide_groups_list]
            pg_settings_page.get_page('https://stage.prodboard.mts.ru/lifecycleadmin/current')
            expected_groups = [i.get_text().replace(' ', '').replace('\n', '').lower() for i in
                               pg_settings_page.side_groups]
            assert actual_groups == expected_groups, 'Группы не совпадают'



    @allure.title("Проверка работу вкладок групп")
    def test_pg_group_work(self, pg_page):
        pg_page.display_mode[1].click()
        with allure.step('Проверяем переключение вкладок'):
            for group in pg_page.product_guide_groups_list:
                with allure.step(f'Кликаем на таб {group.get_text()}'):
                    group.click()
                with allure.step('Проверяем, что вкладка активная'):
                    assert group.is_selected(), 'Вкладка не активная'
        with allure.step('Проверяем, что вкладка серая при отсутствии шагов'):
            for group in (groups := pg_page.product_guide_groups_list.get_items()):
                if int(pg_page.product_guide_group_counters.get_items()[groups.index(group)].get_text()) == 0:
                    assert 'notEmpty' not in group.get_attribute('class'), 'Вкладка отображается активной'
                else:
                    assert 'notEmpty' in group.get_attribute('class'), 'Вкладка отображается серой'

    @allure.title("Каждая группа шагов имеет свою ссылку ")
    @allure.issue('https://jira.mts.ru/browse/PPI-2718', 'PPInfo - Ссылка на группу шагов в PG ')
    def test_pg_group_links(self, pg_page):
        pg_page.display_mode[1].click()
        with allure.step('Группа Разработка и запуск MVP имеет свою ссылку'):
            pg_page.product_guide_groups_list[1].click()
            assert pg_page.url == 'https://stage.prodboard.mts.ru/product/BI_60/guide?tab=%D0%A0%D0%B0%D0%B7%D1%80%D0%B0%D0%B1%D0%BE%D1%82%D0%BA%D0%B0+%D0%B8+%D0%B7%D0%B0%D0%BF%D1%83%D1%81%D0%BA+MVP', 'При переход на таб Разработка и запуск MVP ссылка не изменилась'

        with allure.step('Группа Развитие продукта имеет свою ссылку'):
            pg_page.product_guide_groups_list[2].click()
            assert pg_page.url == 'https://stage.prodboard.mts.ru/product/BI_60/guide?tab=%D0%A0%D0%B0%D0%B7%D0%B2%D0%B8%D1%82%D0%B8%D0%B5+%D0%BF%D1%80%D0%BE%D0%B4%D1%83%D0%BA%D1%82%D0%B0', 'При переход на таб Развитие продукта ссылка не изменилась'

        with allure.step('Группа Закрытие продукта имеет свою ссылку'):
            pg_page.product_guide_groups_list[3].click()
            assert pg_page.url == 'https://stage.prodboard.mts.ru/product/BI_60/guide?tab=%D0%97%D0%B0%D0%BA%D1%80%D1%8B%D1%82%D0%B8%D0%B5+%D0%BF%D1%80%D0%BE%D0%B4%D1%83%D0%BA%D1%82%D0%B0', 'При переход на таб Закрытие продукта ссылка не изменилась'

        with allure.step('Группа Разработка концепции имеет свою ссылку'):
            pg_page.product_guide_groups_list[0].click()
            assert pg_page.url == 'https://stage.prodboard.mts.ru/product/BI_60/guide?tab=%D0%A0%D0%B0%D0%B7%D1%80%D0%B0%D0%B1%D0%BE%D1%82%D0%BA%D0%B0+%D0%BA%D0%BE%D0%BD%D1%86%D0%B5%D0%BF%D1%86%D0%B8%D0%B8', 'При переход на таб Разработка концепции ссылка не изменилась'

    @allure.title("Проверка отображения основных элементов Product Guide / Шаги")
    def test_pg_main_elements_steps(self, pg_page):
        pg_page.display_mode[1].click()
        with allure.step('Проверяем, что шаги отображается'):
            if pg_page.steps_pg:
                assert all(i.is_visible() for i in pg_page.steps_pg), 'Шаги не отображается'
                assert len(pg_page.steps_pg.get_items()) == len(
                    pg_page.step_name.get_items()), 'Ни у каждого шага есть имя'

    @allure.title("Проверка отображения нумерации на шагах")
    @allure.issue('https://jira.mts.ru/browse/PPI-1910', 'PPInfo - Добавление нумерации действий в Product Guide')
    def test_numeric_of_steps(self, pg_page):
        pg_page.display_mode[1].click()
        with allure.step('Проверяем, что у каждого шага есть порядковый номер'):
            assert len(pg_page.steps_pg.get_items()) == len(
                pg_page.step_counters.get_items()), 'Ни у каждого шага есть порядковый номер'
            assert all(i.is_visible() for i in pg_page.step_counters), 'Каунтеры не отображается'
        for group in pg_page.product_guide_groups_list:
            with allure.step(f'Переходим на вкладку {group.get_text()}'):
                group.click()
            if pg_page.steps_pg.get_items():
                expected_indexes = [i for i in range(1, len(pg_page.steps_pg.get_items()) + 1)]
                real_indexes = [int(i.get_text()[:-4]) for i in pg_page.step_counters]

                with allure.step(f'Проверяем, что нумерация верная на вкладке {group.get_text()}'):
                    assert expected_indexes == real_indexes, 'Нумерация неверная'
            else:
                with allure.step('Проверяем, что при отсутствии шагов есть сообщение'):
                    assert pg_page.pg_error.is_visible(), 'текста нет'

    @allure.title("Проверка появления/пропадания новых шагов на странице PG после создания/удаления")
    def test_pg_create_and_delete_step(self, pg_page, pg_settings_page):
        pg_settings_page.delete_test_steps()
        pg_settings_page.create_step(is_active=True)
        with allure.step('Проверяем, что шаг появился в конце'):
            pg_page.get_page('https://stage.prodboard.mts.ru/product-guide/Vneshnii')
            pg_page.display_mode[1].click()
            assert pg_page.step_name[-1].get_text() == 'test_name', 'Шаг не появился/ в конце'
        with allure.step('Удаляем шаг'):
            pg_settings_page.get_page('https://stage.prodboard.mts.ru/lifecycleadmin/current')
            pg_settings_page.delete_test_steps()
        with allure.step('Проверяем, что шаг удалился из списка PG'):
            pg_page.get_page('https://stage.prodboard.mts.ru/product-guide/Vneshnii')
            pg_page.display_mode[1].click()
            with allure.step('Проверяем, что шага нет в конце'):
                assert all(
                    i.get_text() != 'test_name' for i in pg_page.step_name), 'Шаг остался'

    @allure.title("Проверяем, что неактивный шаг не отображается на странице PG")
    def test_pg_create_inactive_step(self, pg_page, pg_settings_page):
        pg_settings_page.delete_test_steps()
        pg_settings_page.create_step()
        pg_page.get_page('https://stage.prodboard.mts.ru/product-guide/Vneshnii')
        pg_page.display_mode[1].click()
        with allure.step('Проверяем, что шага нет в конце'):
            assert all(
                i.get_text() != 'test name' for i in pg_page.step_name), 'Шаг остался'
        with allure.step('Удаляем шаг'):
            pg_settings_page.get_page('https://stage.prodboard.mts.ru/lifecycleadmin/current')
            pg_settings_page.delete_test_steps()

    @allure.title("Проверяем ссылки в шаге PG")
    def test_pg_check_links(self, pg_page, pg_settings_page):
        pg_settings_page.side_groups[-1].click()
        pg_settings_page.delete_all_steps()
        with allure.step('Добавляем активный шаг со ссылкой'):
            pg_settings_page.add_step_button.click()
            pg_settings_page.add_name_to_step()
            pg_settings_page.change_activity_step(True)
            pg_settings_page.add_links_to_step(['test_link', 'https://stage.prodboard.mts.ru'])
            pg_settings_page.add_button_inside.click()
        pg_page.get_page('https://stage.prodboard.mts.ru/product-guide/Vneshnii')
        pg_page.display_mode[1].click()
        with allure.step('Переходим на последнюю вкладку'):
            pg_page.product_guide_groups_list[-1].click()
        with allure.step('Проверяем ссылки в шаге'):
            assert pg_page.step_link_block.is_visible(), 'Блока ссылок нет'
            assert all(link.is_visible() for link in pg_page.step_links), 'Ссылки не видны'
            assert all(link.is_clickable() for link in pg_page.step_links), 'Ссылки некликабельные'
        with allure.step('Удаляем шаг'):
            pg_settings_page.get_page('https://stage.prodboard.mts.ru/lifecycleadmin/current')
            pg_settings_page.side_groups[-1].click()
            pg_settings_page.delete_all_steps()

    @allure.title("Проверяем сотрудники в шаге PG")
    def test_pg_check_users(self, pg_page, pg_settings_page):
        pg_settings_page.side_groups[-1].click()
        pg_settings_page.delete_all_steps()
        with allure.step('Добавляем активный шаг с 3 сотрудниками'):
            pg_settings_page.add_step_button.click()
            pg_settings_page.add_name_to_step()
            pg_settings_page.change_activity_step(True)
            pg_settings_page.add_users_to_step(amount=3)
            pg_settings_page.add_button_inside.click()
        pg_page.get_page('https://stage.prodboard.mts.ru/product-guide/Vneshnii')
        pg_page.display_mode[1].click()
        with allure.step('Переходим на последнюю вкладку'):
            pg_page.product_guide_groups_list[-1].click()
        with allure.step('Проверяем ссылки в шаге'):
            assert pg_page.step_employee_block.is_visible(), 'Блока юзеров нет'
            assert all(user.is_visible() for user in pg_page.step_employees), 'Юзеры не видны'
            assert all(user.is_clickable() for user in pg_page.step_employees), 'Юзеры некликабельные'
        with allure.step('Проверяем, что при клике на сотрудника открывается карточка'):
            with allure.step('Кликаем на сотрудника'):
                pg_page.step_employees[0].click()
            with allure.step('Проверяем, что появилась карточка'):
                assert pg_page.user_card.is_visible(), 'Карточки сотрудника нет'
        with allure.step('Удаляем шаг'):
            pg_settings_page.get_page('https://stage.prodboard.mts.ru/lifecycleadmin/current')
            pg_settings_page.side_groups[-1].click()
            pg_settings_page.delete_all_steps()

    @allure.title("Проверяем файлы в шаге PG")
    def test_pg_check_files(self, pg_page, pg_settings_page):
        pg_settings_page.side_groups[-1].click()
        pg_settings_page.delete_all_steps()
        with allure.step('Добавляем активный шаг с файлом'):
            pg_settings_page.add_step_button.click()
            pg_settings_page.add_name_to_step()
            pg_settings_page.change_activity_step(True)
            pg_settings_page.add_files_to_step()
            pg_settings_page.add_button_inside.click()
            pg_settings_page.wait_force(2)

        pg_page.get_page('https://stage.prodboard.mts.ru/product-guide/Vneshnii')
        pg_page.display_mode[1].click()
        with allure.step('Переходим на последнюю вкладку'):
            pg_page.product_guide_groups_list[-1].click()
        with allure.step('Проверяем ссылки в шаге'):
            assert pg_page.step_files_block.is_visible(), 'Блока файлов нет'
            assert all(file.is_visible() for file in pg_page.step_files), 'Файлы не видны'
            assert all(file.is_clickable() for file in pg_page.step_files), 'Файлы некликабельные'
        with allure.step('Удаляем шаг'):
            pg_settings_page.get_page('https://stage.prodboard.mts.ru/lifecycleadmin/current')
            pg_settings_page.side_groups[-1].click()
            pg_settings_page.delete_all_steps()

    @allure.title("Контекстный поиск в Product Guide / Общая работа поиска")
    @allure.issue('https://jira.mts.ru/browse/PPI-1912', 'PPInfo -Добавить контекстный поиск в Product Guide')
    @pytest.mark.last
    @pytest.mark.parametrize(['name', 'description'], [['черепаха', 'бегемот'], ['ЧЕРЕПАХА', 'БЕГЕМОТ'],
                                                       [' черепаха', ' бегемот']])
    def test_search_pg_general(self, pg_page, pg_settings_page, name, description):
        pg_settings_page.side_groups[-1].click()
        pg_settings_page.delete_all_steps()

        pg_settings_page.create_step(name='Проверка поиска: черепаха', description='Проверка поиска: бегемот',
                                     is_active=True)
        pg_settings_page.side_groups[-1].click()
        pg_settings_page.create_step(is_active=True)
        pg_settings_page.side_groups[-1].click()
        pg_page.get_page('https://stage.prodboard.mts.ru/product-guide/Vneshnii')
        pg_page.display_mode[1].click()
        with allure.step('Переходим на последнюю вкладку'):
            pg_page.product_guide_groups_list[-1].click()
        with allure.step('Ищем необходимый шаг по имени'):
            pg_page.product_guide_search_line.fill(description)

            with allure.step('Проверяем, что шаг нашелся'):
                assert len(pg_page.steps_pg.get_items()) == 1, 'нашлось больше 1 нужного шага'
                assert 'Проверка поиска: черепаха' in pg_page.steps_pg[0].get_text(), 'Нужный шаг не найден'

        pg_page.pg_search_cross.click()
        with allure.step('Ищем необходимый шаг по описанию'):
            pg_page.product_guide_search_line.fill(description)

            with allure.step('Проверяем, что шаг нашелся'):
                assert len(pg_page.steps_pg.get_items()) == 1, 'нашлось больше 1 нужного шага'
                assert 'Проверка поиска: черепаха' in pg_page.steps_pg[0].get_text(), 'Нужный шаг не найден'

    @allure.title("Контекстный поиск в Product Guide / Каунтеры и вкладки групп")
    @allure.issue('https://jira.mts.ru/browse/PPI-1912', 'PPInfo -Добавить контекстный поиск в Product Guide')
    @pytest.mark.last
    def test_search_pg_groups(self, pg_page, pg_settings_page):
        pg_settings_page.side_groups[-1].click()
        pg_settings_page.delete_all_steps()

        pg_settings_page.create_step(name='Проверка поиска: черепаха', description='Проверка поиска: бегемот',
                                     is_active=True)
        pg_settings_page.side_groups[-1].click()
        pg_settings_page.create_step(is_active=True)
        pg_settings_page.side_groups[-1].click()
        pg_page.get_page('https://stage.prodboard.mts.ru/product-guide/Vneshnii')
        pg_page.display_mode[1].click()
        with allure.step('Переходим на последнюю вкладку'):
            pg_page.product_guide_groups_list[-1].click()
        with allure.step('Ищем необходимый шаг'):
            pg_page.product_guide_search_line.fill('черепаха')

        with allure.step('Проверяем, что цифры в каунтерах изменились'):
            assert all(item.get_text() == '0' for item in
                       pg_page.product_guide_group_counters[:-1]), 'На какой-то из вкладок не ноль в каунтере'
            assert pg_page.product_guide_group_counters[
                       -1].get_text() == '1', 'На последней вкладке не 1 результат в каунтере'

        with allure.step('Проверяем, что отображение групп изменилось'):
            assert all('notEmpty' not in item.get_attribute('class') for item in
                       pg_page.product_guide_groups_list[:-1]), 'Остальные отображаются как непустые'
            assert 'notEmpty' in pg_page.product_guide_groups_list[-1].get_attribute(
                'class'), 'Последняя вкладка отображается как пустая'

    @allure.title("Контекстный поиск в Product Guide / Редирект при нахождении шага")
    @allure.issue('https://jira.mts.ru/browse/PPI-1912', 'PPInfo -Добавить контекстный поиск в Product Guide')
    @pytest.mark.last
    def test_search_pg_redirect(self, pg_page, pg_settings_page):
        pg_settings_page.side_groups[-1].click()
        pg_settings_page.delete_all_steps()

        pg_settings_page.create_step(name='Проверка поиска: черепаха', description='Проверка поиска: бегемот',
                                     is_active=True)
        pg_settings_page.side_groups[-1].click()

        pg_page.get_page('https://stage.prodboard.mts.ru/product-guide/Vneshnii')
        pg_page.display_mode[1].click()

        with allure.step('Ищем необходимый шаг'):
            pg_page.product_guide_search_line.fill('черепаха')

        with allure.step('Проверяем, что сообщение на редирект отображается и работает верно'):
            groups = pg_page.product_guide_groups_list.get_items()
            for group in groups[:-1]:
                with allure.step(f'Переходим на вкладку {group.get_text()[:-2]}'):
                    group.click()
                redirect_links = pg_page.search_redirect_links.get_items()
                with allure.step('Проверяем, что редирект отображается корректно'):
                    assert all(i.is_visible() for i in redirect_links), 'Ссылки не видны'
                    assert all(
                        i.is_clickable() for i in redirect_links), 'на ссылки нельзя нажать'
                    assert redirect_links[0].get_text().lower() == groups[-1].get_text()[
                                                                   :-2].lower(), 'Название группы в редиректе неверное'
                with allure.step('Переходим по ссылке в редиректе'):
                    redirect_links[0].click()
                with allure.step('Проверяем, что мы перешли на нужную вкладку'):
                    assert pg_page.product_guide_groups_list[-1].is_selected(), 'Мы не перешли на последнюю вкладку'

    @allure.title("Контекстный поиск в Product Guide / Сообщение о том, что ничего не найдено")
    @allure.issue('https://jira.mts.ru/browse/PPI-1912', 'PPInfo -Добавить контекстный поиск в Product Guide')
    @pytest.mark.last
    def test_search_pg_no_result(self, pg_page, pg_settings_page):
        pg_settings_page.side_groups[-1].click()
        pg_settings_page.delete_all_steps()

        pg_settings_page.create_step(name='Проверка поиска: черепаха', description='Проверка поиска: бегемот',
                                     is_active=True)
        pg_settings_page.side_groups[-1].click()

        pg_page.get_page('https://stage.prodboard.mts.ru/product-guide/Vneshnii')
        pg_page.display_mode[1].click()

        with allure.step('Ищем несуществующий шаг'):
            pg_page.product_guide_search_line.fill('белиберда')

        with allure.step('Проверяем, что сообщение о том, что ничего не найдено отображается на каждой вкладке'):
            for group in pg_page.product_guide_groups_list:
                group.click()
                assert pg_page.pg_search_error.is_visible(), 'Сообщения о том, что ничего не найдено - нет'

    @allure.title("Поиск по тэгам шагов в разделе Product Guide")
    @allure.issue('https://jira.mts.ru/browse/PPI-3304', 'PPInfo - Поиск по тэгам шагов в разделе Product Guide')
    @pytest.mark.last
    def test_search_pg_tags(self, pg_page):
        pg_page.display_mode[1].click()
        with allure.step('Ищем шаг по тегу'):
            pg_page.product_guide_search_line.fill('Французский бульдог')

        with allure.step('Проверяем, что шаг нашелся'):
            assert len(pg_page.steps_pg.get_items()) == 1, 'нашлось больше 1 нужного шага'
            assert 'Не удалять' in pg_page.steps_pg[0].get_text(), 'Нужный шаг не найден'

    @allure.title("У вложенных шагов на странице общего ПГ отображаются чипсы обязательности и повторяемости")
    @allure.issue('https://jira.mts.ru/browse/PPI-2868',
                  'PPInfo - PG: Отображение меток (обязательный, повторяемый) для вложенных шагов')
    def test_cheeps_in_sub_steps(self, pg_page):
        pg_page.get_page('https://stage.prodboard.mts.ru/product-guide/Vneshnii')
        pg_page.display_mode[1].click()
        assert pg_page.required_cheeps_in_internal_step.is_visible()

    @allure.title("У вложенных шагов на странице продукта отображаются чипсы обязательности и повторяемости")
    @allure.issue('https://jira.mts.ru/browse/PPI-2868',
                  'PPInfo - PG: Отображение меток (обязательный, повторяемый) для вложенных шагов')
    def test_cheeps_in_sub_steps_in_product_page(self, pg_page):
        pg_page.display_mode[1].click()
        assert pg_page.required_cheeps_in_internal_step.is_visible()

    @allure.title('Проверка фильтры обязательности')
    @allure.issue('https://jira.mts.ru/browse/PPI-2237', 'PPInfo - Фильтрация шагов в Product Guide')
    def test_check_filter_in_pg_required(self, pg_page):
        pg_page.display_mode[1].click()
        pg_page.choice_filter('Обязательные')
        assert pg_page.assert_chips('required')

    @allure.title('Проверка фильтры повторяемости')
    @allure.issue('https://jira.mts.ru/browse/PPI-2237', 'PPInfo - Фильтрация шагов в Product Guide')
    def test_check_filter_in_pg_repeatable(self, pg_page):
        pg_page.display_mode[1].click()
        pg_page.choice_filter('Повторяемые')
        assert pg_page.assert_chips('repeatable')

    @allure.title('Проверка фильтры PO')
    @allure.issue('https://jira.mts.ru/browse/PPI-2237', 'PPInfo - Фильтрация шагов в Product Guide')
    def test_check_filter_in_pg_po(self, pg_page):
        pg_page.display_mode[1].click()
        pg_page.choice_filter('PO')
        assert pg_page.assert_chips('forPo')

    @allure.title('Проверка фильтры TechLead')
    @allure.issue('https://jira.mts.ru/browse/PPI-2237', 'PPInfo - Фильтрация шагов в Product Guide')
    def test_check_filter_in_pg_cto(self, pg_page):
        pg_page.display_mode[1].click()
        pg_page.choice_filter('Tech Lead')
        assert pg_page.assert_chips('forPo cto')

    @allure.title('Ссылка на конкретный шаг')
    @allure.issue('https://jira.mts.ru/browse/PPI-3491',
                  'PPInfo - Подсвечивать пользователю шаг в PG при переходе на него по ссылке')
    @pytest.mark.parametrize('step_group, group_id',
                             [(0, 'abfe6e2a-b86c-49e2-990b-2d07e6087c31'), (1, '76ed0eb2-e889-4b2b-80be-60b46007285e'),
                              (2, '83e92cfe-1257-49f5-80c8-5b953bcdb3a3')])
    def test_copy_step(self, pg_page, step_group, group_id):
        pg_page.display_mode[1].click()

        pg_page.product_guide_groups_list[step_group].click()

        link = f'https://stage.prodboard.mts.ru/product/BI_60/guide?{pg_page.steps_pg[-1].get_attribute("id").replace("-", "=", 1)}&group={group_id}'
        pg_page.get_page(link)

        assert pg_page.steps_pg[-1].get_attribute(
            "style") == 'border: 2px solid rgb(255, 0, 50); background-color: rgb(254, 232, 224);', 'Ссылка не перевела на шаг и стили не применились'
        pg_page.wait_force(4)
        assert pg_page.steps_pg[-1].get_attribute(
            "style") == 'border: 2px solid rgb(255, 0, 50); background-color: white;', 'Фон не белый или не красная обводка'

    @allure.title('Проверка видимости кнопок действий')
    @allure.issue('https://jira.mts.ru/browse/PPI-4115', 'PPInfo - Product Guide: кнопки действий')
    def test_actions_buttons_is_visible(self, pg_page):
        pg_page.display_mode[1].click()

        assert pg_page.action_button.is_visible(), 'кнопки действий не видны'




