import warnings
from typing import Any

import allure

from API.data.pmd import FavoriteList

warnings.filterwarnings("ignore", message="numpy.dtype size changed")

HOST = 'https://stage.prodboard.example.com'


class FavoritesUrls:
    """
    https://stage.prodboard.example.com/pmd/swagger/rest/internal/index.html#/
    """
    ### FAVORITES

    # Получение избранных продуктов
    GET_FAVORITE = 'v2/product/favorites'

    # Добавление, удаление избранных продуктов
    CHANGE_FAVORITE = 'v1/product/{}/favorites'


class Favorites(FavoritesUrls):
    #### FAVORITES

    @allure.step('Получение избранных продуктов')
    def get_favorite(self, client) -> list[dict[str, Any]]:
        response = client.get(self.GET_FAVORITE)

        FavoriteList(favorites=response)

        return response

    @allure.step('Добавление/удаление продукта из избранного')
    def change_favorite(self, client, product_code: str = 'BI_60') -> None:
        client.post(self.CHANGE_FAVORITE.format(product_code), raw_format=True)
