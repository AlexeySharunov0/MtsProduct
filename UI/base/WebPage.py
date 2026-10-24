import logging
import time

from playwright.sync_api import Page, Locator

from UI.base.WebElement import WebElement

logger = logging.getLogger(__name__)


class WebPage:
    def __init__(self, page: Page):
        self._page = page
        self.context = page.context

    @property
    def url(self) -> str:
        return self._page.url

    def get_element(self, locator: str) -> Locator:
        """
        Получить элемент по локатору
        Args:
            locator: (str) xpath/css/etc.

        Returns: (Locator) искомый элемент

        """
        return self._page.locator(locator)

    def refresh(self) -> None:
        """
        Обновить страницу
        """
        logger.info('Обновляем страницу')
        self._page.reload()

    def get_page(self, link: str) -> None:
        """
        Перейти по ссылке на страницу
        Args:
            link: (str) ссылка
        """
        logger.info(f'Переходим по ссылке {link}')
        self._page.goto(link)

    def go_back(self) -> None:
        """
        Перейти на предыдущую страницу (кнопка назад)
        """
        logger.info('Переходим назад')
        self._page.go_back()

    def go_forward(self) -> None:
        """
        Перейти на следующую страницу (кнопка вперед)
        """
        logger.info('Переходим вперед')
        self._page.go_forward()

    def scroll_page_down(self, down_to: int) -> None:
        """
        Пролистать страницу. Если передать отрицательное значение, пролистнет вверх.
        Args:
            down_to: (int) кол-во пикселей
        """
        self.wait_force(1)
        logger.info(f'Листаем страницу вниз на {down_to} пикселей')
        self._page.mouse.wheel(0, down_to)

    def drag_and_drop(self, element_1: WebElement, element_2: WebElement) -> None:
        """
        Перенести элемент 1 к элементу 2
        Args:
            element_1: (WebElement) source элемент
            element_2: (WebElement) target элемент
        """
        logger.info('Используем drag and drop')
        self._page.drag_and_drop(element_1.locator, element_2.locator)

    def wait(self):
        """
        Ожидание какого-либо события
        """
        logger.info('Ожидаем')
        self._page.wait_for_load_state()

    @staticmethod
    def wait_force(timeout=1):
        """
        Ожидание (i'm sorry for this)
        """
        logger.info('Ожидаем')
        time.sleep(timeout)

    def open_new_tab(self, url: str) -> Page:
        """
        Открыть новую вкладку и перейти по указанной ссылке
        Args:
            url: (str) URL для перехода
        Returns: (Page) новая страница
        """
        logger.info(f'Открываем новую вкладку и переходим по ссылке {url}')
        new_page = self.context.new_page()
        new_page.goto(url)
        return new_page

    def switch_to_tab(self, tab_index: int) -> None:
        """
        Переключиться на вкладку по индексу
        Args:
            tab_index: (int) индекс вкладки
        """
        logger.info(f'Переключаемся на вкладку с индексом {tab_index}')
        pages = self.context.pages
        if 0 <= tab_index < len(pages):
            self._page = pages[tab_index]
        else:
            logger.error('Индекс вкладки вне диапазона')
