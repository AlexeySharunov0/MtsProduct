from UI.base.WebElement import WebElement, ManyWebElements


class CuratorLocators:

    def __init__(self, page):
        # Хедер страницы
        self.header = WebElement(page, '.caption')

        # Выбор куратора
        self.curators_list = WebElement(page, '.groupItem')

        # Варианты выбора куратора
        self.curator_variants = ManyWebElements(page, '.item')

        # Варианты людей из выпадашки поиска
        self.users_variants = ManyWebElements(page, '.foundItemsName')

        # Строка поиска в выборе куратора
        self.search = WebElement(page, '.has-suffix')

        # Крестик в поиске
        self.close_search = WebElement(page, '.search .close')

        # Таблица кураторов
        self.table = WebElement(page, '.curatorsTable')

        # Строка в кураторе с единственным выбором
        self.single_info = WebElement(page, '.single')

        # Хедер таблицы
        self.table_header = WebElement(page, '.headerTable')

        # Столбец кластера
        self.clusters = ManyWebElements(page, '.cluster')

        # Сотрудники в столбце кураторов
        self.curators = ManyWebElements(page, '.jobAndName')

        # Форма выбора куратора в таблице
        self.table_curator_choose = ManyWebElements(page, '.curatorsTable .selectedField')

        # Крестик при выборе куратора в таблице много
        self.curator_delete_button = ManyWebElements(page, '.selectedField .closeButton')

        # Крестик при выборе куратора в таблице много
        self.curator_only_delete_button = ManyWebElements(page, "//*[@class='closeButton']")

        # Кнопка редактировать
        self.edit_button = WebElement(page, '.submitBlock')

        # Кнопка применить
        self.accept_button = WebElement(page, "//*[text()=' Применить ']")

        # Кнопка отмена
        self.undo_button = WebElement(page, "//*[text()=' Отмена ']")

        # Вкладка Тест кураторы один
        self.curators_test_one = WebElement(page, '#d5bd183d-28d7-46a0-8422-69c2830015c1')

        # Вкладка Тест кураторы много
        self.curators_test_many = WebElement(page, '#e80b830c-5eac-471d-a315-39a053dc30db')
