import logging

from playwright.sync_api import Page

from UI.base.WebPage import WebPage
from UI.pages.product_page.dependency.dependency_locators import DependencyLocators

logger = logging.getLogger(__name__)


class DependencyPage(WebPage, DependencyLocators):
    def __init__(self, page: Page, url: str = None):

        WebPage.__init__(self, page)
        DependencyLocators.__init__(self, page)
        self._page = page
        self.base_url = url if url else 'https://stage.prodboard.example.com/product/BI_2201/dependencies'
        self.get_page(self.base_url)

