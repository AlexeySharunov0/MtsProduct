import allure
import pytest

from API.models.pmd.public_product_v1 import ProductV1


@pytest.mark.api
@allure.label('priority', 'Высокий')
@allure.feature('Получение продуктов')
class TestProductV1(ProductV1):


    @allure.title('Получение списка всех продуктов')
    def test_get_products(self, public_gw_client):
        self.get_products(public_gw_client)

    @allure.title('Получение всех документов')
    def test_get_documents(self, public_gw_client):
        self.get_documents(public_gw_client)

    @allure.title('Получение продукта по коду')
    @pytest.mark.parametrize('code', ('BI_60', '60'))
    def test_get_product_by_code(self, public_gw_client, code):
        self.get_product_by_code(public_gw_client, code)

    @allure.title('Получение продукта по несуществующему коду')
    @pytest.mark.parametrize('invalid_code', ('BI_qweqwe', ' ', 'BI 60'))
    def test_get_product_by_invalid_code(self, public_gw_client, invalid_code):
        self.get_product_by_code_400(public_gw_client, invalid_code)

    @allure.title('Выборка продуктов по всем типам аттрибутов')
    @pytest.mark.parametrize('required_attr', (
            'PPinfo_market', 'PPInfo_showcase', 'PPinfo_StructuralProductType', 'PPinfo_start_close_date',
            'Identifikator_SOL', 'employee_business_owner', 'Odin_produkt', 'Mnogo_produktov',
            'PPinfo_resolution', 'PPInfo_site_landing'))  # не работает с множ ссылками и мультюзером
    def test_post_search(self, public_gw_client, required_attr):
        data = self.get_data_for_search({'requiredData': required_attr})
        with allure.step('Проверяем, что по каждому продукту есть информация по заданному атрибуту'):
            assert all(product['attributes'] for product in
                       self.post_search(public_gw_client, data)['products']), 'данные по указанному атрибуту не найдены'
