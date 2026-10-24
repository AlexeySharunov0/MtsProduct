import allure
import pytest

from UI.data.assertions_data import ProductsAsserts as assertions
from UI.tests.productPage.conftest import techno_page


@pytest.mark.ui
@allure.feature("Вкладка Технический состав")
class TestSoftware:
    @allure.title("Проверка кликабельности и отображения таба Технический состав у продуктов с ПО")
    def test_software_tab_check(self, techno_page):
        with allure.step("Проверяем, что таб есть в боковом меню"):
            assert techno_page.software_tab.is_visible(), 'Таба нет в меню'
        with allure.step('Проверяем, что таб Технический состав кликабельный'):
            assert techno_page.software_tab.is_clickable(), 'Таб некликабельный'
        with allure.step("Проверяем, что таб отмечен как активный (черный)"):
            techno_page.wait_force(1)
            assert techno_page.software_tab.get_attribute('class') == 'content', 'Таб окрашен серым'

    @allure.title("Проверка кликабельности и отображения таба Технический состав у продуктов без ПО")
    @pytest.mark.parametrize('techno_page', ['https://stage.prodboard.mts.ru/product/BI_20319/main'], indirect=True)
    def test_software_tab_check_empty(self, techno_page):
        with allure.step("Проверяем, что таб есть в боковом меню"):
            assert techno_page.software_tab.is_visible(), 'Таба нет в меню'
        with allure.step('Проверяем, что таб Технический состав кликабельный'):
            assert techno_page.software_tab.is_clickable(), 'Таб некликабельный'
        with allure.step("Проверяем, что таб отмечен как неактивный (серый)"):
            assert techno_page.software_tab.get_attribute('class') == 'content empty', 'Таб окрашен черным'

    @allure.title("Проверка заголовков на странице Технический состав")
    def test_check_software_headers(self, techno_page):
        with allure.step("Проверяем, что заголовок страницы отображается корректно"):
            assert techno_page.software_header.is_visible(), 'Заголовка нет'
            assert 'Приложения и системы' in techno_page.software_header.get_text(), 'Текст заголовка не совпадает'
        with allure.step("Проверяем, что описание страницы отображается корректно"):
            assert techno_page.tab_description.is_visible(), 'Описания нет'
            assert techno_page.tab_description.get_text() == assertions.software_description, 'Текст описания не совпадает'

    @allure.title("Проверка текста при отсутствии ПО на вкладке Технический состав")
    @pytest.mark.parametrize('techno_page', ['https://stage.prodboard.mts.ru/product/BI_20319/software'], indirect=True)
    def test_check_text_software_no_po(self, techno_page):
        with allure.step("Проверяем, что текст при отсутствии ПО отображается корректно"):
            assert techno_page.techno_none.is_visible(), 'Заголовка нет'
            assert techno_page.techno_none.get_text() == assertions.software_error, 'Текст не совпадает'

    @allure.title("Проверка отображения блока контент в табе Технический состав")
    def test_software_tab_content(self, techno_page):
        with allure.step("Проверяем, что блок контента слева отображается"):
            assert techno_page.software_content.is_visible(), 'Блока руководство нет'

    @allure.title("Проверка работы стрелочек на табе Технический состав")
    @pytest.mark.parametrize('techno_page', ['https://stage.prodboard.mts.ru/product/BI_43/software'], indirect=True)
    def test_arrows_software(self, techno_page):
        with allure.step('Кликаем на первую стрелочку в техно продуктах'):
            techno_page.software_opening[0].click()
        with allure.step('Проверяем, что содержимое первого продукта появилось'):
            assert techno_page.software_info_inside.is_visible(), 'Содержимого нет'
        with allure.step('Кликаем на первую стрелочку в техно продуктах'):
            techno_page.software_opening[0].click()
        with allure.step('Проверяем, что содержимое первого продукта пропало'):
            assert techno_page.software_info_inside.is_not_visible(), 'Содержимого нет'

    @allure.title("Проверка работы нераскрывающихся стрелочек на табе Технический состав")
    def test_empty_arrows_software(self, techno_page):
        with allure.step('Проверяем, что содержимое первого продукта не появилось'):
            assert techno_page.software_empty_product.is_visible(), 'Надписи о том, что продукт пустой нет'
            assert techno_page.software_info_inside.is_not_visible(), 'Контент продукта появился'

    @allure.title('Проверка отображения столбцов в содержимом техно продукта в Техническом составе')
    @pytest.mark.parametrize('techno_page', ['https://stage.prodboard.mts.ru/product/BI_42/software'], indirect=True)
    def test_columns_in_sw(self, techno_page):
        with allure.step('Кликаем на вторую стрелочку в техно продуктах'):
            techno_page.software_opening[0].click()
        with allure.step('Проверяем корректность отображения столбца ИС'):
            assert techno_page.inf_system_column.is_visible(), 'Столбца ИС нет'
        with allure.step('Проверяем корректность отображения столбца Статус'):
            assert techno_page.status_column.is_visible(), 'Столбца Статус нет'
        with allure.step('Проверяем корректность отображения столбца Команда'):
            assert techno_page.team_column.is_visible(), 'Столбца Команда нет'

    @allure.title('Столбец Класса Критичности в ИС')
    @allure.issue('https://jira.mts.ru/browse/PPI-1760', 'PPInfo - Вывести класс критичности ИС')
    @pytest.mark.parametrize('techno_page', ['https://stage.prodboard.mts.ru/product/BI_42/software'], indirect=True)
    def test_critical_class_in_sw(self, techno_page):
        with allure.step('Кликаем на вторую стрелочку в техно продуктах'):
            techno_page.software_opening[0].click()
        with allure.step('Проверяем корректность отображения столбца Класс критичности'):
            assert techno_page.cc_column.is_visible(), 'Нет столбца Класса критичности'
            assert techno_page.cc_column_value.get_text() == 'Mission-critical', 'Нет значения в столбце Класс критичности '

    @allure.title("Нажатие на название возвращает к основной информации о текущем продукте (с таба тех состав)")
    def test_name_returns_to_main_info_from_software(self, product_page, techno_page):
        with allure.step("Кликаем на название продукта"):
            product_page.product_name.click()
        with allure.step("Проверяем, что мы вернулись на главную страницу продукта"):
            assert techno_page.software_header.is_not_visible(), 'Заголовок с Тех состав остался'

    @allure.title("Нажатие на лого возвращает к основной информации о текущем продукте (с таба тех состава)")
    def test_logo_returns_to_main_info_from_software(self, product_page, techno_page):
        with allure.step("Кликаем на лого продукта"):
            product_page.product_logo.click()
        with allure.step("Проверяем, что мы вернулись на главную страницу продукта"):
            assert techno_page.software_header.is_not_visible(), 'Заголовок с Тех состав остался'

    @allure.title('Проверка кнопки Добавить приложение в ArchOps')
    def test_archops_add_button(self, techno_page):
        with allure.step('Кликаем на Добавить приложение в ArchOps'):
            techno_page.archops_add.click()
        with ((allure.step('Проверяем ссылку итоговой страницы'))):
            assert 'https://archops.pages.mts.ru/archops-docs/ru/docs/tasks/upload-app/' == techno_page.archops_add.get_attribute(
                'href'
            ), f'Ссылка итоговой страницы неверная: {techno_page.archops_add.get_attribute("href")}'

    @allure.title('Проверка кнопки Создать систему IMS')
    def test_ims_create_system_button(self, techno_page):
        with allure.step('Кликаем на Создать систему IMS'):
            techno_page.ims_create_system.click()

        with ((allure.step('Проверяем ссылку итоговой страницы'))):
            assert 'https://ims.mts.ru/systems/add' == techno_page.ims_create_system.get_attribute(
                'href'
            ), f'Ссылка итоговой страницы неверная: {techno_page.ims_create_system.get_attribute("href")}'

    @allure.title('Кнопки Тех учетки')
    @allure.issue('https://jira.mts.ru/browse/PPI-4148', 'PPInfo - Отображение ТУЗ ИС продукта')
    def test_tech_users_buttons(self, techno_page):
        techno_page.software_opening[-1].click()
        assert techno_page.tech_users_button.are_visible(), 'Нет кнопки Тех учетки'
        assert techno_page.tech_users_button.get_attributes('href') == [
            'https://ims.mts.ru/system-accounts?systemId=638e5c53-4f48-45d6-a7bf-f707d27e3433',
            'https://ims.mts.ru/system-accounts?systemId=03289f94-7d0f-4b74-ab9c-330844543eef',
            'https://ims.mts.ru/system-accounts?systemId=9c9a33d7-c5ef-4921-a59e-b922f37684bb'], 'Неверная ссылка на Тех учетки'
