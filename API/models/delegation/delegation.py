import json
from typing import Any

import allure

from API.api_fixtures import ppinfo_client
from API.models.pmd.rest_internal_modules.internal_product import InternalProduct

HOST = "https://stage.prodboard.example.com"


class DelegationUrls:
    """
    https://stage.prodboard.example.com/pmd/swagger/public/delegation/index.html#/DelegationService
    https://gitlab.example.com/prodboard/backend/proto/-/blob/develop/gen/proto/go/v1/delegation/delegation.swagger.json?plain=0
    """

    # Получение списка продуктов с делегированием
    GET_DELEGATIONS = "v1/delegation"

    # Выдача прав делегирования
    ADD_DELEGATION = "v1/delegation"

    # Удаление прав делегирования
    DELETE_DELEGATION = "v1/delegation/{}"


class Delegation(DelegationUrls, InternalProduct):

    @allure.step("Получаем список всех делегирований")
    def get_delegations(self, client) -> list[dict[str, Any]]:
        response = self.get_owned_products(client)["delegationProducts"]

        return response

    @allure.step("Добавляем делегирование")
    def add_delegation(self, client, login: str = "regular_user", product_code: str = "BI_2683") -> None:
        data = {"login": login, "productId": product_code}
        client.post(self.ADD_DELEGATION, json=data)

    @allure.step("Завершаем делегирование")
    def delete_delegation(self, client, delegation_id: str) -> None:
        client.delete(self.DELETE_DELEGATION.format(delegation_id))

    @allure.step("Проверяем наличие делегирования")
    def check_presence(self, client, product_code: str = "BI_2683") -> str:
        """
        Метод запрашивает список делегирования и сохраняет в переменную id делегации, если код продукта был найден в списке.
        Проверяет, что внутри этой переменной присутствует значение
        Args:
            product_code: код продукта
            client: клиент для работы с API rest_internal_client
        Returns: id делегирования
        """
        delegation_id = [
            delegation["id"]
            for delegation in self.get_delegations(client)
            if delegation["product"]["code"] == product_code][0]

        assert delegation_id, f"Для продукта {product_code} не найдено делегирования"
        return delegation_id

    @allure.step("Проверяем отсутствие делегирования")
    def check_absence(self, client, product_code: str = "BI_2683") -> None:
        """
        Метод запрашивает список делегирования и сохраняет в переменную id делегации, если код продукта был найден в списке.
        Проверяет, что внутри этой переменной отсутствует значение
        Args:
            product_code: код продукта
            client: клиент для работы с API rest_internal_client

        """
        delegation_id = [
            delegation["id"]
            for delegation in self.get_delegations(client)
            if delegation["product"]["code"] == product_code][0]

        assert not delegation_id, f"Для продукта {product_code} найдено делегирования"

    @allure.title("Очищаем делегирование, если оно есть")
    def remove_delegation(self, ppinfo_client, pmd_client, product_code: str = "BI_2683") -> None:
        """
        Метод запрашивает список делегирования и сохраняет в переменную id делегации, если код продукта был найден в списке.
        Затем метод отправляет запрос на удаление делегирования, если id делегирования было найдено
        Args:
            product_code: код продукта
            ppinfo_client: клиент для работы с API
            pmd_client: клиент для работы с API rest_internal_client

        """
        delegation_id = [
            delegation["id"]
            for delegation in self.get_delegations(pmd_client)
            if delegation["product"]["code"] == product_code][0]

        if delegation_id:
            self.delete_delegation(ppinfo_client, delegation_id)

    @allure.step("Получаем data для заявки")
    def get_data_for_delegation_brief(self):
        """
        Возвращает данные для делегирования заявки на редактирование продукта.

        Возвращает словарь с типом операции и сериализованными данными,
        необходимыми для обновления атрибутов продукта в API.

        Returns:
            dict: Словарь с ключами:
                - "type" (str): Тип операции, например, 'updateProduct'.
                - "data" (str): JSON-строка с ID продукта и изменяемыми атрибутами.
        """
        return {
            "type": "updateProduct",
            "data": json.dumps({
                "id": "BI_2683",
                "attributes": [
                    {
                        "id": "PPinfo_fix_HFM",
                        "values": [
                            {
                                "code": "(PPinfo_Fix_HFM_voc)PPInfo_Fix_HFM",
                                "value": "FIX"
                            }
                        ]
                    }
                ]
            })
        }

    @allure.step("Проверяем, что атрибут редактируем")
    def is_attribute_editable(self, data: dict, attr_id: str) -> bool:
        """Проверяет, редактируем ли атрибут по его идентификатору.

        Args:
            data (dict): Ответ от API, содержащий информацию об атрибутах.
            attr_id (str): Идентификатор атрибута, подлежащего проверке.

        Returns:
            bool: True, если атрибут редактируем (editable=True), иначе False.

        Raises:
            AssertionError: Если атрибут с заданным ID не найден в ответе.
        """
        for group in data["groupAttributes"]:
            for attr in group["attributes"]:
                if attr["id"] == attr_id:
                    return attr["editable"]

        for user in data["users"]:
            if user["id"] == attr_id:
                return user["editable"]

        raise AssertionError(
            f"Атрибут или пользователь с id '{attr_id}' не найден в данных"
        )
