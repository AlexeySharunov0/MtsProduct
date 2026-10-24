import re
from datetime import datetime

import allure
import pytest

from UI.data.assertions_data import ProductsAsserts as assertions
from UI.tests.productPage.conftest import docs_page
from UI.tests.editPage.conftest import add_replace_page


@pytest.mark.ui
@allure.feature("Вкладка Документы")
class TestDocs:

    @allure.title("Проверка кликабельности и отображения таба Документы у продуктов с наличием документов")
    def test_doc_tab_check(self, docs_page):
        with allure.step("Проверяем, что таб есть в боковом меню"):
            assert docs_page.docs_tab.is_visible(), 'Таба нет в меню'
        with allure.step('Проверяем, что таб Документы кликабельный'):
            assert docs_page.docs_tab.is_clickable(), 'Таб некликабельный'
        with allure.step("Проверяем, что таб отмечен как активный (черный)"):
            assert docs_page.docs_tab.get_attribute('class') == 'content', 'Таб окрашен серым'

    @allure.title("Проверка кликабельности и отображения таба Документы у продуктов без документов")
    @pytest.mark.parametrize('docs_page', ['https://stage.prodboard.mts.ru/product/BI_89/main'], indirect=True)
    def test_doc_tab_check_empty(self, docs_page):
        with allure.step("Проверяем, что таб есть в боковом меню"):
            assert docs_page.docs_tab.is_visible(), 'Таба нет в меню'
        with allure.step('Проверяем, что таб Документы кликабельный'):
            assert docs_page.docs_tab.is_clickable(), 'Таб некликабельный'
        with allure.step("Проверяем, что таб отмечен как неактивный (серый)"):
            assert docs_page.docs_tab.get_attribute('class') == 'content empty', 'Таб окрашен черным'

    @allure.title("Проверка заголовков на странице Документы")
    def test_check_doc_headers(self, docs_page):
        with allure.step("Проверяем, что заголовок страницы отображается корректно"):
            assert docs_page.docs_header.is_visible(), 'Заголовка нет'
            assert docs_page.docs_header.get_text() == 'Документы', 'Текст заголовка не совпадает'
        with allure.step("Проверяем, что описание страницы отображается корректно"):
            assert docs_page.tab_description.is_visible(), 'Описания нет'
            assert docs_page.tab_description.get_text() == assertions.docs_description, 'Текст описания не совпадает'

    @allure.title("Проверка текста при отсутствии документов")
    @pytest.mark.parametrize('docs_page', ['https://stage.prodboard.mts.ru/product/BI_89/docs'], indirect=True)
    def test_check_text_docs_no_documents(self, docs_page):
        docs_page.clear_docs()
        with allure.step("Проверяем, что текст при отсутствии документов отображается корректно"):
            assert docs_page.docs_empty.is_visible(), 'Заголовка нет'
            assert docs_page.docs_empty.get_text() == assertions.docs_error, 'Текст ошибки не совпадает'

    @allure.title("Проверка отображения таблицы документов")
    @pytest.mark.parametrize("docs_page", assertions.linkToProduct, indirect=True)
    def test_open_docs(self, docs_page):
        with allure.step('Проверяем, что таблица документов отобразилась'):
            assert docs_page.docs_table.is_visible(), 'Таблицы документов нет'

    @allure.title("Проверка работы поиска на странице Документов")
    def test_docs_search(self, docs_page):
        with allure.step("Вводим текст в строку поиска"):
            docs_page.docs_search = 'Скрытый'
        with allure.step("Проверяем, что нашел поиск"):
            assert docs_page.doc_link.get_text() == 'Скрытый документ', 'Нужный документ не найден'

    @allure.title("Проверка работы поиска на странице Документов при ненахождении документов")
    def test_docs_search_no_result(self, docs_page):
        with allure.step("Вводим текст в строку поиска"):
            docs_page.docs_search.fill('белиберда')
        with allure.step("Проверяем, что нашел поиск"):
            assert docs_page.doc_link.is_not_visible(), 'Документ нашелся'
            assert docs_page.docs_empty_search.is_visible(), 'Текстовки при пустом поиске нет'
            assert docs_page.docs_empty_search.get_text() == 'Документы не найдены', 'Текстовка при пустом поиске не та'
        with allure.step("Проверяем, что строка поиска не пропала"):
            assert docs_page.docs_search.is_visible(), 'Строки поиска нет'

    @allure.title("Нажатие на название возвращает к основной информации о текущем продукте (с таба документов)")
    def test_name_returns_to_main_info_from_docs(self, product_page, docs_page):
        with allure.step("Кликаем на название продукта"):
            product_page.product_name.click()
        with allure.step("Проверяем, что мы вернулись на главную страницу продукта"):
            assert docs_page.docs_header.is_not_visible(), 'Заголовок с Документы остался'

    @allure.title("Нажатие на лого возвращает к основной информации о текущем продукте (с таба документов)")
    def test_logo_returns_to_main_info_from_docs(self, product_page, docs_page):
        with allure.step("Кликаем на лого продукта"):
            product_page.product_logo.click()
        with allure.step("Проверяем, что мы вернулись на главную страницу продукта"):
            assert docs_page.docs_header.is_not_visible(), 'Заголовок с Документы остался'

    @allure.title("Значок лупы отображается в строке поиска на табе Документы")
    @allure.issue('https://jira.mts.ru/browse/PPI-2459',
                  'PPinfo - Отсутствует значок лупы в строке поиска на странице документов')
    def test_check_search_icon_docs(self, docs_page):
        with allure.step("Проверяем, что значок лупы виден"):
            assert docs_page.search_icon_docs.is_visible(), 'значка нет'

    @allure.title("Проверка добавления и удаления документа")
    @pytest.mark.parametrize('docs_page', ['https://stage.prodboard.mts.ru/product/BI_2655/docs'], indirect=True)
    @pytest.mark.parametrize('access_type', assertions.access_types)
    def test_add_delete_file(self, add_replace_page, docs_page, access_type):
        docs_page.clear_docs()
        add_replace_page.add_doc_without_brief(access_type)
        with allure.step("Проверяем, что файл добавился корректно"):
            assert add_replace_page.doc_item.is_visible(), 'Названия файла нет'
            assert add_replace_page.doc_item.get_text() == 'UI_TEST_DOC', 'Название файла не совпадет'
            docs_page.doc_link.click()
            assert docs_page.download_button_in_preview.get_attribute('href').startswith(
                'https://stage.prodboard.mts.ru/pmd/internal/rest/api/v1/product/documents/'), 'Ссылка на скачивание неверная'
            docs_page.close_modal_button.click()

        docs_page.delete_doc_once()
        with allure.step("Проверяем, что документ удалился"):
            assert add_replace_page.doc_item.is_not_visible(), 'Документ не удалился'

    @allure.title("Проверка добавления и удаления ссылки")
    @pytest.mark.parametrize('docs_page', ['https://stage.prodboard.mts.ru/product/BI_2655/docs'], indirect=True)
    @pytest.mark.parametrize('access_type', assertions.access_types)
    def test_add_delete_link(self, add_replace_page, docs_page, access_type):
        docs_page.clear_docs()
        add_replace_page.add_link_without_brief(access_type)
        with allure.step("Проверяем, что ссылка добавилась корректно"):
            assert add_replace_page.doc_item.is_visible(), 'Названия ссылки нет'
            assert add_replace_page.doc_item.get_text() == 'UI_TEST_LINK', 'Название ссылки не совпадет'
            assert docs_page.doc_link.get_attribute(
                'href') == 'https://stage.prodboard.mts.ru/preset/archive', 'Ссылка на переход неверная'
        docs_page.delete_doc_once()
        with allure.step("Проверяем, что документ удалился"):
            assert add_replace_page.doc_item.is_not_visible(), 'Документ не удалился'

    @allure.title("Проверка корректного формата дат у загруженных документов")
    @pytest.mark.parametrize('docs_page', ['https://stage.prodboard.mts.ru/product/BI_2655/docs'], indirect=True)
    def test_docs_data(self, add_replace_page, docs_page):
        add_replace_page.add_doc_without_brief()
        date = docs_page.docs_data.get_text()
        current_date = datetime.now().strftime('%d-%m-%Y').replace("-", ".")
        with allure.step('Проверяем, что дата в корректном формате'):
            assert re.fullmatch("\d\d\.\d\d\.\d\d\d\d", date), f'Дата {date} не в формае дд.мм.гггг'
            assert date == current_date, 'Дата не сегодняшняя'

        docs_page.delete_doc_once()

    @allure.title("Проверка, что после удаления документа появляется сообщение о том, что документы отсутствуют")
    @pytest.mark.parametrize('docs_page', ['https://stage.prodboard.mts.ru/product/BI_2655/docs'], indirect=True)
    def test_doc_check_message_after_delete(self, add_replace_page, docs_page):
        docs_page.clear_docs()
        add_replace_page.add_doc_without_brief()
        with allure.step("Проверяем, что текста при отсутствии документов нет"):
            assert docs_page.docs_empty.is_not_visible(), 'Заголовок есть'
        docs_page.delete_doc_once()
        with allure.step("Проверяем, что текст при отсутствии документов отображается корректно"):
            assert docs_page.docs_empty.is_visible(), 'Заголовка нет'


    # TODO Деделать когда опишу ADD REPLACE
    # @allure.title("Проверка добавления и удаления документа")
    # @pytest.mark.parametrize('docs_page', ['https://stage.prodboard.mts.ru/product/BI_2655/main'], indirect=True)
    # @pytest.mark.parametrize('access_type', assertions.access_types)
    # def test_add_delete_file(self, docs_page, access_type):
    #     docs_page.clear_docs()
    #     docs_page.add_doc_without_brief(access_type)
    #     docs_page.wait_page_loaded()
    #     with allure.step("Проверяем, что файл добавился корректно"):
    #         assert docs_page.doc_item.is_visible(), 'Названия файла нет'
    #         assert docs_page.doc_item.get_text() == 'UI_TEST_DOC', 'Название файла не совпадет'
    #         assert docs_page.doc_link.get_attribute('href').startswith(
    #             'https://stage.prodboard.mts.ru/pmd/internal/rest/api/v1/product/documents/'), 'Ссылка на скачивание неверная'
    #
    #     docs_page.delete_doc_once()
    #     docs_page.wait_page_loaded()
    #     with allure.step("Проверяем, что документ удалился"):
    #         assert docs_page.doc_item.is_not_visible(), 'Документ не удалился'
    #
    # @allure.title("Проверка добавления и удаления ссылки")
    # @pytest.mark.parametrize('docs_page', ['https://stage.prodboard.mts.ru/product/BI_2655/main'], indirect=True)
    # @pytest.mark.parametrize('access_type', assertions.access_types)
    # def test_add_delete_link(self, docs_page, access_type):
    #     docs_page.clear_docs()
    #     docs_page.add_link_without_brief(access_type)
    #     docs_page.wait_page_loaded()
    #     with allure.step("Проверяем, что ссылка добавилась корректно"):
    #         assert docs_page.doc_item.is_visible(), 'Названия ссылки нет'
    #         assert docs_page.doc_item.get_text() == 'UI_TEST_LINK', 'Название ссылки не совпадет'
    #         assert docs_page.doc_link.get_attribute(
    #             'href') == 'https://stage.prodboard.mts.ru/preset/archive', 'Ссылка на переход неверная'
    #     docs_page.delete_doc_once()
    #     docs_page.wait_page_loaded()
    #     with allure.step("Проверяем, что документ удалился"):
    #         assert docs_page.doc_item.is_not_visible(), 'Документ не удалился'
    #
    # @allure.title("Проверка корректного формата дат у загруженных документов")
    # @pytest.mark.parametrize('docs_page', ['https://stage.prodboard.mts.ru/product/BI_2655/main'], indirect=True)
    # def test_docs_data(self, docs_page):
    #     docs_page.wait_page_loaded()
    #     docs_page.add_doc_without_brief()
    #     date = docs_page.docs_data.get_text()
    #     current_date = datetime.now().strftime('%d-%m-%Y').replace("-", ".")
    #     with allure.step('Проверяем, что дата в корректном формате'):
    #         assert re.fullmatch("\d\d\.\d\d\.\d\d\d\d", date), f'Дата {date} не в формае дд.мм.гггг'
    #         assert date == current_date, 'Дата не сегодняшняя'
    #
    #     docs_page.delete_doc_once()
    #
    # @allure.title("Проверка, что после удаления документа появляется сообщение о том, что документы отсутствуют")
    # @pytest.mark.parametrize('docs_page', ['https://stage.prodboard.mts.ru/product/BI_2655/main'], indirect=True)
    # def test_doc_check_message_after_delete(self, docs_page):
    #     docs_page.wait_page_loaded()
    #     docs_page.clear_docs()
    #     docs_page.add_doc_without_brief()
    #     time.sleep(2)  # иначе не успевает удалиться docs-error
    #     with allure.step("Проверяем, что текста при отсутствии документов нет"):
    #         assert docs_page.docs_empty.is_not_visible(), 'Заголовок есть'
    #     docs_page.delete_doc_once()
    #     time.sleep(1)  # иначе не успевает добавиться docs-error
    #     with allure.step("Проверяем, что текст при отсутствии документов отображается корректно"):
    #         assert docs_page.docs_empty.is_visible(), 'Заголовка нет'


@pytest.mark.ui
class TestDocsTechUser:
    @allure.title(f"Проверка, что закрытые документы не отображаются обычным пользователям")
    def test_docs_visible(self, docs_page_user):
        with allure.step('Проверяем, что закрытый документ не виден пользователю'):
            assert ['Распорядительный документ'] not in docs_page_user.doc.get_texts(), 'Скрытый документ виден юзеру'
