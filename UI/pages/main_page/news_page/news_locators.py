from UI.base.WebElement import WebElement, ManyWebElements


class NewsPageLocators:

    def __init__(self, page):
        # Кнопка Добавить новость
        self.add_news_button = WebElement(page, ".addButton")

        # Кнопка добавления ссылки
        self.add_link_in_news = WebElement(page, ".bellBoth")

        # Кнопка Добавить новость на странице создания новости
        self.add_news_on_addpage = WebElement(page, '.submitBlock .mts-button')

        # Кнопка смены активности на странице новости
        self.change_active_on_news_page = WebElement(page, '.pp-toggle')

        # Заголовок в блоке новостей на странице новости
        self.news_header = WebElement(page, '.news .newsCaption')

        # Заголовок в блоке новостей на странице новости
        self.news_header_another = WebElement(page, '.newsCaption')

        # Текст в блоке новостей на странице новости
        self.news_text = WebElement(page, '.newsText')

        # Строка поиска
        self.search_line_news = WebElement(page, '.pp-input__inner')

        # Крестик в строке поиска
        self.search_line_cross = WebElement(page, '.close')

        # Сообщение о том, что ничего не найдено
        self.no_result_message = WebElement(page, "//*[text() = ' Новостей, удовлетворяющих запросу, не нашлось ']")

        # Инпут заголовка
        self.header_input = WebElement(page, ".pp-input__inner")

        # Инпут текста
        self.description_input = WebElement(page, ".pp-textarea__inner")

        # Название новости "Заголовок На удаление"
        self.first_link = WebElement(page, "//*[text() = 'Заголовок На удаление']")

        self.first_link_many = ManyWebElements(page, "//*[text() = 'Заголовок На удаление']")

        # Название новости "Заголовок На удаление х2"
        self.first_link_edit = WebElement(page, "//*[text() = 'Заголовок На удаление х2']")

        self.first_link_edit_many = ManyWebElements(page, "//*[text() = 'Заголовок На удаление х2']")

        # Кнопка удалить на странице добавления новости
        self.first_delete = WebElement(page, "//*[text() = ' Удалить новость ']")

        # Подтверждающая кнопка удалить на странице добавления новости
        self.second_delete = WebElement(page, "//*[text() = ' Удалить']")

        # Кнопка изменения новости
        self.edit_news_button = WebElement(page, "//*[text() = ' Изменить новость ']")

        # Блок новостей на главной странице
        self.news_block = WebElement(page, '.news')

        # Таб Внутренние
        self.internal = WebElement(page, "//*[text() = 'Внутренние ']")

        # Таб Архивные
        self.archive = WebElement(page, "//*[text() = 'Архивные ']")

        # Правая стрелочка на главной
        self.right_arrow = WebElement(page, "//*[@class='chevron' and @alt='r']")

        # Левая стрелочка на главной
        self.left_arrow = WebElement(page, "//*[@class='chevron' and @alt='l']")

        # Каунтер в новостях
        self.news_counter = WebElement(page, '.newsCounter')
