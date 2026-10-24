from UI.base.WebElement import WebElement, ManyWebElements


class AttributesLocators:

    def __init__(self, page):
        # Кнопка добавить атрибут
        self.add_attribute_button = WebElement(page, ".addButton")

        # Строка поиска
        self.search_str = WebElement(page, "div.search input")

        # Первый результат поиска
        self.first_search_result = WebElement(page, "table tr:nth-of-type(2) td:nth-of-type(1) a")

        # Аллерт удаления атрибута
        self.allert_delete = WebElement(page, "//*[text() = 'Атрибут удалён']")

        # СТРАНИЦА СОЗДАНИЯ АТРИБУТА ---------------------------------------------------------------------------------------------------------------------

        # Поле ввода названия
        self.input_name = WebElement(page, "input.pp-input__inner")

        # Инпут описания
        self.input_description = WebElement(page, "textarea.pp-input__inner.pp-textarea__inner")

        # Селектор Типа
        self.type_selector = WebElement(page, ".field .selected")

        # Типы в выпадающем списке
        self.type_items_selector = ManyWebElements(page, ".foundItemsName")

        # Текстовый тип в селекторе
        self.text_type_select = WebElement(page, ".mts-select-dropdown-item:nth-of-type(1)")

        # Числовой тип в селекторе
        self.number_type_select = WebElement(page, ".mts-select-dropdown-item:nth-of-type(2)")

        # Дата тип в селекторе
        self.date_type_select = WebElement(page, ".mts-select-dropdown-item:nth-of-type(3)")

        # Сотрудник тип в селекторе
        self.user_type_select = WebElement(page, ".mts-select-dropdown-item:nth-of-type(4)")

        # Булев тип в селекторе
        self.bool_type_select = WebElement(page, ".mts-select-dropdown-item:nth-of-type(5)")

        # Набор значений тип в селекторе
        self.list_type_select = WebElement(page, ".mts-select-dropdown-item:nth-of-type(6)")

        # кнопка создания атрибута
        self.create_button = WebElement(page, "button.mts-button.mts-button_l")

        # кнопка добавления варианта
        self.add_choosable = WebElement(page, "//*[text() = ' Добавить ']")

        # Поля ввода вариантов выбора
        self.input_choosable_fields = ManyWebElements(page, "div.field:nth-of-type(7) input")

        # СТРАНИЦА ГОТОВОГО АТРИБУТА ---------------------------------------------------------------------------------------------------------------------

        # Скрыть вариант выбора
        self.mute_value_button = WebElement(page, "div.value")

        # input созданного ранее варианта выбора
        self.input_choosable_fields_exists = WebElement(page, "div.value")

        # Кнопка удаления атрибута
        self.delete_attr_button = ManyWebElements(page, "//*[text() = ' Удалить ']")
        self.broken_delete = WebElement(page, "//*[text() = ' Удалить']")

        # Кнопка Отмены
        self.cancel_attr_button = WebElement(page, "//*[text() = ' Отмена']")
