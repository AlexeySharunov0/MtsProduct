import logging

from playwright.sync_api import Page

from UI.base.WebPage import WebPage
from UI.pages.product_page.metrics.metrics_locators import MetricsPageLocators

logger = logging.getLogger(__name__)


class MetricsPage(WebPage, MetricsPageLocators):
    def __init__(self, page: Page, url: str = None):
        WebPage.__init__(self, page)  # Явный вызов инициализатора WebPage
        MetricsPageLocators.__init__(self, page)  # Явный вызов инициализатора CanvasPageLocators
        self._page = page

        self.base_url = url if url else 'https://stage.prodboard.example.com/product/BI_60/metrics'
        self.get_page(self.base_url)
