from UI.base.WebElement import WebElement, ManyWebElements


class RolesLocators:

    def __init__(self, page):
        # СТАРТОВАЯ СТРАНИЦА -----------------------------------------------------------------------------------------------

        # Добавить группу в странице групп пользователей
        self.add_role_button = WebElement(page, '//*[text()=" Добавить группу... "]')

        # Добавить группу кнопка в модальном окне
        self.add_button_in_modal_window = WebElement(page, '//*[text()="Добавить"]')

        # Title - инпут в модальном окне
        self.input_in_modal_window = WebElement(page, 'input.mts-input__inner')

        # Список ролей
        self.all_roles = ManyWebElements(page, 'div.itemName')

        # Кнопка удалить в модальном окне
        self.delete_button_in_modal_window = WebElement(page, '//*[text()=" Удалить "]')

        # Чекбокс множественного выбора в блоке редактирования группы - просмотр
        self.checkbox_multiple_select_view = WebElement(page, '//*[text()=" Просмотр "]')

        # Чекбокс множественного выбора в блоке редактирования группы - редактирование
        self.checkbox_multiple_select_edit = WebElement(page, '//*[text()=" Редактирование "]')

        # Только для административных групп

        # Столбец чекбоксов Просмотр
        self.view_checkbox_column = ManyWebElements(page, 'table td:nth-of-type(2) label')

        # Столбец чекбоксов 2
        self.checkbox_column_2 = ManyWebElements(page, 'table td:nth-of-type(3) label')

        # Столбец чекбоксов 3
        self.checkbox_column_3 = ManyWebElements(page, 'table td:nth-of-type(4) label')

        # Кнопка Сохранить
        self.save_button = WebElement(page, 'button.mts-button.mts-button_m')

        self.edit_buttonqq = ManyWebElements(page, '.itemName .edit')
