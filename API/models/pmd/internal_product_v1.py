from typing import Any

import allure

from API.models.ppinfo.product_v2 import ProductV2

HOST = 'https://stage.prodboard.example.com'


class InternalV1ProductUrls:
    """
    https://stage.prodboard.example.com/pmd/swagger/internal/v1/product/index.html
    """

    # Удаление продукта
    DELETE_PRODUCT = 'v1/product/{}'

    # Восстановление продукта
    RECOVER_PRODUCT = 'v1/product/{}/recover'


class InternalV1Product(InternalV1ProductUrls, ProductV2):

    @allure.step("Получаем данные для удаления продукта")
    def get_data_for_delete(self, reason: str = "Oshibochnoe_zavedenie", description: str = "qwe"):
        return {
            'codeReason': reason,
            'description': description
        }

    @allure.step('Проверка, что продукт удален')
    def check_deleted(self, client, bi: str = 'BI_7099') -> bool:
        return self.get_info_by_product_code(client, bi)['reasonDeletion'] is not None

    @allure.step('Удаление продукта')
    def delete_product(self, client, param: dict[str, Any], bi: str = 'BI_7099') -> dict[str, Any]:
        response = client.delete(self.DELETE_PRODUCT.format(bi), params=param)

        return response

    @allure.step('Некорректное удаление продукта 403')
    def delete_product_403(self, client, param: dict[str, Any], bi: str = 'BI_7099') -> None:
        response = client.delete(self.DELETE_PRODUCT.format(bi), params=param, expected_status_code=403)

        return response

    @allure.step('Некорректное удаление продукта 404')
    def delete_product_404(self, client, param: dict[str, Any], bi: str = 'BI_7099') -> None:
        client.delete(self.DELETE_PRODUCT.format(bi), params=param, expected_status_code=404)

    @allure.step('Некорректное удаление продукта 400')
    def delete_product_400(self, client, param: dict[str, Any], bi: str = 'BI_7099') -> None:
        client.delete(self.DELETE_PRODUCT.format(bi), params=param, expected_status_code=400)

    @allure.step('Восстановление продукта')
    def recover_product(self, client, bi: str = 'BI_7099') -> dict[str, Any]:
        response = client.post(self.RECOVER_PRODUCT.format(bi))

        return response

    @allure.step('Некорректное восстановление продукта')
    def recover_product_404(self, client, bi: str = 'BI_7099'):
        client.post(self.RECOVER_PRODUCT.format(bi), expected_status_code=404)

    @allure.step('Некорректное восстановление продукта')
    def recover_product_400(self, client, bi: str = 'BI_7099'):
        client.post(self.RECOVER_PRODUCT.format(bi), expected_status_code=400)
