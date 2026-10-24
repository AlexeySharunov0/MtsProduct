import logging
import time

import allure
from playwright.sync_api import Page

from UI.base.WebPage import WebPage
from UI.pages.product_page.documents.documents_locators import DocumentsPageLocators

logger = logging.getLogger(__name__)


class DocumentsPage(WebPage, DocumentsPageLocators):
    def __init__(self, page: Page, url: str = None):
        WebPage.__init__(self, page)  # Явный вызов инициализатора WebPage
        DocumentsPageLocators.__init__(self, page)  # Явный вызов инициализатора CanvasPageLocators
        self._page = page

        self.base_url = url if url else 'https://stage.prodboard.example.com/product/BI_60/docs'
        self.get_page(self.base_url)

    @allure.step("Удаляем все документы")
    def clear_docs(self):
        for _ in self.delete_doc_many.get_items():
            self.delete_doc.click()
            self.delete_confirmation.click()

    @allure.step("Удаляем документ")
    def delete_doc_once(self):
        time.sleep(1)
        self.delete_doc.click()
        self.delete_confirmation.click()
        self.wait()
