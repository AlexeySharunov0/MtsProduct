import warnings

import allure
import pytest

from API.models.pmd.rest_internal_modules.system import System

warnings.filterwarnings('ignore', message='numpy.dtype size changed')


#### SYSTEM SoL and RMS
@pytest.mark.api
@allure.feature('SoL and RMS')
class TestSystemApi(System):

    @allure.title('Проверка что Сервисы и капабилите не пустые')
    @allure.issue('https://jira.mts.ru/browse/PPI-2823', 'PPInfo - Отображение капабилити продукта')
    @allure.issue('https://jira.mts.ru/browse/PPI-2827', 'PPInfo - Отображение сервисов продукта')
    @pytest.mark.parametrize('product_code', ['BI_60', 'BI_42'])
    def test_get_edt(self, pmd_admin_rest_client, product_code):

        info_from_edt = self.get_edt(pmd_admin_rest_client, product_code)

        for i in info_from_edt.values():
            assert len(
                i) >= 2, f'В продукте {product_code} нет информации по Сервисам или капабилити'  # 3 - это просто число, я понимаю по нему что объект не пустой

    @allure.title('Проверка что Сервисы и капабилите пустые')
    @allure.issue('https://jira.mts.ru/browse/PPI-2823', 'PPInfo - Отображение капабилити продукта')
    @allure.issue('https://jira.mts.ru/browse/PPI-2827', 'PPInfo - Отображение сервисов продукта')
    @pytest.mark.parametrize('product_code', ['BI_52765', 'BI_52752'])
    def test_get_edt_empty(self, pmd_admin_rest_client, product_code):

        info_from_edt = self.get_edt(pmd_admin_rest_client, product_code)

        for key, value in info_from_edt.items():
            if key != 'link':
                assert value == [], f'В продукте {product_code} есть информация по {key}.\n Кол-во записей - {len(value)}'

    @allure.title('Сервисы в икселе и на ui совпадают')
    @allure.issue('https://jira.mts.ru/browse/PPI-2956', 'PPInfo - Выгрузка сервисов и капабилити продукта в Excel')
    @pytest.mark.parametrize('product_code', ['BI_60', 'BI_42'])
    def test_edt_excel_services(self, pmd_admin_rest_client, product_code, clear_excel):
        with allure.step('Собираем сервисы из API в список'):
            info_from_edt = self.get_edt(pmd_admin_rest_client, product_code)
            services = []
            for i in info_from_edt['realizesServices']:
                services.append(i['code'])
            for i in info_from_edt['servedServices']:
                services.append(i['code'])
        with allure.step('Собираем сервисы из excel в список'):
            ex = self.get_edt_info_by_excel(pmd_admin_rest_client, product_code)['Сервисы']
            services_from_excel = []
            for row in ex.iter_cols(min_row=2, min_col=2, max_col=2, max_row=ex.max_row):
                for cell in row:
                    services_from_excel.append(cell.value)

        assert services == services_from_excel, f'Сервисы на ui и в икселе не совпадают\n Сервисы на ui - {services} \n Сервисы в икселе - {services_from_excel}'

    @allure.title('Капабилити в икселе и на ui совпадают')
    @allure.issue('https://jira.mts.ru/browse/PPI-2956', 'PPInfo - Выгрузка сервисов и капабилити продукта в Excel')
    @pytest.mark.parametrize('product_code', ['BI_60', 'BI_42'])
    def test_edt_excel_capability(self, pmd_admin_rest_client, product_code, clear_excel):
        with allure.step('Собираем сервисы из API в список'):
            info_from_edt = self.get_edt(pmd_admin_rest_client, product_code)
            capability = []
            for i in info_from_edt['capability']:
                capability.append(i['number'])
        with allure.step('Собираем сервисы из excel в список'):
            ex = self.get_edt_info_by_excel(pmd_admin_rest_client, product_code)['Капабилити']
            capability_from_excel = []
            for row in ex.iter_cols(min_row=2, min_col=1, max_col=1, max_row=ex.max_row):
                for cell in row:
                    capability_from_excel.append(cell.value)

        assert capability == capability_from_excel, f'Капабилити в икселе и на ui не совпадают\n Капабилити на ui - {capability} \n Капабилити в икселе - {capability_from_excel}'

    @allure.title('Получаем информацию о проектах RMS')
    @pytest.mark.parametrize('product_code', ['BI_60', 'BI_41', 'BI_43', '43'])
    def test_get_rms(self, pmd_admin_rest_client, product_code):
        assert self.get_rms(pmd_admin_rest_client, product_code), f'По коду {product_code} нет информации'

    @allure.title('Получаем информацию о проектах RMS по несуществующему продукту')
    @pytest.mark.parametrize('product_code', ['BI_232323', '232323'])
    def test_get_rms_no_info(self, pmd_admin_rest_client, product_code):
        assert not self.get_rms(pmd_admin_rest_client,
                                product_code), f'По коду {product_code} нашлись проекты {self.get_rms(pmd_admin_rest_client, product_code)}'

    @allure.title('Получаем информацию о проектах RMS по невалидному коду')
    @pytest.mark.parametrize('product_code', ['тест', 'BI_'])
    def test_get_rms_by_invalid_code(self, pmd_admin_rest_client, product_code):
        self.get_rms_400(pmd_admin_rest_client, product_code)
