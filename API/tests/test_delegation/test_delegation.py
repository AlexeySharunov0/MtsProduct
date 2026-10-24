import allure
import pytest

from API.api_fixtures import ppinfo_user_client
from API.models.delegation.delegation import Delegation
from API.models.ppinfo.brief import Brief
from API.models.ppinfo.product_v2 import ProductV2


@pytest.mark.api
@allure.feature('Делегирование')
@allure.label('priority', 'Высокий')
@allure.issue('https://jira.mts.ru/browse/PPI-148', 'PPInfo - Делегирование прав')
@allure.issue('https://jira.mts.ru/browse/PPI-4050', 'PPInfo - Отображение на странице "Мои продукты"')
class TestDelegation(Delegation, Brief, ProductV2):

    @allure.title('Получаем все делегирования')
    def test_get_delegations(self, rest_internal_client):
        self.get_delegations(rest_internal_client)

    @allure.title('Делегируем полномочия, а потом забираем права')
    def test_make_delegation(self, ppinfo_client, rest_internal_client):
        self.remove_delegation(ppinfo_client, rest_internal_client)
        self.add_delegation(ppinfo_client)
        self.check_presence(rest_internal_client)
        self.remove_delegation(ppinfo_client, rest_internal_client)
        self.check_absence(rest_internal_client)

    @allure.title('Отправляем заявку в рамках делегирования')
    def test_brief_delegation(self, ppinfo_client, ppinfo_user_client, rest_internal_client):
        with allure.step('Выдаем права на делегирование'):
            self.remove_delegation(ppinfo_client, rest_internal_client)
            self.add_delegation(ppinfo_client)
            self.check_presence(rest_internal_client)

        with allure.step('Отправляем заявку на редактирование продукта с делегированием'):
            self.crete_brief_by_user(ppinfo_user_client, self.get_data_for_delegation_brief())

        with allure.step('Забираем права на делегирование'):
            self.check_presence(rest_internal_client)
            self.remove_delegation(ppinfo_client, rest_internal_client)
            self.check_absence(rest_internal_client)

        with allure.step('Пробуем отправить заявку на делегирование без прав'):
            self.crete_brief_by_user_403(ppinfo_user_client, self.get_data_for_delegation_brief())

    @allure.title(
        'С правами делегирования на странице продукта есть возможность редактировать атрибуты (Отображение карандашей на фронте)')
    def test_edit_attributes_with_delegation(self, ppinfo_client, ppinfo_user_client, rest_internal_client):
        product_code = 'BI_2683'
        attribute_1 = 'PPInfo_admin_data'
        attribute_2 = 'employee_tech_lead'

        self.remove_delegation(ppinfo_client, rest_internal_client)

        with allure.step('Проверяем, что атрибуты не редактируемы без делегирования'):
            product_info = self.get_info_by_product_code_by_user(ppinfo_user_client, product_code)

            assert not self.is_attribute_editable(product_info,
                                                  attribute_1), f'Атрибут {attribute_1} должен быть НЕ редактируем без делегирования'
            assert not self.is_attribute_editable(product_info,
                                                  attribute_2), f'Атрибут {attribute_2} должен быть НЕ редактируем без делегирования'

        self.add_delegation(ppinfo_client)
        self.check_presence(rest_internal_client)

        with allure.step('Проверяем, что атрибуты становятся редактируемыми после делегирования'):
            product_info = self.get_info_by_product_code_by_user(ppinfo_user_client, product_code)

            assert self.is_attribute_editable(product_info, attribute_1), f'Атрибут {attribute_1} должен быть редактируем после делегирования'
            assert self.is_attribute_editable(product_info, attribute_2), f'Атрибут {attribute_2} должен быть редактируем после делегирования'

        self.remove_delegation(ppinfo_client, rest_internal_client)

    @allure.title('Продукт исчезает из Делегированных продуктов после архивирования')
    @allure.issue('PPInfo - "Мои продукты" в Архиве: убрать делегирование', 'https://jira.mts.ru/browse/PPI-4239')
    def test_product_disappears_from_delegation_after_archive(self, rest_internal_client, ppinfo_client):
        product_code = 'BI_2683'
        try:
            with allure.step('Получаем список делегированных продуктов'):
                delegations = self.get_delegations(rest_internal_client)

                assert any(delegation for delegation in delegations if delegation['product']['code'] == product_code), 'Активный продукт не найден в списке делегированных'

            with allure.step(f'Архивируем продукт {product_code}'):
                self.change_status(ppinfo_client, 'Arkhiv', 'Архив', product_code)

            with allure.step('Проверяем, что продукт исчез из списка делегированных продуктов'):
                delegations_after = self.get_delegations(rest_internal_client)

                assert not any(
                    delegation for delegation in delegations_after if delegation['product']['code'] == product_code), 'Архивный продукт не удален из списка делегированных'

        finally:
            self.change_status(ppinfo_client, 'Zapushchen_v_PE', 'Запущен в ПЭ', product_code)

    @allure.title('Сортировка в делегирование')
    @allure.issue('PPInfo - "Мои продукты" в Архиве: убрать делегирование', 'https://jira.mts.ru/browse/PPI-4239')
    def test_delegation_products_sorting(self, rest_internal_client, ppinfo_user_client):
        delegation_products = self.get_delegations(rest_internal_client)

        delegation_products_list = []

        for product in delegation_products:
            info_about_product = self.get_info_by_product_code(ppinfo_user_client, product['product']['code'])
            for attribute in info_about_product['hidingAttributes']:
                if attribute['id'] == 'PPinfo_start_close':
                    if attribute['values']:
                        start_close = attribute['values'][0]['code'] == '(PPinfo_spravochnik_start_close)Yes'
                    else:
                        start_close = False

                    delegation_products_list.append((product['product']['name'], start_close))

        sorted_delegation_products_list = sorted(delegation_products_list, key=lambda x: (x[1], x[0]))

        assert sorted_delegation_products_list == delegation_products_list, 'Список делегированных продуктов не отсортирован'
