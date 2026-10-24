import logging

from playwright.sync_api import Page

from UI.base.WebPage import WebPage
from UI.pages.product_page.projects.projects_locators import ProjectsPageLocators

logger = logging.getLogger(__name__)


class ProjectsPage(WebPage, ProjectsPageLocators):
    def __init__(self, page: Page, url: str = None):
        WebPage.__init__(self, page)  # Явный вызов инициализатора WebPage
        ProjectsPageLocators.__init__(self, page)  # Явный вызов инициализатора CanvasPageLocators
        self._page = page

        self.base_url = url if url else 'https://stage.prodboard.example.com/product/BI_60/projects'
        self.get_page(self.base_url)
