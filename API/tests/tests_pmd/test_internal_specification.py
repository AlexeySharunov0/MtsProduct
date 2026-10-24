import allure
import pytest

from API.models.pmd.internal_specifications import InternalSpecification


@pytest.mark.api
@allure.feature('Спецификации')
class TestInternalSpecification(InternalSpecification):

    @allure.title('Получение спецификаций по типам c логином')
    @pytest.mark.parametrize('specification_code', ['Vneshnii', 'Vnutrennii'])
    @pytest.mark.parametrize('login', ['ddsvetov1', 'aikostrov1'])
    def test_get_specification_by_code_and_login(self, pmd_internal_api_gw_client, specification_code, login):
        self.get_specification_by_code_and_login(pmd_internal_api_gw_client, specification_code, login)

    @allure.title('Получение спецификаций по типам без логина')
    @pytest.mark.parametrize('specification_code', ['Vneshnii', 'Vnutrennii'])
    def test_get_specification_by_code_without_login(self, pmd_internal_api_gw_client, specification_code):
        self.get_specification_by_code_and_login(pmd_internal_api_gw_client, specification_code)

    @allure.title('Получение спецификаций по некорреткным типам')
    @pytest.mark.parametrize('specification_code', ['', 'qweqweqwewe'])
    @pytest.mark.parametrize('login', ['ddsvetov1', 'aikostrov1'])
    def test_get_specification_by_invalid_code_and_login(self, pmd_internal_api_gw_client, specification_code, login):
        self.get_specification_by_code_and_login_404(pmd_internal_api_gw_client, specification_code, login)
