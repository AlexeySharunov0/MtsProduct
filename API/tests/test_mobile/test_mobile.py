import allure
import pytest

import requests
from API.models.mobile.mobile import Mobil
from API.utils.helpers import translate_text


@allure.feature('Мобильная апи')
@pytest.mark.api
@allure.issue('PPInfo - Моб. API - Поиск, страница продукта', 'https://jira.mts.ru/browse/PPI-931')
class TestMobilApi(Mobil):

    @allure.title('Проверка поиска по названию в мобильной апи')
    @pytest.mark.parametrize('pattern',
                             ['Маркетолог', 'Марк', 'марк', 'АТС', 'Умный', 'мой коннект', '8-800', 'АОН', 'Бизнес',
                              '*зве', 'Скоринг', 'RCS\RBM', 'библиотека'])
    @allure.issue('https://jira.mts.ru/browse/PPI-1081', 'PPInfo - Удаленные продукты в поисковой выдаче')
    def test_search_name_mobil(self, mobil_client, pattern):

        pattern = pattern.lower()
        for group in self.search(mobil_client, pattern):
            if group['Priority'] == 0:
                assert group['Products']
                for product in group['Products']:
                    if 'test' not in product['name'].lower():
                        assert pattern in product['name'].lower()

    @allure.title('Проверка поиска по названию с английской раскладкой в мобильной апи')
    @pytest.mark.parametrize('pattern',
                             ['vfhr', 'vfhrtnjkju', 'FNC'])
    def test_search_name_eng_mobil(self, mobil_client, pattern):

        incorrect_layout = "qwertyuiop[]asdfghjkl;'\zxcvbnm,."
        correct_layout = 'йцукенгшщзхъфывапролджэёячсмитьбю'

        converted_pattern = translate_text(pattern.lower(), incorrect_layout, correct_layout)
        for group in self.search(mobil_client, pattern):
            if group['Priority'] == 0:
                assert group['Products']
                for product in group['Products']:
                    if 'test' not in product['name'].lower():
                        assert converted_pattern in product['name'].lower()

    @allure.title('Проверка поиска по названию с русской раскладкой в мобильной апи')
    @pytest.mark.parametrize('pattern',
                             ['сфырифсл', 'дшму', 'ьгышс', 'ФИЦ', 'сфдд', 'Ашт'])
    def test_search_name_rus_mobil(self, mobil_client, pattern):

        correct_layout = "qwertyuiop[]asdfghjkl;'\zxcvbnm,."
        incorrect_layout = 'йцукенгшщзхъфывапролджэёячсмитьбю'

        converted_pattern = translate_text(pattern.lower(), incorrect_layout, correct_layout)

        for group in self.search(mobil_client, pattern):
            if group['Priority'] == 0:
                assert group['Products']
                for product in group['Products']:
                    if 'test' not in product['name'].lower():
                        assert converted_pattern in product['name'].lower()

    @allure.title('Проверка поиска по старому названию в мобильной апи')
    @pytest.mark.parametrize('pattern, result',
                             [('test ctujvso', 'новое название'), ('test fqvxtna', 'новое название1'),
                              ('test oalxxlb', 'новое название2')])
    def test_search_old_name_mobil(self, mobil_client, pattern, result):

        for group in self.search(mobil_client, pattern):
            if group['Priority'] == 1:
                assert group['Products']
                for product in group['Products']:
                    assert result in product['name'].lower()

    @allure.title('Проверка поиска по витрине в мобильной апи')
    @pytest.mark.parametrize('pattern, result',
                             [('Марс', 'МТС Поиск'),
                              ('Юпитер', 'МТС Music'),
                              ('Уран', 'Сайт МТС')]
                             )
    def test_search_showcase_mobil(self, mobil_client, pattern, result):

        for group in self.search(mobil_client, pattern):
            if group['Priority'] == 1:
                assert group['Products']
                for product in group['Products']:
                    assert result.lower() == product['name'].lower()

    @allure.title('Проверка поиска по пользователю в мобильном апи')
    @pytest.mark.parametrize('pattern, result',
                             [('Всезнаковый', 'Автотесты_поиск'),
                              ('user-with.all_signs123', 'Автотесты_поиск'),
                              ('Никифоров', 'Автотесты_поиск')]
                             )
    def test_search_users_mobil(self, mobil_client, pattern, result):

        for group in self.search(mobil_client, pattern):
            if group['Priority'] == 1:
                with allure.step('Проверяем, что нужный продукт найден по совпадению в содержании'):
                    assert group['Products'], 'Поиск не дал результатов'

                with allure.step('Проверяем, что нужный продукт найден'):
                    assert any(result.lower() in product['name'].lower() for product in
                               group['Products']), 'Поиск не дал результатов'

    @allure.title('Проверка поиска по коду BI в мобильной апи')
    @pytest.mark.parametrize('pattern, result',
                             [('BI_1287', 'E-sensor'),
                              ('BI_60', 'МТС Маркетолог'),
                              ('BI_1883', 'MTS Social ads'),
                              ('BI_1921', '1C')])
    def test_search_bi_code_mobil(self, mobil_client, pattern, result):

        for group in self.search(mobil_client, pattern):
            if group['Priority'] == 1:
                assert group['Products']
                for product in group['Products']:
                    assert result.lower() == product['name'].lower()

    @allure.title('Проверка поиска по фикрым кода в мобильной апи')
    @pytest.mark.parametrize('pattern, result',
                             [('1287', 'E-sensor'),
                              ('1285', 'Skytracking security'),
                              ('1883', 'MTS Social ads'),
                              ('1921', '1C')])
    def test_search_num_code_mobil(self, mobil_client, pattern, result):

        for group in self.search(mobil_client, pattern):
            if group['Priority'] == 1:
                assert group['Products']
                for product in group['Products']:
                    assert result.lower() == product['name'].lower()


    @allure.title('Проверка поиска по коду Oracle в мобильной апи')
    @pytest.mark.parametrize('pattern, result',
                             [('UDom', 'МТС Умный дом'), ('mMTS', 'Мой МТС')])
    def test_search_oracle_mobil(self, mobil_client, pattern, result):

        for group in self.search(mobil_client, pattern):
            if group['Priority'] == 1:
                assert group['Products']
                for product in group['Products']:
                    assert result.lower() == product['name'].lower()

    @allure.title('Проверка поиска по приложениям в мобильной апи')
    @pytest.mark.parametrize('pattern, result',
                             [('SSO mobile', 'МТС Умный дом'), ('PRO.501', 'МТС Умный дом'),
                              ('PRO501', 'МТС Умный дом')])
    def test_search_app_mobil(self, mobil_client, pattern, result):

        for group in self.search(mobil_client, pattern):
            if group['Priority'] == 1:
                assert group['Products']
                for product in group['Products']:
                    assert result.lower() == product['name'].lower()

    @allure.title('В поиске по названию по имени продукты с инициированным закрытием отображаются не в конце')
    @pytest.mark.parametrize('pattern',
                             ['мтс'])
    @allure.issue('https://jira.mts.ru/browse/PPI-1509',
                  'PPInfo - Порядок отображения карточек с инициировано закрытие')
    def test_search_init_close_name(self, mobil_client, pattern):

        for group in self.search(mobil_client, pattern):
            if group['Priority'] == 0:
                for properties in group['Products'][-1:]:
                    assert properties['code'] == 'BI_271'

    @allure.title('В поиске по названию по содержанию продукты с инициированным закрытием отображаются в конце')
    @pytest.mark.parametrize('pattern',
                             ['зимина', 'Зимина Ольга Николаевна'])
    @allure.issue('https://jira.mts.ru/browse/PPI-1509',
                  'PPInfo - Порядок отображения карточек с инициировано закрытие')
    def test_search_init_close_other(self, mobil_client, pattern):

        for group in self.search(mobil_client, pattern):
            if group['Priority'] == 1:
                for properties in group['Products'][-1:]:
                    assert properties['code'] == 'BI_22315'

    @allure.title('Получение продуктов в мобильной апи и проверка атрибутов')
    @pytest.mark.parametrize('pattern', ['60', '1905', '2914', '3192', '326', '1883'])
    def test_get_product_mobil_attrs(self, mobil_client, pattern):

        product_info = self.get_product_mobil(mobil_client, pattern)

        attr_v1 = ['PPinfo_status', 'PPInfo_main_product', 'PPInfo_new_oracle_code', 'PPinfo_start_close', 'PPinfo_mvp',
                   'PPInfo_data_endmoney', 'PPinfo_market', 'PPinfo_web_app', 'PPInfo_product_block',
                   'Klaster', 'PPInfo_type_develop', 'PPInfo_class_criticality', 'PPInfo_class_product',
                   'PPInfo_internal_KTS', 'PPInfo_tech_strategy', 'PPInfo_comment_strategy',
                   'employee_chief_PO', 'employee_product_owner', 'employee_tech_lead', 'PPInfo_admin_data',
                   'INTEGRATION_Cluster']

        x = [attribute['code'] for attribute in product_info['attributes']]

        assert not set(attr_v1).symmetric_difference(x), f'В АПИ пришли не все атрибуты'

    @allure.title('Получение логотипов по продуктам')
    @pytest.mark.parametrize('pattern', [60, 1905, 326])
    def test_get_logo_product(self, mobil_client, pattern):

        assert self.get_logo(mobil_client, pattern) in ['image/png', 'image/jpeg']

    @allure.title('Получение логотипов по продуктам у которых нет логотипа')
    @pytest.mark.parametrize('pattern', [2914, 3192, 1883])
    def test_get_logo_product_without_logo(self, mobil_client, pattern):

        assert self.get_logo(mobil_client, pattern) == 'image/svg+xml'

    @allure.issue('https://jira.mts.ru/browse/PPI-2351', 'PPInfo - Добавить Мои продукты в Mobile API')
    @allure.title('Получение списка  моих продуктов')
    def test_get_managed_list(self, mobil_client):

        self.get_managed(mobil_client)

    @allure.issue('https://jira.mts.ru/browse/PPI-2351', 'PPInfo - Добавить Мои продукты в Mobile API')
    @allure.title('Порядок продуктов в списке моих продуктов неизменный')
    def test_get_managed_list_sort(self, mobil_client):

        assert self.get_managed(mobil_client) == self.get_managed(mobil_client), 'Каждый новый запрос порядок продуктов меняется'

    @allure.issue('https://jira.mts.ru/browse/PPI-1016', 'PPInfo - Моб. API - Избранное')
    @allure.title('Получение списка избранных продуктов')
    def test_get_favorite_list(self, mobil_client):

        self.get_favorite(mobil_client)

    @allure.issue('https://jira.mts.ru/browse/PPI-1016', 'PPInfo - Моб. API - Избранное')
    @allure.title('Добавление и удаление продукта из списка избранных продуктов')
    def test_add_favorite_list(self, mobil_client):
        self.add_delete_favorite(mobil_client)
        self.check_product_in_favorite(mobil_client)
        self.add_delete_favorite(mobil_client)
        self.check_product_not_in_favorite(mobil_client)

    @allure.title('В мобильной апи есть атрибут Интеграционный кластер')
    @allure.issue('https://jira.mts.ru/browse/PPI-1455',
                  'PPInfo - Добавить атрибут "Интеграционный кластер" в Mobile API')
    def test_cluster_in_mobil_api(self, mobil_client):

        assert any(
            attributes['code'] == 'INTEGRATION_Cluster' for attributes in self.get_product_mobil(mobil_client, '60')['attributes'])

    @allure.title('Получение продукта в мобильной апи v2')
    @allure.issue('https://jira.mts.ru/browse/PPI-2989', 'PPInfo - Передача меню в МультХаб')
    @pytest.mark.parametrize('pattern', ['60', '1905', '2914', '3192', '326', '1883'])
    def test_get_product_mobil_v2(self, pattern, mobil_client):

        product_info = self.get_product_v2(mobil_client, pattern)

        x = [attribute['code'] for attribute in product_info['attributes']]

        attr_v1 = ['PPinfo_status', 'PPInfo_main_product', 'PPInfo_new_oracle_code', 'PPinfo_start_close', 'PPinfo_mvp',
                   'PPInfo_data_endmoney', 'PPinfo_market', 'PPinfo_web_app', 'PPInfo_product_block',
                   'Klaster', 'PPInfo_type_develop', 'PPInfo_class_criticality', 'PPInfo_class_product',
                   'PPInfo_internal_KTS', 'PPInfo_tech_strategy', 'PPInfo_comment_strategy',
                   'employee_chief_PO', 'employee_product_owner', 'employee_tech_lead', 'PPInfo_admin_data',
                   'INTEGRATION_Cluster']

        attr_v2 = ['Vydelennyi_ekspert_IB_', 'Kurator_ot_fin.kontrollinga', 'Kurator_ot_fin._kontrollinga',
                   'Kurator_ot_iurid._podrazdeleniia_new', 'Glavnyi_arkhitektor_klastera',
                   'Kurator_Agile_praktik', 'Kuratory_po_strategii_klastera',
                   'Kuratory_po_podboru_personala_v_MTS_Didzhital',
                   'Kurator_ot_tsentra_finansovogo_partnerstva_Didzhital',
                   'Kuratory_praktik_DevOps_v_klasterakh', 'Administrator_dannykh_klastera', 'PPInfo_site_landing',
                   'Sonfluence', 'Segment_potrebitelei', 'PPinfo_values',
                   'PPinfo_konkurent', 'EXTRA_OldProductName']

        difference_attrs = set(attr_v1 + attr_v2).symmetric_difference(x)
        assert not difference_attrs, f'В АПИ пришли не все атрибуты, проблема в атрибутах {", ".join(difference_attrs)}'
