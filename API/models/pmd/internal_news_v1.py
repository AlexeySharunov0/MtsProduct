import io
from typing import Any

import allure

from API.data.pmd import New, News
from API.utils.file_manager import create_any_image
from API.utils.generate import Gen

HOST = 'https://stage.prodboard.example.com'


class NewsApiUrls:
    """
    https://stage.prodboard.example.com/news-service/swagger/index.html
    """

    # Получить все новости p
    GET_ALL_NEWS = 'v1/news'

    # Поменять порядок новости
    SWAP_NEWS = 'v1/news/swap'

    # Получить конкретную новость по ID p
    GET_NEWS_BI_ID = 'v1/news/{}'

    # Удалить новость
    DELETE_NEWS_BI_ID = 'v1/news/{}'

    # Создать новость
    CREATE_NEW = 'v1/news'

    # Получение дефолтной картинки для новости p
    GET_DEFAULT_IMAGE = 'v1/news/image/default'

    # Получение картинки для новости p
    GET_IMAGE = 'v1/news/{}/image'

    # Изменить новость
    PATCH_NEW = 'v1/news/{}'

    # Добавить картинку к новости
    ADD_IMAGE = 'v1/news/{}/image'

    # Удалить новость
    DELETE_IMAGE = 'v1/news/{}'


class NewsApi(NewsApiUrls):

    @allure.step('Данные для новостей')
    def get_news_data(self, new_params: dict[str, Any] | None = None) -> dict[str, Any]:
        params = {
            "name": "Новость для автотестов " + Gen.generate_text(length=7, lang='eng'),
            "description": "Текст новости " + Gen.generate_text(length=7, lang='eng'),
            "isActive": True
        }
        if new_params:
            params.update(new_params)
        return params

    @allure.step("Данные для свапа")
    def get_news_swap_data(self, client, old_number: int, to_number: int) -> dict[str, Any]:
        return {
            "id": self.get_all_news(client)["news"][old_number - 1]["id"],
            "newWeight": to_number,
            "oldWeight": old_number
        }

    @allure.step('Создание картинки')
    def create_image(self, image_format: str):
        create_any_image(image_format)

        if image_format.lower() in ["png", "jpg"]:
            files = {'file': (f'FILE_NAME.{image_format}', f'example.{image_format}', f'image/{image_format}')}
        else:
            files = {'file': (f'FILE_NAME.{image_format}', f'example.{image_format}', f'image/{image_format} + xml')}
        return files

    @allure.step('Получение всех новостей')
    def get_all_news(self, client, active: bool = None) -> dict[str, Any]:
        params = {
            "onlyActive": active
        }
        response = client.get(self.GET_ALL_NEWS, params=params)
        News(**response)
        return response

    @allure.step('Изменение порядка новостей')
    def swap_news(self, client, data: dict[str, Any]) -> None:
        client.post(self.SWAP_NEWS, json=data, raw_format=True)

    @allure.step('Получение новости по id')
    def get_new_by_id(self, client, new_id: str) -> dict[str, Any]:
        response = client.get(self.GET_NEWS_BI_ID.format(new_id))
        New(**response)

        return response

    @allure.step('Удаление новости по id')
    def delete_new_by_id(self, client, product_id: str) -> None:
        client.delete(self.DELETE_NEWS_BI_ID.format(product_id))

    @allure.step('Изменение новости по id')
    def patch_new_by_id(self, client, new_id: str, json_data: dict[str, Any]) -> None:
        client.patch(self.PATCH_NEW.format(new_id), json=json_data, raw_format=True)

    @allure.step('Некорректное изменение новости по id')
    def patch_new_by_id_400(self, client, new_id: str, json_data: dict[str, Any]) -> None:
        client.patch(self.PATCH_NEW.format(new_id), json=json_data, expected_status_code=400)

    @allure.step('Создание новости')
    def create_new(self, client, data: dict[str, Any], file: dict[str, tuple[str, io.BytesIO, str]]) -> str:
        response = client.post(self.CREATE_NEW, json=data, files=file)
        return response['id']

    @allure.step('Создание инвалидной новости')
    def create_new_400(self, client, data: dict[str, Any], file: dict[str, tuple[str, io.BytesIO, str]]) -> None:
        client.post(self.CREATE_NEW, json=data, files=file, expected_status_code=400)

    @allure.step('Получение дефолтной картинки')
    def get_default_image(self, client) -> None:
        client.get(self.GET_DEFAULT_IMAGE, raw_format=True)

    @allure.step('Получение картинки по id')
    def get_image_by_id(self, client, file_id: str) -> None:
        client.get(self.GET_IMAGE.format(file_id), raw_format=True)

    @allure.step('Замена картинки на новости')
    def get_change_image(self, client, new_id: str, file: dict[str, tuple[str, io.BytesIO, str]]) -> None:
        client.put(self.ADD_IMAGE.format(new_id), files=file, raw_format=True)

    @allure.step('Удаление картинки на новости')
    def get_delete_image(self, client, new_id: str) -> None:
        client.delete(self.DELETE_IMAGE.format(new_id))
