import allure
import pytest

from UI.tests.productPage.conftest import health_page

@pytest.mark.ui
@allure.feature("Вкладка Здоровье")
class TestHealth:

    @allure.title("Проверка отображения и кликабельности таба 'Здоровье'")
    def test_health_tab_display_and_clickability(self, health_page):
        with allure.step("Проверяем, что таб 'Здоровье' отображается в меню"):
            assert health_page.health_tab.is_visible(), "Таб 'Здоровье' не отображается"

        with allure.step("Проверяем, что таб 'Здоровье' кликабелен"):
            assert health_page.health_tab.is_clickable(), "Таб 'Здоровье' не кликабелен"

        with allure.step("Проверяем, что таб стал активным"):
            assert health_page.health_tab.get_attribute('class') == 'content', "Таб 'Здоровье' не стал активным"

    @allure.title("Проверка, что раздел 'Здоровье' отображается серым")
    def test_health_section_gray(self, health_page):
        with allure.step("Переходим на страницу продукта"):
            health_page._page.goto('https://stage.prodboard.mts.ru/product/BI_1286/main')

        with allure.step("Проверяем, что кнопка 'Показать все свойства' отображается"):
            assert health_page.show_all_properties.is_visible(), "Кнопка 'Показать все свойства' не отображается"

        with allure.step("Нажимаем на кнопку 'Показать все свойства'"):
            health_page.show_all_properties.click()

        with allure.step("Проверяем значение 'Класс критичности'"):
            actual_criticality_class = health_page.criticality_class.get_text().strip()
            assert actual_criticality_class == "Оценка не требуется", f"Ожидалось 'Оценка не требуется', но было '{actual_criticality_class}'"

        with allure.step("Проверяем значение 'Класс критичности ИС'"):
            actual_criticality_class_is = health_page.criticality_class_is.get_text().strip()
            assert actual_criticality_class_is == "Не определено", f"Ожидалось 'Не определено', но было '{actual_criticality_class_is}'"

        with allure.step("Переходим на вкладку 'Здоровье'"):
            health_page.health_tab.click()

        with allure.step("Проверяем, что вкладка 'Здоровье' отображается серым "):
            assert 'empty' in health_page.health_tab.get_attribute('class'), "Вкладка 'Здоровье' не имеет класса 'empty'"

    @allure.title("Проверка описания раздела 'Здоровье' на наличие ключевых слов")
    def test_health_description(self, health_page):
        with allure.step("Проверяем, что описание раздела 'Здоровье' отображается"):
            assert health_page.health_description.is_visible(), "Описание раздела 'Здоровье' не отображается"

        with allure.step("Получаем текст описания"):
            actual_text = health_page.health_description.get_text().strip()

        with allure.step("Проверяем наличие ключевых слов в тексте"):
            key_phrases = [
                "PQI",
                "доступность",
                "единичных (ЕИ)",
                "массовых (МИ)",
                "класс критичности",
                "технологическая зрелость"
            ]

            for phrase in key_phrases:
                assert phrase in actual_text, f"Фраза '{phrase}' не найдена в тексте описания"

    @allure.title("Проверка отображения блока 'Технологическая зрелость'")
    def test_technology_maturity_block_display(self, health_page):
        with allure.step("Проверяем, что блок 'Технологическая зрелость' отображается"):
            assert health_page.technology_maturity_block.is_visible(), "Блок 'Технологическая зрелость' не отображается"

    @allure.title("Проверка отображения и текста заголовка блока 'Технологическая зрелость'")
    def test_technology_maturity_block_title(self, health_page):

        with allure.step("Проверяем, что заголовок блока 'Технологическая зрелость' отображается"):
            health_page.verify_element_visibility_and_text(health_page.technology_maturity_block_title,"Технологическая зрелость","Заголовок блока 'Технологическая зрелость'")

    @allure.title("Проверка отображения и текста индекса в блоке 'Технологическая зрелость'")
    def test_technology_maturity_block_index(self, health_page):

        health_page.verify_element_visibility_and_text(health_page.technology_maturity_block_index,"Индекс","Индекс в блоке 'Технологическая зрелость'")

    @allure.title("Проверка отображения и текста даты оценки в блоке 'Технологическая зрелость'")
    def test_technology_maturity_block_date(self, health_page):

        health_page.verify_element_visibility_and_text(health_page.technology_maturity_block_date,"Дата оценки","Дата оценки в блоке 'Технологическая зрелость'")

    @allure.title("Проверка атрибута href ссылки 'Технологическая зрелость'")
    def test_tech_maturity_link_href(self, health_page):
        with allure.step("Проверяем, что ссылка 'Технологическая зрелость' кликабельна"):
            assert health_page.tech_maturity.is_clickable(), "Ссылка 'Технологическая зрелость' не кликабельна"

        with allure.step("Получаем значение атрибута href"):
            actual_href = health_page.tech_maturity.get_attribute("href")

        with allure.step("Проверяем, что href совпадает с ожидаемым"):
            expected_href = "https://selfe.mts.ru/surveys/result/personal-survey?personalSurveyId=95186"
            assert actual_href == expected_href, f"Ожидался href '{expected_href}', но был '{actual_href}'"

    @allure.title("Проверка атрибута href ссылки 'PQI - показатель качества'")
    def test_pqi_link_href(self, health_page):
        with allure.step("Проверяем, что ссылка 'PQI - показатель качества' кликабельна"):
            assert health_page.pqi.is_clickable(), "Ссылка 'PQI - показатель качества' не кликабельна"

        with allure.step("Получаем значение атрибута href"):
            actual_href = health_page.pqi.get_attribute('href')

        with allure.step("Проверяем, что href совпадает с ожидаемым"):
            expected_href = "https://qweb.mts.ru/product_dashboard/products/?product=BI_60&agg=quarter"
            assert actual_href == expected_href, f"Ожидался href '{expected_href}', но был '{actual_href}'"

    @allure.title("Проверка отображения блока 'PQI'")
    def test_pqi_block_display(self, health_page):
        with allure.step("Проверяем, что блок 'PQI' отображается"):
            assert health_page.pqi_block.is_visible(), "Блок 'PQI' не отображается"

    @allure.title("Проверка отображения и текста заголовка блока 'PQI'")
    def test_pqi_block_title(self, health_page):

        health_page.verify_element_visibility_and_text(health_page.pqi_block_title,"PQI - показатель качества","Заголовок блока 'PQI'")

    @allure.title("Проверка отображения 2Q 2025 в блоке PQI")
    def test_pqi_block_quarter_2(self, health_page):

        health_page.verify_element_visibility_and_text(health_page.pqi_block_quarter_2,"2Q 2025","Квартал 2 в блоке PQI")

    @allure.title("Проверка отображения 3Q 2025")
    def test_ppi_block_quarter_3(self, health_page):

        health_page.verify_element_visibility_and_text(health_page.pqi_block_quarter_3,"3Q 2025","Квартал 3 в блоке PQI")

    @allure.title("Проверка отображения блока 'NSAT/tNPS'")
    def test_nsat_tnps_block_display(self, health_page):
        with allure.step("Проверяем, что блок 'NSAT/tNPS' отображается"):
            assert health_page.nsat_tnps_block.is_visible(), "Блок 'NSAT/tNPS' не отображается"

    @allure.title("Проверка отображения и текста заголовка блока 'NSAT/tNPS'")
    def test_nsat_tnps_block_title(self, health_page):

        health_page.verify_element_visibility_and_text(health_page.nsat_tnps_block_title,"NSAT/tNPS","Заголовок блока 'NSAT/tNPS'")

    @allure.title("Проверка отображения и текста внутри блока 'NSAT/tNPS'")
    def test_nsat_tnps_block_text(self, health_page):

        health_page.verify_element_visibility_and_text(health_page.nsat_tnps_block_text,"Функционал в разработке и скоро появится","Текст внутри блока 'NSAT/tNPS'")

    @allure.title("Проверка отображения блока 'Класс критичности'")
    def test_criticality_class_block_display(self, health_page):
        with allure.step("Проверяем, что блок 'Класс критичности' отображается"):
            assert health_page.criticality_class_block.is_visible(), "Блок 'Класс критичности' не отображается"

    @allure.title("Проверка отображения и текста заголовка блока 'Класс критичности'")
    def test_criticality_class_block_title(self, health_page):

        health_page.verify_element_visibility_and_text( health_page.criticality_class_block_title,"Класс критичности","Заголовок блока 'Класс критичности'")

    @allure.title("Проверка отображения атрибута 'Класс критичности'")
    def test_criticality_class_block_attribute(self, health_page):

        health_page.verify_element_visibility_and_text(health_page.criticality_class_block_attribute,"Класс Критичности","Атрибут 'Класс критичности'")

    @allure.title("Проверка отображения и текста 'Дата прохождения' в блоке 'Класс критичности'")
    def test_criticality_class_block_date(self, health_page):

        health_page.verify_element_visibility_and_text(health_page.criticality_class_block_date,"Дата прохождения","Дата прохождения в блоке 'Класс критичности'")

    @allure.title("Проверка отображения и работы подсказки 'Класс критичности систем соответствует классу продукта'")
    def test_criticality_class_suggestion_tooltip(self, health_page):
        with allure.step("Проверяем, что иконка подсказки отображается"):
            assert health_page.criticality_class_suggestion_icon.is_visible(), "Иконка подсказки не отображается"

        with allure.step("Проверяем, что иконка подсказки кликабельна"):
            assert health_page.criticality_class_suggestion_icon.is_clickable(), "Иконка подсказки не кликабельна"

        with allure.step("Кликаем на иконку подсказки"):
            health_page.criticality_class_suggestion_icon.click()

        with allure.step("Проверяем, что текст подсказки отображается"):
            assert health_page.criticality_class_suggestion_text.is_visible(), "Текст подсказки не отображается"

        with allure.step("Проверяем ключевые фразы текста подсказки"):
            actual_text = health_page.criticality_class_suggestion_text.get_text().strip()

            key_phrases = [
                "Согласно ПТ-Э-056",
                "разработать План обеспечения надежности",
                "Владельцу Продукта/ИС",
                "Создание и верификация Плана обеспечения надежности продукта Группы компаний МТС"
            ]

            for phrase in key_phrases:
                assert phrase in actual_text, f"Фраза '{phrase}' не найдена в тексте подсказки"

    @pytest.mark.parametrize("product_id", [
        "BI_133",
        "BI_60"
    ])
    @allure.title("Проверка отображения чипса 'Класс критичности' в зависимости от соотношения значений")
    def test_criticality_class_chip(self, product_id, health_page):
        with allure.step(f"Переходим на страницу продукта {product_id}"):
            health_page._page.goto(f'https://stage.prodboard.mts.ru/product/{product_id}/main')

        with allure.step("Нажимаем на кнопку 'Показать все свойства'"):
            health_page.show_all_properties.click()

        with allure.step("Получаем значение 'Класс критичности ИС' из основной информации"):
            criticality_class_is_main = health_page.criticality_class_is.get_text().strip()

        with allure.step("Переходим на вкладку 'Здоровье'"):
            health_page.health_tab.click()

        with allure.step("Получаем значение 'Класс критичности' из блока на вкладке 'Здоровье'"):
            criticality_class_block_value = health_page.criticality_class_block_value.get_text().strip()

        with allure.step("Проверяем отображение одного из чипсов"):
            if criticality_class_is_main != criticality_class_block_value:
                expected_chip_locator = health_page.criticality_class_chip
                expected_chip_text = "Класс критичности систем не соответствует классу продукта"
            else:
                expected_chip_locator = health_page.criticality_class_chip_match
                expected_chip_text = "Класс критичности систем соответствует классу продукта"

            assert expected_chip_locator.is_visible(), f"Чип '{expected_chip_text}' не отображается"

            actual_chip_text = expected_chip_locator.get_text().strip()
            assert actual_chip_text == expected_chip_text, \
                f"Ожидался текст '{expected_chip_text}', но был '{actual_chip_text}'"
