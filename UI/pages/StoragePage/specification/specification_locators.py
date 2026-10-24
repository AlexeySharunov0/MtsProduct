from UI.base.WebElement import WebElement, ManyWebElements


class SpecificationLocators:

    def __init__(self, page):
        # Кнопка добавить спецификацию
        self.add_spec_button = WebElement(page, ".addBlock")

        # Все спецификации
        self.specs = ManyWebElements(page, "table tr td a")

        # Первый результат поиска
        self.first_spec = WebElement(page, "table tr:nth-of-type(2) td:nth-of-type(1) a")

        # СТРАНИЦА СОЗДАНИЯ СПЕЦИФИКАЦИИ ---------------------------------------------------------------------------------------------------------------------

        # Поле ввода названия
        self.input_name = WebElement(page, "input.pp-input__inner")

        # Кнопка создания спецификации
        self.create_button = WebElement(page, "button.mts-button.mts-button_l")

        # СТРАНИЦА ГОТОВОЙ СПЕЦИФИКАЦИИ ---------------------------------------------------------------------------------------------------------------------

        # Кнопка удаления спецификации
        self.delete_spec_button = WebElement(page, "//*[text() = ' Удалить ']")

        # Кнопка подтверждения удаления спецификации
        self.delete_spec_button_second = WebElement(page, "//*[text() = ' Удалить']")

        # Кнопка Редактирования
        self.edit_spec_button = WebElement(page, "//*[text() = ' Изменить спецификацию ']")

        # Тоглы атрибутов
        self.toggles = ManyWebElements(page, "label.pp-toggle.pp-toggle_s")
