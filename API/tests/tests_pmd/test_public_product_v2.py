import allure
import pytest

from API.models.pmd.public_product_v2 import ProductV2


@pytest.mark.api
@allure.label('priority', 'Высокий')
@allure.feature('Получение продуктов')
class TestProductV2(ProductV2):

    @allure.title('Поиск пост запросом')
    @pytest.mark.parametrize('product_name',
                             ['Маркетолог', 'Марк', 'марк', 'АТС', 'Умный', 'мой коннект', '8-800', 'АОН', 'Бизнес',
                              '*зве', 'Скоринг', 'RCS\RBM'])
    def test_search_by_name(self, public_gw_client, product_name):
        data = {
            "query": product_name
        }

        assert all(product_name.lower() in i['name'].lower() for i in
                   self.search_by_name(public_gw_client, data)['products']), f"По запросу {product_name} было найдено невалидное значение"

    @allure.title('Получение значений атрибутов на конкретную дату')
    @pytest.mark.parametrize('attr_name', ['PPinfo_market', 'PPinfo_fix_HFM'])
    def test_get_attribute_story(self, public_gw_client, attr_name):
        data = self.get_data_for_story(attr_name=attr_name)

        assert self.get_attribute_story(public_gw_client, data)['products'], 'На данную дату нет данных о текущем атрибуте'

    @allure.title('Получение значений несуществующих атрибутов на конкретную дату')
    def test_get_attribute_story_invalid_attr(self, public_gw_client):
        data = self.get_data_for_story(attr_name='QWERTYUIOP{')

        assert all(not i['attributes'] for i in self.get_attribute_story(public_gw_client, data)[
            'products']), f'На данную дату нашлась след. информация {self.get_attribute_story(public_gw_client, data)["products"]}'

    @allure.title('Получение значений атрибутов на несуществующую дату')
    def test_get_attribute_story_invalid_date(self, public_gw_client):
        data = self.get_data_for_story(date="2002-02-18T21:00:00.000Z")

        self.get_attribute_story(public_gw_client, data)

        assert not self.get_attribute_story(public_gw_client, data)[
            'products'], f'На данную дату нашлась след. информация {self.get_attribute_story(public_gw_client, data)["products"]}'
