import logging

from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebElement as SeleniumWebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from termcolor import colored

logger = logging.getLogger(__name__)


class WebElement(object):
    _locator = ('', '')
    _web_driver = None
    _page = None
    _timeout = 5
    _wait_after_click = False

    def __init__(self, timeout: int = 5, wait_after_click: bool = False, element: SeleniumWebElement = None,
                 new_locator: tuple = None, index_of_many_elements: int = None,
                 **kwargs):
        self.move = None
        self._timeout = timeout
        self._wait_after_click = wait_after_click
        self.element = element

        if new_locator:
            self._locator = new_locator

        for attr in kwargs:
            self._locator = (str(attr).replace('_', ' '), str(kwargs.get(attr)))

        self.logging_name = f'<{self._locator[0]}="{self._locator[1]}"'
        if index_of_many_elements:
            self.logging_name += f'[{index_of_many_elements}]>'
        else:
            self.logging_name += '>'

    def find(self, timeout: int = 5) -> SeleniumWebElement:
        """
        Ищет элемент на странице. Exception возникает, если элемент не найден.
        Args:
            timeout: время, которое максимально функция будет ожидать при поиске элемента до возникновения ошибки.

        Returns: (SeleniumWebElement) искомый элемент.
        """
        if self.element:
            return self.element

        element = None

        try:
            element = WebDriverWait(self._web_driver, timeout).until(EC.presence_of_element_located(self._locator))
        except Exception as e:
            logger.error(colored(f'Элемент {self.logging_name} не найден. Ошибка: {e}', 'red'))

        return element

    def get_child(self, query: str, timeout: int = 5, is_class_instance: bool = True) -> 'WebElement':
        """
        Ищет дочерний элемент текущего элемента по аргументу. _predicate - самодельный вариант Expected Condition от
        selenium (по умолчанию нет варианта для поиска дочерних элементов).
        Аргумент driver нужен, чтобы под капотом until передавал туда webdriver.
        Args:
            query: аргумент (класс, xpath, id, css_selector), по которому производится поиск.
            timeout: время, которое максимально функция будет ожидать при поиске элемента до возникновения ошибки
            is_class_instance: указатель на то, что если передаем обычную строку, то это проверка на класс.

        Returns: (WebElement) искомый дочерний элемент.
        """
        logger.info(f'Ищем дочерний элемент по запросу {query}')

        element = self.find()

        if query.startswith('.') or query.startswith('#'):
            def _predicate(driver):
                return element.find_element(By.CSS_SELECTOR, query)

        elif query.startswith('//'):
            def _predicate(driver):
                return element.find_element(By.XPATH, query)
        elif is_class_instance:
            def _predicate(driver):
                return element.find_element(By.CLASS_NAME, query)
        else:
            def _predicate(driver):
                return element.find_element(By.ID, query)

        new_element = WebDriverWait(self._web_driver, timeout).until(_predicate)
        return WebElement(element=new_element)

    def get_children(self, query: str, timeout: int = 5, is_class_instance: bool = True) -> list[SeleniumWebElement]:
        """
        Ищет дочерние элементы текущего элемента по аргументу. _predicate - самодельный вариант Expected Condition от
        selenium (по умолчанию нет варианта для поиска дочерних элементов).
        Аргумент driver нужен, чтобы под капотом until передавал туда webdriver.
        Args:
            query: аргумент (класс, xpath, id, css_selector), по которому производится поиск.
            timeout: время, которое максимально функция будет ожидать при поиске элемента до возникновения ошибки
            is_class_instance: указатель на то, что если передаем обычную строку, то это проверка на класс.

        Returns: (WebElement) список искомых дочерних элементов.
        """
        logger.info(f'Ищем дочерний элемент по запросу {query}')

        element = self.find()

        if query.startswith('.') or query.startswith('#'):
            def _predicate(driver):
                return element.find_elements(By.CSS_SELECTOR, query)

        elif query.startswith('//'):
            def _predicate(driver):
                return element.find_elements(By.XPATH, query)
        elif is_class_instance:
            def _predicate(driver):
                return element.find_elements(By.CLASS_NAME, query)
        else:
            def _predicate(driver):
                return element.find_elements(By.ID, query)

        new_element = WebDriverWait(self._web_driver, timeout).until(_predicate)
        return new_element

    def wait_to_be_clickable(self, timeout: int = 5, should_be_clickable: bool = True) -> SeleniumWebElement | None:
        """
        Ждет, пока элемент станет кликабельным. Вспомогательная функция для is_clickable(), click().
        Args:
            timeout: время ожидания
            should_be_clickable: должен ли элемент быть кликабельным (вспомогательный параметр для логирования)

        Returns: (SeleniumWebElement) элемент, если он кликабельный / None если элемент не кликабельный.
        """
        element = None
        func_arg = self.element or self._locator

        try:
            element = WebDriverWait(self._web_driver, timeout).until(EC.element_to_be_clickable(func_arg))
        except Exception as e:
            if should_be_clickable:
                logger.error(colored(f'Элемент {self.logging_name} не кликабельный. Ошибка {e}', 'red'))
            else:
                logger.info(f'Элемент {self.logging_name} не кликабельный.')

        return element

    def wait_to_be_visible(self, timeout: int = 5, should_be_visible: bool = True) -> SeleniumWebElement | None:
        """
        Ждет, пока элемент станет видимым. Вспомогательная функция для is_visible().
        Args:
            timeout: время ожидания
            should_be_visible: должен ли элемент быть виден (вспомогательный параметр для логирования)

        Returns: (SeleniumWebElement) элемент, если он виден / None если элемент не виден.
        """
        element = None
        current_element = self.find()

        try:
            element = WebDriverWait(self._web_driver, timeout).until(EC.visibility_of(current_element))
        except Exception as e:
            if should_be_visible:
                logger.error(colored(f'Элемент {self.logging_name} не виден. Ошибка: {e}', 'red'))
            else:
                logger.info(f'Элемент {self.logging_name} не виден.')

        return element

    def is_clickable(self) -> bool:
        """
        Проверяет, является ли элемент кликабельным.
        Returns: True если элемент кликабельный, False иначе.
        """
        logger.info(f'Проверяем, что элемент {self.logging_name} кликабельный')

        element = self.wait_to_be_clickable(timeout=self._timeout)

        return bool(element)

    def is_not_clickable(self) -> bool:
        """
        Проверяет, является ли элемент кликабельным.
        Returns: False если элемент кликабельный, True иначе.
        """
        logger.info(f'Проверяем, что элемент {self.logging_name} кликабельный')

        element = self.wait_to_be_clickable(timeout=self._timeout, should_be_clickable=False)

        return not bool(element)

    def is_visible(self) -> bool:
        """
        Проверяет, отображается ли элемент на странице.
        Returns: True если элемент виден, False иначе.
        """
        logger.info(f'Проверяем, что элемент {self.logging_name} виден на странице')

        element = self.wait_to_be_visible(timeout=self._timeout)

        return bool(element)

    def is_not_visible(self) -> bool:
        """
        Проверяет, отображается ли элемент на странице.
        Returns: False если элемент виден, True иначе.
        """
        logger.info(f'Проверяем, что элемент {self.logging_name} не виден на странице')

        element = self.wait_to_be_visible(timeout=self._timeout, should_be_visible=False)

        return not bool(element)

    def is_selected(self) -> bool:
        """
        Проверяет, есть ли в аргументе класса значение selected.
        Returns: True если selected есть, False иначе.
        """
        logger.info(f'Проверяем, что элемент {self.logging_name} выбран')

        return 'selected' in self.get_attribute('class')

    def is_not_selected(self) -> bool:
        """
        Проверяет, есть ли в аргументе класса значение selected.
        Returns: False если selected есть, True иначе.
        """
        logger.info(f'Проверяем, что элемент {self.logging_name} не выбран')

        return 'selected' not in self.get_attribute('class')

    def is_disabled(self) -> bool:
        """
        Проверяет, есть ли в аргументе класса значение disabled.
        Returns: True если disabled есть, False иначе.
        """
        logger.info(f'Проверяем, что элемент {self.logging_name} отключен')

        return 'disabled' in self.get_attribute('class')

    def is_not_disabled(self) -> bool:
        """
        Проверяет, есть ли в аргументе класса значение disabled.
        Returns: False если disabled есть, True иначе.
        """
        logger.info(f'Проверяем, что элемент {self.logging_name} не отключен')

        return 'disabled' not in self.get_attribute('class')

    def is_checked(self) -> bool:
        """
        Проверяет, есть ли в аргументе класса значение is-checked.
        Returns: True если checked есть, False иначе.
        """
        logger.info(f'Проверяем, что элемент {self.logging_name} отмечен (checked)')

        return 'is-checked' in self.get_attribute('class')

    def is_not_checked(self) -> bool:
        """
        Проверяет, есть ли в аргументе класса значение is-checked.
        Returns: False если checked есть, True иначе.
        """
        logger.info(f'Проверяем, что элемент {self.logging_name} не отмечен (checked)')

        return 'is-checked' not in self.get_attribute('class')

    def is_active_item(self) -> bool:
        """
        Проверяет, есть ли в аргументе класса значение activeItem.
        Returns: True если activeItem есть, False иначе.
        """
        logger.info(f'Проверяем, что элемент {self.logging_name} активный')

        return 'is-activeItem' in self.get_attribute('class')

    def is_not_active_item(self) -> bool:
        """
        Проверяет, есть ли в аргументе класса значение activeItem.
        Returns: False если activeItem есть, True иначе.
        """
        logger.info(f'Проверяем, что элемент {self.logging_name} не активный')

        return 'is-activeItem' not in self.get_attribute('class')

    def is_any(self, value: str) -> bool:
        """
        Проверяет, есть ли в аргументе класса значение value.
        Args:
            value: значение для поиска

        Returns: True если value есть, False иначе.
        """
        logger.info(f'Проверяем, что {value} есть в элементе {self.logging_name}')

        return value in self.get_attribute('class')

    def is_not_any(self, value: str) -> bool:
        """
        Проверяет, есть ли в аргументе класса значение value.
        Args:
            value: значение для поиска

        Returns: False если value есть, True иначе.
        """
        logger.info(f'Проверяем, что {value} нет в элементе {self.logging_name}')

        return value not in self.get_attribute('class')

    def _set_value(self, web_driver, value: str | Keys, clear: bool = False) -> None:
        """
        Отправляет в форму (элемент) текст или клавиши с клавиатуры. Функция для внутреннего использования
        Args:
            value: текст, который необходимо ввести в форму. / Клавиша, которую необходимо нажать
            clear: флаг, очищать ли элемент перед введением текста
        """

        element = self.find()

        if clear:
            element.clear()

        element.send_keys(value)

    def send_keys(self, keys: str | Keys, clear: bool = False) -> None:
        """
        Отправляет в форму (элемент) текст или клавиши с клавиатуры
        Args:
            keys: текст, который необходимо ввести в форму. / Клавиша, которую необходимо нажать
            clear: флаг, очищать ли элемент перед введением текста

        """
        logger.info(f'Заполняем элемент {self.logging_name}')

        keys = keys.replace('\n', '\ue007')

        element = self.find()

        if clear:
            element.clear()
        element.click()
        element.send_keys(keys)

    def get_text(self) -> str:
        """
        Получить текст, относящийся к элементу
        Returns: (str) текст элемента
        """
        logger.info(f'Получаем текст элемента {self.logging_name}')

        text = ''
        element = self.find()

        try:
            text = str(element.text)
        except Exception as e:
            logger.error(colored(f'Ошибка при поиске текста: {e}', 'red'))

        return text

    def get_attribute(self, attr_name: str) -> str:
        """
        Получить значение необходимого атрибута элемента.
        Args:
            attr_name: название атрибута (class, tag, type etc.)

        Returns: (str) Значение атрибута
        """
        logger.info(f'Получаем атрибут {attr_name} у элемента {self.logging_name}')

        element = self.find()

        try:
            value = element.get_attribute(attr_name)
            return value
        except Exception as e:
            logger.error(colored(f'Ошибка при поиске атрибута {attr_name}: {e}'))
            raise Exception

    def click(self) -> None:
        """
        Нажать по элементу ЛКМ
        """
        logger.info(f'Кликаем по элементу {self.logging_name}')

        element = self.wait_to_be_clickable()
        try:
            element.click()
        except Exception as e:
            logger.error(colored(f'Ошибка при клике: {e}'))

        if self._wait_after_click:
            self._page.wait_page_loaded()

    def right_mouse_click(self) -> None:
        """
        Нажать по элементу ПКМ
        """
        logger.info(f'Кликаем по элементу {self.logging_name} правой кнопкой мыши')

        element = self.wait_to_be_clickable()

        try:
            action = ActionChains(self._web_driver)
            action.context_click(on_element=element).perform()
        except Exception as e:
            logger.error(colored(f'Ошибка при клике правой кнопкой мыши: {e}'))
            raise Exception

    def drag_and_drop(self, x_offset: int, y_offset: int) -> None:
        """
        Перетащить элемент с зажатой левой кнопкой мыши (НЕСТАБИЛЬНО)
        Args:
            x_offset: смещение по оси ОХ
            y_offset: смещение по оси ОУ
        """
        element = self.wait_to_be_clickable()

        try:
            action = ActionChains(self._web_driver)
            action.drag_and_drop_by_offset(element, x_offset, y_offset).perform()
        except Exception as e:
            logger.error(colored(f'Ошибка при перетаскивании элемента: {e}'))
            raise Exception

    def scroll_to_element(self) -> None:
        """
        Пролистнуть страницу до элемента
        """
        logger.info(f'Листаем страницу до элемента {self.logging_name}')

        element = self.find()

        try:
            action = ActionChains(self._web_driver)
            action.move_to_element(element).perform()
        except Exception as e:
            logger.error(colored(f'Ошибка при листании страницы до элемента {self.logging_name}: {e}'))
            raise Exception

    def delete(self) -> None:
        """
        Удалить элемент со страницы
        """
        element = self.find()

        self._web_driver.execute_script("arguments[0].remove();", element)


class ManyWebElements(WebElement):

    def __getitem__(self, item: int) -> WebElement:
        """
        Перегрузка операции итерирования по элементам
        Args:
            item: порядковый номер элемента

        Returns: (WebElement) элемент под номером item
        """
        elements = self.get_items()

        return elements[item]

    def get_items(self) -> list[WebElement]:
        """
        Возвращает список всех элементов с типом WebElement
        Returns: список всех элементов с типом WebElement
        """
        elements = self.find()
        new_elements = []

        for elem in elements:
            new_elements.append(
                WebElement(element=elem, new_locator=self._locator, index_of_many_elements=elements.index(elem)))

        return new_elements

    def find(self, timeout: int = 5) -> list[SeleniumWebElement]:
        """
        Ищет элементы на странице. Exception возникает, если элементы не найдены.
        Args:
            timeout: время, которое максимально функция будет ожидать при поиске элемента до возникновения ошибки.

        Returns: (list[SeleniumWebElement]) список найденных элементов
        """
        elements = []

        try:
            elements = WebDriverWait(self._web_driver, timeout).until(
                EC.presence_of_all_elements_located(self._locator))
        except Exception as e:
            logger.error(colored(f'Элементов с локатором {self.logging_name} не найдено. Ошибка:{e}', 'red'))

        return elements

    def are_visible(self, amount: int = None) -> bool:
        """
        Проверяет, отображаются ли первые amount элементы на странице.
        Args:
            amount: количество элементов, которые необходимо проверить (если не указано, проверяет все элементы)

        Returns: True если все элементы видны, False иначе.
        """
        logger.info(f'Проверяем, что элементы {self.logging_name} видны')

        return all(elem.is_visible() for elem in self.get_items()[:amount])

    def are_not_visible(self, amount: int = None) -> bool:
        """
        Проверяет, отображаются ли первые amount элементы на странице.
        Args:
            amount: количество элементов, которые необходимо проверить (если не указано, проверяет все элементы)

        Returns: False если все элементы видны, True иначе.
        """
        logger.info(f'Проверяем, что элементы {self.logging_name} не видны')

        return all(elem.is_not_visible() for elem in self.get_items()[:amount])

    def are_clickable(self, amount: int = None) -> bool:
        """
        Проверяет, кликабельные ли первые amount элементы на странице.
        Args:
            amount: количество элементов, которые необходимо проверить (если не указано, проверяет все элементы)

        Returns: True если все элементы кликабельные, False иначе.
        """
        logger.info(f'Проверяем, что элементы {self.logging_name} кликабельные')

        return all(elem.is_clickable() for elem in self.get_items()[:amount])

    def are_not_clickable(self, amount: int = None) -> bool:
        """
        Проверяет, кликабельные ли первые amount элементы на странице.
        Args:
            amount: количество элементов, которые необходимо проверить (если не указано, проверяет все элементы)

        Returns: False если все элементы кликабельные, True иначе.
        """
        logger.info(f'Проверяем, что элементы {self.logging_name} не кликабельные')

        return all(elem.is_not_clickable() for elem in self.get_items()[:amount])

    def are_selected(self, amount: int = None) -> bool:
        """
        Проверяет, есть ли в аргументе класса всех элементов значение selected.
        Args:
            amount: количество элементов, которые необходимо проверить (если не указано, проверяет все элементы)

        Returns: True если selected есть, False иначе.
        """
        logger.info(f'Проверяем, что элементы {self.logging_name} выбраны')

        return all(elem.is_selected() for elem in self.get_items()[:amount])

    def are_not_selected(self, amount: int = None) -> bool:
        """
        Проверяет, есть ли в аргументе класса всех элементов значение selected.
        Args:
            amount: количество элементов, которые необходимо проверить (если не указано, проверяет все элементы)

        Returns: False если selected есть, True иначе.
        """
        logger.info(f'Проверяем, что элементы {self.logging_name} не выбраны')

        return all(elem.is_not_selected() for elem in self.get_items()[:amount])

    def are_disabled(self, amount: int = None) -> bool:
        """
        Проверяет, есть ли в аргументе класса всех элементов значение disabled.
        Args:
            amount: количество элементов, которые необходимо проверить (если не указано, проверяет все элементы)

        Returns: True если disabled есть, False иначе.
        """
        logger.info(f'Проверяем, что элементы {self.logging_name} отключены')

        return all(elem.is_disabled() for elem in self.get_items()[:amount])

    def are_not_disabled(self, amount: int = None) -> bool:
        """
        Проверяет, есть ли в аргументе класса всех элементов значение disabled.
        Args:
            amount: количество элементов, которые необходимо проверить (если не указано, проверяет все элементы)

        Returns: False если disabled есть, True иначе.
        """
        logger.info(f'Проверяем, что элементы {self.logging_name} не отключены')

        return all(elem.is_not_disabled() for elem in self.get_items()[:amount])

    def are_checked(self, amount: int = None) -> bool:
        """
        Проверяет, есть ли в аргументе класса всех элементов значение checked.
        Args:
            amount: количество элементов, которые необходимо проверить (если не указано, проверяет все элементы)

        Returns: True если checked есть, False иначе.
        """
        logger.info(f'Проверяем, что элементы {self.logging_name} отмечены (checked)')

        return all(elem.is_checked() for elem in self.get_items()[:amount])

    def are_not_checked(self, amount: int = None) -> bool:
        """
        Проверяет, есть ли в аргументе класса всех элементов значение checked.
        Args:
            amount: количество элементов, которые необходимо проверить (если не указано, проверяет все элементы)

        Returns: False если checked есть, True иначе.
        """
        logger.info(f'Проверяем, что элементы {self.logging_name} не отмечены (checked)')

        return all(elem.is_not_checked() for elem in self.get_items()[:amount])

    def are_active_item(self, amount: int = None) -> bool:
        """
        Проверяет, есть ли в аргументе класса всех элементов значение activeItem.
        Args:
            amount: количество элементов, которые необходимо проверить (если не указано, проверяет все элементы)

        Returns: True если activeItem есть, False иначе.
        """
        logger.info(f'Проверяем, что элементы {self.logging_name} активные')

        return all(elem.is_active_item() for elem in self.get_items()[:amount])

    def are_not_active_item(self, amount: int = None) -> bool:
        """
        Проверяет, есть ли в аргументе класса всех элементов значение activeItem.
        Args:
            amount: количество элементов, которые необходимо проверить (если не указано, проверяет все элементы)

        Returns: False если activeItem есть, True иначе.
        """
        logger.info(f'Проверяем, что элементы {self.logging_name} не активные')

        return all(elem.is_not_active_item() for elem in self.get_items()[:amount])

    def click(self, amount: int = None) -> None:
        """
        Нажать по всем элементам ЛКМ
        Args:
            amount: количество элементов, которые необходимо кликнуть (если не указано, кликает на все элементы)
        """
        logger.info(f'Кликаем по элементам {self.logging_name}')

        for item in self.get_items()[:amount]:
            item.click()

    def count(self) -> int:
        """
        Подсчет количества элементов с указанным локатором.
        Returns: (int) количество элементов
        """
        logger.info(f'Получаем количество элементов {self.logging_name}')

        elements = self.find()

        return len(elements)

    def get_text(self) -> list[str]:
        """
        Получить текст всех элементов с указанным локатором
        Returns: (list[str]) текст
        """
        logger.info(f'Получаем текст элемента {self.logging_name}')

        elements = self.find()
        result = []

        for element in elements:
            text = ''

            try:
                text = str(element.text)
            except Exception as e:
                logger.error(colored(f'Ошибка при поиске текста: {e}', 'red'))

            result.append(text)

        return result

    def get_attribute(self, attr_name: str) -> list[str]:
        """
        Получить значение необходимого атрибута элементов.
        Args:
            attr_name: название атрибута (class, tag, type etc.)

        Returns: (list[str]) Значение атрибута
        """

        results = []
        elements = self.find()

        for element in elements:
            results.append(element.get_attribute(attr_name))

        return results
