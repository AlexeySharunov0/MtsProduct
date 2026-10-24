from UI.base.WebElement import WebElement, ManyWebElements


class PGLocators:

    def __init__(self, page):
        # Главная ---------------------------------------------------------------------------------------------------------

        # Заголовок на странице Product Guide
        self.header = WebElement(page, '.caption')

        # Боковое меню с вкладками
        self.side_menu = WebElement(page, '.groupItem')

        # Вкладки
        self.side_groups = ManyWebElements(page, "//*[contains(@class, 'productGuideStep')]")

        # Кнопка "Добавить шаг"
        self.add_step_button = WebElement(page, '.lifeCycleList .mts-button')

        # Таблица шагов
        self.table_steps = WebElement(page, '.lifeCycleTable')

        # Шаги на главной
        self.steps = ManyWebElements(page, "//*[@class='productGuideRow']/td[2]/a")

        # Строки на главной
        self.rows_steps = ManyWebElements(page, '.productGuideRow')

        # Тестовый шаг
        self.test_step = WebElement(page, "//*[text()='test_name']")

        # Добавление/редактирование шага ----------------------------------------------------------------------------------

        # Хедер на странице редактирование
        self.step_header = WebElement(page, '.contentNews .main .caption')

        # Кнопка Редактировать основной шаг
        self.edit_step_button = WebElement(page, '#editAction')

        # Кнопка добавить вложенный шаг
        self.add_sub_action_button = WebElement(page, '#add_sub_step')

        # Тогл активности
        self.activity_toggle = WebElement(page, '.pp-toggle')

        # Название шага
        self.step_name = WebElement(page, '.has-suffix')

        # Описание шага
        self.step_description = WebElement(page, '.pp-textarea__inner-box .pp-input__inner')

        # Обязательность шага (0-1)
        self.step_required_radio_button = ManyWebElements(page, '.pp-radio-button')

        # Повторяемость шага (2-3)
        self.step_repeatable_radio_button = ManyWebElements(page, '.pp-radio-button')

        # Поле Сотрудники
        self.step_users = WebElement(page, '.selectedField')

        # Поле Сотрудники Поиск фио
        self.step_users_find_line = WebElement(page, '.itemsField .pp-input__inner-box .has-suffix')

        # Поле Сотрудники Лупа
        self.step_find_button = WebElement(page, '.find')

        # Найденные сотрудники
        self.found_users = ManyWebElements(page, '.foundItems .item')

        # Кнопка Добавить ссылку
        self.add_link_button = WebElement(page, '.link__addition')

        # Название ссылки
        self.link_name_input = WebElement(page, "//*[@class='link__multiple'][last()]/div[1]/div/input")

        # Ссылка
        self.link_input = WebElement(page, "//*[@class='link__multiple'][last()]/div[2]/div/input")

        # Блоки ссылок
        self.link_blocks = ManyWebElements(page, '.link__multiple')

        # Кнопка Удалить ссылку
        self.delete_link_button = WebElement(page, '.link__removal')

        # Форма загрузки файлов
        self.add_file_form = WebElement(page, ".uploadArea #assetsFieldHandle")

        # Поле загрузки файлов
        self.add_files_block = WebElement(page, '.uploadArea')

        # Загруженные файлы
        self.chosen_files = ManyWebElements(page, '.chosen')

        # Кнопки удаления файлов
        self.delete_files_buttons = ManyWebElements(page, "//*[@title='Убрать файл']")

        # Блок условий
        self.conditions_block = WebElement(page, '.conditions')

        # Дополнительные условия
        self.conditions = ManyWebElements(page, '.condition')

        # Выбор значений у условий
        self.conditions_values = ManyWebElements(page, '.foundItems .item')

        # Выбранные значения у условий
        self.conditions_chosen_values = ManyWebElements(page, '.condition .universalItem')

        # Блок кнопок сохранения
        self.edit_block = WebElement(page, '.submitBlock.modal')

        # Кнопка Удалить
        self.delete_step_button = WebElement(page, "//*[text()=' Удалить ']")

        # Кнопка Сохранить изменения
        self.save_changes_button = WebElement(page, "//*[text()='Сохранить изменения']")

        # Кнопка Добавить
        self.add_button_inside = WebElement(page, "//*[text()='Добавить']")

        # Подтверждение удаления шага
        self.delete_step_approval = WebElement(page, "//*[@class='buttonsDelete']/button[2]")

        # Надпись при отсутствии шагов
        self.no_steps_text = WebElement(page, '.absent')

        # Форма Группы
        self.groups_field = WebElement(page, '#groups')

        # Тоглы активности на странице всех действий
        self.activity_toggles = ManyWebElements(page, '.pp-toggle')

        # Кнопка К деталям шага
        self.to_details_button = WebElement(page, "//*[contains(text(), '←')]")

        # Превью шага - сам шаг
        self.step_preview = WebElement(page, '.step')

        # Превью шага - значок с номером
        self.step_number_preview = WebElement(page, '.serialNumber')

        # Превью шага - чипс обязательности
        self.step_required_chips_preview = WebElement(page, '.required')

        # Превью шага - чипс повторяемости
        self.step_repeatable_chips_preview = WebElement(page, '.repeatable')

        # Превью шага - название шага
        self.step_name_preview = WebElement(page, '.name')

        # Превью шага - описание шага
        self.step_description_preview = WebElement(page, '.description')

        # Превью шага - сотрудники
        self.step_employees_preview = ManyWebElements(page, '.employee')

        # Превью шага - ссылки
        self.step_links_preview = ManyWebElements(page, '.link')

        # Превью шага - файлы
        self.step_files_preview = ManyWebElements(page, '.files .file')
