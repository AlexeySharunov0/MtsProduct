import re
from datetime import datetime, timedelta

import allure
import openpyxl
import pytest

from API.models.cache.cache import Cache
from API.models.ppinfo.brief import Brief
from API.models.ppinfo.product_v1 import ProductV1
from API.models.ppinfo.product_v2 import ProductV2
from API.models.ppinfo.rest import Rest
from API.models.ppinfo.tag import Tag
from API.utils.helpers import get_atomic_products


#################################################################### Добавление документа


@pytest.mark.api
@pytest.mark.last
@allure.feature("Добавление документа")
class TestRestAddDocument(Rest):
    @allure.title("Отправка заявки на добавление публичного/закрытого документа админ/автосогласование")
    @pytest.mark.parametrize("access_type", ["public", "chanelDepended"])
    @pytest.mark.parametrize("file_format",
                             [".xlsx", ".xls", ".doc", ".docx", ".ppt", ".pptx", ".txt", ".pdf", ".3gp", ".avi", ".mov",
                              ".mp4",
                              ".mp3", ".mkv", ".wav", ".jpg", ".jpeg", ".svg", ".png", ".zip", ".rar", ".gif", ".msg",
                              ".exe", ".rtf"])
    def test_post_brief_doc_public(self, ppinfo_api_client, access_type, file_format):
        data = self.get_data_for_doc_brief(access_type, file_format)

        self.post_brief_doc(ppinfo_api_client, data, file_format)

    @allure.title("Отправка заявки на добавление публичного/закрытого документа юзер")
    @pytest.mark.parametrize("access_type", ["public", "chanelDepended"])
    @pytest.mark.parametrize("file_format",
                             [".xlsx", ".xls", ".doc", ".docx", ".ppt", ".pptx", ".txt", ".pdf", ".3gp", ".avi", ".mov",
                              ".mp4",
                              ".mp3", ".mkv", ".wav", ".jpg", ".jpeg", ".svg", ".png", ".zip", ".rar", ".gif", ".msg",
                              ".exe", ".rtf"])
    def test_post_brief_doc_public_user(self, ppinfo_user_api_client, access_type, file_format):
        data = self.get_data_for_doc_brief(access_type, file_format)

        self.post_brief_doc_user(ppinfo_user_api_client, data, file_format)

    @allure.title("Отправка заявки на добавление публичного/закрытого документа / ошибка / пустое имя")
    @pytest.mark.parametrize("access_type", ["public", "chanelDepended"])
    def test_post_brief_doc_error_empty_name(self, ppinfo_api_client, access_type):
        data = self.get_data_for_doc_brief(access_type, name="")

        self.invalid_post_brief_doc(ppinfo_api_client, data)

    @allure.title("Отправка заявки на добавление публичного/закрытого документа и скачивание его")
    @pytest.mark.parametrize("access_type", ["public", "chanelDepended"])
    @pytest.mark.parametrize("file_format",
                             [".xlsx", ".xls", ".doc", ".docx", ".ppt", ".pptx", ".txt", ".pdf", ".3gp", ".avi", ".mov",
                              ".mp4",
                              ".mp3", ".mkv", ".wav", ".jpg", ".jpeg", ".svg", ".png", ".zip", ".rar", ".gif", ".msg",
                              ".exe", ".rtf"])
    def test_get_brief_doc_and_download(self, ppinfo_api_client, access_type, file_format):
        data = self.get_data_for_doc_brief(access_type, file_format)

        self.download_doc_from_brief(ppinfo_api_client, self.post_brief_doc(ppinfo_api_client, data, file_format))


@pytest.mark.api
@pytest.mark.last
@allure.feature("Заявки")
@allure.feature('Excel')
@allure.issue('https://jira.mts.ru/browse/PPI-2303', 'PPInfo - Выгрузка Excel с заявками')
class TestBriefsExcel(Rest, Brief):
    @allure.title("Загрузка Excel Отчет по заявкам")
    @pytest.mark.parametrize('year', ['2024', '2025', '2026'])
    def test_briefs_excel(self, ppinfo_api_client, year, clear_excel):
        excel = self.create_excel_doc(self.get_brief_excel(ppinfo_api_client, year))
        if int(year) == datetime.now().year:
            with allure.step('Проверяем, что эксель не пустой'):
                assert not excel.empty, "Файл эксель пустой"

        wb = openpyxl.load_workbook('filename_excel.xlsx')
        with allure.step('Проверяем, что название листа выбранный год'):
            assert wb.sheetnames[0] == year, f'Название не то: {wb.sheetnames[0]} != {year}'

    @allure.title("Проверяем наличие столбцов в Excel Отчет по заявкам")
    @allure.issue('https://jira.mts.ru/browse/PPI-2854',
                  'PPInfo - Добавить тип продукта в выгрузку по заявкам в РМ Администратора PPInfo')
    def test_briefs_excel_check_cols(self, ppinfo_api_client, clear_excel):
        excel = self.create_excel_doc(self.get_brief_excel(ppinfo_api_client))

        with allure.step('Проверяем, что все нужные столбцы присутствуют'):
            assert {'Номер', 'Наименование продукта', 'Тип продукта', 'Тип заявки',
                    'Статус заявки', 'Дата создания', 'Дата решения', 'Автор', 'Исполнитель', 'Комментарий'}.issubset(
                excel.columns), "Столбцы не совпадают"

        with allure.step("Проверяем, что все столбцы в таблице заполнены"):
            empty_cols = [col for col in excel.columns if excel[col].isnull().all()]

            assert not empty_cols, f'Столбцы {empty_cols} пустые'

    @allure.title("Excel Отчет по заявкам / Столбец Номер")
    def test_briefs_excel_number_col(self, ppinfo_client, ppinfo_api_client, clear_excel):
        self.create_excel_doc(self.get_brief_excel(ppinfo_api_client))

        wb = openpyxl.load_workbook('filename_excel.xlsx')
        ws = wb.active

        with allure.step("Проверяем, что гиперссылки ведут на страницу заявки"):
            links = [ws.cell(row=row_number, column=1).hyperlink.target for row_number in range(2, ws.max_row)]
            wrong_links = [i for i in links if "https://stage.prodboard.mts.ru/brief/" not in i]

            assert not wrong_links, f'Среди гиперссылок есть ссылки неверного формата: {wrong_links}'

        with allure.step("Проверяем, что в самом верху самая последняя опубликованная заявка"):
            brief_numbers = []
            for status in ['statusDone', 'statusDeclined']:
                for is_owned in [True, False]:
                    brief_numbers.append(
                        self.get_briefs(ppinfo_client, self.get_briefs_params(
                            {"status": status, 'isOwned': is_owned, 'limit': 10000}))['briefs'][0][
                            'number'])

        assert ws.cell(row=2, column=1).value in brief_numbers, 'Первая заявка не самая последняя опубликованная'

    @allure.title("Excel Отчет по заявкам / Столбец статус")
    def test_briefs_excel_status_col(self, ppinfo_api_client, clear_excel):
        self.create_excel_doc(self.get_brief_excel(ppinfo_api_client))

        wb = openpyxl.load_workbook('filename_excel.xlsx')
        ws = wb.active

        with allure.step("Проверяем, что в Excel попадают только опубликованные заявки"):
            values = [ws.cell(row=row_number, column=5).value for row_number in range(2, ws.max_row)]

            assert all(i in ['Отклонена', 'Опубликована'] for i in values), 'В Excel есть заявка не в том статусе'

    @allure.title("Excel Отчет по заявкам / Столбцы Дата создания и дата решения")
    @pytest.mark.parametrize('year', ['2024', '2025', '2026'])
    def test_briefs_excel_date_cols(self, ppinfo_api_client, year, clear_excel):
        self.create_excel_doc(self.get_brief_excel(ppinfo_api_client, year))

        wb = openpyxl.load_workbook('filename_excel.xlsx')
        ws = wb.active
        if int(year) == datetime.now().year:
            with allure.step("Проверяем, что все даты в Excel за указанный год"):
                creation_dates = [ws.cell(row=row_number, column=6).value[6:10] for row_number in range(2, ws.max_row)]
                execution_dates = [ws.cell(row=row_number, column=7).value[6:10] for row_number in range(2, ws.max_row)]
                assert all(i == year for i in creation_dates), 'Даты создания не за текущий год'
                assert all(i == year for i in execution_dates), 'Даты исполнения не за текущий год'


####################################################################  Метрики
@pytest.mark.api
@allure.feature("Метрики")
class TestRestMetrics(Rest, ProductV1):
    @allure.title("Получение данных по метрикам")
    @pytest.mark.parametrize('code', ['BI_60', 'BI_42', 'BI_51'])
    def test_get_metrics(self, ppinfo_api_client, code):
        assert self.get_metrics(ppinfo_api_client, code)['metricsLinks'], 'Пустой ответ'

    @allure.title("Изменение отображения дашборда в зависимости от атрибута Сбор метрик")
    @allure.issue('https://jira.mts.ru/browse/PPI-3008', 'PPInfo - Дашборд "Светофор" переключить на атрибут продукта')
    @pytest.mark.parametrize('value_attribute, value_metrics',
                             [([{"code": "Da", "value": "Да"}], 1), ([{"code": "Net", "value": "Нет"}], 2), ([], 2)])
    def test_get_metrics_dashboard(self, ppinfo_api_client, ppinfo_client, value_attribute, value_metrics):
        data = {"id": "BI_2769", "attributes": [{"id": "Sbor_metrik", "values": value_attribute}],
                "notification": False, "type": "Vneshnii"}

        self.change_product(ppinfo_client, data)

        assert self.get_metrics(ppinfo_api_client, 'BI_2769')[
                   'typeText'] == value_metrics, 'Значение в метриках не соответствует атрибуту Сбор метрик'

    @allure.title('Получение метрик по продуктам, у которых нет витрины качества ИТ')
    @allure.issue('https://jira.mts.ru/browse/PPI-2666',
                  'PPInfo - Проверять наличие данных по ссылке на Витрину качества ИТ')
    @pytest.mark.parametrize('code', ['BI_1562', 'BI_2912'])
    def test_get_metrics_no_showcase(self, ppinfo_api_client, code):
        required_showcase = \
            [i for i in self.get_metrics(ppinfo_api_client, code)['metricsLinks'] if i['code'] == 'PPinfo_IT_quality'][
                0]
        with allure.step('Проверяем, что витрина пустая'):
            assert not required_showcase['value'], 'Витрина не пустая'

    @allure.title('Получение метрик по продуктам, у которых есть витрина качества ИТ')
    @allure.issue('https://jira.mts.ru/browse/PPI-2666',
                  'PPInfo - Проверять наличие данных по ссылке на Витрину качества ИТ')
    @pytest.mark.parametrize('code', ['BI_60', 'BI_201', 'BI_42', 'BI_41'])
    def test_get_metrics_showcase(self, ppinfo_api_client, code):
        required_showcase = \
            [i for i in self.get_metrics(ppinfo_api_client, code)['metricsLinks'] if i['code'] == 'PPinfo_IT_quality'][
                0]
        with allure.step('Проверяем, что витрина не пустая'):
            assert required_showcase['value'], 'Витрина пустая'

    @allure.title('Получение Портала ДККО по продуктам, у которых есть портал ДККО')
    @allure.issue('https://jira.mts.ru/browse/PPI-2983',
                  ' PPInfo - Получение актуальных ссылок с Портал по качеству ДККО - QWEB')
    @pytest.mark.parametrize('code', ['BI_60', 'BI_42'])
    def test_get_metrics_showcase_dkko_yes(self, ppinfo_api_client, code):
        required_showcase = \
            [i for i in self.get_metrics(ppinfo_api_client, code)['metricsLinks'] if
             i['code'] == 'PPInfo_Dashbord_Qweb'][
                0]
        with allure.step('Проверяем, что витрина не пустая'):
            assert required_showcase['value'], 'Витрина пустая'

    @allure.title('Получение Портала ДККО по продуктам, у которых нет портала ДККО')
    @allure.issue('https://jira.mts.ru/browse/PPI-2983',
                  'PPInfo - Получение актуальных ссылок с Портал по качеству ДККО - QWEB')
    @pytest.mark.parametrize('code', ['BI_26', 'BI_201'])
    def test_get_metrics_showcase_dkko_no(self, ppinfo_api_client, code):
        required_showcase = \
            [i for i in self.get_metrics(ppinfo_api_client, code)['metricsLinks'] if
             i['code'] == 'PPInfo_Dashbord_Qweb'][
                0]
        with allure.step('Проверяем, что витрина не пустая'):
            assert not required_showcase['value'], 'Витрина заполнена, хотя должна быть пустая'


##### Excel
@pytest.mark.api
@allure.feature("Excel")
class TestRestExcel(Rest, Cache, ProductV2):
    ############ Все документы Excel

    @allure.title("Загрузка excel Все документы")
    def test_excel_all_docs(self, ppinfo_api_client, clear_excel):
        excel = self.create_excel_doc(self.get_all_docs_excel(ppinfo_api_client))

        with allure.step('Проверяем, что эксель не пустой'):
            assert not excel.empty, "Файл эксель Все документы пустой"

    @allure.title("Проверяем наличие столбцов в excel Все документы")
    def test_excel_all_docs_check_cols(self, ppinfo_api_client, clear_excel):
        excel = self.create_excel_doc(self.get_all_docs_excel(ppinfo_api_client))

        with allure.step('Проверяем, что все нужные столбцы присутствуют'):
            assert {'Название продукта', 'Ссылка на документ', 'Дата добавления документа',
                    'Комментарий документа'}.issubset(excel.columns), "Столбцы не совпадают"

        with allure.step("Проверяем, что все столбцы в таблице заполнены"):
            empty_cols = [col for col in excel.columns if excel[col].isnull().all()]

            assert not empty_cols, f'Столбцы {empty_cols} пустые'

    @allure.title("Excel Все документы, проверка значений 1 столбца (Название документа)")
    def test_excel_all_doc_check_first_col(self, ppinfo_api_client, clear_excel):
        self.create_excel_doc(self.get_all_docs_excel(ppinfo_api_client))
        wb = openpyxl.load_workbook('filename_excel.xlsx')

        ws = wb.active

        with allure.step("Проверяем, что гиперссылки ведут на страницу продукта ppinfo"):
            links = [ws.cell(row=row_number, column=1).hyperlink.target for row_number in range(2, ws.max_row)]
            wrong_links = [i for i in links if "https://stage.prodboard.mts.ru/product/" not in i]

            assert not wrong_links, f'Среди гиперссылок есть ссылки неверного формата: {wrong_links}'

        with allure.step("Проверяем, что в ячейках есть заменяющий текст"):
            assert all(ws.cell(row=row_number, column=1).hyperlink.display for row_number in
                       range(2, ws.max_row)), "В некоторых ячейках отсутствует заменяющий текст"

    @allure.title("Excel Все документы, проверка значений 2 столбца (Ссылка на документ)")
    def test_excel_all_doc_check_second_col(self, ppinfo_api_client, clear_excel):
        self.create_excel_doc(self.get_all_docs_excel(ppinfo_api_client))
        wb = openpyxl.load_workbook('filename_excel.xlsx')

        ws = wb.active

        with allure.step("Проверяем, что все значения являются гиперссылками"):
            assert all(ws.cell(row=row_number, column=2).hyperlink.target for row_number in
                       range(2, ws.max_row)), "Некоторые ячейки не являются гиперссылками"

        with allure.step("Проверяем, что в ячейках есть заменяющий текст"):
            assert all(ws.cell(row=row_number, column=2).hyperlink.display for row_number in
                       range(2, ws.max_row)), "В некоторых ячейках отсутствует заменяющий текст"

    @allure.title("Excel Все документы, проверка значений 3 столбца (Дата добавления документа)")
    def test_excel_all_doc_check_third_col(self, ppinfo_api_client, clear_excel):
        self.create_excel_doc(self.get_all_docs_excel(ppinfo_api_client))
        wb = openpyxl.load_workbook('filename_excel.xlsx')

        ws = wb.active

        with allure.step("Проверяем, что все значения являются датами ДД.ММ.ГГГГ"):
            dates = [ws.cell(row=row_number, column=3).value for row_number in range(2, ws.max_row)]
            assert all(re.search("([0-9]{2}\.[0-9]{2}\.[0-9]{4})", date) for date in
                       dates), "Некоторые значения не являются датами в формате ДД.ММ.ГГГГ"

    ##################################################### Получение документа по его айдишнику

    @allure.title("Качаем документ по айди")
    @pytest.mark.parametrize('file_id',
                             ['3f54dc96-6015-488e-b885-9e2b5adc3642', 'ed7ff164-3262-4303-9576-37990c482169'])
    def test_get_doc_by_id(self, ppinfo_api_client, file_id):
        self.get_doc_by_id(ppinfo_api_client, file_id)


##################################################### Excel все продукты

@pytest.mark.excel
class TestExcel(Rest, Tag):
    # """
    # * Наполнение вкладок продуктами:
    # * "Продукты": Внешние + внутренние + атомарные внешние + атомарные внутренние - только активные продукты
    # * Продукты без учета атомарных: Внешние + внутренние - только активные продукты
    # * Хабы: Хабы + атомарные хабы - только активные хабы
    # * Продукты и хабы: Внешние + внутренние + атомарные внешние + атомарные внутренние + хабы
    # * Архивные продукты -> Архив : Архивные внутренние + архивные внешние + архивные хабы
    # * Удаленные: Удаленные внутренние + удаленные внешние + удаленные хабы
    #
    # """
    # Проверка столбцов во всех документах
    @allure.title("В икселе Все продукты корректный набор столбцов")
    @pytest.mark.parametrize('sheet_name',
                             ['Все направления',
                              'Телеком',
                              'Финтех',
                              'Медиа',
                              'Ad-tech',
                              'MWS',
                              'Юрент',
                              'УК Экосистемы МТС'])
    def test_excel_all_products_check_columns(self, ppinfo_api_client, ppinfo_client, sheet_name):
        self.create_excel_doc(self.get_excel_all(ppinfo_api_client))

        self.check_columns(ppinfo_client, sheet_name, True)

    @allure.title("В икселе Все продукты, включая атомарные корректный набор столбцов")
    @pytest.mark.parametrize('sheet_name',
                             ['Все направления',
                              'Телеком',
                              'Финтех',
                              'Медиа',
                              'Ad-tech',
                              'MWS',
                              'Юрент',
                              'УК Экосистемы МТС'])
    def test_excel_all_and_atomic_check_columns(self, ppinfo_api_client, ppinfo_client, sheet_name):
        self.create_excel_doc(self.get_excel_all_and_atomic(ppinfo_api_client))

        self.check_columns(ppinfo_client, sheet_name)

    @allure.title("В икселе Продукты и хабы корректный набор столбцов")
    @pytest.mark.parametrize('sheet_name',
                             ['Все направления',
                              'Телеком',
                              'Финтех',
                              'Медиа',
                              'Ad-tech',
                              'MWS',
                              'Юрент',
                              'УК Экосистемы МТС'])
    def test_excel_products_and_hubs_check_columns(self, ppinfo_api_client, ppinfo_client, sheet_name):
        self.create_excel_doc(self.get_excel_products_and_hubs(ppinfo_api_client))

        self.check_columns(ppinfo_client, sheet_name)

    @allure.title("В икселе Архив корректный набор столбцов")
    @pytest.mark.parametrize('sheet_name',
                             ['Архив',
                              'Удалённые'])
    def test_excel_archive_check_columns(self, ppinfo_api_client, ppinfo_client, sheet_name):
        self.create_excel_doc(self.get_excel_archive(ppinfo_api_client))

        self.check_columns(ppinfo_client, sheet_name, delete_main_product=True)

    @allure.title("Загрузка Excel Все продукты и проверка наличия и последовательности всех листов")
    def test_excel_all_products_check_sheets(self, ppinfo_api_client):
        excel = self.create_excel_doc(self.get_excel_all(ppinfo_api_client))

        with allure.step('Проверяем, что эксель не пустой'):
            assert not excel.empty, "Файл эксель Все документы пустой"

        wb = openpyxl.load_workbook('filename_excel.xlsx')

        with allure.step('Проверяем порядок и наличие всех листов'):
            assert wb.sheetnames == ['Все направления',
                                     'Телеком',
                                     'Финтех',
                                     'Медиа',
                                     'Ad-tech',
                                     'MWS',
                                     'Юрент',
                                     'УК Экосистемы МТС'], "Названия столбцов не совпадают"

    @allure.title("Загрузка Excel Все продукты и проверка наличия и последовательности всех листов")
    def test_excel_all_and_atomic_check_sheets(self, ppinfo_api_client):
        excel = self.create_excel_doc(self.get_excel_all_and_atomic(ppinfo_api_client))

        with allure.step('Проверяем, что эксель не пустой'):
            assert not excel.empty, "Файл эксель Все документы пустой"

        wb = openpyxl.load_workbook('filename_excel.xlsx')

        with allure.step('Проверяем порядок и наличие всех листов'):
            assert wb.sheetnames == ['Все направления',
                                     'Телеком',
                                     'Финтех',
                                     'Медиа',
                                     'Ad-tech',
                                     'MWS',
                                     'Юрент',
                                     'УК Экосистемы МТС'], "Названия столбцов не совпадают"


    @allure.title("Загрузка Excel Все продукты и проверка наличия и последовательности всех листов")
    def test_excel_products_and_hubs_check_sheets(self, ppinfo_api_client):
        excel = self.create_excel_doc(self.get_excel_products_and_hubs(ppinfo_api_client))

        with allure.step('Проверяем, что эксель не пустой'):
            assert not excel.empty, "Файл эксель Все документы пустой"

        wb = openpyxl.load_workbook('filename_excel.xlsx')

        with allure.step('Проверяем порядок и наличие всех листов'):
            assert wb.sheetnames == ['Все направления',
                                     'Телеком',
                                     'Финтех',
                                     'Медиа',
                                     'Ad-tech',
                                     'MWS',
                                     'Юрент',
                                     'УК Экосистемы МТС'], "Названия столбцов не совпадают"

    @allure.title("Загрузка Excel Все продукты и проверка наличия и последовательности всех листов")
    def test_excel_archive_check_sheets(self, ppinfo_api_client):
        excel = self.create_excel_doc(self.get_excel_archive(ppinfo_api_client))

        with allure.step('Проверяем, что эксель не пустой'):
            assert not excel.empty, "Файл эксель Все документы пустой"

        wb = openpyxl.load_workbook('filename_excel.xlsx')

        with allure.step('Проверяем порядок и наличие всех листов'):
            assert wb.sheetnames == ['Архив',
                              'Удалённые'], "Названия столбцов не совпадают"

    @allure.title("Excel Все продукты, проверка количества продуктов на листе Продукты")
    @pytest.mark.parametrize('sheet_name', ['Все направления',
                              'Телеком',
                              'Финтех',
                              'Медиа',
                              'Ad-tech',
                              'MWS',
                              'Юрент',
                              'УК Экосистемы МТС'])
    def test_excel_all_products_check_amount_sheet(self, ppinfo_api_client, ppinfo_client, cache_client, sheet_name):

        '''
        * "Продукты": Внешние + внутренние
        В иксель попадают все продукты вне зависимости присутствия или отсутствия значения по атрибутам. Чтоб сравнить с главной страницей я удаляю строки из икселя где значения по РНД, тип объекта учета или напровления группу пустое
        '''
        self.create_excel_doc(self.get_excel_all(ppinfo_api_client))
        wb = openpyxl.load_workbook('filename_excel.xlsx')
        ws = wb[sheet_name]



        self.delete_rows_from_excel(wb, self.get_column_index(wb, 'R&D'))
        self.delete_rows_from_excel(wb, self.get_column_index(wb, 'Направление группы'))
        self.delete_rows_from_excel(wb, self.get_column_index(wb, 'Тип объекта учёта'))

        products_in_excel = []
        for row in range(2, ws.max_row + 1):
            value = ws.cell(row=row, column=1).value
            products_in_excel.append(value)

        products_in_main_page = self.get_products_by_directions(cache_client, 'Ad-teh' if sheet_name == 'Ad-tech' else sheet_name, 'false')

        set_excel = set(products_in_excel)
        set_main_page = set(products_in_main_page)

        only_in_excel = set_excel - set_main_page
        only_in_main_page = set_main_page - set_excel

        assert not only_in_excel and not only_in_main_page, (f"Продукты, которые есть только в Excel, но нет на главной странице: {only_in_excel} \n"
                                                             f"Продукты, которые есть только на главной странице, но нет в Excel: {only_in_main_page}")



    @allure.title("Excel Все продукты, проверка количества продуктов на листе Продукты без учета атомарных")
    @pytest.mark.parametrize('sheet_name', ['Все направления',
                              'Телеком',
                              'Финтех',
                              'Медиа',
                              'Ad-tech',
                              'MWS',
                              'Юрент',
                              'УК Экосистемы МТС'])
    def test_excel_all_and_atomic_check_amount_sheet(self, ppinfo_api_client, cache_client, sheet_name):
        '''
        * Продукты, включая атомарные
        В исксель попадают все продукты включая атомарные
        '''
        self.create_excel_doc(self.get_excel_all_and_atomic(ppinfo_api_client))
        wb = openpyxl.load_workbook('filename_excel.xlsx')
        ws = wb[sheet_name]

        self.delete_rows_from_excel(wb, self.get_column_index(wb, 'R&D'))
        self.delete_rows_from_excel(wb, self.get_column_index(wb, 'Направление группы'))
        self.delete_rows_from_excel(wb, self.get_column_index(wb, 'Тип объекта учёта'))
        products_in_excel = []
        for row in range(2, ws.max_row + 1):
            value = ws.cell(row=row, column=1).value
            products_in_excel.append(value)

        products_in_main_page = self.get_products_by_directions(cache_client, 'Ad-teh' if sheet_name == 'Ad-tech' else sheet_name, 'true')

        set_excel = set(products_in_excel)
        set_main_page = set(products_in_main_page)

        only_in_excel = set_excel - set_main_page
        only_in_main_page = set_main_page - set_excel

        assert not only_in_excel and not only_in_main_page, (
            f"Продукты, которые есть только в Excel, но нет на главной странице: {only_in_excel} \n"
            f"Продукты, которые есть только на главной странице, но нет в Excel: {only_in_main_page}")


    @allure.title("Excel Все продукты, проверка количества продуктов на Хабы")
    @pytest.mark.parametrize('sheet_name', ['Все направления',
                              'Телеком',
                              'Финтех',
                              'Медиа',
                              'Ad-tech',
                              'MWS',
                              'Юрент',
                              'УК Экосистемы МТС'])
    def test_excel_products_and_hubs_check_amount_sheet(self, ppinfo_api_client, cache_client, sheet_name):
        '''
        * Продукты и хабы
        В иксель попадают все породукты и хабы, включая атомраыне
        '''
        self.create_excel_doc(self.get_excel_products_and_hubs(ppinfo_api_client))

        wb = openpyxl.load_workbook('filename_excel.xlsx')
        ws = wb[sheet_name]

        self.delete_rows_from_excel(wb, self.get_column_index(wb, 'R&D'), is_hub=True)
        self.delete_rows_from_excel(wb, self.get_column_index(wb, 'Направление группы'))
        self.delete_rows_from_excel(wb, self.get_column_index(wb, 'Тип объекта учёта'))

        products_in_excel = []
        for row in range(2, ws.max_row + 1):
            value = ws.cell(row=row, column=1).value
            products_in_excel.append(value)

        products_in_main_page = self.get_products_by_directions(cache_client, 'Ad-teh' if sheet_name == 'Ad-tech' else sheet_name, 'true')
        hubs_in_main_page = self.get_hubs_by_directions(cache_client, 'Ad-teh' if sheet_name == 'Ad-tech' else sheet_name, 'true')

        all_main_page = products_in_main_page + hubs_in_main_page



        set_excel = set(products_in_excel)
        set_main_page = set(all_main_page)

        only_in_excel = set_excel - set_main_page
        only_in_main_page = set_main_page - set_excel

        assert not only_in_excel and not only_in_main_page, (
            f"Продукты, которые есть только в Excel, но нет на главной странице: {only_in_excel} \n"
            f"Продукты, которые есть только на главной странице, но нет в Excel: {only_in_main_page}")


    @allure.title("Excel Все продукты, проверка количества продуктов на листах Архивные")
    @pytest.mark.parametrize('sheet_name',
                             ['Архив',
                              'Удалённые'])
    def test_excel_archive_check_amount_sheet(self, ppinfo_api_client, ppinfo_client, cache_client, sheet_name):
        '''
        * Архив : Архивные внутренние + архивные внешние + архивные хабы
        '''
        self.create_excel_doc(self.get_excel_archive(ppinfo_api_client))

        wb = openpyxl.load_workbook('filename_excel.xlsx')
        ws = wb[sheet_name]

        products_in_excel = []
        for row in range(2, ws.max_row + 1):
            value = ws.cell(row=row, column=1).value
            products_in_excel.append(value)

        products_in_archive = self.get_archive_by_directions(cache_client, 'Архивные' if sheet_name == 'Архив' else sheet_name)

        set_excel = set(products_in_excel)
        set_main_page = set(products_in_archive)

        only_in_excel = set_excel - set_main_page
        only_in_main_page = set_main_page - set_excel

        assert not only_in_excel and not only_in_main_page, (
            f"Продукты, которые есть только в Excel, но нет на главной странице: {only_in_excel} \n"
            f"Продукты, которые есть только на главной странице, но нет в Excel: {only_in_main_page}")


    @allure.title("Получение Excel Все продукты и проверка формата значений в столбце Код BI")
    def test_excel_all_products_check_bi_col(self, ppinfo_client, ppinfo_api_client):
        self.add_col_to_excel(ppinfo_client, "EXTRA_CodeBI")
        self.create_excel_doc(self.get_excel_all(ppinfo_api_client))

        wb = openpyxl.load_workbook('filename_excel.xlsx')

        ws = wb.active

        req_col = [i for i in ws.columns if i[0].value == "Код BI_"][0][1:]
        with allure.step("Проверяем, что все ячейки в столбце код BI имеют формат BI_..."):
            assert all(i.value.startswith("BI_") for i in req_col), 'Некоторые значения не имеют нужный формат'

    @allure.title("Получение Excel Все продукты и проверка формата значений в столбце Название продукта")
    def test_excel_all_products_check_name_col(self, ppinfo_client, ppinfo_api_client):
        self.add_col_to_excel(ppinfo_client, "EXTRA_ProductName")
        self.add_col_to_excel(ppinfo_client, "EXTRA_CodeBI")
        self.create_excel_doc(self.get_excel_all(ppinfo_api_client))

        wb = openpyxl.load_workbook('filename_excel.xlsx')

        ws = wb.active

        cols_name = [i for i in ws.columns if i[0].value == "Название продукта"][0][1:]
        cols_code = [i for i in ws.columns if i[0].value == "Код BI_"][0][1:]

        with allure.step("Проверяем, что все значения являются гиперссылками"):
            assert all(i.hyperlink for i in cols_name), "Не все значения являются гиперссылками"

        with allure.step("Проверяем, что гиперссылки имеют нужный формат"):
            req_links = [f"https://stage.prodboard.mts.ru/product/{code.value}/main".replace(" ", "") for code in
                         cols_code]
            assert all(
                i.hyperlink.target == req_links[cols_name.index(i)] for i in cols_name), "Есть ссылка неверного формата"

        with allure.step("Проверяем, что у гиперссылок есть замещающий текст"):
            assert all(i.hyperlink.display for i in cols_name), "Есть гиперссылка без замещающего текста"

    @allure.title("Получение Excel Все продукты и проверка формата значений в столбце Тип продукта")
    def test_excel_all_products_check_type_col(self, ppinfo_client, ppinfo_api_client):
        self.add_col_to_excel(ppinfo_client, "EXTRA_ProductType")
        self.create_excel_doc(self.get_excel_all(ppinfo_api_client))

        wb = openpyxl.load_workbook('filename_excel.xlsx')

        ws = wb.active

        cols_type = [i for i in ws.columns if i[0].value == "Тип продукта"][0][1:]

        with allure.step("Проверяем, что тип продукта указан верно"):
            assert all(i.value.replace(" ", "") in ["Внешний", "Внутренний"] for i in
                       cols_type), "Есть продукты неизвестного типа"

    @allure.title("Получение Excel Все продукты и проверка формата значений в столбце Юзер (Вице-Президент)")
    def test_excel_all_products_check_user_col(self, ppinfo_client, ppinfo_api_client):
        self.add_col_to_excel(ppinfo_client, "employee_sponsor")
        self.create_excel_doc(self.get_excel_all(ppinfo_api_client))

        wb = openpyxl.load_workbook('filename_excel.xlsx')

        ws = wb.active

        cols_user = [i for i in ws.columns if i[0].value == "Вице-президент"][0][1:]

        pattern1 = re.compile(r"^([А-ЯЁ][а-яё]+)\s+([А-ЯЁ][а-яё]+)\s+\(.+\)$")
        pattern2 = re.compile(r"^([А-ЯЁ][а-яё]+)\s([А-ЯЁ][а-яё]+)\s([А-ЯЁ][а-яё]+)\s\(.+\)$")
        with allure.step("Проверяем, что значения имеют вид ФИО/ФИ(логин)"):
            errors = []

            for owner in cols_user:
                if not (re.search(pattern1, owner.value) or re.search(pattern2,
                                                                      owner.value) or "Не определено1" in owner.value):
                    errors.append(f"Значение {owner.value} не соответствует формату ФИО или ФИО+(логин)")

        assert not errors, "\n".join(errors)

    @allure.title("Получение Excel Все продукты и проверка формата значений в столбце Юзер Email (Вице-Президент)")
    @allure.issue("https://jira.mts.ru/browse/PPI-1809", "PPInfo - Добавить в выгрузки e-mail сотрудников")
    def test_excel_all_products_check_user_email_col(self, ppinfo_client, ppinfo_api_client):
        self.add_col_to_excel(ppinfo_client, "employee_sponsor")
        self.add_col_to_excel(ppinfo_client, "SYSTEM_ExcelIncludeEmailColumn", "excelAdditionalFields")
        self.create_excel_doc(self.get_excel_all(ppinfo_api_client))

        wb = openpyxl.load_workbook('filename_excel.xlsx')

        ws = wb.active

        cols_email = [i for i in ws.columns if i[0].value == "Вице-президент e-mail"][0][1:]

        with allure.step("Проверяем, что email указаны в верном формате"):
            assert all("@" in i.value and "mts" in i.value and ".ru" in i.value for i in cols_email if
                       i.value != "Не определено1" and "user" not in i.value and "None" not in i.value), "Почта неверного формата"

    @allure.title("Получение Excel Все продукты и проверка формата значений в столбце Дата (Дата запуска)")
    def test_excel_all_products_check_date_col(self, ppinfo_client, ppinfo_api_client):
        self.add_col_to_excel(ppinfo_client, "PPinfo_execution_date")
        self.create_excel_doc(self.get_excel_all(ppinfo_api_client))

        wb = openpyxl.load_workbook('filename_excel.xlsx')

        ws = wb.active

        cols_date = [i for i in ws.columns if i[0].value == "Дата запуска"][0][1:]

        with allure.step("Проверяем, что дата приходит в нужном формате"):
            assert all(re.search("([0-9]{2}\.[0-9]{2}\.[0-9]{4})", date.value) for date in cols_date if
                       date.value != "Не определено"), "Некоторые даты не в формате ДД.ММ.ГГГГ"

    @allure.title("Получение Excel Все продукты и проверка формата значений в столбце код Oracle")
    @allure.issue('https://jira.mts.ru/browse/PPI-2457', 'PPInfo - Убрать пробелы после кодов Oracle')
    def test_excel_all_products_check_oracle_code_col(self, ppinfo_client, ppinfo_api_client):
        self.add_col_to_excel(ppinfo_client, "PPinfo_execution_date")
        self.create_excel_doc(self.get_excel_all(ppinfo_api_client))

        wb = openpyxl.load_workbook('filename_excel.xlsx')

        ws = wb.active

        cols_code = [i for i in ws.columns if i[0].value == "Новый код продукта в Oracle"][0][1:]

        with allure.step('Проверяем, что нет пробелов в конце/начале значения'):
            assert all(i.value[-1] != ' ' or i.value[0] != ' ' for i in cols_code), 'Есть пробел в коде Oracle'

    @allure.title(
        "Получение Excel Все продукты и проверка формата значений в столбце Ссылка/системная (Тест Вычисляемая ссылка)")
    def test_excel_all_products_check_system_link_col(self, ppinfo_client, ppinfo_api_client, clear_excel):
        self.add_col_to_excel(ppinfo_client, "test_vychisliaemaia_ssylka")
        self.create_excel_doc(self.get_excel_all(ppinfo_api_client))

        wb = openpyxl.load_workbook('filename_excel.xlsx')

        ws = wb.active

        cols_link = [i for i in ws.columns if i[0].value == "тест вычисляемая ссылка"][0][1:]

        with allure.step("Проверяем, что все значения являются гиперссылками"):
            assert all(i.hyperlink for i in cols_link), "Не все значения являются гиперссылками"

        with allure.step("Проверяем, что гиперссылки имеют нужный формат"):
            assert all(i.hyperlink.target.startswith("  http://radar.mcc.mts-corp.ru/product/mcc/BI_") for i in
                       cols_link), "Некоторые ссылки имеют не тот формат"

        with allure.step("Проверяем, что у гиперссылок есть замещающий текст"):
            assert all(i.hyperlink.display == "тест вычисляемая ссылка" for i in
                       cols_link), "Есть гиперссылка без замещающего текста"

    @allure.title("Получение Excel Все продукты и проверка формата значений в столбце Множ ссылок")
    @allure.issue('https://jira.mts.ru/browse/PPI-546', 'Формат ссылок в выгрузках Excel')
    def test_excel_all_products_check_multilink_col(self, ppinfo_client, ppinfo_api_client, clear_excel):
        self.add_col_to_excel(ppinfo_client, "Test_mnozh_ssylki")
        self.create_excel_doc(self.get_excel_all(ppinfo_api_client))

        wb = openpyxl.load_workbook('filename_excel.xlsx')

        sheet = wb.active

        row_value = 'BI_5691'
        col_value = 'Тест множ ссылки (для тестов, аттр не менять )'

        with allure.step('Ищем номер строки и столбца'):
            try:
                row_num = next(
                    row[0].row for row in sheet.iter_rows(min_row=1, max_row=sheet.max_row, min_col=1, max_col=1)
                    if row[0].value.replace(" ", "") == row_value)
                col_num = next(cell.column for column_cells in
                               sheet.iter_cols(min_row=1, max_row=1, min_col=1, max_col=sheet.max_column)
                               for cell in column_cells if col_value in cell.value)
            except StopIteration:
                pytest.fail("Could not find the specified cell.")

        pattern = r"https?://\S+"
        cell_value = sheet.cell(row=row_num, column=col_num).value

        with allure.step(
                'Проверяем что формат множественных ссылок равен - Текст ссылки {пробел} Ссылка, текст ссылки {пробел} Ссылка'):
            assert re.findall(pattern,
                              cell_value), f"Значение клетки '{cell_value}' не соответствует ожидаемому шаблону."

    @allure.title('Получение Excel Все продукты и проверка формата значений в столбце Тех.Комитет_2')
    @allure.issue('https://jira.mts.ru/browse/PPI-3573', 'PPInfo - Выгружать ссылку на ТК в виде даты')
    def test_excel_all_products_check_tech_committee_col(self, ppinfo_api_client, clear_excel):
        self.create_excel_doc(self.get_excel_all(ppinfo_api_client))

        wb = openpyxl.load_workbook('filename_excel.xlsx')

        ws = wb.active

        cols_code = [i for i in ws.columns if i[0].value == "Тех.Комитет_2"][0][1:]

        with allure.step('Проверяем, что значения начинаются как ссылки'):
            for i in cols_code:
                if i.value != 'Не определено':
                    assert i.hyperlink, 'В значении Тех.Комитет_2 указана не ссылка'
                    assert datetime.strptime(i.value, "%d.%m.%Y"), 'Значение не в формате ДД:ММ:ГГ'

    ##################################################### Excel Изменение атрибутов
    @allure.title("Загрузка Excel Изменение атрибутов и проверка столбцов")
    @allure.issue('https://jira.mts.ru/browse/PPI-438', 'PPInfo - Выгрузка Excel с датами изменения атрибутов')
    def test_excel_attr_updates_check_cols(self, ppinfo_api_client, clear_excel):
        params = {
            "attributes": "employee_senior_PO,PPinfo_web_app,PPinfo_execution_date,Mnozhestvo,Odin_produkt,PPinfo_product_problem"
        }
        excel = self.create_excel_doc(self.get_excel_update(ppinfo_api_client, params))

        with allure.step('Проверяем, что эксель не пустой'):
            assert not excel.empty, "Файл эксель Все документы пустой"

        with allure.step('Проверяем, что все нужные столбцы присутствуют'):
            assert {'Код_BI', 'Название продукта', 'Тип продукта', 'Статус', 'Дата изменения',
                    'Структурный тип продукта', 'Дата изменения', 'Senior Product Owner',
                    'Дата изменения', 'Web, app', 'Дата изменения', 'Дата запуска', 'Дата изменения',
                    'Множество', 'Дата изменения', 'Один продукт', 'Дата изменения', 'Проблема',
                    'Дата изменения'}.issubset(excel.columns), "Столбцы не совпадают"

    @allure.title("Загрузка Excel Изменение атрибутов и проверка названия листа")
    @allure.issue('https://jira.mts.ru/browse/PPI-438', 'PPInfo - Выгрузка Excel с датами изменения атрибутов')
    def test_excel_attr_updates_check_sheet(self, ppinfo_api_client, clear_excel):
        params = {
            "attributes": "employee_senior_PO"
        }
        self.create_excel_doc(self.get_excel_update(ppinfo_api_client, params))
        wb = openpyxl.load_workbook('filename_excel.xlsx')

        with allure.step("Проверяем, что название листа - сегодняшняя дата"):
            current_date = datetime.now().strftime("%d.%m.%Y")
            assert wb.sheetnames[0] == current_date, f"{wb.sheetnames[0]} != {current_date}"

    @allure.title("Загрузка Excel Изменение атрибутов и проверка, что даты изменяются")
    @allure.issue('https://jira.mts.ru/browse/PPI-438', 'PPInfo - Выгрузка Excel с датами изменения атрибутов')
    def test_excel_attr_updates_check_date(self, ppinfo_api_client, clear_excel):
        params = {
            "attributes": "PPInfo_showcase"
        }
        self.create_excel_doc(self.get_excel_update(ppinfo_api_client, params))
        wb = openpyxl.load_workbook('filename_excel.xlsx')

        ws = wb.active

        current_date = datetime.now().strftime("%d.%m.%Y")
        yesterday = (datetime.now() - timedelta(days=1)).strftime("%d.%m.%Y")
        with allure.step('Проверяем, что дата меняется'):
            dates = [i.value.strftime("%d.%m.%Y") for i in ws["I"][1:] if i.value is not None]

            assert any(yesterday == date or current_date == date for date in
                       dates), f'Значения Витрины менялись в даты {dates}'

    @allure.title("Получение Excel Изменение атрибутов и проверка формата значений в столбце Код BI")
    def test_excel_attr_updates_check_bi_col(self, ppinfo_api_client, clear_excel):
        params = {
            "attributes": "PPInfo_showcase"
        }
        self.create_excel_doc(self.get_excel_update(ppinfo_api_client, params))

        wb = openpyxl.load_workbook('filename_excel.xlsx')

        ws = wb.active

        req_col = [i for i in ws.columns if i[0].value == "Код_BI"][0][1:]
        with allure.step("Проверяем, что все ячейки в столбце код BI имеют формат BI_..."):
            assert all(i.value.startswith("BI_") for i in req_col), 'Некоторые значения не имеют нужный формат'

    @allure.title("Получение Excel Изменение атрибутов и проверка формата значений в столбце Название продукта")
    def test_excel_attr_updates_check_name_col(self, ppinfo_api_client, clear_excel):
        params = {
            "attributes": "PPInfo_showcase"
        }
        self.create_excel_doc(self.get_excel_update(ppinfo_api_client, params))

        wb = openpyxl.load_workbook('filename_excel.xlsx')

        ws = wb.active

        cols_name = [i for i in ws.columns if i[0].value == "Название продукта"][0][1:]
        cols_code = [i for i in ws.columns if i[0].value == "Код_BI"][0][1:]

        with allure.step("Проверяем, что все значения являются гиперссылками"):
            assert all(i.hyperlink for i in cols_name), "Не все значения являются гиперссылками"

        with allure.step("Проверяем, что гиперссылки имеют нужный формат"):
            req_links = [f"https://stage.prodboard.mts.ru/product/{code.value}/main" for code in cols_code]
            assert all(
                i.hyperlink.target == req_links[cols_name.index(i)] for i in cols_name), "Есть ссылка неверного формата"

        with allure.step("Проверяем, что у гиперссылок есть замещающий текст"):
            assert all(i.hyperlink.display for i in cols_name), "Есть гиперссылка без замещающего текста"

    @allure.title("Получение Excel Изменение атрибутов и проверка формата значений в столбце Тип продукта")
    def test_excel_attr_updates_check_type_col(self, ppinfo_api_client, clear_excel):
        params = {
            "attributes": "PPInfo_showcase"
        }
        self.create_excel_doc(self.get_excel_update(ppinfo_api_client, params))

        wb = openpyxl.load_workbook('filename_excel.xlsx')

        ws = wb.active

        cols_type = [i for i in ws.columns if i[0].value == "Тип продукта"][0][1:]

        with allure.step("Проверяем, что тип продукта указан верно"):
            assert all(i.value in ["Внешний", "Внутренний"] for i in cols_type), "Есть продукты неизвестного типа"

    ##################################################### Качаем Excel Внешние и Внутренние на дату и на период

    @allure.title("Загрузка Excel на период и проверка названия листа ")
    def test_excel_story_period_check_sheet(self, ppinfo_api_client, clear_excel):
        current_date = datetime.now().date()
        yesterday = (datetime.now() - timedelta(days=3)).date()
        params = self.get_story_data(date_from=str(yesterday), date_to=str(current_date))

        excel = self.create_excel_doc(self.get_story_excel(ppinfo_api_client, params))

        with allure.step('Проверяем, что эксель не пустой'):
            assert not excel.empty, "Файл эксель на период пустой"

        wb = openpyxl.load_workbook('filename_excel.xlsx')

        with allure.step("Проверяем, что название листа в верном формате"):
            assert wb.sheetnames[0] == f'Продукты и хабы'

    @allure.title("Загрузка Excel на дату и проверка названия листа ")
    def test_excel_story_date_check_sheet(self, ppinfo_api_client, clear_excel):
        yesterday = (datetime.now() - timedelta(days=3)).date()
        params = self.get_story_data(date_from=str(yesterday))

        excel = self.create_excel_doc(self.get_story_excel(ppinfo_api_client, params))

        with allure.step('Проверяем, что эксель не пустой'):
            assert not excel.empty, "Файл эксель на период пустой"

        wb = openpyxl.load_workbook('filename_excel.xlsx')

        with allure.step("Проверяем, что название листа в верном формате"):
            assert wb.sheetnames[0] == f'Продукты и хабы'

    @allure.title("Загрузка Excel на период и проверка столбцов ")
    def test_excel_story_period_check_cols(self, ppinfo_api_client, clear_excel):
        current_date = datetime.now().date()
        yesterday = (datetime.now() - timedelta(days=3)).date()
        params = self.get_story_data(date_from=str(yesterday), date_to=str(current_date))

        excel = self.create_excel_doc(self.get_story_excel(ppinfo_api_client, params))

        with allure.step("Проверяем, что все столбцы в таблице заполнены"):
            empty_cols = [col for col in excel.columns if excel[col].isnull().all()]

            assert not empty_cols, f'Столбцы {empty_cols} пустые'

        with allure.step('Проверяем, что все нужные столбцы присутствуют'):
            assert {'Код BI', 'Название продукта', 'Название продукта', 'Тип продукта', 'Тип продукта',
                    'Структурный тип продукта', 'Структурный тип продукта', 'Статус', 'Статус'}.issubset(
                excel.columns), "Столбцы не совпадают"

        wb = openpyxl.load_workbook('filename_excel.xlsx')
        ws = wb.active

        with allure.step("Проверяем, что на столбцах присутствует дата"):
            time_check = [None] + [yesterday.strftime("%d.%m.%Y"), current_date.strftime("%d.%m.%Y")] * (
                    (ws.max_column - 1) // 2)
            time_check = iter(time_check)
            assert all(i[1].value == next(time_check) for i in ws.columns), "Даты не в том формате"

    @allure.title("Загрузка Excel на дату и проверка столбцов ")
    def test_excel_story_date_check_cols(self, ppinfo_api_client, clear_excel):
        yesterday = (datetime.now() - timedelta(days=3)).date()
        params = self.get_story_data(date_from=str(yesterday))

        excel = self.create_excel_doc(self.get_story_excel(ppinfo_api_client, params))

        with allure.step("Проверяем, что все столбцы в таблице заполнены"):
            empty_cols = [col for col in excel.columns if excel[col].isnull().all()]

            assert not empty_cols, f'Столбцы {empty_cols} пустые'

        with allure.step('Проверяем, что все нужные столбцы присутствуют'):
            assert {'Код BI', 'Название продукта', 'Тип продукта', 'Структурный тип продукта', 'Статус'}.issubset(
                excel.columns), "Столбцы не совпадают"

        wb = openpyxl.load_workbook('filename_excel.xlsx')
        ws = wb.active

        with allure.step("Проверяем, что на столбцах отсутсвует дата"):
            time_check = [None] + [yesterday.strftime("%d.%m.%Y")] * (ws.max_column - 1)
            time_check = iter(time_check)
            assert all(i[1].value != next(time_check) for i in ws.columns), "Даты присутствуют"

    @allure.title("Загрузка Excel на период с атрибутами")
    def test_excel_story_period_check_cols_attr(self, ppinfo_api_client, clear_excel):
        current_date = datetime.now().date()
        yesterday = (datetime.now() - timedelta(days=3)).date()
        params = self.get_story_data(date_from=str(yesterday), date_to=str(current_date),
                                     attributes="employee_chief_PO,PPinfo_MTS_Brand,PPInfo_site_landing")

        self.create_excel_doc(self.get_story_excel(ppinfo_api_client, params))

        wb = openpyxl.load_workbook('filename_excel.xlsx')
        ws = wb.active
        cols_names = [i[0].value for i in ws.columns]

        with allure.step("Проверяем, что столбцы появились"):
            assert all(name in cols_names for name in
                       ["Chief product owner", "Бренд МТС", "Сайт"]), "Некоторые атрибуты не появились"

    @allure.title("Загрузка Excel на дату с атрибутами")
    def test_excel_story_date_check_cols_attr(self, ppinfo_api_client, clear_excel):
        yesterday = (datetime.now() - timedelta(days=3)).date()
        params = self.get_story_data(date_from=str(yesterday),
                                     attributes="employee_chief_PO,PPinfo_MTS_Brand,PPInfo_site_landing")

        self.create_excel_doc(self.get_story_excel(ppinfo_api_client, params))

        wb = openpyxl.load_workbook('filename_excel.xlsx')
        ws = wb.active
        cols_names = [i[0].value for i in ws.columns]

        with allure.step("Проверяем, что столбцы появились"):
            assert all(name in cols_names for name in
                       ["Chief product owner", "Бренд МТС", "Сайт"]), "Некоторые атрибуты не появились"

    @allure.title("Загрузка Excel на период и проверка формата значений в столбце Код BI")
    def test_excel_story_period_check_bi_col(self, ppinfo_api_client, clear_excel):
        current_date = datetime.now().date()
        yesterday = (datetime.now() - timedelta(days=3)).date()
        params = self.get_story_data(date_from=str(yesterday), date_to=str(current_date))
        self.create_excel_doc(self.get_story_excel(ppinfo_api_client, params))

        wb = openpyxl.load_workbook('filename_excel.xlsx')

        ws = wb.active

        req_col = [i for i in ws.columns if i[0].value == "Код BI"][0][2:]
        with allure.step("Проверяем, что все ячейки в столбце код BI имеют формат BI_..."):
            assert all(i.value.startswith("BI_") for i in req_col), 'Некоторые значения не имеют нужный формат'

    @allure.title("Загрузка Excel на дату и проверка формата значений в столбце Код BI")
    def test_excel_story_date_check_bi_col(self, ppinfo_api_client, clear_excel):
        yesterday = (datetime.now() - timedelta(days=3)).date()
        params = self.get_story_data(date_from=str(yesterday))
        self.create_excel_doc(self.get_story_excel(ppinfo_api_client, params))

        wb = openpyxl.load_workbook('filename_excel.xlsx')

        ws = wb.active

        req_col = [i for i in ws.columns if i[0].value == "Код BI"][0][1:]
        with allure.step("Проверяем, что все ячейки в столбце код BI имеют формат BI_..."):
            assert all(i.value.startswith("BI_") for i in req_col), 'Некоторые значения не имеют нужный формат'

    @allure.title("Загрузка Excel на период и проверка формата значений в столбце Название продукта")
    def test_excel_story_period_check_name_col(self, ppinfo_api_client, clear_excel):
        current_date = datetime.now().date()
        yesterday = (datetime.now() - timedelta(days=3)).date()
        params = self.get_story_data(date_from=str(yesterday), date_to=str(current_date))
        self.create_excel_doc(self.get_story_excel(ppinfo_api_client, params))

        wb = openpyxl.load_workbook('filename_excel.xlsx')

        ws = wb.active

        cols_name = [i for i in ws.columns if i[0].value == "Название продукта"][0][2:]
        cols_code = [i for i in ws.columns if i[0].value == "Код BI"][0][2:]

        with allure.step("Проверяем, что все значения являются гиперссылками"):
            assert all(i.hyperlink for i in cols_name if i.value is not None), "Не все значения являются гиперссылками"

        with allure.step("Проверяем, что гиперссылки имеют нужный формат"):
            req_links = [f"https://stage.prodboard.mts.ru/product/{code.value}/main" for code in cols_code]
            assert all(
                i.hyperlink.target == req_links[cols_name.index(i)] for i in
                cols_name if i.value is not None), "Есть ссылка неверного формата"

        with allure.step("Проверяем, что у гиперссылок есть замещающий текст"):
            assert all(i.value for i in cols_name if i.value is not None), "Есть гиперссылка без замещающего текста"

    @allure.title("Загрузка Excel на дату и проверка формата значений в столбце Название продукта")
    def test_excel_story_date_check_name_col(self, ppinfo_api_client, clear_excel):
        yesterday = (datetime.now() - timedelta(days=3)).date()
        params = self.get_story_data(date_from=str(yesterday))
        self.create_excel_doc(self.get_story_excel(ppinfo_api_client, params))

        wb = openpyxl.load_workbook('filename_excel.xlsx')

        ws = wb.active

        cols_name = [i for i in ws.columns if i[0].value == "Название продукта"][0][1:]
        cols_code = [i for i in ws.columns if i[0].value == "Код BI"][0][1:]

        with allure.step("Проверяем, что все значения являются гиперссылками"):
            assert all(i.hyperlink for i in cols_name), "Не все значения являются гиперссылками"

        with allure.step("Проверяем, что гиперссылки имеют нужный формат"):
            req_links = [f"https://stage.prodboard.mts.ru/product/{code.value}/main" for code in cols_code]
            assert all(
                i.hyperlink.target == req_links[cols_name.index(i)] for i in
                cols_name), "Есть ссылка неверного формата"

        with allure.step("Проверяем, что у гиперссылок есть замещающий текст"):
            assert all(i.value for i in cols_name), "Есть гиперссылка без замещающего текста"

    @allure.title("Загрузка Excel на период и проверка формата значений в столбце тип продукта")
    def test_excel_story_period_check_type_col(self, ppinfo_api_client, clear_excel):
        current_date = datetime.now().date()
        yesterday = (datetime.now() - timedelta(days=3)).date()
        params = self.get_story_data(date_from=str(yesterday), date_to=str(current_date))
        self.create_excel_doc(self.get_story_excel(ppinfo_api_client, params))

        wb = openpyxl.load_workbook('filename_excel.xlsx')

        ws = wb.active

        cols_type = [i for i in ws.columns if i[0].value == "Тип продукта"][1][2:]

        with allure.step("Проверяем, что тип продукта указан верно"):
            incorrect_types = [i.value for i in cols_type if i.value not in ["Внешний", "Внутренний"]]
            if len(incorrect_types) > 15:
                assert False, f"Есть продукты неизвестного типа {incorrect_types}"  # Ужасный костыль, так как на стаге есть странные данные, и по некоторым продуктам не указан тип, на проде все норм. На стаге 12 таких продуктов

    @allure.title("Загрузка Excel на дату и проверка формата значений в столбце тип продукта")
    def test_excel_story_date_check_type_col(self, ppinfo_api_client, clear_excel):
        yesterday = (datetime.now() - timedelta(days=3)).date()
        params = self.get_story_data(date_from=str(yesterday))
        self.create_excel_doc(self.get_story_excel(ppinfo_api_client, params))

        wb = openpyxl.load_workbook('filename_excel.xlsx')

        ws = wb.active

        cols_type = [i for i in ws.columns if i[0].value == "Тип продукта"][0][1:]

        with allure.step("Проверяем, что тип продукта указан верно"):
            assert all(i.value in ["Внешний", "Внутренний"] for i in cols_type if
                       i.value is not None), "Есть продукты неизвестного типа"

    @allure.title("Загрузка Excel на период и кол-во продуктов в столбце Продукты и хабы")
    def test_excel_story_period_count_product_product_and_hubs(self, ppinfo_api_client, ppinfo_client, cache_client,
                                                               clear_excel):
        current_date = datetime.now().date()
        yesterday = (datetime.now() - timedelta(days=3)).date()
        params = self.get_story_data(date_from=str(yesterday), date_to=str(current_date), attributes='R&D,Napravlenie_gruppy,Tip_obieekta_ucheta')
        self.create_excel_doc(self.get_story_excel(ppinfo_api_client, params))

        wb = openpyxl.load_workbook('filename_excel.xlsx')

        ws = wb['Продукты и хабы']

        self.delete_rows_from_excel(wb, self.get_column_index(wb, 'R&D', sheet_name='Продукты и хабы'), is_hub=True,
                                    sheet_name='Продукты и хабы')
        self.delete_rows_from_excel(wb, self.get_column_index(wb, 'Направление группы', sheet_name='Продукты и хабы'),
                                    sheet_name='Продукты и хабы')
        self.delete_rows_from_excel(wb, self.get_column_index(wb, 'Тип объекта учёта', sheet_name='Продукты и хабы'),
                                    sheet_name='Продукты и хабы')

        products_in_excel = []
        for row in range(2, ws.max_row + 1):
            value = ws.cell(row=row, column=1).value
            products_in_excel.append(value)

        products_in_excel.remove(None) # Костыль чтоб удалить Нон из второй строки

        products_in_main_page = self.get_products_by_directions(cache_client,
                                                                'Все направления',
                                                                'true')
        hubs_in_main_page = self.get_hubs_by_directions(cache_client,
                                                        'Все направления', 'true')

        all_main_page = products_in_main_page + hubs_in_main_page

        set_excel = set(products_in_excel)
        set_main_page = set(all_main_page)

        only_in_excel = set_excel - set_main_page
        only_in_main_page = set_main_page - set_excel

        assert not only_in_excel and not only_in_main_page, (
            f"Продукты, которые есть только в Excel, но нет на главной странице: {only_in_excel} \n"
            f"Продукты, которые есть только на главной странице, но нет в Excel: {only_in_main_page}")

    @allure.title("Загрузка Excel на период и кол-во продуктов в столбце Архив")
    def test_excel_story_period_count_product_archive(self, ppinfo_api_client, ppinfo_client, cache_client, clear_excel):
        current_date = datetime.now().date()
        yesterday = (datetime.now() - timedelta(days=3)).date()
        params = self.get_story_data(date_from=str(yesterday), date_to=str(current_date), attributes='R&D,Napravlenie_gruppy,Tip_obieekta_ucheta')
        self.create_excel_doc(self.get_story_excel(ppinfo_api_client, params))

        wb = openpyxl.load_workbook('filename_excel.xlsx')
        ws = wb['Архив']

        self.delete_rows_from_excel(wb, self.get_column_index(wb, 'R&D', sheet_name='Архив'), is_hub=True,
                                    sheet_name='Архив')
        self.delete_rows_from_excel(wb, self.get_column_index(wb, 'Направление группы', sheet_name='Архив'),
                                    sheet_name='Архив')
        self.delete_rows_from_excel(wb, self.get_column_index(wb, 'Тип объекта учёта', sheet_name='Архив'),
                                    sheet_name='Архив')

        products_in_excel = []
        for row in range(2, ws.max_row + 1):
            value = ws.cell(row=row, column=1).value
            products_in_excel.append(value)

        products_in_excel.remove(None) # Костыль чтоб удалить Нон из второй строки


        products_in_archive_page = self.get_archive_by_directions(cache_client, 'Архивные')
        atomic_archive = list((set(get_atomic_products()) - set(self.get_only_active_atomics(ppinfo_client))) - set(self.get_only_deleted_atomics(ppinfo_client)))
        atomic_arcive_bi = ['BI_' + str(atom_code) for atom_code in atomic_archive]


        archive = products_in_archive_page + atomic_arcive_bi


        set_excel = set(products_in_excel)
        set_deleted_page = set(archive)

        only_in_excel = set_excel - set_deleted_page
        only_in_deleted_page = set_deleted_page - set_excel

        assert not only_in_excel and not only_in_deleted_page, (
            f"Продукты, которые есть только в Excel, но нет на главной странице: {only_in_excel} \n"
            f"Продукты, которые есть только на главной странице, но нет в Excel: {only_in_deleted_page}")



    @allure.title("Загрузка Excel на период и кол-во продуктов в столбце Удаленные")
    def test_excel_story_period_count_product_deleted(self, ppinfo_api_client, ppinfo_client, cache_client,
                                                      clear_excel):
        current_date = datetime.now().date()
        yesterday = (datetime.now() - timedelta(days=3)).date()
        params = self.get_story_data(date_from=str(yesterday), date_to=str(current_date), attributes='R&D,Napravlenie_gruppy,Tip_obieekta_ucheta')
        self.create_excel_doc(self.get_story_excel(ppinfo_api_client, params))

        wb = openpyxl.load_workbook('filename_excel.xlsx')

        ws = wb['Удаленные продукты']


        self.delete_rows_from_excel(wb, self.get_column_index(wb, 'R&D', sheet_name='Удаленные продукты'), is_hub=True,
                                    sheet_name='Удаленные продукты')
        self.delete_rows_from_excel(wb, self.get_column_index(wb, 'Направление группы', sheet_name='Удаленные продукты'),
                                    sheet_name='Удаленные продукты')
        self.delete_rows_from_excel(wb, self.get_column_index(wb, 'Тип объекта учёта', sheet_name='Удаленные продукты'),
                                    sheet_name='Удаленные продукты')

        products_in_excel = []
        for row in range(2, ws.max_row + 1):
            value = ws.cell(row=row, column=1).value
            products_in_excel.append(value)

        products_in_excel.remove(None) # Костыль чтоб удалить Нон из второй строки



        deleted = self.get_archive_by_directions(cache_client, 'Удалённые') + ['BI_' + str(atom_code) for atom_code in self.get_only_deleted_atomics(ppinfo_client)]

        set_excel = set(products_in_excel)
        set_deleted_page = set(deleted)

        only_in_excel = set_excel - set_deleted_page
        only_in_deleted_page = set_deleted_page - set_excel

        assert not only_in_excel and not only_in_deleted_page, (
            f"Продукты, которые есть только в Excel, но нет на главной странице: {only_in_excel} \n"
            f"Продукты, которые есть только на главной странице, но нет в Excel: {only_in_deleted_page}")

    @allure.title("Загрузка Excel на период и кол-во продуктов в столбце Продукты и хабы")
    def test_excel_story_date_count_product_product_and_hubs(self, ppinfo_api_client, ppinfo_client, cache_client,
                                                             clear_excel):
        today = datetime.now().date()
        params = self.get_story_data(date_from=str(today), attributes='R&D,Napravlenie_gruppy,Tip_obieekta_ucheta')
        self.create_excel_doc(self.get_story_excel(ppinfo_api_client, params))

        wb = openpyxl.load_workbook('filename_excel.xlsx')

        ws = wb['Продукты и хабы']

        self.delete_rows_from_excel(wb, self.get_column_index(wb, 'R&D', sheet_name='Продукты и хабы'), is_hub=True, sheet_name='Продукты и хабы')
        self.delete_rows_from_excel(wb, self.get_column_index(wb, 'Направление группы', sheet_name='Продукты и хабы'), sheet_name='Продукты и хабы')
        self.delete_rows_from_excel(wb, self.get_column_index(wb, 'Тип объекта учёта', sheet_name='Продукты и хабы'), sheet_name='Продукты и хабы')


        products_in_excel = []
        for row in range(2, ws.max_row + 1):
            value = ws.cell(row=row, column=1).value
            products_in_excel.append(value)

        products_in_main_page = self.get_products_by_directions(cache_client,
                                                                'Все направления',
                                                                'true')
        hubs_in_main_page = self.get_hubs_by_directions(cache_client,
                                                        'Все направления', 'true')

        all_main_page = products_in_main_page + hubs_in_main_page

        set_excel = set(products_in_excel)
        set_main_page = set(all_main_page)

        only_in_excel = set_excel - set_main_page
        only_in_main_page = set_main_page - set_excel

        assert not only_in_excel and not only_in_main_page, (
            f"Продукты, которые есть только в Excel, но нет на главной странице: {only_in_excel} \n"
            f"Продукты, которые есть только на главной странице, но нет в Excel: {only_in_main_page}")


    @allure.title("Загрузка Excel на Дату и кол-во продуктов в столбце Архив")
    def test_excel_story_date_count_product_archive(self, ppinfo_api_client, ppinfo_client, cache_client, clear_excel):
        today = datetime.now().date()
        params = self.get_story_data(date_from=str(today), attributes='R&D,Napravlenie_gruppy,Tip_obieekta_ucheta')
        self.create_excel_doc(self.get_story_excel(ppinfo_api_client, params))

        wb = openpyxl.load_workbook('filename_excel.xlsx')
        ws = wb['Архив']

        self.delete_rows_from_excel(wb, self.get_column_index(wb, 'R&D', sheet_name='Архив'), is_hub=True,
                                    sheet_name='Архив')
        self.delete_rows_from_excel(wb, self.get_column_index(wb, 'Направление группы', sheet_name='Архив'),
                                    sheet_name='Архив')
        self.delete_rows_from_excel(wb, self.get_column_index(wb, 'Тип объекта учёта', sheet_name='Архив'),
                                    sheet_name='Архив')

        products_in_excel = []
        for row in range(2, ws.max_row + 1):
            value = ws.cell(row=row, column=1).value
            products_in_excel.append(value)

        products_in_archive_page = self.get_archive_by_directions(cache_client, 'Архивные')
        atomic_archive = list((set(get_atomic_products()) - set(self.get_only_active_atomics(ppinfo_client))) - set(
            self.get_only_deleted_atomics(ppinfo_client)))
        atomic_arcive_bi = ['BI_' + str(atom_code) for atom_code in atomic_archive]

        archive = products_in_archive_page + atomic_arcive_bi

        set_excel = set(products_in_excel)
        set_deleted_page = set(archive)

        only_in_excel = set_excel - set_deleted_page
        only_in_deleted_page = set_deleted_page - set_excel

        assert not only_in_excel and not only_in_deleted_page, (
            f"Продукты, которые есть только в Excel, но нет на главной странице: {only_in_excel} \n"
            f"Продукты, которые есть только на главной странице, но нет в Excel: {only_in_deleted_page}")


    @allure.title("Загрузка Excel на Дату и кол-во продуктов в столбце Удаленные")
    def test_excel_story_date_count_product_deleted(self, ppinfo_api_client, ppinfo_client, cache_client, clear_excel):
        today = datetime.now().date()
        params = self.get_story_data(date_from=str(today), attributes='R&D,Napravlenie_gruppy,Tip_obieekta_ucheta')
        self.create_excel_doc(self.get_story_excel(ppinfo_api_client, params))

        wb = openpyxl.load_workbook('filename_excel.xlsx')

        ws = wb['Удаленные продукты']

        self.delete_rows_from_excel(wb, self.get_column_index(wb, 'R&D', sheet_name='Удаленные продукты'), is_hub=True,
                                    sheet_name='Удаленные продукты')
        self.delete_rows_from_excel(wb,
                                    self.get_column_index(wb, 'Направление группы', sheet_name='Удаленные продукты'),
                                    sheet_name='Удаленные продукты')
        self.delete_rows_from_excel(wb, self.get_column_index(wb, 'Тип объекта учёта', sheet_name='Удаленные продукты'),
                                    sheet_name='Удаленные продукты')

        products_in_excel = []
        for row in range(2, ws.max_row + 1):
            value = ws.cell(row=row, column=1).value
            products_in_excel.append(value)

        deleted = self.get_archive_by_directions(cache_client, 'Удалённые') + ['BI_' + str(atom_code) for atom_code in
                                                                               self.get_only_deleted_atomics(
                                                                                   ppinfo_client)]

        set_excel = set(products_in_excel)
        set_deleted_page = set(deleted)

        only_in_excel = set_excel - set_deleted_page
        only_in_deleted_page = set_deleted_page - set_excel

        assert not only_in_excel and not only_in_deleted_page, (
            f"Продукты, которые есть только в Excel, но нет на главной странице: {only_in_excel} \n"
            f"Продукты, которые есть только на главной странице, но нет в Excel: {only_in_deleted_page}")
    ##################################################### Список атрибутов

    @allure.title('Получения списка атрибутов')
    def test_get_attribute_list(self, ppinfo_api_client):

        self.get_attributes_list(ppinfo_api_client)

    ##################################################### Вкладка Сотрудники

    @allure.title('Получение инфы о доп, уволенных и неактивных юзерах и проверка порядка вкладок')
    @allure.issue('https://jira.mts.ru/browse/PPI-1424', 'PPInfo - Отчет по неактивным пользователям')
    def test_get_users_report_order(self, ppinfo_api_client):

        assert [item['name'] for item in self.get_users_report(ppinfo_api_client)] == ['Уволенные сотрудники',
                                                                                       'Уволенные кураторы',
                                                                                       'Неактивные сотрудники',
                                                                                       'Неактивные кураторы',
                                                                                       'Дополнительные сотрудники',
                                                                                       'Дополнительные кураторы']

    @allure.title('В отчет о сотрудниках не должна попадать инфа про удаленные продукты')
    @allure.issue('https://jira.mts.ru/browse/PPI-1675',
                  'PPInfo - В раздел "Сотрудники" не должны попадать удаленные продукты')
    def test_get_users_report_not_deleted_product(self, ppinfo_api_client):

        for prod in self.get_users_report(ppinfo_api_client):
            if prod['name'] == 'Уволенные сотрудники':
                for user in prod['users']:
                    if user['login'] == 'ikaverin':
                        assert len(user['positions']) == 1, "В сотрудники попал удаленный продкукт"

    @allure.title('Продукты с Инициированным закрытием должны попадать в отчет')
    @allure.issue('https://jira.mts.ru/browse/PPI-3498',
                  'PPInfo - Удаленные сотрудники у продукта с статусом "Инициировано закрытие" (в админку)')
    def test_get_users_report_int_close(self, ppinfo_api_client):

        for prod in self.get_users_report(ppinfo_api_client):
            if prod['name'] == 'Уволенные сотрудники':
                for user in prod['users']:
                    if user['login'] == 'ikaverin':
                        assert any(product['id'] == 'BI_213' for product in user['positions'][0]['products'])

    @allure.title('В отчет о сотрудниках не должна попадать инфа про архивные продукты')
    @allure.issue('https://jira.mts.ru/browse/PPI-1769',
                  'PPInfo - В раздел "Сотрудники" не должны попадать архивные продукты')
    def test_get_users_report_not_archived_product(self, ppinfo_api_client):
        for prod in self.get_users_report(ppinfo_api_client):
            for user in prod['users']:
                for position in user['positions']:
                    for product in position["products"]:
                        assert product["status"]["attributeName"] not in ["(PPinfo_status)Out_of_use",
                                                                          "(PPinfo_status)Canceled"], f'У юзера {user["login"]} архивный продукт {product["id"]}'

    @allure.title('В отчет о сотрудниках не должна попадать инфа про продукты с иниц. закрытие')
    @allure.issue('https://jira.mts.ru/browse/PPI-1911',
                  'PPInfo - Убрать продукты с инициировано закрытие из "Сотрудников"')
    def test_get_users_report_not_start_close_product(self, ppinfo_api_client):
        for prod in self.get_users_report(ppinfo_api_client):
            for user in prod['users']:
                for position in user['positions']:
                    for product in position["products"]:
                        assert not product[
                            "startClose"], f'У юзера {user["login"]} продукт {product["id"]} с иниц. закрытие'

    # def test1(self, ppinfo_api_client):
    #     current_date = datetime.now().date()
    #     yesterday = (datetime.now() - timedelta(days=3)).date()
    #     params = self.get_story_data(date_from=str(yesterday), date_to=str(current_date))
    #     self.create_excel_doc(self.get_story_excel(ppinfo_api_client, params))
    #
    #     wb = openpyxl.load_workbook('filename_excel.xlsx')['Продукты и хабы']
    #
    #     # Создайте пустой список
    #     bi_code_list = []
    #
    #     # Пройдите по всем строкам в столбце "Код BI" и добавьте каждое значение в список
    #     for row in wb.iter_rows(min_row=2, min_col=1, max_col=1, values_only=True):
    #         bi_code_list.append(row[0])
    #
    #     self.create_excel_doc(self.get_excel_all_product(ppinfo_api_client))
    #
    #     wb = openpyxl.load_workbook('filename_excel.xlsx')['Продукты и хабы']
    #
    #     # Создайте пустой список
    #     bi_code_list_2 = []
    #
    #     # Пройдите по всем строкам в столбце "Код BI" и добавьте каждое значение в список
    #     for row in wb.iter_rows(min_row=2, min_col=1, max_col=1, values_only=True):
    #         bi_code_list_2.append(row[0])
    #
    #     # превращаем списки в множества
    #     set1 = set(bi_code_list)
    #     set2 = set(bi_code_list_2)
    #
    #     # Используем операцию вычитания множеств, чтобы удалить одинаковые элементы
    #     unique_to_list1 = set1 - set2
    #     unique_to_list2 = set2 - set1
    #
    #     # Объединяем уникальные элементы обоих списков
    #     unique_elements = list(unique_to_list1) + list(unique_to_list2)
    #
    #     print(unique_to_list1)
    #
    #     print(unique_to_list2)
    #
    #     print(unique_elements)

        ##################################################### EPM / ECO-MODULES

    #######  ЭКО МОДУЛИ
    @allure.title("Получение эко модулей по продукту, проверка, что если есть статус, то должна быть ссылка на Jira")
    @pytest.mark.parametrize("bi_code", ['BI_60', 'BI_42', 'BI_43', 'BI_49', 'BI_49', 'BI_1141'])
    def test_eco_modules_jira_link(self, ppinfo_api_client, bi_code):
        integration_list = []
        no_integration_list = []
        response = self.eco_modules_by_code(ppinfo_api_client, bi_code)

        with allure.step("Проверяем, что у продукта есть эко модули"):
            assert response['modules'] and response['headers'], f'По продукту не найдены эко модули'
        for module in response['modules']:
            for row in module['rows']:
                if row['id'] in ("Integrated", "Applicable", "NotApplicable"):
                    if not row['link']:
                        integration_list.append(module['productName'])
                elif row['id'] == 'Empty':
                    if row['link']:
                        no_integration_list.append(module['productName'])

        with allure.step("Проверяем, что у модулей с интеграцией есть ссылка"):
            assert not integration_list, f"У модулей {integration_list} есть интеграция, но нет ссылки"

        with allure.step("Проверяем, что у модулей без интеграцией нет ссылка"):
            assert not no_integration_list, f"У модулей {integration_list} нет интеграции, но есть ссылка"

    @allure.title("Получение экомодулей по продукту, у которого нет эко модулей")
    @pytest.mark.parametrize("bi_code", ['BI_63', 'BI_1561', 'BI_1'])
    def test_no_eco_modules(self, ppinfo_api_client, bi_code):
        response = self.eco_modules_by_code(ppinfo_api_client, bi_code)

        with allure.step("Проверяем, что нет эко модулей"):
            assert not response['modules'] and not response['headers'], f'По продукту найдены эко модули {response}'

    @allure.title("Получение экомодулей по продукту, проверка сортировки экомодулей")
    @allure.issue('https://jira.mts.ru/browse/PPI-2224',
                  'PPinfo - Эко-модули отсортированы не по кол-ву интеграций')
    @pytest.mark.parametrize("bi_code", ['BI_60', 'BI_22', 'BI_51', "BI_1141", 'BI_47'])
    def test_eco_modules_sort(self, ppinfo_api_client, bi_code):
        number_of_integrations = []
        for module in self.eco_modules_by_code(ppinfo_api_client, bi_code)['modules']:
            integration_tmp = sum([1 for i in module["rows"] if i["id"] == 'Empty'])
            number_of_integrations.append(integration_tmp)

        with allure.step("Проверяем, что эко модули отсортированы от большего кол-ва интеграций к меньшему"):
            assert sorted(number_of_integrations) == number_of_integrations, 'Элементы не в том порядке'

    @allure.title("Получение экомодулей по продукту, проверка кол-ва столбцов")
    @pytest.mark.parametrize("bi_code", ['BI_42'])
    def test_eco_modules_headers(self, ppinfo_api_client, bi_code):
        col_number = len(self.eco_modules_by_code(ppinfo_api_client, bi_code)['headers'])
        with allure.step("Проверяем, что кол-во хедеров равно кол-ву записей по каждому продукту"):
            for module in self.eco_modules_by_code(ppinfo_api_client, bi_code)['modules']:
                assert len(module["rows"]) == col_number, f"кол-во столбцов в записи {module['productName']}"

    #######  ПРОДУКТЫ С ЭПМ
    @allure.title("Получение продуктов с эпм, и проверка, что есть ссылки на Jira, если статус подходит")
    @pytest.mark.parametrize("bi_code",
                             ['BI_188', 'BI_200', 'BI_201', 'BI_148', 'BI_189', 'BI_199', 'BI_198', 'BI_262'])
    def test_epm(self, ppinfo_api_client, bi_code):
        integration_list = []
        no_integration_list = []
        response = self.epm_by_code(ppinfo_api_client, bi_code)

        with allure.step("Проверяем, что у продукта есть продукты с эпм"):
            assert response["products"] and response["headers"], "У продукта нет продуктов с ЭМП"

        for module in response['products']:
            for row in module['rows']:
                if row['id'] in ("Integrated", "Applicable", "NotApplicable"):
                    if not row['link']:
                        integration_list.append(module['productName'])
                elif row['id'] == 'Empty':
                    if row['link']:
                        no_integration_list.append(module['productName'])

        with allure.step("Проверяем, что у модулей с интеграцией есть ссылка"):
            assert not integration_list, f"У продуктов {integration_list} есть интеграция, но нет ссылки"

        with allure.step("Проверяем, что у модулей без интеграцией нет ссылка"):
            assert not no_integration_list, f"У продуктов {integration_list} нет интеграции, но есть ссылка"

    @pytest.mark.parametrize("bi_code", ['BI_60', 'BI_42', 'BI_1536', 'BI_1141'])
    def test_no_epm(self, ppinfo_api_client, bi_code):
        response = self.epm_by_code(ppinfo_api_client, bi_code)

        with allure.step("Проверяем, что у продукта нет продуктов с эпм"):
            assert not response["products"] and not response["headers"], f"У продукта есть продукты с ЭМП {response}"

    @allure.title("Проверка сортировки продуктов с ЭПМ")
    @pytest.mark.parametrize("bi_code", ['BI_200', 'BI_201', 'BI_187', 'BI_188', 'BI_198'])
    def test_products_with_epm_sort(self, ppinfo_api_client, bi_code):
        current_status_pos = 0
        statuses = self.get_statuses_list
        with allure.step("Проверяем, что продукты с ЭМП отсортированы по статусам (от активных к архивным)"):
            for product in self.epm_by_code(ppinfo_api_client, bi_code)["products"]:
                assert statuses.index(product["productStatus"][
                                          "code"]) >= current_status_pos, f'Статус продукта {product["productStatus"]["code"]}, раньше встречался'  # {statuses[current_status_pos]}

                current_status_pos = statuses.index(product["productStatus"]["code"])

    @allure.title("Получение эпм', проверка кол-ва столбцов")
    @pytest.mark.parametrize("bi_code", ['BI_200', 'BI_201', 'BI_187', 'BI_188', 'BI_198'])
    def test_epm_headers(self, ppinfo_api_client, bi_code):

        col_number = len(self.epm_by_code(ppinfo_api_client, bi_code)["headers"])
        with allure.step("Проверяем, что кол-во хедеров равно кол-ву записей по каждому продукту"):
            for module in self.epm_by_code(ppinfo_api_client, bi_code)["products"]:
                assert len(module["rows"]) == col_number, f"кол-во столбцов в записи {module['productName']}"

    ##################################################### Excel epm

    @allure.title("Получение excel по ЕПМ по проверка все листов")
    def test_excel_epm_sheets(self, ppinfo_api_client, clear_excel):

        sheet_names = self.excel_epm(ppinfo_api_client)
        sheet_names = sheet_names.sheetnames
        sheet_names.remove('Продукты и хабы')

        assert sorted(sheet_names) == sorted(['SEO + Аналитика',
                                              'Unified Messaging System',
                                              'Биометрия',
                                              'Дизайн-система',
                                              'МТС ID',
                                              'МТС Pay',
                                              'МТС Профиль',
                                              'Обратная связь',
                                              'Справка'])

    @allure.title("Получение excel по ЕПМ по проверка соответсвия столбцов / SEO + Аналитика")
    def test_excel_epm_seo_analiz(self, ppinfo_api_client, clear_excel):

        workbook = self.excel_epm(ppinfo_api_client)
        sheet = workbook['SEO + Аналитика']
        column_headers = [cell.value for cell in sheet[1]]

        header_eco = []

        for header in self.epm_by_code(ppinfo_api_client, 'BI_200')['headers']:
            header_eco.append(header)

        assert column_headers == ['Код BI_',
                                  'Новый код продукта в Oracle',
                                  'Название продукта',
                                  'Тип продукта',
                                  'Структурный тип продукта',
                                  'Категория продукта',
                                  'Блок',
                                  'Статус',
                                  'Инициировано закрытие',
                                  'Chief product owner',
                                  'Product owner',
                                  'Chief Technology Officer'] + header_eco

    @allure.title("Получение excel по ЕПМ по проверка соответсвия столбцов / Unified Messaging System")
    def test_excel_epm_ums(self, ppinfo_api_client, clear_excel):

        workbook = self.excel_epm(ppinfo_api_client)
        sheet = workbook['Unified Messaging System']
        column_headers = [cell.value for cell in sheet[1]]

        header_eco = []

        for header in self.epm_by_code(ppinfo_api_client, 'BI_201')['headers']:
            header_eco.append(header)

        assert column_headers == ['Код BI_',
                                  'Новый код продукта в Oracle',
                                  'Название продукта',
                                  'Тип продукта',
                                  'Структурный тип продукта',
                                  'Категория продукта',
                                  'Блок',
                                  'Статус',
                                  'Инициировано закрытие',
                                  'Chief product owner',
                                  'Product owner',
                                  'Chief Technology Officer'] + header_eco

    @allure.title("Получение excel по ЕПМ по проверка соответсвия столбцов / Биометрия")
    def test_excel_epm_bio(self, ppinfo_api_client, clear_excel):

        workbook = self.excel_epm(ppinfo_api_client)
        sheet = workbook['Биометрия']
        column_headers = [cell.value for cell in sheet[1]]
        header_eco = []

        for header in self.epm_by_code(ppinfo_api_client, 'BI_187')['headers']:
            header_eco.append(header)

        assert column_headers == ['Код BI_',
                                  'Новый код продукта в Oracle',
                                  'Название продукта',
                                  'Тип продукта',
                                  'Структурный тип продукта',
                                  'Категория продукта',
                                  'Блок',
                                  'Статус',
                                  'Инициировано закрытие',
                                  'Chief product owner',
                                  'Product owner',
                                  'Chief Technology Officer'] + header_eco

    @allure.title("Получение excel по ЕПМ по проверка соответствия столбцов / Дизайн-система")
    def test_excel_epm_desing(self, ppinfo_api_client, clear_excel):

        workbook = self.excel_epm(ppinfo_api_client)
        sheet = workbook['Дизайн-система']
        column_headers = [cell.value for cell in sheet[1]]

        header_eco = []

        for header in self.epm_by_code(ppinfo_api_client, 'BI_262')['headers']:
            header_eco.append(header)

        assert column_headers == ['Код BI_',
                                  'Новый код продукта в Oracle',
                                  'Название продукта',
                                  'Тип продукта',
                                  'Структурный тип продукта',
                                  'Категория продукта',
                                  'Блок',
                                  'Статус',
                                  'Инициировано закрытие',
                                  'Chief product owner',
                                  'Product owner',
                                  'Chief Technology Officer'] + header_eco

    @allure.title("Получение excel по ЕПМ по проверка соответсвия столбцов / МТС ID")
    def test_excel_epm_mts_id(self, ppinfo_api_client, clear_excel):

        workbook = self.excel_epm(ppinfo_api_client)
        sheet = workbook['МТС ID']
        column_headers = [cell.value for cell in sheet[1]]

        header_eco = []

        for header in self.epm_by_code(ppinfo_api_client, 'BI_188')['headers']:
            header_eco.append(header)

        assert column_headers == ['Код BI_',
                                  'Новый код продукта в Oracle',
                                  'Название продукта',
                                  'Тип продукта',
                                  'Структурный тип продукта',
                                  'Категория продукта',
                                  'Блок',
                                  'Статус',
                                  'Инициировано закрытие',
                                  'Chief product owner',
                                  'Product owner',
                                  'Chief Technology Officer'] + header_eco

    @allure.title("Получение excel по ЕПМ по проверка соответсвия столбцов / МТС Pay")
    def test_excel_epm_mts_pay(self, ppinfo_api_client, clear_excel):

        workbook = self.excel_epm(ppinfo_api_client)
        sheet = workbook['МТС Pay']
        column_headers = [cell.value for cell in sheet[1]]

        header_eco = []

        for header in self.epm_by_code(ppinfo_api_client, 'BI_148')['headers']:
            header_eco.append(header)

        assert column_headers == ['Код BI_',
                                  'Новый код продукта в Oracle',
                                  'Название продукта',
                                  'Тип продукта',
                                  'Структурный тип продукта',
                                  'Категория продукта',
                                  'Блок',
                                  'Статус',
                                  'Инициировано закрытие',
                                  'Chief product owner',
                                  'Product owner',
                                  'Chief Technology Officer'] + header_eco

    @allure.title("Получение excel по ЕПМ по проверка соответсвия столбцов / МТС Профиль")
    def test_excel_epm_mts_profile(self, ppinfo_api_client, clear_excel):

        workbook = self.excel_epm(ppinfo_api_client)
        sheet = workbook['МТС Профиль']
        column_headers = [cell.value for cell in sheet[1]]
        header_eco = []

        for header in self.epm_by_code(ppinfo_api_client, 'BI_189')['headers']:
            header_eco.append(header)

        assert column_headers == ['Код BI_',
                                  'Новый код продукта в Oracle',
                                  'Название продукта',
                                  'Тип продукта',
                                  'Структурный тип продукта',
                                  'Категория продукта',
                                  'Блок',
                                  'Статус',
                                  'Инициировано закрытие',
                                  'Chief product owner',
                                  'Product owner',
                                  'Chief Technology Officer'] + header_eco

    @allure.title("Получение excel по ЕПМ по проверка соответсвия столбцов / Обратная связь")
    def test_excel_epm_feedback(self, ppinfo_api_client, clear_excel):

        workbook = self.excel_epm(ppinfo_api_client)
        sheet = workbook['Обратная связь']
        column_headers = [cell.value for cell in sheet[1]]

        header_eco = []

        for header in self.epm_by_code(ppinfo_api_client, 'BI_199')['headers']:
            header_eco.append(header)

        assert column_headers == ['Код BI_',
                                  'Новый код продукта в Oracle',
                                  'Название продукта',
                                  'Тип продукта',
                                  'Структурный тип продукта',
                                  'Категория продукта',
                                  'Блок',
                                  'Статус',
                                  'Инициировано закрытие',
                                  'Chief product owner',
                                  'Product owner',
                                  'Chief Technology Officer'] + header_eco

    @allure.title("Получение excel по ЕПМ по проверка соответсвия столбцов / Справка")
    def test_excel_epm_spravka(self, ppinfo_api_client, clear_excel):

        workbook = self.excel_epm(ppinfo_api_client)
        sheet = workbook['Справка']
        column_headers = [cell.value for cell in sheet[1]]

        header_eco = []

        for header in self.epm_by_code(ppinfo_api_client, 'BI_198')['headers']:
            header_eco.append(header)

        assert column_headers == ['Код BI_',
                                  'Новый код продукта в Oracle',
                                  'Название продукта',
                                  'Тип продукта',
                                  'Структурный тип продукта',
                                  'Категория продукта',
                                  'Блок',
                                  'Статус',
                                  'Инициировано закрытие',
                                  'Chief product owner',
                                  'Product owner',
                                  'Chief Technology Officer'] + header_eco
