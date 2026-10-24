import logging
import allure

from playwright.sync_api import Page

from UI.base.WebPage import WebPage
from UI.pages.product_page.health.health_locators import HealthPageLocators

logger = logging.getLogger(__name__)


class HealthPage(WebPage, HealthPageLocators):
    def __init__(self, page: Page, url: str = None):

        WebPage.__init__(self, page)
        HealthPageLocators.__init__(self, page)
        self._page = page
        self.base_url = url if url else 'https://stage.prodboard.example.com/product/BI_60/health'
        self.get_page(self.base_url)

    @allure.step("Проверить видимость и текст элемента")
    def verify_element_visibility_and_text(self, element, expected_text, element_name):
        """
        Проверяет видимость и текст элемента.
        element: Элемент, который нужно проверить.
        expected_text: Ожидаемый текст элемента.
        element_name: Имя элемента для шага Allure.
        """
        with allure.step(f"Проверяем, что {element_name} отображается"):
            assert element.is_visible(), f"{element_name} не отображается"

        with allure.step(f"Проверяем текст {element_name}"):
            actual_text = element.get_text().strip()
            assert actual_text == expected_text, f"Ожидался текст '{expected_text}', но был '{actual_text}'"