from typing import Any

import allure

from API.data.ppinfo import Draft

HOST = 'https://stage.prodboard.example.com'


class DraftsUrls:
    """
    https://stage.prodboard.example.com/ppinfo/swagger/draft/index.html
    """

    # Получение черновика
    GET_DRAFT = 'v1/draft'

    # Удаление черновика
    DELETE_DRAFT = 'v1/draft'

    # Создание черновика
    CREATE_DRAFT = 'v1/draft'

    # Получение черновиков
    GET_DRAFTS = 'v1/drafts'


class Drafts(DraftsUrls):

    @allure.step('Установка параметров')
    def get_draft_params(self, new_params: dict[str, str] | None = None) -> dict[str, str]:
        params = {
            'login': 'admin_user',
            'externalId': 'Internal',
            'type': 'createProduct',
            'data': '{"name":[{"value":"Тестовый черновик test","code":"Тестовый черновик test"}]}'
        }
        if new_params:
            params.update(new_params)

        return params

    @allure.step('Получение черновика')
    def get_draft(self, client, params: dict[str, Any]) -> dict[str, Any]:
        response = client.get(self.GET_DRAFT, params=params)

        Draft(**response)

        return response

    @allure.step('Получение черновика с ошибкой')
    def get_draft_404(self, client, params: dict[str, Any]) -> None:
        client.get(self.GET_DRAFT, params=params, expected_status_code=404)

    @allure.step('Удаление черновика')
    def delete_draft(self, client, params: dict[str, Any]) -> None:
        client.delete(self.DELETE_DRAFT, params=params)

    @allure.step('Создание черновика')
    def create_draft(self, client, data: dict[str, Any]) -> None:
        response = client.put(self.CREATE_DRAFT, json=data)

        return response
