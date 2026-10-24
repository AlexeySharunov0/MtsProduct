import allure
import pytest

from UI.data.assertions_data import ProductsAsserts as assertions
from UI.tests.productPage.conftest import projects_page, product_page


@pytest.mark.ui
@allure.feature("Вкладка Проекты")
class TestProjects:
    @allure.title("Проверка кликабельности и отображения таба Проекты у продукта с проектами")
    def test_project_tab_check(self, projects_page):
        with allure.step("Проверяем, что таб есть в боковом меню"):
            assert projects_page.project_tab.is_visible(), 'Таба нет в меню'
        with allure.step('Проверяем, что таб Документы кликабельный'):
            assert projects_page.project_tab.is_clickable(), 'Таб некликабельный'
        with allure.step("Проверяем, что таб отмечен как активный (черный)"):
            assert projects_page.project_tab.get_attribute('class') == 'content', 'Таб окрашен серым'

    @allure.title("Проверка кликабельности и отображения таба Проекты у продуктов без проектов")
    @pytest.mark.parametrize('projects_page', ['https://stage.prodboard.mts.ru/product/BI_20319/main'], indirect=True)
    def test_project_tab_check_empty(self, projects_page):
        with allure.step("Проверяем, что таб есть в боковом меню"):
            assert projects_page.project_tab.is_visible(), 'Таба нет в меню'
        with allure.step('Проверяем, что таб Документы кликабельный'):
            assert projects_page.project_tab.is_clickable(), 'Таб некликабельный'
        with allure.step("Проверяем, что таб отмечен как неактивный (серый)"):
            assert projects_page.project_tab.get_attribute('class') == 'content empty', 'Таб окрашен черным'

    @allure.title("Проверка заголовков на странице Проекты")
    def test_check_project_headers(self, projects_page):
        with allure.step("Проверяем, что заголовок страницы отображается корректно"):
            assert projects_page.project_header.is_visible(), 'Заголовка нет'
            assert projects_page.project_header.get_text() == 'Проекты', 'Текст заголовка не совпадает'
        with allure.step("Проверяем, что описание страницы отображается корректно"):
            assert projects_page.tab_description.is_visible(), 'Описания нет'
            assert projects_page.tab_description.get_text() == assertions.project_description, 'Текст описания не совпадает'

    @allure.title("Проверка корректного отображения таблицы Hyperion на странице продукта")
    def test_open_projects_hyperion(self, projects_page):
        with allure.step("Проверяем, что таблица Hyperion отображается по умолчанию"):
            projects_page.hyperion_tab_project_tab.click()
            assert projects_page.table_hype.is_visible(), 'Таблица не видна'

    @allure.title("Проверка корректного отображения таблицы проектов DaVinci на странице продукта")
    def test_open_projects_davinci(self, projects_page):
        with allure.step("Кликаем по таблице DaVinci"):
            projects_page.davinci_tab_project_tab.click()
        with allure.step("Проверяем, что вкладка выделилась"):
            assert projects_page.davinci_tab_project_tab.is_selected(), 'Вкладка не выделилась красным'
        with allure.step("Проверяем, что таблица DaVinci отображается"):
            assert projects_page.davinci_table.is_visible(), 'Таблица не видна'

    @allure.title("Проверка корректного отображения таблицы RMS на странице продукта")
    @pytest.mark.monitoring
    def test_open_projects_rms(self, projects_page):
        with allure.step("Кликаем по таблице RMS"):
            projects_page.rms_tab_project_tab.click()
        with allure.step("Проверяем, что вкладка выделилась"):
            assert projects_page.rms_tab_project_tab.is_selected(), 'Вкладка не выделилась красным'
        with allure.step("Проверяем, что таблица RMS отображается"):
            assert projects_page.table_rms.is_visible(), 'Таблица не видна'

    @allure.title("Проверка корректного отображения таблицы OEBS на странице продукта")
    @pytest.mark.xfail(reason='Ошибка на стороне OEBS которую не собираются править')
    def test_open_projects_oebs(self, projects_page):
        with allure.step("Кликаем по таблице OEBS"):
            projects_page.oebs_tab_project_tab.click()
        with allure.step("Проверяем, что вкладка выделилась"):
            assert projects_page.oebs_tab_project_tab.is_selected(), 'Вкладка не выделилась красным'
        with allure.step("Проверяем, что таблица OEBS отображается"):
            assert projects_page.table_oebs.is_visible(), 'Таблица не видна'

    @allure.title(
        "Проверка корректного отображения карточки уволенного сотрудника во вкладке 'Проекты' на странице продукта")
    @pytest.mark.skip(reason='Найти продукт с уволенным')
    def test_fired_owner_projects(self, product_page, projects_page):
        with allure.step('Кликаем по уволенному пользователю'):
            projects_page.hyperion_tab_project_tab.click()
            product_page.fired_user_sudakova.click()
        with allure.step("Проверяем, что пользователь уволен"):
            assert product_page.fired_status.is_visible(), 'Нет чипса "Уволен"'

    @allure.title("Проверка работы поиска на табе Проекты, Hyperion")
    def test_search_projects_hyperion(self, projects_page):
        projects_page.hyperion_tab_project_tab.click()
        with allure.step("Проверяем, что есть проект Гео..."):
            assert projects_page.project_first.is_visible(), 'Проекта нет'
        with allure.step("Вводим запрос в строку поиска"):
            projects_page.search_projects_hyperion.fill("Инжектор МТС")
        with allure.step("Проверяем результаты поиска"):
            assert projects_page.project_inzhector.is_visible(), 'Нужный проект не найден'
            assert projects_page.project_first.is_not_visible(), 'Найден лишний проект'

    @allure.title("Проверка работы поиска на табе Проекты, DaVinci")
    def test_search_projects_davinci(self, projects_page):
        with allure.step("Кликаем по таблице DaVinci"):
            projects_page.davinci_tab_project_tab.click()
        with allure.step("Проверяем, что есть проект 'новый проект'"):
            assert projects_page.project_new_project.is_visible(), 'Проекта нет'
        with allure.step("Вводим запрос в строку поиска"):
            projects_page.search_projects_davinci.fill("белиберда")
        with allure.step("Проверяем результаты поиска"):
            assert projects_page.project_new_project.is_not_visible(), 'Найден лишний проект'

    @allure.title("Проверка работы поиска на табе Проекты, RMS")
    def test_search_projects_rms(self, projects_page):
        with allure.step("Кликаем по таблице RMS"):
            projects_page.rms_tab_project_tab.click()
        with allure.step("Проверяем, что есть проект R04933"):
            assert projects_page.project_R04933.is_visible(), 'Проекта нет'
        with allure.step("Вводим запрос в строку поиска"):
            projects_page.search_projects_rms.fill("R05037")
        with allure.step("Проверяем результаты поиска"):
            assert projects_page.project_R05037.is_visible(), 'Нужный проект не найден'
            assert projects_page.project_R04933.is_not_visible(), 'Найден лишний проект'

    @allure.title("Нажатие на название возвращает к основной информации о текущем продукте (с таба проектов)")
    def test_name_returns_to_main_info_from_projects(self, product_page, projects_page):
        with allure.step("Кликаем на название продукта"):
            product_page.product_name.click()
        with allure.step("Проверяем, что мы вернулись на главную страницу продукта"):
            assert projects_page.project_header.is_not_visible(), 'Заголовок с Проекты остался'

    @allure.title("Нажатие на лого возвращает к основной информации о текущем продукте (с таба проектов)")
    def test_logo_returns_to_main_info_from_projects(self, product_page, projects_page):
        with allure.step("Кликаем на лого продукта"):
            product_page.product_logo.click()
        with allure.step("Проверяем, что мы вернулись на главную страницу продукта"):
            assert projects_page.project_header.is_not_visible(), 'Заголовок с Проекты остался'

    @allure.title('Проверка кнопки Запустить легкий старт на странице DaVinci Внутреннего продукта')
    @pytest.mark.parametrize('projects_page', ['https://stage.prodboard.mts.ru/product/BI_1561/projects'],
                             indirect=True)
    def test_davinci_easy_start_button_internal(self, projects_page):
        with allure.step('Кликаем на Запустить легкий старт'):
            projects_page.davinci_easy_start_button.click()

        with allure.step('Проверяем ссылку итоговой страницы'):
            assert 'https://davinci.mts.ru/projects/create/inner-mvp' == projects_page.davinci_easy_start_button.get_attribute(
                'href'
            ), f'Ссылка итоговой страницы неверная: {projects_page.davinci_easy_start_button.get_attribute("href")}'

    @allure.title('Проверка кнопки Запустить легкий старт на странице DaVinci Внешнего продукта')
    def test_davinci_easy_start_button_external(self, projects_page):
        with allure.step('Кликаем на Запустить легкий старт'):
            projects_page.davinci_easy_start_button.click()

        with allure.step('Проверяем ссылку итоговой страницы'):
            assert 'https://davinci.mts.ru/projects/create/mvp' == projects_page.davinci_easy_start_button.get_attribute(
                'href'
            ), f'Ссылка итоговой страницы неверная: {projects_page.davinci_easy_start_button.get_attribute("href")}'

    @allure.title('Проверка кнопки Начать защиту инвестиций по продукту на странице DaVinci')
    @pytest.mark.parametrize('projects_page', ['https://stage.prodboard.mts.ru/product/BI_1561/projects'],
                             indirect=True)
    def test_davinci_protect_investments_button(self, projects_page):
        with allure.step('Кликаем на Начать защиту инвестиций по продукту'):
            projects_page.davinci_protect_investments.click()

        with allure.step('Проверяем ссылку итоговой страницы'):
            assert 'https://davinci.mts.ru/projects/create/invest-product/' == projects_page.davinci_protect_investments.get_attribute(
                'href'
            ), f'Ссылка итоговой страницы неверная: {projects_page.davinci_protect_investments.__getattribute__("href")}'

    @allure.title('Проверка кнопки Создать проект на странице RMS')
    @pytest.mark.parametrize('projects_page', ['https://stage.prodboard.mts.ru/product/BI_1561/projects'],
                             indirect=True)
    def test_rms_create_project_button(self, projects_page):
        with allure.step('Кликаем на Создать проект'):
            projects_page.rms_tab_project_tab.click()
            projects_page.rms_create_project.click()

        with ((allure.step('Проверяем ссылку итоговой страницы'))):
            assert 'https://rms.mtsit.com/requests/projects/create' == projects_page.rms_create_project.get_attribute(
                'href'
            ), f'Ссылка итоговой страницы неверная: {projects_page.rms_create_project.get_attribute("href")}'
