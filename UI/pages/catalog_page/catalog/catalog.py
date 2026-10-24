import logging

import allure
from playwright.sync_api import Page

from API.models.ppinfo.product_v2 import ProductV2
from UI.base.WebPage import WebPage
from UI.pages.catalog_page.catalog.catalog_locators import CatalogPageLocators

logger = logging.getLogger(__name__)


class CatalogPage(WebPage, CatalogPageLocators):
    def __init__(self, page: Page, url: str = None):
        WebPage.__init__(self, page)  # Явный вызов инициализатора WebPage
        CatalogPageLocators.__init__(self, page)  # Явный вызов инициализатора CanvasPageLocators
        self._page = page
        self.base_url = url if url else 'https://stage.prodboard.example.com/preset/all'
        self.get_page(self.base_url)

    def execute_search(self, word: str):
        """ Выполняет поиск переданной строки в строке поиска и закрывает её """

        with allure.step('Кликаем на строку поиска'):
            self.wait_force(1)
            self.search_str_closed.click()
        with allure.step(f'Вводим слово по которому нужно осуществить поиск - {word}'):
            self.search_str.fill(word)
        with allure.step('Нажимаем ENTER'):
            self.search_str.press_key("Enter")
            self.wait_force(2)

    def check_ecosystem_product(self, ppinfo_client, product_url: str) -> bool:
        """
        Метод для проверки Экосистемности первого по счету продукта
        Args:
            ppinfo_client: Клиент API для работы с ppinfo service
            product_url: Получаем сырой урл первого продукта
        Returns:
            Возвращаем True, если продукт Экосистемный и False в противном случае
        """
        product = ProductV2()

        bi_code = product_url.strip('/').split('/')[-1]
        info_about_product = product.get_info_by_product_code(ppinfo_client, product_code=bi_code)

        for attr in info_about_product['hidingAttributes']:
            if attr['id'] == 'PPInfo_IsEcosystem':
                return attr['values'][0]['value'] == 'Да'

    def check_word_in_list_item(self, first_word_of_param, page_filter_chipses_texts):
        for chip_text in page_filter_chipses_texts:
            if first_word_of_param in chip_text:
                return True
        return False
