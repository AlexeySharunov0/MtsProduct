import logging
import random
import string
import time

from selenium.common import WebDriverException
from termcolor import colored

logger = logging.getLogger(__name__)


class WebPage(object):
    _web_driver = None

    def __init__(self, driver, url=''):
        self._web_driver = driver
        self._web_driver.implicitly_wait(5)
        self.get(url)

    def __setattr__(self, name, value):
        if not name.startswith('_'):
            self.__getattribute__(name)._set_value(self._web_driver, value)
        else:
            super(WebPage, self).__setattr__(name, value)

    def __getattribute__(self, item):
        attr = object.__getattribute__(self, item)

        if not item.startswith('_') and not callable(attr):
            attr._web_driver = self._web_driver
            attr._page = self

        return attr

    def get(self, url: str, retries: int = 5, delay: int = 2) -> None:
        """
        Переход на указанную страницу с ретраями в случае ошибки.

        Args:
            url: ссылка, на которую осуществляется переход
            retries: количество попыток
            delay: задержка между попытками в секундах
        """
        logger.info(f'Переходим на страницу {url}')

        attempt = 0
        while attempt < retries:
            try:
                self._web_driver.get(url)
                self.wait_page_loaded()
                break
            except WebDriverException as e:
                logger.error(f'Ошибка при переходе на страницу {url}: {e}')
                attempt += 1
                if attempt < retries:
                    logger.info(f'Пробуем снова через {delay} секунд...')
                    time.sleep(delay)
                else:
                    logger.error(f'Не удалось перейти на страницу {url} после {retries} попыток')
                    raise  # Пробрасываем исключение, если все попытки исчерпаны

    def go_back(self) -> None:
        """
        Переход на страницу назад
        """
        logger.info(f'Возвращаемся назад')

        self._web_driver.back()
        self.wait_page_loaded()

    def refresh(self) -> None:
        """
        Обновление текущей страницы
        """
        logger.info(f'Обновляем текущую страницу')

        self._web_driver.refresh()
        self.wait_page_loaded()

    def screenshot(self, file_name: str = 'screenshot.png') -> None:
        """
        Сделать скриншот
        Args:
            file_name: название файла, в который будет сохранен скриншот
        """
        logger.info(f'Делаем скриншот')

        self._web_driver.save_screenshot(file_name)

    def scroll_down(self, offset: int = 0) -> None:
        """
        Пролистнуть страницу вниз
        Args:
            offset: количество пикселей, на которое необходимо пролистнуть страницу
        """
        logger.info(f'Листаем страницу вниз на {offset}')

        if offset:
            self._web_driver.execute_script('window.scrollTo(0, {0});'.format(offset))
        else:
            self._web_driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')

    def scroll_up(self, offset: int = 0) -> None:
        """
        Пролистнуть страницу вверх
        Args:
            offset: количество пикселей, на которое необходимо пролистнуть страницу
        """
        logger.info(f'Листаем страницу вверх на {offset}')

        if offset:
            self._web_driver.execute_script('window.scrollTo(0, -{0});'.format(offset))
        else:
            self._web_driver.execute_script('window.scrollTo(0, -document.body.scrollHeight);')

    def switch_to_iframe(self, iframe: int | str) -> None:
        """
        Переключение на iframe
        Args:
            iframe: имя, индекс или элемент iframe
        """
        logger.info('Переходим на iframe')

        self._web_driver.switch_to.frame(iframe)

    def switch_out_iframe(self) -> None:
        """
        Отмена переключения на iframe
        """
        logger.info('Выходим из iframe')

        self._web_driver.switch_to.default_content()

    def get_current_url(self) -> str:
        """
        Получение ссылки на текущую страницу
        Returns: (str) ссылка на текущую страницу
        """
        logger.info('Получаем ссылку на текущую страницу')

        return self._web_driver.current_url

    def get_page_source(self) -> str:
        """
        Получить исходный код страницы в формате строки
        Returns: (str) HTML страницы
        """
        source = ''
        try:
            source = self._web_driver.page_source
        except:
            logger.error(colored('Не получается получить страницу', 'red'))

        return source

    def verify_javascript_errors(self,
                                 ignored_errors="{'level': 'SEVERE', 'message': 'https://stage.prodboard.example.com/ppinfo/api/v1/user - Failed to load resource: the server responded with a status of 401 ()', 'source': 'network', 'timestamp': 1676536589084}") -> None:
        """
        Verify that there are no JavaScript errors present on the page.
        """
        ignored_errors = ignored_errors or []
        javascript_logs = self._web_driver.get_log("browser")

        for log_message in javascript_logs:
            if log_message['level'] != 'WARNING':
                ignore = False
                for error in ignored_errors:
                    if error in log_message['message']:
                        ignore = True
                        break

                assert ignore, 'JavaScript error present on the page: "{}"'.format(log_message)

    def wait_page_loaded(self, timeout: int = 10) -> None:
        """
        Ожидание загрузки страницы
        Args:
            timeout: время ожидания
        """
        logger.info(f'Дожидаемся загрузки страницы')
        page_loaded = False
        k = 0

        source = self._web_driver.page_source

        while not page_loaded and k < timeout * 2:
            time.sleep(2)
            k += 1

            try:
                self._web_driver.execute_script("return document.readyState")
                page_loaded = True
            except:
                pass

        if not page_loaded:
            logger.error(colored(f'Страница не загрузилась после {timeout} секунд ожидания'))

    @staticmethod
    def generate_text(length: int, lang: str = 'eng') -> str:
        """
        Сгенерировать рандомный текст
        Args:
            length: длина текста
            lang: rus/eng выбор языка

        Returns: (str) случайная последовательность букв

        """
        if lang == "rus":
            cyrillic = "ёйцукенгшщзхъфывапролджэячсмитьбю "
            return ''.join(random.choices(cyrillic, k=length))
        if lang == "eng":
            return ''.join(random.choices(string.ascii_lowercase + " ", k=length))
