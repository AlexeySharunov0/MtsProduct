from UI.base.WebElement import WebElement, ManyWebElements


class MainPageLocators:

    def __init__(self, page):
        # Таб Основной информации
        self.main_info_tab = WebElement(page, '#menu_main')

        # Таб атомарных продуктов
        self.atomic_tab = WebElement(page, '#menu_atomic')

        # Таб Демо
        self.demo_tab = WebElement(page, "#menu_demo")

        # Таб документов
        self.docs_tab = WebElement(page, "#menu_docs")

        # Таб экосистемных модулей / Продуктов ЕПМ
        self.eco_tab = WebElement(page, '#menu_eco')

        # Таб метрик
        self.metrics_tab = WebElement(page, '#menu_metrics')

        # Таб Product Guide
        self.product_guide_tab = WebElement(page, "#menu_guide")

        # Таб проектов
        self.project_tab = WebElement(page, "#menu_projects")

        # Таб сервисов и капабилити
        self.services_tab = WebElement(page, '#menu_services')

        # Таб ПО
        self.software_tab = WebElement(page, "#menu_software")

        # Название продукта
        self.product_name = WebElement(page, '#nameProduct')

        # Лого продукта
        self.product_logo = WebElement(page, "//*[@title='Логотип продукта']")

        # Кнопка добавить в избранное
        self.add_to_favorite_button = WebElement(page, '#addToFavorite')

        # Кнопка удалить из избранного
        self.delete_from_favorite_button = WebElement(page, '#delFromFavorite')

        # Каунтер избранного
        self.favorite_counter = WebElement(page, '#headerCounter')

        # Блок чипсов продукта
        self.product_chips_property = WebElement(page, '.productChips')

        # Кнопка Нашли ошибку?
        self.found_bug_button = WebElement(page, '#reportInaccuracies')

        # Блок оценки
        self.rait = WebElement(page, 'productRatings')

        # Кнопка Задать вопрос
        self.ask_questions_button = WebElement(page, '.link .mts-button')

        # Ссылка на родительский продукт ТОЛЬКО у атомарных
        self.main_product_link = WebElement(page, '.mainProduct .link')

        # Боковое меню с табами
        self.product_sidebar = WebElement(page, '.sidebar')

        # Хедер Основная информация
        self.main_info_header = WebElement(page, '#main-info')

        # Хедер Свойства
        self.properties_header = WebElement(page,
                                            "//*[@class='productInfo']/*[@class='attributes']/*[@class='caption small']")

        # Хедер Руководство
        self.owners_header = WebElement(page, "//*[text()='Руководство продукта']")

        # Хедер Полезные ссылки и сервисы
        self.useful_links_header = WebElement(page,
                                              "//*[@class='productLinksAndServices']/*[text()='Полезные ссылки и сервисы']")

        # Хедер Оценки
        self.rating_header = WebElement(page, '.product-ratings__header')

        # Хедер Действия
        self.actions_header = WebElement(page, "//*[@class='productLinksAndServices']/*[text()='Действия']")

        # Хедер Цикл финансирования
        self.financing_header = WebElement(page,
                                           "//*[@class='propertyInColumnBlock-caption' and text()='Цикл финансирования']")

        # Прогрессбар жизненого цикла
        self.lifecycle = WebElement(page, '.lifeCycle')

        # Статус "Формирование идеи" на прогрессбаре
        self.idea_formation_status = WebElement(page, "//*[@class='name' and text()='Формирование идеи']")

        # Статус "Разработка" на прогрессбаре
        self.in_work_status = WebElement(page, "//*[@class='name' and text()='Разработка']")

        # Статус "Пилот" на прогрессбаре
        self.pilot_status = WebElement(page, "//*[@class='name' and text()='Пилот']")

        # Статус "Запущен в КЭ" на прогрессбаре
        self.in_use_status = WebElement(page, "//*[@class='name' and text()='Запущен в КЭ']")

        # Статус "Выведен из КЭ" на прогрессбаре
        self.out_of_use_status = WebElement(page, "//*[@class='name' and text()='Архив']")

        # Блок описание
        self.description_block = WebElement(page, '.description')

        # Блок действий под описанием
        self.actions_under_description = WebElement(page, '.productLinks')

        # Блок руководство
        self.owners_block = WebElement(page, '.owners')

        # Блок Полезные ссылки и действия
        self.useful_links_block = WebElement(page, '.productLinksAndServices')

        # Блок оценки
        self.rating_block = WebElement(page, '.product-ratings')

        # Блок действия
        self.actions_block = WebElement(page, "//*[@class='asideBlock']/*[last()]")

        # Блок цикл финансирования
        self.financing_block = WebElement(page, '.asideBlock .propertyInColumnBlock')

        # Блок табов над атрибутами
        self.tabs_horizontal = WebElement(page, '.pp-tabs')

        # Табы над атрибутами
        self.pp_tabs = ManyWebElements(page, '.pp-tab')

        # Первая ячейка атрибутов
        self.first_cell = WebElement(page, '.attributeTable .cell .caption')

        # Блок связанные продукты
        self.related_product = WebElement(page, "//*[text() = 'Связанные продукты']")

        # Блок характеристики
        self.attributes_block = WebElement(page, '.attributeTable')

        # Кнопка "Показать все свойства "
        self.show_other_button = WebElement(page, "//*[text()='Показать все свойства ']")

        # Кнопка "скрыть остальные"
        self.hide_other_button = WebElement(page, "//*[text()='Скрыть все свойства ']")

        # Блок изменения продукта
        self.edit_product_block = WebElement(page, '.editBlock')

        # Блок модального окна изменения продукта для юзера
        self.edit_product_block_user_modal = WebElement(page, '.userModal')

        # Кнопка Редактировать
        self.edit_button = WebElement(page, "//*[text()=' Редактировать']")

        # Кнопка "Обратиться к админу"
        self.call_admin_button = WebElement(page, "//*[text()=' Обратиться к Администратору ']")

        # Кнопка Удалить
        self.delete_button = WebElement(page, ".removeButton .mts-button")

        # Блок "Руководство" (Текст)
        self.owners_text = WebElement(page, '.productAside .productOwner .name')

        # Ключевые свойства
        self.key_prop = ManyWebElements(page, '.productChips .productChip')

        # Модалка о невозможности удалить продукт пока у него есть атомарные
        self.cant_delete = WebElement(page, ".atomicBlock")

        # Текст на модалке при удалении атомарных
        self.cant_delete_text = WebElement(page, '.deleteAtomic')

        # Кнопка перехода в модалеке о невозможности удалить продукт пока у него есть атомарные
        self.cant_delete_go_to_atomic = WebElement(page, ".deleteProduct .link")

        # Кнопка удалить в модалке об удалении атомарного
        self.cant_delete_button = WebElement(page, '//*[@class="deleteProduct"]/*[@class="buttons"]/button[2]')

        # Активный сотрудник
        self.user_zimina = WebElement(page, ".owners #zimina .link")

        # Уволенный сотрудник Акимова Юлия Сериковна
        self.fired_user_haritonov = WebElement(page, ".owners #aakharitonov3 .link")

        # Уволенный сотрудник Бирюков Андрей Александрович
        self.fired_user_biryukov = WebElement(page, "//*[text() = 'Бирюков Андрей Александрович']")

        # Уволенный сотрудник Стариков Алексей Валерьевич
        self.fired_user_starikov = WebElement(page, "//*[text() = 'Стариков Алексей Валерьевич']")

        # Уволенный сотрудник Кинжалов А. Г.
        self.fired_user_sudakova = WebElement(page, "//*[text() = 'Судакова Л. Б.']")

        # Статус уволен
        self.fired_status = WebElement(page, '.badgeFired')

        # Конец срока финансирования на прогрессбаре
        self.fin_close_on_progressbar = WebElement(page, '.endFinancing')

        # Карточка сотрудника
        self.user_card = WebElement(page, '.userCard')

        # Ссылка на пульс в карточке
        self.pulse_link = WebElement(page, '.linkPulse')

        # Мобильный телефон в карточке
        self.mobile_number = WebElement(page, "//*[@class='details']/div[1]/*[@class='value']")

        # Почта в карточке
        self.email_card = WebElement(page, "//*[@class='details']/div[2]/*[@class='value']")

        # Блок структуры в карточке
        self.org_block = WebElement(page, '.detailsBlock')

        # Ссылка на SOL на странице продукта
        self.sol_link = WebElement(page, "#PPInfo_card_SOL")

        # CPO в атрибутах
        self.po_attribute = WebElement(page, "//*[@id='gr_employee_sponsor']/div/span/div")

        # Код продукта на странице продукта
        self.product_code = WebElement(page, ".productCode")

        # Модалка об удалении продукта (обычного)
        self.delete_product_modal_window = WebElement(page, '.deleteProduct')

        # Инпут причины удаления
        self.reason_deleted_input = WebElement(page, "//*[@class='pp-input__inner pp-textarea__inner']")

        # Кнопка удалить в модалке удаления
        self.delete_in_modal_button = WebElement(page, '//*[@class="deleteProduct"]/*[@class="buttons"]/button[2]')

        # Радиобаттоны в модалке удаления
        self.radio_buttons = ManyWebElements(page, '.pp-radio-button')

        # Кнопка опубликовать продукт
        self.get_back_from_dead_button = WebElement(page, "//*[text()=' Опубликовать ']")

        # Чипс о том, что продукт удален
        self.deleted_chips = WebElement(page, '.deleted')

        # Тост об архивность продукта
        self.is_archived_toast = WebElement(page, '.pp-toast__content')

        # Текст у названия продукта о том что продукт архный
        self.is_archived_text = WebElement(page, '.isArchivedText')

        # Индекс тех зрелости в блоке тех зрелости
        self.index_tm = WebElement(page, '#index_TMA_tech .value')

        # Ссылка на Оценку в Selfe
        self.selfe = WebElement(page, '//*[@id="techMaturity"]/div[4]/a')

        # Дата прохождения тех зрелости в блоке тех зрелости
        self.tma_complete_date = WebElement(page, '#TMA_complete_date_tech .value')

        # Дата последнего изменения атрибутов
        self.date_with_tooltip = WebElement(page, '.dateWithTooltip')

        # Модальное окно для юзера, у которого нет прав
        self.user_modal = WebElement(page, '.userModal')

        # Карандаши в чипсах ключевых свойств
        self.edit_in_chips = ManyWebElements(page, '.productChips .editButton')
