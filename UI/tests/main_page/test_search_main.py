import allure
import pytest

import UI.data.assertions_data as assertions
from UI.tests.main_page.conftest import main_page
from UI.utils.EnvProvider import EnvProvider


@pytest.mark.ui
@pytest.mark.external
@pytest.mark.search
@pytest.mark.mainpage
@allure.feature("Поиск")
class TestSearchMainPage:

    @allure.title("Поиск с валидным названием продукта на вкладке внешние")
    @pytest.mark.parametrize("product_title", assertions.ProductsAsserts.productName)
    @pytest.mark.monitoring
    @pytest.mark.availability
    def test_search_normal(self, product_title, main_page):
        main_page.execute_search_main(product_title)
        main_page.product_name_chip_on_search_results.click()
        with allure.step('Проверяем что поиск дал результаты'):
            assert main_page.product_title.is_visible(), f"Product {product_title} title is invisible"
        with allure.step('Проверяем что искомый продукт найден по названию'):
            assert product_title in main_page.product_title.get_text(), \
                f"Product {product_title} title is not the same with {main_page.product_title.get_text()}"

    @allure.title("Поиск с частичным названием продукта на вкладке внешние")
    @pytest.mark.parametrize("rusSearchPattern,productName", assertions.ProductsAsserts.rusSearchPattern_to_productName)
    def test_search_part(self, rusSearchPattern, productName, main_page):
        main_page.execute_search_main(rusSearchPattern)
        main_page.product_name_chip_on_search_results.click()
        products_titles = main_page.products_titles.get_texts()
        with allure.step('Проверяем что искомый продукт найден по части названия'):
            assert productName in products_titles, f'Products list for search "{rusSearchPattern} should contains {productName}"'

    @allure.title("Поиск английскими буквами на вкрадке внешние")
    @pytest.mark.parametrize("engSearchPattern,productName", assertions.ProductsAsserts.engSearchPattern_to_productName)
    def test_search_eng(self, engSearchPattern, productName, main_page):
        main_page.execute_search_main(engSearchPattern)
        main_page.product_name_chip_on_search_results.click()
        products_titles = main_page.products_titles.get_texts()
        with allure.step('Проверяем что искомый продукт найден по названию с неправильной раскладкой'):
            assert productName in products_titles, f'Products list for search "{engSearchPattern} should contains {productName}"'

    @allure.title("Поиск по оракл id продукта на вкрадке внешние")
    @pytest.mark.parametrize("oracleID,productName", assertions.ProductsAsserts.oracleID_to_productName)
    def test_search_oracle(self, oracleID, productName, main_page):
        main_page.execute_search_main(oracleID)
        main_page.oracle_chip_on_search_results.click()
        text = main_page.product_title.get_text()
        with allure.step('Проверяем что искомый продукт найден по коду oracle'):
            assert text == productName, \
                f"For oracle oracleID {oracleID} didn't found product {productName}"

    @allure.title("Поиск по старому названию на вкрадке внешние")
    @pytest.mark.parametrize("old_name,productName", assertions.ProductsAsserts.Old_name_to_new)
    def test_search_old_name(self, old_name, productName, main_page):
        main_page.execute_search_main(old_name)
        text = main_page.all_product_title.get_texts()
        with allure.step('Проверяем что искомый продукт найден по старому названию'):
            assert productName in text, \
                f"For old name {old_name} didn't found product {productName}"

    @allure.title("Поиск по витрине на вкрадке внешние")
    @pytest.mark.parametrize("showcase, productName", assertions.ProductsAsserts.showcase)
    def test_search_showcase(self, showcase, productName, main_page):
        main_page.execute_search_main(showcase)
        main_page.showcase_name_chip_on_search_results.click()
        text = main_page.all_product_title.get_texts()
        with allure.step('Проверяем что искомый продукт найден по витрине'):
            assert productName in text, \
                f"For old name {showcase} didn't found product {productName}"

    @allure.title("Проверка ссылки на продукт на вкладке внешние")
    @pytest.mark.parametrize("ID, category, productName", assertions.ProductsAsserts.ID_to_category_to_productName)
    def test_link_to_product(self, ID, category, productName, main_page):
        main_page.execute_search_main(productName)
        with allure.step('Переходим на страницу первого продукта'):
            main_page.products[0].click()
        with allure.step('Проверяем что урл продукта соответствует ожидаемому'):
            link = main_page.url
            expected = EnvProvider.getBaseUrl() + f'/product/{ID}/main'
            assert link == expected, f"Link : '{link}' to the product '{productName}' is mismatch to the expected: '{expected}'"

    @allure.title("Поиск по ФИО владельца продукта на вкрадке внешние")
    @pytest.mark.parametrize("FIO, productList", assertions.ProductsAsserts.FIO_to_productList)
    @pytest.mark.monitoring
    @pytest.mark.availability
    def test_search_FIO(self, FIO, productList, main_page):
        main_page.execute_search_main(FIO)
        main_page.fio_chip_on_search_results.click()
        got_products = main_page.products_titles.get_texts()
        with allure.step('Проверяем что поиск отработал корректно'):
            assert set(productList).issubset(set(got_products)), \
                f"Expected {productList} to be in products list {got_products} for FIO: {FIO}"

    @allure.title("Поиск по названию атомарного на вкрадке внешние")
    @pytest.mark.parametrize("product", assertions.ProductsAsserts.atomicProducts)
    @pytest.mark.monitoring
    def test_search_atomic(self, product, main_page):
        main_page.execute_search_main(product)
        with allure.step('Проверяем что искомый продукт найден по коду названию атомарного продукта'):
            assert product in main_page.products_titles.get_texts(), \
                f"Product {product} title is not the same\
             with {main_page.product_title.get_text()} "

    @allure.title("Поиск по коду BI на вкрадке внешние")
    @pytest.mark.parametrize("code, product", assertions.ProductsAsserts.BI_to_productList)
    @pytest.mark.monitoring
    def test_search_BI(self, code, product, main_page):
        main_page.execute_search_main(code)
        main_page.bi_code_chip_on_search_results.click()
        text = main_page.product_title.get_text()
        with allure.step('Проверяем что искомый продукт найден по коду BI'):
            assert text == product, \
                f"For oracle BI code {code} didn't found product {product}"

    @allure.title("Поиск по коду без BI на вкрадке внешние")
    @pytest.mark.parametrize("code, product", assertions.ProductsAsserts.code_bi_to_productList)
    @pytest.mark.monitoring
    def test_search_code_BI(self, code, product, main_page):
        main_page.execute_search_main(code)
        main_page.bi_code_chip_on_search_results.click()
        text = main_page.product_title.get_text()
        with allure.step('Проверяем что искомый продукт найден по коду BI'):
            assert text == product, \
                f"For oracle BI code {code} didn't found product {product}"

    @allure.title("Поиск по приложению")
    @pytest.mark.parametrize("app, product", [('SSO mobile', 'МТС Умный дом'), ('PRO.501', 'МТС Умный дом'),
                                              ('PRO501', 'МТС Умный дом')])
    @pytest.mark.monitoring
    def test_search_app(self, app, product, main_page):
        main_page.execute_search_main(app)
        main_page.app_chip_on_search_results.click()
        text = main_page.product_title.get_text()
        with allure.step('Проверяем что искомый продукт найден по коду BI'):
            assert text == product, \
                f"For oracle BI code {app} didn't found product {product}"

    @allure.title("Поиск по системе")
    @allure.issue('https://jira.mts.ru/browse/PPI-4498', 'PPInfo - Поиск продукта по названию, команде поддержки ИС')
    @pytest.mark.parametrize("system, product", [('mts-cb-dev', 'МТС Cashback'), ('mts-cb', 'МТС Cashback'),
                                                 ('cb-dev', 'МТС Cashback'), ('C/PRM', 'МТС Cashback')])
    @pytest.mark.monitoring
    def test_search_system(self, system, product, main_page):
        main_page.execute_search_main(system)
        main_page.system_chip_on_search_results.click()
        text = main_page.product_title.get_text()
        with allure.step('Проверяем что искомый продукт найден по коду BI'):
            assert text == product, \
                f"For oracle BI code {system} didn't found product {product}"

    @allure.title("Поиск по Команде поддержки ИС")
    @allure.issue('https://jira.mts.ru/browse/PPI-4498', 'PPInfo - Поиск продукта по названию, команде поддержки ИС')
    @pytest.mark.parametrize("help_team_is, product", [('КЦ ИТ Поддержка МТС Cashback', 'МТС Cashback'),
                                                       ('BIM Virtual Group', 'МТС Тестировани')])
    @pytest.mark.monitoring
    def test_search_help_team_is(self, help_team_is, product, main_page):
        main_page.execute_search_main(help_team_is)
        main_page.help_team_is_chip_on_search_results.click()
        text = main_page.product_title.get_text()
        with allure.step('Проверяем что искомый продукт найден по коду BI'):
            assert text == product, \
                f"For oracle BI code {help_team_is} didn't found product {product}"

    @allure.title("Поиск по Тегам")
    @pytest.mark.parametrize("pattern, product",
                             [('Боксер', 'МТС Cashback'),
                              ('френч', 'МТС Cashback'),
                              ('такса', 'МТС Cashback')]
                             )
    @pytest.mark.monitoring
    def test_search_tags(self, pattern, product, main_page):
        main_page.execute_search_main(pattern)
        main_page.tags_chip_on_search_results.click()
        text = main_page.product_title.get_text()
        with allure.step('Проверяем что искомый продукт найден по коду BI'):
            assert text == product, \
                f"For oracle BI code {pattern} didn't found product {product}"

    @allure.title('Имя сотрудника на карточке отображается корректно на вкрадке внешние')
    def test_owner_name_in_card(self, main_page):
        names = main_page.ownerName.get_texts()
        assert 'Сотрудник не' not in names

    @allure.title("В поиске у хабов отображается тип Хаб")
    @allure.issue('https://jira.mts.ru/browse/PPI-3674',
                  'PPInfo - Отображать в поиске у хабов текст "Хаб"')
    def test_search_hub(self, main_page):
        main_page.execute_search_main('Хаб')
        main_page.product_name_chip_on_search_results.click()
        assert main_page.product_type_on_cards[0].get_text().replace('\xa0', '') == 'Хаб'

    @allure.title("'Показать все' в подсказках")
    @allure.issue('https://jira.mts.ru/browse/PPI-4520','PPInfo - Поиск: показать все результаты (после всех подсказок)')
    def test_suggestion_check_all(self, main_page):
        with allure.step('Кликаем на строку поиска'):
            main_page.search_str_closed.click()
        with allure.step(f'Вводим слово по которому нужно осуществить поиск -  МТС'):
            main_page.search_str.fill('МТС')
            assert main_page.check_all_in_search.is_visible(), 'Кнопка "Показать все" не отображается'

    @allure.title("Поиск по коду сервиса")
    @allure.issue("https://jira.mts.ru/browse/PPI-3819", "PPInfo - Поиск продукта по коду и названию сервиса")
    @pytest.mark.parametrize("service_code", ["SBS.2111", "SBS.2112"])
    def test_search_by_service_code(self, service_code, main_page):
        with allure.step(f"Вводим код '{service_code}' в поле поиска"):
            main_page.execute_search_main(service_code)

        with allure.step("Ждём, пока результаты загрузятся"):
            assert main_page.products.are_visible(), "Результаты поиска не загрузились"

        with allure.step("Проверяем, что наш продукт присутствует в результатах"):
            product_titles = main_page.products.get_texts()
            assert any("Apple Music" in title for title in product_titles), \
                f"Продукт с кодом сервиса '{service_code}' не найден в результатах"

    @allure.title("Поиск по полному названию сервиса")
    @allure.issue("https://jira.mts.ru/browse/PPI-3819", "PPInfo - Поиск продукта по коду и названию сервиса")
    @pytest.mark.parametrize("full_name", ["[Инфраструктура] Apple Music", "[Временный] Apple Music"])
    def test_search_by_service_full_name(self, full_name, main_page):
        with allure.step(f"Вводим '{full_name}' в поле поиска"):
            main_page.execute_search_main(full_name)

        with allure.step("Ждём, пока результаты загрузятся"):
            assert main_page.products.are_visible(), "Результаты поиска не загрузились"

        with allure.step("Проверяем, что продукт присутствует в результатах"):
            product_titles = main_page.products.get_texts()
            assert any("Apple Music" in title for title in product_titles), \
                f"Продукт с именем сервиса '{full_name}' не найден в результатах"

    @allure.title("Поиск по частичному названию сервиса")
    @allure.issue("https://jira.mts.ru/browse/PPI-3819", "PPInfo - Поиск продукта по коду и названию сервиса")
    @pytest.mark.parametrize("partial_name", ["[Временный]", "[Инфраструктура]"])
    def test_search_by_partial_name(self, partial_name, main_page):
        with allure.step('Кликаем на строку поиска'):
            main_page.search_str_closed.click()

        with allure.step(f'Вводим текст "{partial_name}" в поле поиска'):
            main_page.search_str.fill(partial_name)

        with allure.step('Кликаем на кнопку "Показать все"'):
            main_page.check_all_in_search.click()

        with allure.step('Проверяем, что результаты поиска загрузились'):
            assert main_page.products.are_visible()

        with allure.step('Получаем тексты всех заголовков продуктов'):
            product_titles = main_page.all_product_title.get_texts()

        with allure.step('Проверяем, что продукт присутствует в результатах'):
            assert any("apple music" in title.lower() for title in product_titles), \
                f"Продукт с именем сервиса '{partial_name}' не найден в результатах"


    @allure.title("Проверка отображения и текста подсказок 'Архив' и 'Удалён'")
    @allure.issue("https://jira.mts.ru/browse/PPI-4603", "PPInfo - В подсказках в поиске отображать, что продукт архивный ")
    @pytest.mark.parametrize(
        "search_text, expected_suggestion, suggestion",
        [
            ("1100", "Архив", "archive_suggestion"),
            ("тест 1108", "Удалён", "deleted_suggestion"),
        ]
    )
    def test_search_suggestions_have_archive_and_deleted(self, main_page, search_text, expected_suggestion, suggestion):
        with allure.step("Кликаем на строку поиска"):
            main_page.search_str_closed.click()

        with allure.step(f"Вводим текст: {search_text}"):
            main_page.search_str.fill(search_text)

        suggestion_element = getattr(main_page, suggestion)

        with allure.step(f"Ожидаем отображения подсказки '{expected_suggestion}'"):
            assert suggestion_element.is_visible(), f"Подсказка '{expected_suggestion}' не отображена"

        with allure.step(f"Проверяем текст подсказки '{expected_suggestion}'"):
            assert expected_suggestion in suggestion_element.get_text(), f"Текст подсказки '{expected_suggestion}' некорректен"

    @allure.title("Проверка наличия иконок у подсказок 'Архив' и 'Удалён'")
    @allure.issue("https://jira.mts.ru/browse/PPI-4603", "PPInfo - В подсказках в поиске отображать, что продукт архивный ")
    @pytest.mark.parametrize(
        "search_text, expected_icon",
        [
            ("1100", "archive_icon"),
            ("тест 1108", "deleted_icon"),
        ]
    )
    def test_search_suggestions_have_icons(self, main_page, search_text, expected_icon):
        with allure.step('Кликаем на строку поиска'):
            main_page.search_str_closed.click()

        with allure.step(f"Вводим текст: {search_text}"):
            main_page.search_str.fill(search_text)

        icon_element = getattr(main_page, expected_icon)

        with allure.step(f"Ожидаем отображения иконки '{expected_icon}'"):
            assert icon_element.is_visible(), f"Иконка '{expected_icon}' не отображена"






