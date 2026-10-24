from datetime import datetime

import allure
import pytest

from UI.tests.settingsPage.conftest import pg_page
from paths import ROOT


@pytest.mark.ui
@allure.feature("Product Guide")
class TestProductGuideSettings:
    @allure.title("Проверяем отображение основных элементов на странице настроек Product Guide / Заголовок")
    def test_pg_check_header(self, pg_page):

        with allure.step("Проверем корректное отображение заголовка"):
            assert pg_page.header.is_visible(), 'Заголовка страницы нет'
            assert pg_page.header.get_text() == 'Шаги Product Guide', 'Текст не совпадает'

    @allure.title("Проверяем отображение основных элементов на странице настроек Product Guide / Боковое меню")
    def test_pg_check_side_menu(self, pg_page):

        with allure.step("Проверяем наличие бокового меню"):
            assert pg_page.side_menu.is_visible(), 'Меню нет'
            with allure.step("Проверяем кликабельность групп"):
                for i in pg_page.side_groups:
                    assert i.is_clickable(), f'Группа {i.get_text()} не кликабельна'

    @allure.title("Проверяем отображение основных элементов на странице настроек Product Guide / Кнопка Добавить шаг")
    def test_pg_check_add_step_button(self, pg_page):

        with allure.step("Проверяем отображение кнопки Добавить шаг"):
            assert pg_page.add_step_button.is_visible(), 'Кнопки нет'
            assert pg_page.add_step_button.is_clickable(), 'На кнопку нельзя нажать'

    @allure.title("Проверяем отображение основных элементов на странице настроек Product Guide / Шаги")
    def test_pg_check_steps(self, pg_page):
        with allure.step("Проверяем отображение таблицы шагов"):
            assert pg_page.table_steps.is_visible(), 'Таблицы шагов нет'
        with allure.step('Проверяем кликабельность шагов'):
            for step in pg_page.steps:
                assert step.is_clickable(), f'На шаг {step.get_text()} нельзя нажать'
        with allure.step('Проверяем тоглы активности'):
            assert all(i.is_clickable() for i in pg_page.activity_toggles), 'На тоглы нельзя нажать'
            assert any(i.is_checked() for i in pg_page.activity_toggles), 'Все тоглы выключены'

    @allure.title("Проверяем работу вкладок бокового меню PG")
    def test_pg_side_groups_work(self, pg_page):

        prev_text = ''
        for group in pg_page.side_groups:
            with allure.step(f'Жмем на вкладку {group.get_text()}'):
                group.click()
            with allure.step("Проверяем, что вкладка стала активной"):
                assert 'active' in group.get_attribute('class'), 'Вкладка не стала активной'
            with allure.step("Проверяем, что шаги сменились"):
                if pg_page.no_steps_text.is_not_visible():
                    assert pg_page.steps.get_texts() != prev_text, 'Шаги не сменились'
                    prev_text = pg_page.steps.get_texts()

    @allure.title("Проверяем создание обычного шага PG")
    @pytest.mark.parametrize('is_active', [True, False])
    def test_pg_add_step(self, pg_page, is_active):
        pg_page.delete_test_steps()
        pg_page.create_step(is_active)
        pg_page.side_groups[0].click()
        with allure.step("Проверяем, что шаг добавился в общий список"):
            assert pg_page.steps[-1].get_text() == 'test_name', 'Новый шаг не добавился'
        with allure.step("Проверяем, что дата добавления шага актуальная"):
            current_date = datetime.now().strftime('%d-%m-%y').replace("-", ".")
            assert current_date in pg_page.rows_steps[-1].get_text(), 'Дата не та'
        with allure.step("Проверяем, что активность шага согласно тоглу"):
            assert is_active is pg_page.activity_toggles[-1].is_checked(), 'Активность не та, что при создании'

        pg_page.delete_test_steps()

    @allure.title("Проверяем создание внешнего/внутреннего шага PG")
    @allure.issue('https://jira.mts.ru/browse/PPI-2148', 'PPInfo - Добавить столбец "Тип продукта" в Product Guide')
    @pytest.mark.parametrize('step_type', [['Внешний'], ['Внутренний'], ['Внешний', 'Внутренний']])
    def test_pg_add_type_step(self, pg_page, step_type):
        pg_page.delete_test_steps()
        with allure.step('Жмем на Добавить шаг'):
            pg_page.add_step_button.click()
        pg_page.add_name_to_step()
        pg_page.change_activity_step()
        pg_page.change_condition(value_list=step_type, index_of_condition=1)
        with allure.step('Жмем на Добавить шаг'):
            pg_page.add_button_inside.click()
            pg_page.side_groups[0].click()
            pg_page.wait()
        with allure.step("Проверяем, что тип продукта как при создании"):
            if len(step_type) == 1:
                assert step_type[0] in pg_page.rows_steps[-1].get_text(), 'Тип не тот'
            else:
                assert f'{step_type[0]}, {step_type[1].lower()}' in pg_page.rows_steps[
                    -1].get_text(), 'Тип не тот'

        pg_page.delete_test_steps()

    @allure.title("Проверяем наличие текста при отсутствии шагов")
    def test_pg_no_steps_text(self, pg_page):
        with allure.step("Переходим на последнюю вкладку"):
            pg_page.side_groups[-1].click()
        pg_page.create_step()
        pg_page.side_groups[-1].click()
        with allure.step("Проверяем, что текста нет"):
            assert pg_page.no_steps_text.is_not_visible(), 'Текст есть'
        pg_page.delete_all_steps()
        with allure.step("Проверяем, что текст появился"):
            assert pg_page.no_steps_text.is_visible(), 'Текста нет'
            assert pg_page.no_steps_text.get_text() == 'Шаги не добавлены', 'Текст не тот'

    @allure.title("Проверяем отображение основных элементов на странице шага Product Guide / Заголовок")
    def test_pg_step_check_header(self, pg_page):

        with allure.step("Жмем кнопку Добавить шаг"):
            pg_page.add_step_button.click()
        with allure.step("Проверем корректное отображение заголовка"):
            assert pg_page.step_header.is_visible(), 'Заголовка страницы нет'
            assert pg_page.step_header.get_text() == 'Добавление шага', 'Текст не совпадает'

    @allure.title("Проверяем отображение основных элементов на странице шага Product Guide / Кнопка активности")
    def test_pg_step_check_activity_toggle(self, pg_page):

        with allure.step("Жмем кнопку Добавить шаг"):
            pg_page.add_step_button.click()
        with allure.step("Проверяем корректное отображение тогла активности"):
            assert pg_page.activity_toggle.is_visible(), 'Тогла нет'
            assert pg_page.activity_toggle.is_not_checked(), 'Тогл включен по умолчанию'
        with allure.step("Жмем на тогл"):
            pg_page.activity_toggle.click()
        with allure.step("Проверяем, что тогл переключился"):
            assert pg_page.activity_toggle.is_checked(), 'Тогл не переключился'

    @allure.title("Проверяем отображение основных элементов на странице шага Product Guide / Название и описание")
    def test_pg_step_check_name_and_descr(self, pg_page):

        with allure.step("Жмем кнопку Добавить шаг"):
            pg_page.add_step_button.click()
        with allure.step("Проверяем корректное отображение формы названия"):
            assert pg_page.step_name.is_visible(), 'Формы названия нет'
        with allure.step("Проверяем корректное отображение формы описания"):
            assert pg_page.step_description.is_visible(), 'Формы описания нет'

    @allure.title("Проверяем отображение основных элементов на странице шага Product Guide / Кнопки обязательности")
    def test_pg_step_check_required_button(self, pg_page):

        with allure.step("Жмем кнопку Добавить шаг"):
            pg_page.add_step_button.click()
        buttons = pg_page.step_required_radio_button.get_items()
        with allure.step("Проверяем корректное отображение Кнопок обязательности действия"):
            for button in buttons[:2]:
                assert button.is_visible(), f'Кнопки {button.get_text()} нет'
                assert button.is_clickable(), f'На кнопку {button.get_text()} нельзя нажать'
        with allure.step('Проверяем, что действие по умолчанию необязательное'):
            assert buttons[0].is_checked(), 'Кнопка Необязательный не включена по умолчанию'
            assert buttons[1].is_not_checked(), 'Кнопка Обязательный включена по умолчанию'
        with allure.step('Жмем на кнопку Обязательный'):
            buttons[1].click()
        buttons = pg_page.step_required_radio_button.get_items()
        with allure.step('Проверяем, что действие стало обязательное'):
            assert buttons[0].is_not_checked(), 'Кнопка Необязательный включена'
            assert buttons[1].is_checked(), 'Кнопка Обязательный не включена'

    @allure.title("Проверяем отображение основных элементов на странице шага Product Guide / Кнопки повторяемости")
    def test_pg_step_check_repeatable_button(self, pg_page):

        with allure.step("Жмем кнопку Добавить шаг"):
            pg_page.add_step_button.click()
        buttons = pg_page.step_repeatable_radio_button.get_items()
        with allure.step("Проверяем корректное отображение Кнопок повторяемости действия"):
            for button in buttons[2:]:
                assert button.is_visible(), f'Кнопки {button.get_text()} нет'
                assert button.is_clickable(), f'На кнопку {button.get_text()} нельзя нажать'
        with allure.step('Проверяем, что действие по умолчанию обычное'):
            assert buttons[2].is_checked(), 'Кнопка обычный не включена по умолчанию'
            assert buttons[3].is_not_checked(), 'Кнопка повторяемый включена по умолчанию'
        with allure.step('Жмем на кнопку Повторяемый'):
            buttons[3].click()
        buttons = pg_page.step_repeatable_radio_button.get_items()
        with allure.step('Проверяем, что действие стало повторяемое'):
            assert buttons[2].is_not_checked(), 'Кнопка обычный включена'
            assert buttons[3].is_checked(), 'Кнопка повторяемый не включена'

    @allure.title("Проверяем отображение основных элементов на странице шага Product Guide / Форма сотрудников")
    def test_pg_step_check_user_form(self, pg_page):

        with allure.step("Жмем кнопку Добавить шаг"):
            pg_page.add_step_button.click()
        with allure.step("Проверяем корректное отображение формы сотрудников"):
            assert pg_page.step_users.is_visible(), 'Формы нет'
            assert pg_page.step_users.is_clickable(), 'На форму нельзя нажать'
        with allure.step('Жмем на форму'):
            pg_page.step_users.click()
        with allure.step('Проверяем, что появилась форма с ФИО'):
            assert pg_page.step_users_find_line.is_visible(), 'Формы для ввода ФИО не появилось'
        with allure.step('Вводим текст в форму ФИО'):
            pg_page.step_users_find_line.fill('Иванов')
            pg_page.step_find_button.click()
        with allure.step('Проверяем, что появились сотрудники'):
            assert all(user.is_visible() for user in pg_page.found_users), 'Пользователей нет'
        with allure.step("Выбираем первых трех пользователей"):
            for user in pg_page.found_users[:3]:
                user.click()
        with allure.step('Проверяем, что пользователи появились в форме'):
            assert pg_page.found_users.get_texts(), 'Пользователей нет'

    @allure.title("Проверяем отображение основных элементов на странице шага Product Guide / Форма ссылки")
    def test_pg_step_check_link_form(self, pg_page):

        with allure.step("Жмем кнопку Добавить шаг"):
            pg_page.add_step_button.click()
        with allure.step("Проверяем корректное отображение формы ссылок"):
            assert pg_page.link_name_input.is_visible(), 'Названия ссылки нет'
            assert pg_page.link_input.is_visible(), 'Значения ссылки ссылки нет'
        with allure.step("Проверяем корректное отображение кнопок ссылок"):
            assert pg_page.delete_link_button[0].is_visible(), 'Кнопки Удалить ссылку нет'
            assert pg_page.add_link_button.is_visible(), 'Кнопки Добавить ссылку нет'
            assert pg_page.delete_link_button[0].is_clickable(), 'На кнопку Удалить ссылку нельзя нажать'
            assert pg_page.add_link_button.is_clickable(), 'На кнопку Добавить ссылку нельзя нажать'
        with allure.step("Проверяем, что по умолчанию отображается один блок ссылок"):
            assert len(pg_page.link_blocks.get_items()) == 2, 'Блока не 2'
        with allure.step('Жмем на кнопку удалить ссылку'):
            while pg_page.delete_link_button.is_visible():
                pg_page.delete_link_button.click()
        with allure.step('Проверяем, что кнопка Удалить пропала'):
            assert pg_page.delete_link_button.is_not_visible(), 'Кнопка есть'
        with allure.step("Проверяем, что блок ссылки пропал"):
            assert pg_page.link_blocks.are_not_visible(), 'Блок есть'


    @allure.title("Проверяем отображение основных элементов на странице шага Product Guide / Форма файлов")
    def test_pg_step_check_file_form(self, pg_page):

        with allure.step("Жмем кнопку Добавить шаг"):
            pg_page.add_step_button.click()
        with allure.step("Проверяем корректное отображение формы файлов"):
            assert pg_page.add_files_block.is_visible(), 'Формы файлов нет'
        doc_name = '/UI/data/test_file.docx'
        doc_full_name = ROOT + doc_name
        pg_page.scroll_page_down(1000)
        with allure.step("Добавляем 2 файла в форму"):
            pg_page.add_file_form.input_file(doc_full_name)
            pg_page.add_file_form.input_file(doc_full_name)
        with allure.step('Проверяем, что файлы загрузились'):
            assert all(
                file.is_visible() for file in pg_page.chosen_files), 'Файлы не загрузились'
        with allure.step("Удаляем первый файл"):
            pg_page.delete_files_buttons[0].click()
        with allure.step("Проверяем, что остался один файл"):
            assert len(pg_page.chosen_files.get_items()) == 1, 'Файл не один'

    @allure.title("Проверяем отображение основных элементов на странице шага Product Guide / Блок условий")
    def test_pg_step_check_conditions_forms(self, pg_page):

        with allure.step("Жмем кнопку Добавить шаг"):
            pg_page.add_step_button.click()
        pg_page.scroll_page_down(1000)
        with allure.step("Проверяем отображение и работу каждой формы условий"):
            conditions = pg_page.conditions.get_items()
            for cond in conditions:
                with allure.step("Проверяем, что условие отображается"):
                    assert cond.is_visible(), 'Условия нет'
                with allure.step("Жмем на форму условия"):
                    cond.click()
                with allure.step("Проверяем, что появились значения"):
                    assert pg_page.conditions_values, 'Значений нет'
                current_len = len(pg_page.conditions_chosen_values.get_items())
                with allure.step("Выбираем первое значение"):
                    for value in pg_page.conditions_values[:1]:
                        value.click()
                with allure.step("Проверяем, что выбранное значение добавилось или удалилось"):
                    new_len = len(pg_page.conditions_chosen_values.get_items())
                    assert new_len + 1 == current_len or new_len - 1 == current_len, 'Значения не изменились'
                with allure.step("Закрываем условие"):
                    cond.click()

    @allure.title('Проверяем, что форма групп не пропадает в редактировании шага')
    @allure.issue('https://jira.mts.ru/browse/PPI-2527',
                  'PPinfo - Пропадает группа в условиях внутри редактирования шага')
    def test_check_group_field(self, pg_page):

        with allure.step("Жмем кнопку Добавить шаг"):
            pg_page.add_step_button.click()
        pg_page.add_name_to_step()
        pg_page.add_links_to_step(['123', '123'])
        pg_page.scroll_page_down(500)
        with allure.step('Жмем на кнопку Добавить'):
            pg_page.add_button_inside.click()
        with allure.step('Проверяем, что форма Группы не пропала'):
            assert pg_page.groups_field.is_visible(), 'Форма пропала'

    @allure.title('Отображение элементов на странице превью шага / Основное')
    def test_check_step_preview_menu(self, pg_page):
        pg_page.create_step()
        with allure.step('Проверяем, что мы попали на страницу превью шага'):
            assert pg_page.step_preview.is_visible(), 'Превью шага нет'
        with allure.step('Проверяем, что есть кнопки редактирования и добавления вложенного'):
            assert pg_page.edit_step_button.is_clickable(), 'Кнопки нет / кнопка некликабельная'
            assert pg_page.add_sub_action_button.is_clickable(), 'Кнопки нет / кнопка некликабельная'

        pg_page.delete_current_step()

    @allure.title('Отображение элементов на странице превью шага / Блок названия')
    def test_check_step_preview_name_block(self, pg_page):
        pg_page.create_step(description='про ве роч ка')
        with allure.step('Проверяем, что чипс с номером отображается'):
            assert pg_page.step_number_preview.is_visible(), 'чипса нет'
        with allure.step('Проверяем, что название отображается корректно'):
            assert pg_page.step_name_preview.is_visible(), 'Названия нет'
            assert pg_page.step_name_preview.get_text() == 'test_name', 'Название не то'
        with allure.step('Проверяем, что описание отображается корректно'):
            assert pg_page.step_description_preview.is_visible(), 'Названия нет'
            assert pg_page.step_description_preview.get_text() == 'про ве роч ка', 'Описание не то'

        pg_page.delete_current_step()

    @allure.title('Отображение элементов на странице превью шага / Метки')
    def test_check_step_preview_chips(self, pg_page):
        with allure.step('Жмем на кнопку Добавить шаг'):
            pg_page.add_step_button.click()
        with allure.step('Заполняем шаг'):
            pg_page.add_name_to_step()
            pg_page.change_required_step()
            pg_page.change_repeatable_step()
            with allure.step('Жмем на кнопку Добавить'):
                pg_page.add_button_inside.click()
        with allure.step('Проверяем наличие чипсов обязательности и повторяемости'):
            assert pg_page.step_required_chips_preview.is_visible(), 'Чипса обязательности нет'
            assert pg_page.step_repeatable_chips_preview.is_visible(), 'Чипса повторяемости нет'

        pg_page.delete_current_step()

    @allure.title('Отображение элементов на странице превью шага / Сотрудники')
    def test_check_step_preview_employees(self, pg_page):
        with allure.step('Жмем на кнопку Добавить шаг'):
            pg_page.add_step_button.click()
        with allure.step('Заполняем шаг'):
            pg_page.add_name_to_step()
            pg_page.add_users_to_step(amount=3)
            with allure.step('Жмем на кнопку Добавить'):
                pg_page.add_button_inside.click()
        with allure.step('Проверяем отображение всех сотрудников'):
            assert pg_page.step_employees_preview.count() == 3, 'Кол-во сотрудников не как при создании'
            assert all('иванов' in i.get_text().lower() for i in
                       pg_page.step_employees_preview), 'Добавился сотрудник не по заданному паттерну'

        pg_page.delete_current_step()

    @allure.title('Отображение элементов на странице превью шага / Ссылки')
    def test_check_step_preview_links(self, pg_page):
        with allure.step('Жмем на кнопку Добавить шаг'):
            pg_page.add_step_button.click()
        with allure.step('Заполняем шаг'):
            pg_page.add_name_to_step()
            pg_page.add_links_to_step()
            with allure.step('Жмем на кнопку Добавить'):
                pg_page.add_button_inside.click()
        with allure.step('Проверяем отображение ссылки'):
            assert pg_page.step_links_preview.count() == 1, 'Кол-во ссылок не как при создании'
            assert 'тестовая ссылка' in pg_page.step_links_preview[
                0].get_text(), 'Добавилась ссылка не по заданному паттерну'
            assert 'https://newportal.mts.ru/' in pg_page.step_links_preview[
                0].get_attribute('href'), 'Добавилась ссылка не по заданному паттерну'

        pg_page.delete_current_step()

    @allure.title('Отображение элементов на странице превью шага / Файлы')
    def test_check_step_preview_files(self, pg_page):
        with allure.step('Жмем на кнопку Добавить шаг'):
            pg_page.add_step_button.click()
        with allure.step('Заполняем шаг'):
            pg_page.add_name_to_step()
            pg_page.scroll_page_down(1000)
            pg_page.add_files_to_step(3)
            with allure.step('Жмем на кнопку Добавить'):
                pg_page.add_button_inside.click()
        with allure.step('Проверяем отображение файлов'):
            pg_page.wait_force(2)
            assert pg_page.step_files_preview.count() == 3, 'Кол-во файлов не как при создании'

        pg_page.delete_current_step()

    @allure.title('Вложенный шаги в админке / Отсутствие вложенных по умолчанию')
    def test_sub_action_admin_no_steps_default(self, pg_page):
        pg_page.create_step()
        with allure.step('Проверяем, что по умолчанию вложенных шагов нет'):
            assert pg_page.no_steps_text.is_visible(), 'Текста при отсутствии шагов нет'
            assert pg_page.steps.are_not_visible(), 'Вложенные шаги есть'

        pg_page.delete_current_step()

    @allure.title('Вложенный шаги в админке / Отсутствие условий и меток в добавлении вложенного шага')
    def test_sub_action_admin_no_elements(self, pg_page):
        pg_page.create_step()
        with allure.step('Жмем на кнопку Добавить вложенный'):
            pg_page.add_sub_action_button.click()
        with allure.step('Проверяем, что нет радиобаттонов повторяемости и обязательности'):
            # за счет того, что одинаковый локатор у всех кнопок, проверяем одним условием без использования индексации
            assert pg_page.step_required_radio_button.are_visible(), 'Кнопки есть'
        with allure.step('Проверяем, что нет блока условий'):
            assert pg_page.conditions_block.is_not_visible(), 'Блок есть'
            pg_page.go_back()

        pg_page.delete_current_step()

    @allure.title('Вложенный шаги в админке / Добавление вложенного шага')
    def test_sub_action_admin_add(self, pg_page):
        pg_page.create_step()
        [pg_page.create_sub_action(name=f'вложенный {i}') for i in range(2)]
        with allure.step('Проверяем, что 2 вложенных шага появились в таблице'):
            assert pg_page.steps.count() == 2, 'Шагов не 2'
            for i in range(2):
                assert pg_page.steps[i].get_text() == f'вложенный {i}', f'у {i + 1} шага название не то'

        pg_page.delete_current_step()

    @allure.title('Вложенный шаги в админке / Отображение в общей таблице')
    def test_sub_action_admin_table_sign(self, pg_page):
        pg_page.create_step()
        pg_page.create_sub_action(name=f'вложенный 1')
        with allure.step('Выходим на страницу шагов'):
            pg_page.side_groups[0].click()
        with allure.step('Проверяем, что у созданного шага есть отмеетка о наличии вложенных шагов'):
            assert 'Есть' in pg_page.rows_steps[-1].get_text(), 'Отметки нет'
        pg_page.steps[-1].click()

        pg_page.delete_current_step()

    @allure.title('Вложенный шаги в админке / Актуальная дата последнего обновления')
    def test_sub_action_admin_date(self, pg_page):
        pg_page.create_step()
        pg_page.create_sub_action(name=f'вложенный 1')
        with allure.step('Проверяем, что дата обновления шага актуальная'):
            assert datetime.now().strftime('%d.%m.%y') in pg_page.rows_steps[0].get_text(), 'Даты нет'

        pg_page.delete_current_step()

    @allure.title('Вложенный шаги в админке / Смена активности через тогл')
    def test_sub_action_admin_activity_change(self, pg_page):
        pg_page.create_step()
        pg_page.create_sub_action(name=f'вложенный 1', is_active=False)
        with allure.step('Жмем на тогл'):
            pg_page.activity_toggle.click()

        with allure.step('Проверяем, что тогл включен'):
            assert pg_page.activity_toggle.is_checked(), 'Тогл выключен'

        pg_page.delete_current_step()

    @allure.title('Вложенный шаги в админке / Возвращение к основному шагу')
    def test_sub_action_admin_get_back_to_main(self, pg_page):
        pg_page.create_step()
        pg_page.create_sub_action(name=f'вложенный 1', is_active=False)
        current_url = pg_page.url
        with allure.step('Переходим во вложенный шаг'):
            pg_page.steps[0].click()
        with allure.step('Проверяем, что кнопка возврата к главному шагу отображается корректно'):
            assert pg_page.to_details_button.is_visible(), 'Кнопки нет'
            assert pg_page.to_details_button.is_clickable(), 'Кнопка не кликабельная'
        with allure.step('Жмем на кнопку возврата'):
            pg_page.to_details_button.click()
        with allure.step('Проверяем, что мы вернулись на страницу превью'):
            assert pg_page.url == current_url, 'Мы вернулись не туда'

        pg_page.delete_current_step()
