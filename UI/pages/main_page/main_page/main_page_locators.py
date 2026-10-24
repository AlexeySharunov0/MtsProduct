from UI.base.WebElement import WebElement, ManyWebElements


class MainPageLocators:

    def __init__(self, page):
        # ХЕДЕР ------
        # ЛОГО ---
        # ТАБЫ ---
        # СТРОКА ПОИСКА ---
        # ИЗБРАННОЕ ---
        # ВЫПАДАЮЩЕЕ МЕНЮ В ФИО ---

        # НАВИГАЦИЯ ------
        # КАТЕГОРИИ ---
        # ФИЛЬТРЫ ---
        # СТАТУСЫ ---

        # КНОПКИ СКАЧИВАНИЯ ИКСЕЛЬ И ДОБАВЛЕНИЯ ПРОДУКТА ------

        # КОНТЕНТ ------

        # ДЛЯ GOTO ------

        # ХЕДЕР ------------------------------------------------------------------------------------------------------------

        # ЛОГО --------------------------------------------

        # Лого
        self.logo = WebElement(page, '#logo')

        # FAQ
        self.faq = WebElement(page, '.faq')

        # МОЙ ПОРТФЕЛЬ --------------------------------------------

        # Значок Мой портфель на главное
        self.my_briefcase = WebElement(page, "//*[text() = 'Мой портфель ']")

        # Таб проектов
        self.projects = WebElement(page, "//*[text() = 'Проекты']")

        # iframe на табе проектов
        self.iframe_in_projects = WebElement(page, '#dashboard')

        # ТАБЫ --------------------------------------------

        # Таб Внешние
        self.external = WebElement(page, '#commercial')

        # Таб Внутренние
        self.internal = WebElement(page, '#internal')

        # Таб Архивные
        self.archive = WebElement(page, "//*[text() = 'Архивные ']")

        # Таб  Хаб
        self.hab = WebElement(page, "//*[text() = 'Продуктовый хаб ']")

        # Таб Сервисы
        self.services = WebElement(page, "//*[text() = 'Сервисы ']")

        # Каунтер в табe внешние
        self.external_category_counter = WebElement(page, '#commercial')

        # Каунтер в табe внутренние
        self.internal_category_counter = WebElement(page, '#internal')

        # Каунтер в табe архивные
        self.archive_category_counter = WebElement(page, '#archive')

        # Каунтер в табe хабы
        self.habs_category_counter = WebElement(page, '#hub')

        # Каунтер в табe сервисы
        self.services_category_counter = WebElement(page, '#service')

        # СТРОКА ПОИСКА --------------------------------------------

        # Подсказка "Архив" в поиске
        self.archive_suggestion = WebElement(page, "//span[contains(text(), 'Архив')]")

        # Подсказка "Удалён" в поиске
        self.deleted_suggestion = WebElement(page, "//span[contains(text(), 'Удалён')]")

        # Иконка "Архив" в подсказках поиска
        self.archive_icon = WebElement(page, "//img[contains(@src, 'archive')]")

        # Иконка "Удалён" в подсказках поиска
        self.deleted_icon = WebElement(page, "//img[contains(@src, 'trash-rounded')]")

        # Строка поиска
        self.search_str = WebElement(page, '.productSearchInput .input')

        # Открытая строка поиска
        self.search_str_opened = WebElement(page, '.productSearchInput')

        # Закрытая строка поиска
        self.search_str_closed = WebElement(page, '.productSearchInput')

        # Крестик на строке поиска
        self.closed = WebElement(page, '.suffixIcon')

        # Кнопка "Показать все результаты поиска"
        self.check_all_in_search = WebElement(page, "//*[text() = ' Показать все результаты поиска ']")

        # ИЗБРАННОЕ --------------------------------------------

        # Кнопка Избранные
        self.favorites_button = WebElement(page, '.buttonFavorites')

        # Первый избранный продукт в модальном окне
        self.first_favorite = WebElement(page, '.favorites .productItem')

        # ВЫПАДАЮЩЕЕ МЕНЮ В ФИО --------------------------------------------

        # Аватарка и ФИО в правом верхнем углу
        self.fio = WebElement(page, "//*[text() = ' Светов Даниил ']")

        # Выпадающее меню для админа
        self.dropdown_menu = WebElement(page, '.userWithDropdown')

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

        # Пунк меню Изменения атрибутов
        self.change_statuses_menu_item = WebElement(page, "//*[text() = 'Изменение свойств продуктов']")

        # Раздел Изменения Класса критичности
        self.change_criticality_class = WebElement(page, "//*[text() = 'Класс критичности ']")

        # НАВИГАЦИЯ --------------------------------------------------------------------------------------------------------

        self.catalogue_button = WebElement(page, '//*[text() = " Каталог всех продуктов "]')

        self.closed_products = WebElement(page, '//*[text() = "Закрытые продукты "]')

        self.archive_catalogue_button = WebElement(page, '//*[text() = " Архив продуктов "]')

        # КАТЕГОРИИ ---------------------------------------------

        # Категория Все
        self.category_all = WebElement(page, '#all')

        # Категория продуктов Product Governance
        self.category_PG = WebElement(page, '#(PPInfo_category_spravochnik)Governance')

        # Заголовок категории Product Governance
        self.category_title_PG = WebElement(page, '#Governance')

        # Категория продуктов Легкий старт
        self.category_ezstart = WebElement(page, '#(PPInfo_category_spravochnik)Lightstart')

        # Заголовок категории Легкий старт
        self.category_title_ezstart = WebElement(page, '#Lightstart')

        # Категория продуктов Мтс банк(Базовае)
        self.category_MTSBank = WebElement(page, '#(PPInfo_category_spravochnik)Bank')

        # Заголовок категории Мтс банк(Базовае)
        self.category_title_MTSBank = WebElement(page, '#Bank')

        # Категория продуктов Телеком(Базовае)
        self.category_telecom = WebElement(page, '#(PPInfo_category_spravochnik)Telecom')

        # Заголовок категории Телеком(Базовае)
        self.category_title_telecom = WebElement(page, '#Telecom')

        # Категория продуктов Партнерские
        self.category_partner = WebElement(page, '#(PPInfo_category_spravochnik)Partner')

        # Заголовок категории Партнерские
        self.category_title_partner = WebElement(page, '#Partner')

        # Категория продуктов Big Data
        self.category_bigdata = WebElement(page, '#(PPInfo_category_spravochnik)Bigdata')

        # Заголовок категории Big Data
        self.category_title_bigdata = WebElement(page, '#Bigdata')

        # Категория продуктов МТС ИИ
        self.category_mtsII = WebElement(page, '#(PPInfo_category_spravochnik)AI')

        # Заголовок категории МТС ИИ
        self.category_title_mtsII = WebElement(page, '#AI')

        # Категория продуктов Сайты
        self.category_sites = WebElement(page, '#(PPInfo_category_spravochnik)Site')

        # Заголовок категории Сайты
        self.category_title_sites = WebElement(page, '#Site')

        # Категория продуктов Другое
        self.category_other = WebElement(page, '#(PPInfo_category_spravochnik)Other')

        # Заголовок категории Другое
        self.category_title_other = WebElement(page, '#Other')

        # ФИЛЬТРЫ ----------------------------------------------

        # Каунтер в фильтрах
        self.count_in_filter = ManyWebElements(page, '.dropdownItem .count')

        # Фильтр Рынок
        self.filter_market = WebElement(page, '#PPinfo_market')

        # Параметр B2B в фильтре рынок
        self.b2b = WebElement(page, '#(PPinfo_market)B2B_block')

        # Параметр Не указан
        self.NotSpecified_block = WebElement(page, '#NotSpecified_block')

        # Фильтр BO
        self.filter_BO = WebElement(page, '#employee_business_owner')

        # Фильтр CPO
        self.filter_CPO = WebElement(page, '#employee_chief_PO')

        # Фильтр Вице президент
        self.filter_sponsor = WebElement(page, '#employee_sponsor')

        # Параметр Гаврилова Инесса в фильтре Вице президент
        self.galactoin = WebElement(page, '#igalakt_block')

        # Параметр Горбунов александр в фильтре Вице президент
        self.gorbunov = WebElement(page, '#AGO_block')

        # Параметр Зимина Ольга в фильтре Вице президент
        self.zimina = WebElement(page, '#zimina_block')

        # Фильтр Web, app
        self.filter_web_app = WebElement(page, '#PPinfo_web_app')

        # Параметр web, app
        self.web_app = WebElement(page, '#(PPinfo_spravochnik_webapp)WEBAPP_block')

        # Фильтр Бренд МТС
        self.filter_MTS_brand = WebElement(page, '#PPinfo_MTS_Brand')

        # Параметр Бренд МТС ДА
        self.filter_MTS_brand_yes = WebElement(page, '#(PPinfo_MTSBrand)MTSBrand_yes_block')

        # Фильтр Инициированно закрытие
        self.filter_start_closing = WebElement(page, '#PPinfo_start_close')

        # Параметр Инициированно закрытие
        self.filter_start_closing_yes = WebElement(page, '#(PPinfo_spravochnik_start_close)Yes_block')

        # Фильтр Легкий старт
        self.filter_ez_start = WebElement(page, '#PPinfo_mvp')

        # Параметр Легкий старт Нет
        self.filter_ez_start_yes = WebElement(page, '#(PPinfo_mvp)MVPNo_block')

        # Чипс выбранного фильтра
        self.filter_chips = WebElement(page, '.selectedValue')

        # Чипсы выбранного фильтра
        self.filter_chipses = ManyWebElements(page, '.selectedValue')

        # Кнопка " Все фильтры"
        self.all_filters = WebElement(page, '.allFilters')

        # Все фильтры в меню всех фильтров
        self.all_filters_in_all_filters_menu = ManyWebElements(page, ".filter .title")

        # Строка поиска в меню Всех фильтров
        self.filters_search = WebElement(page, '.content input.pp-input__inner')

        # Первый по счету фильтр
        self.filter_in_menu = WebElement(page, '.content .filter:nth-of-type(1)')

        # Первый атрибут в первом фильтре
        self.filter_attr = WebElement(page, "//*[text() = 'Выбрать всё ']")

        # Все значения первого по счету фильтра
        self.filter_values = WebElement(page, '.values')

        # Атрибуты в первом фильтре
        self.filter_attrs = ManyWebElements(page, '.checkbox')

        # Кнопка Сбросить фильтры
        self.drop_filt = WebElement(page, '.sidebarFilters .resetButton .mts-button__inner')

        # Чипс Сбросить фильтры
        self.drop_filt_chips = WebElement(page, "//*[text() = 'Сбросить']")

        # Кнопка закрытия меню фильтров
        self.close_filter_menu = WebElement(page, '.closeButton')

        # Все значение в фильтре
        self.all_value_in_filters = ManyWebElements(page, '.pp-dropdown-popper .pp-dropdown-item')

        # СТАТУСЫ -----------------------------------------------------

        # Статус Формирование идеи
        self.status_idea = WebElement(page, "//*[text() = 'Формирование идеи']")

        # Статус Разработка
        self.status_development = WebElement(page, "//*[text() = 'Разработка']")

        # Статус  Запуск пилота
        self.status_start_MVP = WebElement(page, "//*[text() = 'Запуск пилота']")

        # Статус Запуск отменен
        self.status_closed = WebElement(page, "//*[text() = 'Запуск отменен']")

        # Статус  Ожидание решения
        self.status_waiting = WebElement(page, "//*[text() = 'Ожидание решения']")

        # Статус  Запущен в КЭ
        self.status_start_commercial = WebElement(page, "//*[text() = 'Запущен в КЭ']")

        # Счетчик активного статуса
        self.active_status_counter = WebElement(page, "button.productStatusItem.selected span.count")

        # КНОПКИ СКАЧИВАНИЯ ИКСЕЛЬ И ДОБАВЛЕНИЯ ПРОДУКТА -------------------------------------------------------------------

        # Кнопка Добавить продукт
        self.add_product = WebElement(page, "#addProduct")

        # Кнопка добавления продукта на странице добавления продуктов
        self.add_product_on_page = ManyWebElements(page, "//*[text() = 'Выбрать']")

        # Кнопка добавления Внутерннего продукта
        self.add_int = WebElement(page, "//*[text() = 'Внутренний']")

        # Кнопка добавления Сервиса
        self.add_service = WebElement(page, "//*[text() = 'Сервис']")

        # Блоки добавления продукта на странице добаления продукта для внешних сервисов
        self.add_cards = ManyWebElements(page, '.card')

        # Кнопки выбора типа продукта на странице добавления
        self.add_cards_buttons = ManyWebElements(page, '.cardButton')

        # Ссылки на примеры на странице добавления
        self.add_cards_links = ManyWebElements(page, '.links span a')

        # Кнопка перехода в отчеты иксель
        self.excel = WebElement(page, '#excel')

        # Стрелочка скачать эксель
        self.excel_arrow = WebElement(page, '.content .chevron')

        # Модальное окно Excel
        self.excel_modal_window = WebElement(page, '.selectDate')

        # Выбор Excel после нажатия кнопки
        self.excel_variants = ManyWebElements(page, '.reports .mts-button')

        # Кнопка Скачать
        self.download = WebElement(page, '.submitBlock')

        # Кнопка С учётом выбранных фильтров
        self.excel_load_with_filters = WebElement(page, '#externalWithFilters')

        # Кнопка На одну дату
        self.excel_load_one_date = WebElement(page, "//div[@id='reportByDate']/parent::a")

        # Кнопка На период
        self.excel_load_period = WebElement(page, "//div[@id='reportByPeriod']/parent::a")

        # Кнопка Продукты
        self.excel_load_all = WebElement(page, "//div[@id='general']/parent::a")

        # Кнопка Все прикреплённые документы
        self.excel_load_all_docs = WebElement(page, "//div[@id='allAttachedDocs']/parent::a")

        # Кнопка Проверка кластера
        self.excel_cluster = WebElement(page, '#getClusterFile')

        # Кнопка иксель Изменение атрибутов
        self.excel_update_attr = WebElement(page, "#changeAttributesReport")

        # Аллерт при загрузке икселя
        self.alert = WebElement(page, "//*[text() = 'Файл формируется. Скоро начнется скачивание']")

        # Аллерт при отсутствии даты
        self.alert_date = WebElement(page, "//*[text() = 'Пожалуйста, укажите дату выгрузки отчёта']")

        self.alert_dates = WebElement(page, "//*[text() = 'Пожалуйста, укажите даты отчёта']")

        # Датапикер в модалке скачивания иксель на одну дату
        self.datapicker_one_date = WebElement(page, ".oneDateWidth")

        # Все атрибуты в Excel
        self.all_attributes_excel = ManyWebElements(page, '.attributes .attribute .pp-checkbox')

        # Необязательные атрибуты Excel
        self.other_attributes_excel = ManyWebElements(page, '.attributesContainer .attributes .attribute .pp-checkbox')

        # Выбрать все атрибуты
        self.choose_all_button = WebElement(page, "//*[text()='Выбрать все']")

        # Датапикер в модалке скачивания иксель начало периода
        self.datapicker_period_begin = WebElement(page, '#periodBegin')

        # Датапикер в модалке скачивания иксель конец периода
        self.datapicker_period_end = WebElement(page, '#periodEnd')

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
        self.product_card = WebElement(page, '.productCard')

        # Заголовок продукта внутри карточки
        self.title_in_prod = WebElement(page, '.productHeader .name')

        # Названия в блоках продуктов
        self.products_titles = ManyWebElements(page, '.productList .header')

        # Заголовки категорий
        self.headers_categories = ManyWebElements(page, '.captionCategory')

        # Выключатель архивных продуктов в поиске
        self.archive_products_search_show_toggle = WebElement(page, "div.showArchive label")

        # Карточки архивных продуктов
        self.archive_products_card = WebElement(page, "a.productItem.archived")

        # Кнопка добавления избранного на в хедере
        self.add_favorite_in_header = WebElement(page, '#addToFavorite')

        # Кнопка удаления из избранного на в хедере
        self.delete_favorite_in_header = WebElement(page, '#delFromFavorite')

        # Тип продукта в блоке продуктов
        self.product_type_on_cards = ManyWebElements(page, '.footer .type .content')

        # Чипс "Название продукта" в поисковой выдаче
        self.product_name_chip_on_search_results = WebElement(page, "//*[text() = 'Название продукта']")

        # Чипс "ID продукта" в поисковой выдаче
        self.bi_code_chip_on_search_results = WebElement(page, "//*[text() = 'ID продукта']")

        # Чипс "Приложения" в поисковой выдаче
        self.app_chip_on_search_results = WebElement(page, "//*[text() = 'Приложения']")

        # Чипс "Системы" в поисковой выдаче
        self.system_chip_on_search_results = WebElement(page, "//*[text() = 'Системы']")

        # Чипс "DNS и домены" в поисковой выдаче
        self.showcase_name_chip_on_search_results = WebElement(page, "//*[text() = 'DNS и домены']")

        # Чипс "Команда поддержки ИС" в поисковой выдаче
        self.help_team_is_chip_on_search_results = WebElement(page, "//*[text() = 'Команда поддержки ИС']")

        # Чипс "Теги" в поисковой выдаче
        self.tags_chip_on_search_results = WebElement(page, "//*[text() = 'Теги']")

        # Чипс "Код Oracle" в поисковой выдаче
        self.oracle_chip_on_search_results = WebElement(page, "//*[text() = 'Код Oracle']")

        # Чипс "ФИО руководства" в поисковой выдаче
        self.fio_chip_on_search_results = WebElement(page, "//*[text() = 'ФИО руководства']")

        # Чипс "Название продукта" в поисковой выдаче
        self.product_name_chip_on_search_results = WebElement(page, "//*[text() = 'Название продукта']")

        # ДЛЯ GOTO ---------------------------------------------------------------------------------------------------------

        # Пункт меню Главная страница
        self.main_page_menu_item = WebElement(page, "//*[text() = 'Главная страница']")

        # Пункт меню Страница Внешнего продукта
        self.product_page_menu_item_commercial = WebElement(page, "//*[text() = 'Страница внешнего продукта']")

        # Пункт меню Страница Внутреннего продукта
        self.product_page_menu_item_internal = WebElement(page, "//*[text() = 'Страница внутреннего продукта']")

        # Пункт меню Форма добавления продукта
        self.required_fields_settings = WebElement(page, "//*[text() = 'Форма добавления продукта']")

        # Пункт меню Управление уведомлениями
        self.notifications_menu_item = WebElement(page, "//*[text() = 'Управление уведомлениями']")

        # Пункт меню Выйти
        self.quit_menu_item = WebElement(page, '.exitIcon')

        # Уволенные сотрудники в на станице уволеных сотрудников
        self.fired_owners = WebElement(page, '.employees')
