import allure
import pytest

from API.models.ppinfo.draft import Drafts


@pytest.mark.api
@allure.feature('Черновики')
class TestDraft(Drafts):

    @allure.title('Создание черновика на апдейт продукта')
    @pytest.mark.parametrize('product_id', ('BI_42', 'BI_200', 'BI_1124'))
    def test_create_draft_update_product(self, ppinfo_client, product_id):
        params = self.get_draft_params({'externalId': product_id, 'type': 'updateProduct'})

        self.create_draft(ppinfo_client, params)

        with allure.step('Проверяем, что такой черновик появился'):
            self.get_draft(ppinfo_client, params)

        self.delete_draft(ppinfo_client, params)

        with allure.step('Проверяем, что черновик удалился'):
            self.get_draft_404(ppinfo_client, params)

    @allure.title('Создание черновика на создание продукта')
    @pytest.mark.parametrize('product_type', ('Internal', 'Commercial'))
    def test_create_draft_add_product(self, ppinfo_client, product_type):
        params = self.get_draft_params({'externalId': product_type})

        self.create_draft(ppinfo_client, params)

        with allure.step('Проверяем, что такой черновик появился'):
            self.get_draft(ppinfo_client, params)

        self.delete_draft(ppinfo_client, params)

        with allure.step('Проверяем, что черновик удалился'):
            self.get_draft_404(ppinfo_client, params)
