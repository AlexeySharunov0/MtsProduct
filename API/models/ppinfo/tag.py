from typing import Dict, Any

import allure

from API.data.ppinfo import TagClass

HOST = 'https://stage.prodboard.example.com'


# TODO: дозаполнить раздел
class TagUrls:
    """
    https://stage.prodboard.example.com/ppinfo/swagger/tag/index.html#/
    """

    ADD_ATTRIBUTE = 'v1/tag/attribute'

    DELETE_ATTRIBUTE = 'v1/tag/{}/attribute/{}'

    ADD_USER = 'v1/tag/user'

    DELETE_USER = 'v1/tag/{}/user/{}'

    GET_TAG = 'v1/tag/{}'


class Tag(TagUrls):

    @allure.step("Добавление атрибута")
    def add_attr(self, client, attr_id: str, tag_id: str) -> None:
        data = {
            "id": attr_id,
            "tagId": tag_id
        }
        client.post(self.ADD_ATTRIBUTE, json=data)

    @allure.step("Удаление атрибута")
    def delete_attr(self, client, tag_id: str, attr_id: str) -> None:
        client.delete(self.DELETE_ATTRIBUTE.format(tag_id, attr_id))

    @allure.step("Добавление юзера")
    def add_user(self, client, data: Dict[str, str]) -> None:
        client.post(self.ADD_USER, json=data)

    @allure.step("Удаление юзера")
    def delete_user(self, client, tag_id: str, login: str, session=False) -> None:
        client.delete(self.DELETE_USER.format(tag_id, login))

    @allure.step("Получаем значения в разделе")
    def get_tag_info(self, client, tag_id: str) -> Dict[str, Any]:
        response = client.get(self.GET_TAG.format(tag_id))

        TagClass(**response)

        return response

    @allure.step('Получение информации о всех активных атрибутах из настроек')
    def get_all_active_attributes(self, client, product_type: str):
        info_from_tag = self.get_tag_info(client, product_type)

        active_attr = [attr['name'] for attr in info_from_tag['attributes'] if attr['isEnable']]

        return active_attr
