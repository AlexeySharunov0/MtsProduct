import warnings

import allure
import pytest

from API.models.pmd.rest_internal_modules.favorites import Favorites

warnings.filterwarnings('ignore', message='numpy.dtype size changed')


#### FAVORITES
@pytest.mark.api
@allure.feature('Избранное')
class TestFavorite(Favorites):

    @allure.title('Получение избранных продуктов')
    def test_favorite(self, rest_internal_client):
        self.get_favorite(rest_internal_client)

    @allure.title('Проверка Избранного')
    @allure.description('Проверяем добавление/удаление продукта в Избранное/из Избранного на продукте PPInfo')
    def test_favorite_products(self, rest_internal_client):
        with allure.step('Проверяем что продукта нет в избранных'):
            if any('BI_60' in favorite['code'] for favorite in
                   self.get_favorite(rest_internal_client)):
                self.change_favorite(rest_internal_client)

        with allure.step('Добавляем продукт в избранное'):
            self.change_favorite(rest_internal_client)

        with allure.step('Проверяем что продукта в избранных'):
            assert any('BI_60' in favorite['code'] for favorite in
                       self.get_favorite(rest_internal_client)), 'Продукт не в избранных, хотя должен там быть'

        with allure.step('Удаляем продукт из избранных'):
            self.change_favorite(rest_internal_client)

        with allure.step('Проверяем что продукта нет в избранных'):
            assert not any('BI_60' in favorite['code'] for favorite in
                           self.get_favorite(rest_internal_client)), 'Продукт в избранных, хотя не должен там быть'
