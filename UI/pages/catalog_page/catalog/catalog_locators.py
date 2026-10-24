from UI.base.WebElement import WebElement, ManyWebElements


class CatalogPageLocators:
    def __init__(self, page):
        # ХЕДЕР ------------------------------------------------------------------------------------------------------------

        # ЛОГО ---
        # Здесь можно добавить элементы, связанные с логотипом

        # ТАБЫ -------------------------------------------------------------------------------------------------------------

        # Таб Все
        self.all = WebElement(page, "//*[text() = 'Все ']")

        # Таб Внешние
        self.external = WebElement(page, "#commercial")

        # Таб Внутренние
        self.internal = WebElement(page, "#internal")

        # Таб Архивные
        self.archive = WebElement(page, "//*[text() = 'Архивные ']")

        # СТРОКА ПОИСКА ----------------------------------------------------------------------------------------------------

        # Строка поиска
        self.search_str = WebElement(page, "input.input")

        # Открытая строка поиска
        self.search_str_opened = WebElement(page, ".productSearchInput")

        # Закрытая строка поиска
        self.search_str_closed = WebElement(page, ".productSearchInput")

        # Крестик на строке поиска
        self.closed = WebElement(page, ".suffixIcon")

        # ИЗБРАННОЕ --------------------------------------------------------------------------------------------------------

        # Кнопка Избранные
        self.favorites_button = WebElement(page, ".buttonFavoritesBlock .favoritesFlag")

        # Первый избранный продукт в модальном окне
        self.first_favorite = WebElement(page, ".favorites .productItem")

        # ВЫПАДАЮЩЕЕ МЕНЮ В ФИО --------------------------------------------------------------------------------------------

        # Аватарка и ФИО в правом верхнем углу
        self.fio = WebElement(page, "//*[text() = ' Светов Даниил ']")

        # Пункт меню Заявки
        self.applications_menu_item = WebElement(page, "//*[text() = 'Заявки']")

        # Пункт меню Уволенные сотрудники
        self.fired_menu_item = WebElement(page, "//*[text() = 'Сотрудники']")

        # Пункт меню Дополнительные сотрудники
        self.additional_menu_item = WebElement(page, "//*[text() = 'Дополнительные сотрудники']")

        # Пункт меню Хранилище
        self.storage_menu_item = WebElement(page, "//*[text() = 'Хранилище']")

        # Пункт меню Массовое изменение продуктов
        self.bulk_ops_menu_item = WebElement(page, "//*[text() = 'Массовое изменение продуктов']")

        # Пункт меню Группы пользователей
        self.user_groups_menu_item = WebElement(page, "//*[text() = 'Группы пользователей']")

        # Пункт меню Изменения атрибутов
        self.change_statuses_menu_item = WebElement(page, "//*[text() = 'Изменение свойств продуктов']")

        # Раздел Изменения Класса критичности
        self.change_criticality_class = WebElement(page, "//*[text() = 'Класс критичности ']")

        # НАВИГАЦИЯ --------------------------------------------------------------------------------------------------------

        # КАТЕГОРИИ ---
        # Здесь можно добавить элементы, связанные с категориями

        # ФИЛЬТРЫ ----------------------------------------------------------------------------------------------------------

        # Все фильтры в меню всех фильтров
        self.all_filters_in_all_filters_menu = ManyWebElements(page, ".filter .title")

        # СТАТУСЫ ---
        # Здесь можно добавить элементы, связанные со статусами

        # КНОПКИ СКАЧИВАНИЯ ИКСЕЛЬ И ДОБАВЛЕНИЯ ПРОДУКТА -------------------------------------------------------------------

        # Кнопка добавления продукта на странице добавления продуктов
        self.add_product_on_page = ManyWebElements(page, "//*[text() = 'Выбрать']")

        # Блоки добавления продукта на странице добаления продукта для внешних сервисов
        self.add_cards = ManyWebElements(page, '.card')

        # Кнопки выбора типа продукта на странице добавления
        self.add_cards_buttons = ManyWebElements(page, '.cardButton')

        # Ссылки на примеры на странице добавления
        self.add_cards_links = ManyWebElements(page, '.links span a')

        # Кнопка Скачать иксель
        self.excel = WebElement(page, "//*[text() = ' Скачать Excel ']")

        # Модальное окно Excel
        self.excel_modal_window = WebElement(page, '.selectDate')

        # Выбор Excel после нажатия кнопки
        self.excel_variants = ManyWebElements(page, '.dropdownItem')

        # Кнопка Скачать
        self.download = WebElement(page, ".footerSelectDate .mts-button")

        # Кнопка На одну дату
        self.excel_load_one_date = WebElement(page, "#reportByDate")

        # Кнопка На период
        self.excel_load_period = WebElement(page, "#reportByPeriod")

        # Кнопка Все продукты
        self.excel_load_all = WebElement(page, '#allProducts')

        # Кнопка Все прикреплённые документы
        self.excel_load_all_docs = WebElement(page, 'link=Все прикреплённые документы')

        # Кнопка Проверка кластера
        self.excel_cluster = WebElement(page, '#getClusterFile')

        # Кнопка иксель Изменение атрибутов
        self.excel_update_attr = WebElement(page, "//*[text() = ' Изменение атрибутов ']")

        # Аллерт при отсутствии даты
        self.alert_date = WebElement(page, "//*[text() = 'Пожалуйста, укажите дату выгрузки отчёта']")

        self.alert_dates = WebElement(page, "//*[text() = 'Пожалуйста, укажите даты отчёта']")

        # Датапикер в модалке скачивания иксель на одну дату
        self.datapicker_one_date = WebElement(page, ".oneDateWidth")

        # Все атрибуты в Excel
        self.all_attributes_excel = ManyWebElements(page, '.attributes .attribute .pp-checkbox')

        # Необязательные атрибуты Excel
        self.other_attributes_excel = ManyWebElements(page,
                                                      '.attributesContainer .attributes .attribute .pp-checkbox')

        # Выбрать все атрибуты
        self.choose_all_button = WebElement(page, "//*[text()='Выбрать все']")

        # Датапикер в модалке скачивания иксель начало периода
        self.datapicker_period_begin = WebElement(page, "#periodBegin")

        # Датапикер в модалке скачивания иксель конец периода
        self.datapicker_period_end = WebElement(page, "#periodEnd")

        # КОНТЕНТ ----------------------------------------------------------------------------------------------------------

        # Звездочка на первой карточке продукта на витрине
        self.eco_icon = WebElement(page, '.footer .eco')

        # Название одного продукта из блока
        self.product_title = WebElement(page, '.productList .productItem .header')

        # Название всех продуктов продукта из блока
        self.all_product_title = ManyWebElements(page, '.productList .productItem .header')

        # Имя пользователя на карточке продукта
        self.ownerName = ManyWebElements(page, '.ownerName')

        # Кирпичи продуктов
        self.products = ManyWebElements(page, '.productItem')

        # карточка первого продукта
        self.product_card = WebElement(page, '.productItem')

        # Заголовок продукта внутри карточки
        self.title_in_prod = WebElement(page, '.productHeader .name')

        # Названия в блоках продуктов
        self.products_titles = ManyWebElements(page, '.productList .header')

        # Заголовки категорий
        self.headers_categories = ManyWebElements(page, '.captionCategory')

        # Кнопка добавления избранного на в хедере
        self.add_favorite_in_header = WebElement(page, '#addToFavorite')

        # Кнопка удаления из избранного на в хедере
        self.delete_favorite_in_header = WebElement(page, '#delFromFavorite')
