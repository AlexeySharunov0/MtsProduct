import warnings

import allure
import pytest

from API.models.pmd.rest_internal_modules.internal_specification_rest import InternalSpecification

warnings.filterwarnings('ignore', message='numpy.dtype size changed')


#### INTERNAL SPECIFICATION
@pytest.mark.api
@allure.feature('Oracle')
@allure.issue('https://jira.mts.ru/browse/PPI-1429', 'PPInfo - Доработка валидации кода Oracle')
class TestOracleApi(InternalSpecification):

    @allure.title('Валидация уникального кода oracle')
    @pytest.mark.parametrize('oracle_code', ['MAAs', 'ASDF'])
    def test_validate_oracle(self, rest_internal_client, oracle_code):
        assert self.validate_oracle(rest_internal_client, oracle_code) == {'error': '', 'matchingValues': []}

    @allure.title('Валидация неуникального кода oracle')
    @pytest.mark.parametrize('oracle_code', ['MAAS', 'CB', 'CPP', 'MAUT'])
    def test_validate_oracle_duplicate(self, rest_internal_client, oracle_code):
        assert self.validate_oracle(rest_internal_client, oracle_code)['matchingValues']

    @allure.title('Валидация невалидного кода oracle')
    @pytest.mark.parametrize('oracle_code', ['M A', '123', '!@#'])
    def test_validate_oracle_invalid(self, rest_internal_client, oracle_code):
        assert self.validate_oracle(rest_internal_client, oracle_code)[
                   'error'] == 'Код должен содержать латинские буквы;'

    @allure.title('Валидация кода oracle с слишком большим кол-вом символом')
    @pytest.mark.parametrize('oracle_code', ['M qweqweA', 'as qwed'])
    def test_validate_oracle_max_letters(self, rest_internal_client, oracle_code):
        assert self.validate_oracle(rest_internal_client, oracle_code)[
                   'error'] == 'Код должен содержать латинские буквы; Код должен иметь длину от 1 до 4 символов включительно.'


@pytest.mark.api
@allure.feature('Спецификации')
class TestIndividualSpecificationForm(InternalSpecification):
    @allure.title('Получение индивидуальных спецификаций для форм')
    @allure.issue('https://jira.mts.ru/browse/PPI-2434',
                  'PPInfo - Создать API для получения индивидуальной спецификации для форм')
    @pytest.mark.parametrize('form_id', ['addAction', 'AdminAddCommercialProduct', 'AdminAddInternalProduct',
                                         'UserAddCommercialProduct', 'UserAddInternalProduct'])
    def test_get_individual_specification(self, rest_internal_client, form_id):
        assert self.get_individual_specification(rest_internal_client, form_id), 'Спецификации формы нет'

    @allure.title('Получение индивидуальных спецификаций для форм Excel')
    @allure.issue('https://jira.mts.ru/browse/PPI-2654',
                  'PPInfo - Добавить спецификацию в api формы отчетов на даты, изменение атрибутов')
    @pytest.mark.parametrize('form_id', ['AdminExcelDate', 'UserExcelDate'])
    def test_get_individual_specification_excel(self, rest_internal_client, form_id):
        assert self.get_individual_specification(rest_internal_client, form_id), 'Спецификации формы нет'

    @allure.title('Проверка, что админская и юзерская формы для Excel отличаются')
    @allure.issue('https://jira.mts.ru/browse/PPI-2654',
                  'PPInfo - Добавить спецификацию в api формы отчетов на даты, изменение атрибутов')
    def test_get_individual_specification_excel_difference(self, rest_internal_client):
        form_admin = self.get_individual_specification(rest_internal_client, 'AdminExcelDate')
        form_user = self.get_individual_specification(rest_internal_client, 'UserExcelDate')
        with allure.step('Проверяем, что формы отличаются'):
            assert form_admin != form_user, 'Формы не отличаются'
