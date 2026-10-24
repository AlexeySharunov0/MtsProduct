import allure
import pytest

from API.models.pmd.internal_product_v1 import InternalV1Product


@pytest.mark.api
@allure.label('priority', 'Высокий')
@allure.feature('Удаление/восстановление продукта')
@allure.issue('https://jira.mts.ru/browse/PPI-628', 'PPInfo - Удаление продуктов')
class TestDeleteProduct(InternalV1Product):

    @allure.title('Корректное удаление продукта')
    @pytest.mark.parametrize('reason', ['Oshibochnoe_zavedenie', 'Reviu_kataloga', 'Reshenie_komandy_produkta'])
    def test_delete_product(self, ppinfo_client, pmd_internal_gw_client, reason):

        params = self.get_data_for_delete(reason)

        if self.check_deleted(ppinfo_client):
            self.recover_product(pmd_internal_gw_client)

        self.delete_product(pmd_internal_gw_client, params)

        assert self.check_deleted(ppinfo_client), 'Продукт не удалился'

    @allure.title('Попытка удаления продукта с атомарными')
    def test_delete_product_with_atomic(self, ppinfo_client, pmd_internal_gw_client):

        params = self.get_data_for_delete()

        if self.check_deleted(ppinfo_client, bi='BI_60'):
            self.recover_product(pmd_internal_gw_client, bi='BI_60')

        self.delete_product_403(pmd_internal_gw_client, params, bi='BI_60')

        assert not self.check_deleted(ppinfo_client, bi='BI_60'), 'Продукт удалился'

    @allure.title('Попытка удаления несуществующего продукта')
    @allure.issue('https://jira.mts.ru/browse/PPI-2088',
                  'PPinfo - 500 ошибка в методе удаления продукта по несуществующему BI коду')
    def test_delete_invalid_product(self, pmd_internal_gw_client):

        params = self.get_data_for_delete()

        self.delete_product_404(pmd_internal_gw_client, params, bi='BI_1234512345')

    @allure.title('Удаление удаленного продукта')
    def test_delete_deleted(self, ppinfo_client, pmd_internal_gw_client):

        params = self.get_data_for_delete()

        if not self.check_deleted(ppinfo_client):
            self.delete_product(pmd_internal_gw_client, params)

        self.delete_product_400(pmd_internal_gw_client, params)

    @allure.title('Удаление с некорректной причиной')
    @pytest.mark.parametrize('reason', ['invalid_reason', None])
    def test_invalid_reason(self, ppinfo_client, pmd_internal_gw_client, reason):

        params = self.get_data_for_delete(reason)

        if self.check_deleted(ppinfo_client):
            self.recover_product(pmd_internal_gw_client)

        self.delete_product_400(pmd_internal_gw_client, params)

        assert not self.check_deleted(ppinfo_client), 'Продукт удалился'

    @allure.title('Удаление с некорректным комментарием')
    @pytest.mark.parametrize('description', [
        '7777 777 777 777 777 777 777 777 777 777 777 777 777 777 777 777 777 777 777 777 777 777 777 777 777 777 777 777 777 777 777 777 777 777 777 777 777 777 777 7777',
        None])
    def test_invalid_description(self, ppinfo_client, pmd_internal_gw_client, description):

        params = self.get_data_for_delete(description=description)

        if self.check_deleted(ppinfo_client):
            self.recover_product(pmd_internal_gw_client)

        self.delete_product_400(pmd_internal_gw_client, params)

        assert not self.check_deleted(ppinfo_client), 'Продукт удалился'

    @allure.title('Корректное восстановление продукта')
    def test_recover_product(self, ppinfo_client, pmd_internal_gw_client):

        if not self.check_deleted(ppinfo_client):
            self.delete_product(pmd_internal_gw_client, self.get_data_for_delete())

        self.recover_product(pmd_internal_gw_client)

        assert not self.check_deleted(ppinfo_client), 'Продукт не восстановился'

    @allure.title('Восстановление НЕ удаленного продукта')
    def test_recover_recovered(self, ppinfo_client, pmd_internal_gw_client):

        if not self.check_deleted(ppinfo_client):
            self.recover_product_400(pmd_internal_gw_client)
        else:
            self.recover_product(pmd_internal_gw_client)
            self.recover_product_400(pmd_internal_gw_client)

        assert not self.check_deleted(ppinfo_client), 'Продукт восстановился'

    @allure.title('Попытка восстановления несуществующего продукта')
    @allure.issue('https://jira.mts.ru/browse/PPI-2089',
                  'PPinfo - 500 ошибка в методе восстановления продукта по несуществующему BI коду')
    def test_recover_invalid_product(self, pmd_internal_gw_client):

        self.recover_product_404(pmd_internal_gw_client, bi='BI_12345')
