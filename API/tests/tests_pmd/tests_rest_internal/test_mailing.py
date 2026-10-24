import warnings
from urllib.parse import urlparse, parse_qs

import allure
import pytest

from API.models.notification.notification import Notifications
from API.models.pmd.rest_internal_modules.mailing import Mailing
from API.utils.helpers import decode_unicode_in_collection

warnings.filterwarnings('ignore', message='numpy.dtype size changed')


# MAILING
@pytest.mark.api
@pytest.mark.lastv2
@allure.feature('Рассылка')
@allure.issue('https://jira.mts.ru/browse/PPI-2748',
              'PPInfo - Выгрузка в Excel статуса ответов рассылки актуализации данных')
@allure.issue('https://jira.mts.ru/browse/PPI-2747',
              'PPInfo - Отправка нотификации по актуализации данных')
@allure.issue('https://jira.mts.ru/browse/PPI-3365',
              'PPInfo - Управлять набором атрибутов для нотификации об актуализации данных (админка)')
class TestMailing(Mailing, Notifications):

    @allure.title('Запускаем рассылку')
    @pytest.mark.parametrize('product_type', ['notificationAttributesCommercial', 'notificationAttributesInternal'])
    def test_seng_mailing_without_skip_limit(self, rest_internal_client, product_type):
        assert self.send_mailing(rest_internal_client, product_type)['details'][0][
                   'message'] == 'Рассылку можно запустить через 90 дней'

    @allure.title('Количество строк в икселе')
    def test_excel_count_rows(self, rest_internal_client, clear_excel):

        self.delete_mailing_from_db('pmd')

        self.send_mailing_with_skip_limit(rest_internal_client, 'notificationAttributesCommercial')

        self.send_mailing_with_skip_limit(rest_internal_client, 'notificationAttributesInternal')

        count_rows = self.get_mailing_excel(rest_internal_client).max_row - 1

        count_messages = self.get_count_mailing_from_db('pmd')

        assert count_rows == count_messages, f'Количество строк в икселе({count_rows}) не совпадает с количеством отправленных сообщений({count_messages})'

    @allure.title('В рассылке состав атрибутов соответствует настройкам')
    @pytest.mark.parametrize('product_type', ['notificationAttributesCommercial', 'notificationAttributesInternal'])
    def test_comparison_tags_and_notification(self, rest_internal_client, ppinfo_client, product_type):
        self.delete_mailing_from_db('pmd')

        self.send_mailing_with_skip_limit(rest_internal_client, product_type)

        list_bodies = self.get_bodies_mailing_from_db('pmd')

        attributes_from_tag = self.get_all_active_attributes(ppinfo_client, product_type)

        for i in range(len(list_bodies)):
            assert [item['name'] for item in
                    decode_unicode_in_collection(list_bodies[i])['templateMeta'][
                        'createAttributes']] == attributes_from_tag

    @allure.title('Значение атрибутов в спецификации совпадают с актуальными (которые на странице продукта)')
    @pytest.mark.parametrize('product_type, product_codes', [
        ('notificationAttributesCommercial', ['BI_60']),
        ('notificationAttributesInternal', ['BI_63'])
    ])
    def test_attribute_values_in_the_notification_are_correct(self, ppinfo_client, rest_internal_client, product_type, product_codes):
        self.delete_mailing_from_db('pmd')
        self.send_mailing_with_skip_limit(rest_internal_client, product_type)
        list_bodies = self.get_bodies_mailing_from_db('pmd')

        for product_code in product_codes:
            for i in range(len(list_bodies)):
                if list_bodies[i]['templateMeta']['link'].split('/')[-2] == product_code:
                    attrs = [{item['name']: item['value']} for item in
                             list_bodies[i]['templateMeta']['createAttributes']]
                    for attr in attrs:
                        actual_value = next(iter(attr.values()))

                        expected_value = self.get_value_by_attribute_code_from_product(ppinfo_client, product_code, *attr.keys())
                        assert expected_value == actual_value, (
                            f'У продукта {product_code} в атрибуте {"".join(attr.keys())} '
                            f'на странице продукта значение {expected_value} не совпадает с значением  в нотификации {actual_value}')

    @allure.title(
        'Письма приходят только по продуктам которые соответвуют критериям (НЕ удаленные/архивные/банковские)')
    @pytest.mark.parametrize('product_type', [
        'notificationAttributesCommercial', 'notificationAttributesInternal'
    ])
    def test_legitimacy_of_products_being_included_in_the_notification(self, ppinfo_client, rest_internal_client, product_type):

        self.delete_mailing_from_db('pmd')
        self.send_mailing_with_skip_limit(rest_internal_client, product_type)
        list_bodies = self.get_bodies_mailing_from_db('pmd')

        error_products = []
        for i in range(len(list_bodies)):
            parsed_url = urlparse(list_bodies[i]['templateMeta']['link'])
            product_code = f"BI_{parse_qs(parsed_url.query).get('productCode', [None])[0]}"
            if not self.checking_the_legitimacy_of_sending(ppinfo_client, product_code):
                error_products.append(product_code)

        assert not len(error_products), f'Письма не должны были отправиться по продуктам {error_products}'

    @allure.title('Письма приходят корректным получателям')
    @pytest.mark.parametrize('product_type', [
        'notificationAttributesCommercial', 'notificationAttributesInternal'
    ])
    def test_check_recipients(self, ppinfo_client, rest_internal_client, user_service_client, product_type):

        self.delete_mailing_from_db('pmd')
        self.send_mailing_with_skip_limit(rest_internal_client, product_type)
        list_bodies = self.get_bodies_mailing_from_db('pmd')

        for i in range(len(list_bodies)):
            parsed_url = urlparse(list_bodies[i]['templateMeta']['link'])
            product_code = f"BI_{parse_qs(parsed_url.query).get('productCode', [None])[0]}"
            result = {}
            if 'to' in list_bodies[i].keys():
                result.update({'to': ''.join(list_bodies[i]['to'][0])})
            if 'cc' in list_bodies[i].keys():
                result.update({'cc': ''.join(list_bodies[i]['cc'][0])})

            info_po_cto_from_product = self.get_po_and_cto_from_product(user_service_client, ppinfo_client, product_code)

            error_text = f'Продукт  {product_code} \n Руководство в продукте {info_po_cto_from_product} \n Получатели нотификации {result}'

            print(error_text)

            if 'po' in info_po_cto_from_product.keys() and 'cto' in info_po_cto_from_product.keys():
                assert info_po_cto_from_product['po'] == result['to'], error_text
                assert info_po_cto_from_product['cto'] == result['cc'], error_text

            elif 'po' in info_po_cto_from_product.keys() and 'cto' not in info_po_cto_from_product.keys():
                assert info_po_cto_from_product['po'] == result['to'], error_text

            elif 'po' not in info_po_cto_from_product.keys() and 'cto' in info_po_cto_from_product.keys():
                assert info_po_cto_from_product['cto'] == result['to'], error_text
