import allure
import pytest

from API.models.pmd.public_specification import PublicSpecification


@pytest.mark.api
@allure.label('priority', 'Высокий')
@allure.feature('Спецификации public')
class TestPublicSpecification(PublicSpecification):

    @allure.title('Получение всех спецификаций')
    def test_get_specifications(self, public_gw_client):
        self.get_specifications(public_gw_client)

    @allure.title('Получение атрибутов по code')
    @pytest.mark.parametrize('attribute_code',
                             ['', 'employee_business_owner', 'SYSTEM_Jira', 'PPInfo_qbrmemo_link', 'PPInfo_showcase',
                              'PPinfo_start_date_MVP', 'PPInfo_Eco_Integration_Andr'])
    def test_get_attributes_by_code(self, public_gw_client, attribute_code):
        params = {
            'codes': attribute_code
        }
        self.get_attributes_by_code(public_gw_client, params)

    @allure.title('Получение атрибутов по несуществующему code')
    @pytest.mark.parametrize('attribute_code',
                             ['привет', 'a code'])
    def test_get_attributes_by_code(self, public_gw_client, attribute_code):
        params = {
            'codes': attribute_code
        }
        assert not self.get_attributes_by_code(public_gw_client, params)[
            'attributes'], f'{self.get_attributes_by_code(public_gw_client, params)["attributes"]} были найдены по коду {attribute_code}'

    @allure.title('Получение спецификаций по code')
    @pytest.mark.parametrize('specification_code',
                             ['Vneshnii', 'Vnutrennii'])
    def test_get_specification_by_code(self, public_gw_client, specification_code):
        self.get_specification_by_code(public_gw_client, specification_code)

    @allure.title('Получение спецификаций по невалидному code')
    @pytest.mark.parametrize('specification_code',
                             ['', 'йцуйцу'])
    def test_get_specification_by_invalid_code(self, public_gw_client, specification_code):
        self.get_specification_by_code_404(public_gw_client, specification_code)

    @allure.title('Получение спецификаций по id')
    @pytest.mark.parametrize('specification_id',
                             ['37b386a8-6dde-5947-8307-b117266b82da', '9dffdd8b-935d-31c7-6b1a-f3d58e649b9c'])
    def test_get_specification_by_id(self, public_gw_client, specification_id):
        self.get_specification_by_id(public_gw_client, specification_id)

    @allure.title('Получение спецификаций по невалидному id')
    @pytest.mark.parametrize('specification_id',
                             ['37b386a8-6dde-5947-8307-b117266bqqda', 'qweqwe'])
    def test_get_specification_by_invalid_id(self, public_gw_client, specification_id):
        self.get_specification_by_id_400(public_gw_client, specification_id)
