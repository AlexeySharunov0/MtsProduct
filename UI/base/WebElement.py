import logging

from playwright.sync_api import Page, Locator, expect
from playwright.sync_api import TimeoutError

logger = logging.getLogger(__name__)


class WebElement:
    def __init__(self, page: Page, locator: str = None, element: Locator = None):
        self._page = page
        self.locator = locator
        self.element = self._page.locator(locator).nth(0) if element is None else element
        self.logging_name = f'<{locator}>'
        self._timeout = 30000

    def __getitem__(self, item: int) -> "WebElement":
        """
        Перегрузка операции получения элемента по индексу
        Args:
            item: (int) порядковый номер элемента

        Returns: (WebElement) новая сущность элемента под указанным порядковым номером

        """
        return WebElement(self._page, locator=self.locator, element=self._page.locator(self.locator).nth(item))

    def check_element(self) -> None:
        """
        Проверка, что элемент присутствует на странице
        """
        try:
            self._page.wait_for_selector(self.locator, timeout=self._timeout)
        except TimeoutError as e:
            logger.error(f'Элемент {self.logging_name} не найден')
            raise e

    def get_attribute(self, attribute_name: str) -> str:
        """
        Получить значение атрибута элемента
        Args:
            attribute_name: (str) название атрибута (class, type, id etc.)

        Returns: (str) значение атрибута
        """
        logger.info(f'Получаем значение атрибута {attribute_name} у элемента {self.logging_name}')

        return self.element.get_attribute(attribute_name)

    def get_text(self) -> str:
        """
        Получить текст элемента
        Returns: (str) текст
        """
        logger.info(f'Получаем текст элемента {self.logging_name}')

        return self.element.inner_text()

    def get_input_text(self) -> str:
        """
        Получить текст элемента (работает для input, textarea, select)
        Returns: (str) текст
        """
        logger.info(f'Получаем текст элемента {self.logging_name}')

        return self.element.input_value()

    def get_child(self, query: str, timeout: int = 5000, is_class_instance: bool = True) -> 'WebElement' or None:
        """
        Ищет дочерний элемент текущего элемента.

        Args:
            query: селектор (CSS, XPath, класс или ID)
            timeout: время ожидания в миллисекундах (по умолчанию 5000)
            is_class_instance: если True и query не начинается с ./#//, ищет по классу

        Returns:
            WebElement: найденный дочерний элемент
        """
        logger.info(f'Ищем дочерний элемент по запросу {query}')

        # Получаем элемент-родитель
        parent_element = self.element if hasattr(self, 'element') else self._page.locator(self.locator)

        try:
            # Определяем тип селектора
            if query.startswith('.') or query.startswith('#'):
                locator = parent_element.locator(f'css={query}')
            elif query.startswith('//'):
                locator = parent_element.locator(f'xpath={query}')
            elif is_class_instance:
                locator = parent_element.locator(f'.{query}')
            else:
                locator = parent_element.locator(f'#{query}')

            # Ждем появления элемента
            locator.wait_for(timeout=timeout)

            # Возвращаем первый найденный элемент
            return WebElement(self._page, element=locator.first)
        except TimeoutError:
            # Если элемент не найден, возвращаем None
            logger.info(f'Элемент по запросу {query} не найден')
            return

    def get_children(self, query: str, timeout: int = 5000, is_class_instance: bool = True) -> list['WebElement']:
        """
        Ищет дочерние элементы текущего элемента.

        Args:
            query: селектор (CSS, XPath, класс или ID)
            timeout: время ожидания в миллисекундах (по умолчанию 5000)
            is_class_instance: если True и query не начинается с ./#//, ищет по классу

        Returns:
            List[WebElement]: список найденных элементов
        """
        logger.info(f'Ищем дочерние элементы по запросу {query}')

        parent_element = self.element if hasattr(self, 'element') else self._page.locator(self.locator)

        try:
            if query.startswith('.') or query.startswith('#'):
                locator = parent_element.locator(f'css={query}')
            elif query.startswith('//'):
                locator = parent_element.locator(f'xpath={query}')
            elif is_class_instance:
                locator = parent_element.locator(f'.{query}')
            else:
                locator = parent_element.locator(f'#{query}')

            # Ждем появления хотя бы одного элемента
            locator.first.wait_for(timeout=timeout)

            # Возвращаем все элементы как WebElement
            return [WebElement(self._page, element=item) for item in locator.all()]

        except TimeoutError:
            # Если элементы не найдены, возвращаем пустой список
            logger.info(f'Элементы по запросу {query} не найдены')
            return []

    def get_parent(self) -> "WebElement":
        """
        Получить родительский элемент текущего элемента
        Returns: (WebElement) родительский элемент
        """
        logger.info(f'Получаем родителя элемента {self.logging_name}')
        if self.locator.startswith('.'):
            tmp_locator = f"//*[@class='{self.locator[1:]}']"
        elif self.locator.startswith('#'):
            tmp_locator = f"//*[@id='{self.locator[1:]}']"
        else:
            tmp_locator = self.locator
        return WebElement(self._page, tmp_locator + '/..')

    def get_modified_element(self, modification: str, number: int) -> "WebElement":
        """
        Получить другой элемент, связанный с текущим элементом. Работает только для xpath
        Args:
            modification: (str) будет добавлено к локатору текущего элемента для получения нового
            number: (int) для итерации
        Returns: (WebElement) другой элемент
        """
        logger.info(f'Получаем связанный элемент элемента {self.logging_name}')
        return WebElement(self._page, f'({self.locator})[{number + 1}]' + modification)

    def count(self) -> int:
        """
        Посчитать кол-во элементов с искомым локатором
        Returns: (int) кол-во элементов
        """
        logger.info(f'Получаем количество элементов {self.logging_name}')

        return self._page.locator(self.locator).count()

    def fill(self, text: str, clear: bool = True) -> None:
        """
        Ввод данных через insert в любое поле
        Args:
            text: (str) текст, который требуется ввести
            clear: (bool) если True, поле будет очищено перед вводом текста
        """
        logger.info(f'Вводим текст {text} в элемент {self.logging_name}')

        if clear:
            self.element.fill(text)
        else:
            current_value = self.element.evaluate('el => el.value')
            new_value = f"{current_value}{text}"
            self.element.fill(new_value)

    def fill_human_like(self, text: str, delay: int = 100) -> None:
        """
        Ввод данных по одной клавише в любое поле (human-like way)
        Args:
            text: (str) текст, который требуется ввести
            delay: (int) задержка между нажиманием клавиш в мс
        """
        logger.info(f'Вводим текст {text} в элемент {self.logging_name}')

        self.element.press_sequentially(text, delay=delay)

    def press_key(self, key: str) -> None:
        """
        Нажать клавишу с клавиатуры
        Args:
            key: (str) https://developer.mozilla.org/en-US/docs/Web/API/UI_Events/Keyboard_event_key_values
        """
        logger.info(f'Жмем кнопку {key}')

        self.element.press(key)

    def click(self, amount: int = 1, force: bool = False) -> None:
        """
        Клик по элементу
        """
        logger.info(f'Кликаем по элементу {self.logging_name}')
        self.element.click(click_count=amount, timeout=self._timeout, force=force)

    def clear(self) -> None:
        """
        Очистить инпут элемента
        """
        logger.info('Очищаем инпут элемента')

        self.element.clear()

    def set_checked(self, is_checked: bool = True) -> None:
        """
        Переключить чекбокс
        Args:
            is_checked: (bool) True - включить, False - выключить
        """
        logger.info(f'Меняем состояние элемента {self.logging_name} на checked:{is_checked}')

        self.element.set_checked(is_checked)

    def drag_to(self, target_element: "WebElement", horizontal_shift: int = 250, vertical_shift: int = 5) -> None:
        """
        Использование drag and drop для перемещения одного элемента (self) относительно другого (target) со смещением.
        source элемент перемещается на позицию (x+horizontal_shift, y+vertical_shift); x,y - кор-ды верхнего левого угла
        target элемента.
        Args:
            target_element: (WebElement) элемент, относительно которого будет происходить перемещение.
            horizontal_shift: (int) сдвиг по горизонтали
            vertical_shift: (int) сдвиг по вертикали
        """
        logger.info(f'Передвигаем элемент {self.logging_name} к элементу {target_element.logging_name}')
        element_position = target_element.element.bounding_box()
        self._page.mouse.wheel(100, 100)
        self.click()
        # self._page.mouse.move(my_position['x'], my_position['y'])
        self._page.mouse.down(button='left')

        self._page.mouse.move(element_position['x'] + horizontal_shift, element_position['y'] + vertical_shift)
        self._page.mouse.up()

    def move(self, horizontal_shift: int = 250, vertical_shift: int = 0):
        """
        Передвинуть элемент на указанное кол-во пикселей
        Args:
            horizontal_shift: (int) сдвиг по горизонтали
            vertical_shift: (int) сдвиг по вертикали
        """
        logger.info(f'Передвигаем элемент {self.logging_name}')

        element_position = self.element.bounding_box()

        self._page.mouse.wheel(100, 100)
        self.click()
        self._page.mouse.move(element_position['x'], element_position['y'])
        self._page.mouse.down(button='left')
        self._page.mouse.move(element_position['x'] + horizontal_shift, element_position['y'] + vertical_shift)
        self._page.mouse.up()

    def input_file(self, path: str) -> None:
        """
        Загрузить файл в инпут
        Args:
            path: (str) путь к файлу
        """
        logger.info(f'Загружаем файл {path} в элемент {self.logging_name}')

        try:
            self._page.locator(self.locator).set_input_files(path)
        except Exception as e:
            logger.error(f'Не удалось загрузить файл {path} в элемент {self.logging_name}')
            raise e

    def is_visible(self) -> bool:
        """
        Проверка, что элемент виден
        Returns: True если элемент виден, False иначе
        """
        logger.info(f'Проверяем, что элемент {self.logging_name} виден')
        try:
            self.check_element()
            expect(self.element).to_be_visible()
            return True
        except AssertionError:
            logger.error(f'Элемент {self.logging_name} не виден')
            return False
        except TimeoutError:
            return False

    def is_not_visible(self) -> bool:
        """
        Проверка, что элемент не виден
        Returns: True если элемент не виден, False иначе
        """
        logger.info(f'Проверяем, что элемент {self.logging_name} не виден')
        try:
            self.check_element()
            expect(self.element).not_to_be_visible()
            return True
        except AssertionError:
            logger.error(f'Элемент {self.logging_name} виден')
            return False
        except TimeoutError:
            return True

    def is_clickable(self) -> bool:
        """
        Проверка, что элемент кликабелен (виден и enabled)
        Returns: True если элемент кликабелен, False иначе
        """
        logger.info(f'Проверяем, что элемент {self.logging_name} кликабелен')
        try:
            self.check_element()
            expect(self.element).to_be_enabled()
            expect(self.element).to_be_visible()
            return True
        except AssertionError:
            logger.error(f'Элемент {self.logging_name} не кликабелен')
            return False
        except TimeoutError:
            return False

    def is_not_clickable(self) -> bool:
        """
        Проверка, что элемент НЕ кликабелен (невидим или disabled)
        Returns: True если элемент не кликабелен, False иначе
        """
        logger.info(f'Проверяем, что элемент {self.logging_name} не кликабелен')
        try:
            self.check_element()
            expect(self.element).not_to_be_enabled()
            return True
        except AssertionError:
            try:
                # Проверяем, может элемент просто невидим
                expect(self.element).not_to_be_visible()
                return True
            except AssertionError:
                logger.error(f'Элемент {self.logging_name} кликабелен')
                return False
        except TimeoutError:
            return True

    def is_checked(self) -> bool:
        """
        Проверка, что элемент включен
        Returns: True если элемент включен, False иначе
        """
        logger.info(f'Проверяем, что элемент {self.logging_name} включен')
        self.check_element()
        try:
            return 'is-checked' in self.get_attribute('class')
        except AssertionError:
            logger.error(f'Элемент {self.logging_name} не включен')
            return False

    def is_not_checked(self) -> bool:
        """
        Проверка, что элемент выключен
        Returns: True если элемент выключен, False иначе
        """
        logger.info(f'Проверяем, что элемент {self.logging_name} выключен')
        self.check_element()
        try:
            return 'is-checked' not in self.get_attribute('class')

        except AssertionError:
            logger.error(f'Элемент {self.logging_name} включен')
            return False

    def is_selected(self) -> bool:
        """
        Проверяет, есть ли в аргументе класса значение selected.
        Returns: True если selected есть, False иначе.
        """
        logger.info(f'Проверяем, что элемент {self.logging_name} выключен')
        self.check_element()
        try:
            return 'selected' in self.get_attribute('class')

        except AssertionError:
            logger.error(f'Элемент {self.logging_name} включен')
            return False

    def is_not_selected(self) -> bool:
        """
        Проверяет, есть ли в аргументе класса значение selected.
        Returns: False если selected есть, True иначе.
        """

        logger.info(f'Проверяем, что элемент {self.logging_name} выключен')
        self.check_element()
        try:
            return 'selected' not in self.get_attribute('class')

        except AssertionError:
            logger.error(f'Элемент {self.logging_name} включен')
            return False

    def is_disabled(self) -> bool:
        """
        Проверка, что с элементом нельзя взаимодействовать
        Returns: True если нельзя взаимодействовать, False иначе
        """
        logger.info(f'Проверяем, что с элементом {self.logging_name} нельзя взаимодействовать')
        self.check_element()
        try:
            return 'disabled' in self.get_attribute('class')
        except AssertionError:
            logger.error(f'С элементом {self.logging_name} можно взаимодействовать')
            return False

    def is_not_disabled(self) -> bool:
        """
        Проверка, что с элементом можно взаимодействовать
        Returns: True если можно взаимодействовать, False иначе
        """
        logger.info(f'Проверяем, что с элементом {self.logging_name} можно взаимодействовать')
        self.check_element()
        try:
            return 'disabled' not in self.get_attribute('class')
        except AssertionError:
            logger.error(f'С элементом {self.logging_name} нельзя взаимодействовать')
            return False

    def has_value(self, attribute_name: str, value: str) -> bool:
        """
        Проверка, что значение value есть в значении атрибута элемента
        Args:
            attribute_name: (str) атрибут, в котором происходит поиск
            value: (str) значение, которое ищется

        Returns: (bool) True если значение есть, False иначе
        """
        logger.info(f'Проверяем, что {value} есть в значении атрибута {attribute_name} у элемента {self.logging_name}')

        return value.lower() in self.element.get_attribute(attribute_name).lower()

    def highlight_element(self) -> None:
        """
        Подсветить элемент (debug)
        """
        self.element.highlight()


class ManyWebElements:
    def __init__(self, page: Page, locator: str = None, elements: Locator = None):
        self._page = page
        self.locator = locator
        self.elements = self._page.locator(locator) if elements is None else elements
        self.logging_name = f'<{locator}>'
        self._timeout = 5000

    def __getitem__(self, item: int) -> WebElement:
        """
        Перегрузка операции итерирования по элементам
        Args:
            item: порядковый номер элемента

        Returns: (Locator) элемент под номером item
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

        for index, elem in enumerate(elements):
            new_elements.append(WebElement(self._page, locator=self.locator, element=elem))

        return new_elements

    def find(self) -> list[Locator]:
        """
        Ищет элементы на странице.
        Returns: (list[Locator]) список найденных элементов
        """
        try:
            self.check_elements()
            elements = self.elements.all()
        except Exception as e:
            print(f'Элементов с локатором {self.locator} не найдено. Ошибка: {e}')
            elements = []

        return elements

    def check_elements(self) -> None:
        """
        Проверка, что элементы присутствуют на странице
        """
        try:
            self._page.wait_for_selector(self.locator, timeout=self._timeout)
        except TimeoutError as e:
            logger.error(f'Элементы {self.logging_name} не найдены')
            raise e

    def get_attributes(self, attribute_name: str) -> list[str]:
        """
        Получить значения атрибута для всех элементов
        Args:
            attribute_name: (str) название атрибута (class, type, id etc.)

        Returns: (list[str]) список значений атрибута
        """
        logger.info(f'Получаем значения атрибута {attribute_name} у элементов {self.logging_name}')
        return [el.get_attribute(attribute_name) for el in self.find()]

    def get_texts(self) -> list[str]:
        """
        Получить текст всех элементов
        Returns: (list[str]) список текстов
        """
        logger.info(f'Получаем тексты элементов {self.logging_name}')
        return [el.inner_text() for el in self.find()]

    def get_input_texts(self) -> list[str]:
        """
        Получить текст всех элементов (работает для input, textarea, select)
        Returns: (list[str]) список текстов
        """
        logger.info(f'Получаем тексты элементов {self.logging_name}')
        return [el.input_value() for el in self.find()]

    def get_parents(self) -> list["WebElement"]:
        """
        Получить родительские элементы для всех элементов коллекции
        Returns: (list[WebElement]) список родительских элементов
        """
        logger.info(f'Получаем родителей элементов {self.logging_name}')

        parents = []
        for i in range(self.count()):
            element = self[i]
            parents.append(element.get_parent())
        return parents

    def count(self) -> int:
        """
        Получить количество элементов в коллекции
        Returns: (int) количество элементов
        """
        logger.info(f'Получаем количество элементов {self.logging_name}')
        return self.elements.count()

    def fill_all(self, text: str) -> None:
        """
        Заполнить все элементы текстом
        Args:
            text: (str) текст для заполнения
        """
        logger.info(f'Заполняем все элементы {self.logging_name} текстом {text}')
        for el in self.find():
            el.fill(text)

    def fill_all_human_like(self, text: str, delay: int = 100) -> None:
        """
        Заполнить все элементы текстом (human-like way)
        Args:
            text: (str) текст для заполнения
            delay: (int) задержка между нажатиями в мс
        """
        logger.info(f'Заполняем все элементы {self.logging_name} текстом {text} (human-like)')
        for el in self.find():
            el.press_sequentially(text, delay=delay)

    def press_keys(self, key: str) -> None:
        """
        Нажать клавишу на всех элементах
        Args:
            key: (str) клавиша для нажатия
        """
        logger.info(f'Нажимаем клавишу {key} на всех элементах {self.logging_name}')
        for el in self.find():
            el.press(key)

    def click_all(self, amount: int = 1) -> None:
        """
        Кликнуть по всем элементам
        Args:
            amount: (int) количество кликов
        """
        logger.info(f'Кликаем по всем элементам {self.logging_name}')
        for el in self.find():
            el.click(click_count=amount)

    def clear_all(self) -> None:
        """
        Очистить все элементы
        """
        logger.info(f'Очищаем все элементы {self.logging_name}')
        for el in self.find():
            el.clear()

    def set_all_checked(self, is_checked: bool = True) -> None:
        """
        Установить состояние checked для всех элементов
        Args:
            is_checked: (bool) состояние checked
        """
        logger.info(f'Устанавливаем checked={is_checked} для всех элементов {self.logging_name}')
        for el in self.find():
            el.set_checked(is_checked)

    def are_visible(self) -> bool:
        """
        Проверить, что все элементы видны
        Returns: (bool) True если все видны, False иначе
        """
        logger.info(f'Проверяем, что все элементы {self.logging_name} видны')
        try:
            for el in self.elements.all():
                expect(el).to_be_visible()
            return True
        except AssertionError:
            logger.error(f'Не все элементы {self.logging_name} видны')
            return False

    def are_not_visible(self) -> bool:
        """
        Проверить, что все элементы не видны
        Returns: (bool) True если все не видны, False иначе
        """
        logger.info(f'Проверяем, что все элементы {self.logging_name} не видны')
        try:
            for el in self.elements.all():
                expect(el).not_to_be_visible()
            return True
        except AssertionError:
            logger.error(f'Некоторые элементы {self.logging_name} видны')
            return False

    def are_checked(self, amount: int = None) -> bool:
        """
        Проверить, что все элементы checked
        Returns: (bool) True если все checked, False иначе
        """
        logger.info(f'Проверяем, что все элементы {self.logging_name} checked')
        try:
            for el in self.elements.all()[:amount]:
                expect(el).to_be_checked()
            return True
        except AssertionError:
            logger.error(f'Не все элементы {self.logging_name} checked')
            return False

    def are_not_checked(self) -> bool:
        """
        Проверить, что все элементы не checked
        Returns: (bool) True если все не checked, False иначе
        """
        logger.info(f'Проверяем, что все элементы {self.logging_name} не checked')
        try:
            for el in self.elements.all():
                expect(el).not_to_be_checked()
            return True
        except AssertionError:
            logger.error(f'Некоторые элементы {self.logging_name} checked')
            return False

    def are_disabled(self) -> bool:
        """
        Проверить, что все элементы disabled
        Returns: (bool) True если все disabled, False иначе
        """
        logger.info(f'Проверяем, что все элементы {self.logging_name} disabled')
        try:
            for el in self.elements.all():
                expect(el).to_be_disabled()
            return True
        except AssertionError:
            logger.error(f'Не все элементы {self.logging_name} disabled')
            return False

    def are_not_disabled(self) -> bool:
        """
        Проверить, что все элементы не disabled
        Returns: (bool) True если все не disabled, False иначе
        """
        logger.info(f'Проверяем, что все элементы {self.logging_name} не disabled')
        try:
            for el in self.elements.all():
                expect(el).not_to_be_disabled()
            return True
        except AssertionError:
            logger.error(f'Некоторые элементы {self.logging_name} disabled')
            return False

    def are_clickable(self) -> bool:
        """
        Проверить, что все элементы кликабельны
        Returns: (bool) True если все кликабельны, False иначе
        """
        logger.info(f'Проверяем, что все элементы {self.logging_name} кликабельны')
        try:
            for el in self.elements.all():
                expect(el).to_be_enabled()  # Assuming clickable means the element is enabled
                expect(el).to_be_visible()  # And visible
            return True
        except AssertionError:
            logger.error(f'Не все элементы {self.logging_name} кликабельны')
            return False

    def are_not_clickable(self) -> bool:
        """
        Проверить, что все элементы не кликабельны
        Returns: (bool) True если все не кликабельны, False иначе
        """
        logger.info(f'Проверяем, что все элементы {self.logging_name} не кликабельны')
        try:
            for el in self.elements.all():
                expect(el).not_to_be_enabled()  # Assuming non-clickable means the element is disabled
                expect(el).not_to_be_visible()  # Or not visible
            return True
        except AssertionError:
            logger.error(f'Некоторые элементы {self.logging_name} кликабельны')
            return False

    def filter_by_text(self, text: str) -> list["WebElement"]:
        """
        Отфильтровать элементы по тексту
        Args:
            text: (str) текст для фильтрации

        Returns: (list[WebElement]) список элементов, содержащих текст
        """
        logger.info(f'Фильтруем элементы {self.logging_name} по тексту {text}')

        filtered = []
        for i in range(self.count()):
            element = self[i]
            if text.lower() in element.get_text().lower():
                filtered.append(element)
        return filtered

    def highlight_all(self) -> None:
        """
        Подсветить все элементы (debug)
        """
        for el in self.elements.all():
            el.highlight()
