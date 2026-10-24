import allure
import pytest

from UI.tests.main_page.conftest import main_page, user_main_page


@pytest.mark.ui
@allure.feature("Главная страница")
class TestNavigation:

    @allure.title("Отображение карточек добавления продуктов")
    def test_page_add_product(self, main_page):
        main_page.add_product.click()
        with allure.step('Проверяем, что карточки добавления отображены'):
            assert all(i.is_visible() for i in main_page.add_cards), 'Карточки не отображены'
        with allure.step('Проверяем, что кнопки добавления отображены и кликабельны'):
            assert all(i.is_clickable() for i in main_page.add_cards_buttons), 'Кнопки не кликабельны'
            assert all(i.is_visible() for i in main_page.add_cards_buttons), 'Кнопки не отображены'
        with allure.step('Проверяем, что ссылки на примеры отображены и кликабельны'):
            assert all(i.is_clickable() for i in main_page.add_cards_links), 'Ссылки не кликабельны'
            assert all(i.is_visible() for i in main_page.add_cards_links), 'Ссылки не отображены'

    @allure.title('Скачивание Excel / Админ')
    def test_excel_admin(self, main_page):
        with allure.step('Проверяем кнопку Скачать Excel'):
            assert main_page.excel.is_visible(), 'Кнопки нет'
            assert main_page.excel.is_clickable(), 'На кнопку нельзя нажать'
        with allure.step('Кликаем "Скачать Exel"'):
            main_page.excel.click()
        with allure.step('Проверяем элементы выпадашки'):
            assert all(i.is_clickable() for i in main_page.excel_variants), 'На некоторые элементы нельзя нажать'
            count_of_menu_items = 10
            assert len(main_page.excel_variants.get_items()) == count_of_menu_items, 'Вариантов Excel не 7'

    @allure.title("Скачивание Excel на одну дату / Проверка элементов")
    def test_excel_on_one_date_elements(self, main_page):
        with allure.step('Кликаем "Скачать Exel"'):
            main_page.excel.click()
        with allure.step('Выбираем "...на одну дату"'):
            main_page.excel_load_one_date.click()
        with allure.step('Проверяем, что появилось модальное окно'):
            assert main_page.excel_modal_window.is_visible(), 'Модальное окно не появилось'
        with allure.step('Проверяем, что есть поле выбора даты'):
            assert main_page.datapicker_one_date.is_visible(), 'Поля выбора даты нет'
        required_attributes = main_page.all_attributes_excel.get_items()[:4]
        with allure.step('Проверяем, что все обязательные атрибуты предвключены и их нельзя модифицировать'):
            assert required_attributes, 'Обязательных атрибутов нет'
            assert all(i.is_checked() for i in required_attributes), 'Обязательные атрибуты не включены по умолчанию'
            assert all(i.is_disabled() for i in required_attributes), 'Обязательные атрибуты можно выключить'
        with allure.step('Проверяем необязательные атрибуты'):
            other_attrs = main_page.all_attributes_excel.get_items()[4:]
            assert other_attrs, 'небязательных атрибутов нет'
            assert all(i.is_not_checked() for i in other_attrs), 'Необязательные атрибуты включены по умолчанию'
        with allure.step('Жмем кнопку Выбрать все'):
            main_page.choose_all_button.click()
            main_page.datapicker_one_date.click()
            main_page.datapicker_one_date.press_key('ArrowLeft')
        with allure.step('Проверяем, что все элементы выбрались'):
            assert main_page.all_attributes_excel.get_items()[4:], 'небязательных атрибутов нет'
            assert all(i.is_checked() for i in main_page.all_attributes_excel.get_items()[4:]), 'Атрибуты не выбрались'
        with allure.step('Проверяем кнопку скачивания'):
            assert main_page.download.is_visible(), 'Кнопки нет'
            assert main_page.download.is_clickable(), 'На кнопку нельзя нажать'

    @allure.title("Скачивание Excel на одну дату / Общая проверка работы")
    def test_excel_on_one_date_general(self, main_page):
        with allure.step('Кликаем "Скачать Exel"'):
            main_page.excel.click()
        with allure.step('Выбираем "...на одну дату"'):
            main_page.excel_load_one_date.click()
        with allure.step('В модальном окне выбираем дату'):
            main_page.datapicker_one_date.click()
            main_page.datapicker_one_date.press_key('ArrowLeft')
        with allure.step('Кликаем на "Скачать"'):
            main_page.download.click()
        with allure.step('Проверяем, что осталось модальное окно'):
            assert main_page.excel_modal_window.is_visible(), 'Модальное окно не осталось'

    @allure.title("Скачивание Excel на период / Проверка элементов")
    def test_excel_on_period_elements(self, main_page):
        with allure.step('Кликаем "Скачать Exel"'):
            main_page.excel.click()
        with allure.step('Выбираем "...на период"'):
            main_page.excel_load_period.click()
        with allure.step('Проверяем, что появилось модальное окно'):
            assert main_page.excel_modal_window.is_visible(), 'Модальное окно не появилось'
        with allure.step('Проверяем, что есть поле выбора даты'):
            assert main_page.datapicker_period_begin.is_visible(), 'Поля выбора даты нет'
            assert main_page.datapicker_period_end.is_visible(), 'Поля выбора даты нет'
        required_attributes = main_page.all_attributes_excel.get_items()[:4]
        with allure.step('Проверяем, что все обязательные атрибуты предвключены и их нельзя модифицировать'):
            assert required_attributes, 'Обязательных атрибутов нет'
            assert all(i.is_checked() for i in required_attributes), 'Обязательные атрибуты не включены по умолчанию'
            assert all(i.is_disabled() for i in required_attributes), 'Обязательные атрибуты можно выключить'
        with allure.step('Проверяем необязательные атрибуты'):
            other_attrs = main_page.all_attributes_excel.get_items()[4:]
            assert other_attrs, 'небязательных атрибутов нет'
            assert all(i.is_not_checked() for i in other_attrs), 'Необязательные атрибуты включены по умолчанию'
        with allure.step('Жмем кнопку Выбрать все'):
            main_page.choose_all_button.click()
        with allure.step('Проверяем, что все элементы выбрались'):
            assert main_page.other_attributes_excel, 'небязательных атрибутов нет'
            assert all(i.is_checked() for i in main_page.all_attributes_excel.get_items()[4:]), 'Атрибуты не выбрались'
        with allure.step('Проверяем кнопку скачивания'):
            assert main_page.download.is_visible(), 'Кнопки нет'
            assert main_page.download.is_clickable(), 'На кнопку нельзя нажать'

    @allure.title("Скачивание Excel на период / Общая проверка работы")
    def test_excel_on_period_general(self, main_page):
        with allure.step('Кликаем "Скачать Exel"'):
            main_page.excel.click()
        with allure.step('Выбираем "...на период"'):
            main_page.excel_load_period.click()
        with allure.step('В модальном окне выбираем даты'):
            main_page.datapicker_period_begin.click()
            main_page.datapicker_period_begin.press_key('ArrowLeft')
            main_page.datapicker_period_end.click()
            main_page.datapicker_period_end.press_key('ArrowRight')
        with allure.step('Кликаем на "Скачать"'):
            main_page.download.click()
        with allure.step('Проверяем, что осталось модальное окно'):
            assert main_page.excel_modal_window.is_visible(), 'Модальное окно не осталось'

    @allure.title("Скачивание Excel на период / Попытка скачать без задания даты")
    @pytest.mark.parametrize('date_type', ['right', 'left', 'none'])
    def test_excel_on_period_no_date(self, main_page, date_type):
        with allure.step('Кликаем "Скачать Exel"'):
            main_page.excel.click()
        with allure.step('Выбираем "...на период"'):
            main_page.excel_load_period.click()
        if date_type == 'left':
            with allure.step('Выбираем только дату начала'):
                main_page.datapicker_period_begin.click()
                main_page.datapicker_period_begin.press_key('ArrowLeft')
        elif date_type == 'right':
            main_page.datapicker_period_end.click()
            main_page.datapicker_period_end.press_key('ArrowRight')
        with allure.step('Кликаем на "Скачать"'):
            main_page.download.click()
        with allure.step('Проверяем, что появился аллерт, что нужно выбрать дату'):
            assert main_page.alert_dates.is_visible(), 'Аллерт не появился'

    @allure.title("Скачивание Excel Продукты")
    def test_excel_all(self, main_page):
        with allure.step('Кликаем "Скачать Exel"'):
            main_page.excel.click()
        href = main_page.excel_load_all.get_attribute("href")
        with allure.step('Проверяем, что ссылка на скачивание соответствует ожидаемой'):
            assert href == '/ppinfo/api/v1/product/list/xlsx/general', 'Урл не соответствует ожидаемому'

    @allure.title("Скачивание Excel Все документы")
    def test_excel_docs(self, main_page):
        with allure.step('Кликаем "Скачать Exel"'):
            main_page.excel.click()
        href = main_page.excel_load_all_docs.get_attribute("href")
        with allure.step('Проверяем, что ссылка на скачивание соответствует ожидаемой'):
            assert href == '/ppinfo/api/v1/product/document/xlsx', 'Урл не соответствует ожидаемому'

    @allure.title(f"Кнопка на скачивание эксель Изменение атрибутов отображена админам")
    @allure.issue('https://jira.mts.ru/browse/PPI-438', 'PPInfo - Выгрузка Excel с датами изменения атрибутов')
    def test_excel_update_attr(self, main_page):
        with allure.step('Кликаем на кнопку Excel'):
            main_page.excel.click()
        with allure.step('Кнопка иксель изменение атрибутов на месте и отображается админам'):
            assert main_page.excel_update_attr.is_visible(), 'Кнопка иксель изменение атрибутов не отображена админам'

    @allure.title(f"Ссылка на скачивание эксель Изменение атрибутов не отображены пользователям")
    @allure.issue('https://jira.mts.ru/browse/PPI-438', 'PPInfo - Выгрузка Excel с датами изменения атрибутов')
    def test_excel_update_attr_users(self, user_main_page):
        with allure.step('Кликаем на кнопку Excel'):
            user_main_page.excel.click()
        with allure.step('Кнопка иксель изменение атрибутов не отображается обычным пользователям'):
            assert user_main_page.excel_update_attr.is_not_visible(), 'Кнопка иксель изменение атрибутов отображена обычным пользователям'

    @allure.title(f"Ссылка на скачивание эксель Все прикрепленные документы не отображены пользователям")
    def test_excel_all_docs_users(self, user_main_page):
        with allure.step('Кликаем на кнопку Excel'):
            user_main_page.excel.click()
        with allure.step('Кнопка иксель Все прикрепленные документы не отображается обычным пользователям'):
            assert user_main_page.excel_load_all_docs.is_not_visible(), 'Кнопка иксель Все прикрепленные документы отображена обычным пользователям'

    @allure.title(f"Ссылка на скачивание эксель Проверка кластера не отображены пользователям")
    def test_excel_cluster_users(self, user_main_page):
        with allure.step('Кликаем на кнопку Excel'):
            user_main_page.excel.click()
        with allure.step('Кнопка иксель Проверка кластера не отображается обычным пользователям'):
            assert user_main_page.excel_cluster.is_not_visible(), 'Кнопка иксель Проверка кластера отображена обычным пользователям'
