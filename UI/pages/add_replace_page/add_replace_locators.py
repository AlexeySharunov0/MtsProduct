from UI.base.WebElement import WebElement, ManyWebElements


class AddPageLocators:
    def __init__(self, page):
        # Инпут логина
        self.login_input = WebElement(page, '#username')

        # Инпут пароля
        self.password_input = WebElement(page, '#password')

        # Кнопка авторизации
        self.login_button = WebElement(page, '.btn')

        # СОЗДАНИЕ

        # Шаги в форме добавления продукта
        self.steps = WebElement(page, '.steps')

        # Кнопки выбора типа продукта
        self.choose_type_button = ManyWebElements(page, '.card .mts-button')

        # Значок на пройденном шаге
        self.check_mark = ManyWebElements(page, '.statusIcon')

        # Кнопка Показать еще в админской форме добавления
        self.show_all_button = WebElement(page, '.showMoreRow .mts-button')

        # Тоггл отключения информирования
        self.notification_toggle = WebElement(page, '.pp-toggle.pp-toggle_m')

        self.notification_toggle_in_brief = WebElement(page, '.editBlock .notify .pp-toggle')

        # Поле ввода сотрудника
        self.po_input = WebElement(page, '.search .pp-input__inner')

        # Кнопка лупы
        self.find = WebElement(page, '.find')

        # Выбор конкретного сотрудника
        self.user = WebElement(page, '.foundItemsName')

        # Кнопка очистить поля
        self.clear_button = WebElement(page, "//*[text() = ' Очистить поля ']")

        # Кнопка Отправить на модерацию
        self.go_button = WebElement(page, "//*[text() = ' Отправить на модерацию ']")

        # Кнопка Добавить продукт
        self.save_button = WebElement(page, "//*[text() = ' Добавить продукт ']")

        # Статус заявки
        self.status_info = WebElement(page, '.status')

        # Заголовок на стартовой странице
        self.header = WebElement(page, '.productHeader')

        # Блок руководства
        self.owners = WebElement(page, '.asideBlock')

        # Блок оценки
        self.rait = WebElement(page, '.productRatings')

        # Блок характеристики
        self.attr = WebElement(page, '.attributeTable')

        # Чипс New
        self.isNew = WebElement(page, '.isNew')

        # Ссылка на FAQ
        self.faq = WebElement(page, '.steps .faq .link')

        # РЕДАКТИРОВАНИЕ

        # кнопка Редактировать
        self.edit_button = WebElement(page, "//*[text() = ' Редактировать']")

        # Кнопка удалить черновик
        self.delete_edit = WebElement(page, "//*[text() = ' Удалить черновик ']")

        # Инпут стринги в открывшейся модалке
        self.input_replace_string = WebElement(page, '.link .pp-input__inner')

        # Инпут в открывшейся модалке
        self.input_replace = WebElement(page, '.selectedField')

        # кнопка Записать
        self.save_button_replace = WebElement(page, "//*[text() = 'Записать']")

        self.show_all = WebElement(page, "//*[text() = 'Показать все свойства ']")

        # Кнопка изменить
        self.replace = WebElement(page, "//*[text() = ' Применить']")

        # Кнопка Отправить на модерацию
        self.moder_button = WebElement(page, "//*[text() = 'Отправить на модерацию']")

        # Публичное описание синяя ссылка
        self.public_links = ManyWebElements(page, '.productLinks .nameCell .captionLink')

        # Интпут в открывшейся модалке
        self.input_in_modal = WebElement(page, '.pp-input__inner-box .pp-input__inner')

        # Крестик для удаления атрибута
        self.x = WebElement(page, '.pp-icon.pp-pp-icon-close.pp-icon_m')

        # Заголовок в модалке редактирование свойства
        self.replace_header = WebElement(page, "//*[text() = 'Редактирование свойства']")

        # Аватарка и ФИО в правом верхнем углу
        self.fio = WebElement(page, '.safeAvatar')

        # Раздел Заявки в выпадашке под ФИО
        self.briefs = WebElement(page, "//*[text() = 'Заявки']")

        # Первая в счету заявка в РМ сотрудника группы опрос
        self.link_first_brief = WebElement(page, '.briefsTable .link')

        # Ссылка на продукт в заявке
        self.link_to_product_in_brief = WebElement(page, "//*[contains(@href, '/product/BI_')]")

        # Кнопка Взять в работу
        self.take_to_work = WebElement(page, "//*[text() = ' Взять в работу ']")

        # Кнопка Отклонить
        self.reject = WebElement(page, "//*[text() = ' Отклонить ']")

        # Кнопка Вернуть на доработку
        self.revision = WebElement(page, "//*[text() = ' Вернуть на доработку ']")

        # Кнопка Записать в МПС
        self.save = WebElement(page, "//div[contains(@class, 'floatBlock')]//*[text() = ' Записать ']")

        # Кнопка Одобрить и записать
        self.save_doc = WebElement(page, "//*[text() = ' Одобрить и записать ']")

        # Кнопка отправить на модерацию повторно
        self.re_moderation = WebElement(page, "//*[text() = ' Отправить на модерацию повторно ']")

        # Поле Описание на странице дороботки инициатором
        self.input_re_moderation = WebElement(
            page, '//*[@id="app"]/div/div/div/div/div/div/div[2]/div/div[2]/div/div[2]/label/div/input')

        # Инпут коммента для админа
        self.comment_for_admin = WebElement(page,
                                            "//div[@class='briefInformation']//div[4]//label[1]//div[1]//input[1]")

        # Кнопка сохранить у поля коммента для админа
        self.comment_for_admin_button = WebElement(page, "//div[4]//button[1]//span[1]")

        # Коммент в столбце в РМ опрос
        self.comment_on_rm = WebElement(
            page,
            "body > div:nth-child(4) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(2) > table:nth-child(1) > tr:nth-child(2) > td:nth-child(7) > div:nth-child(1)")

        # Тогл редактирования от лица админа после записи заявки в работу
        self.toggle_replace_admin = WebElement(page, '.briefOnWork .pp-toggle__switch')

        self.input_name_replace_admin_toggle = WebElement(page, '#name .pp-input__inner')

        # Заявка на создание продукта в списке заявок
        self.create_product_brief = WebElement(page, "//*[text() = ' Создание ']")

        # Заявка на изменение продукта в списке заявок
        self.edit_product_brief = WebElement(page, "//*[text() = ' Изменение ']")

        # строки таблицы заявок
        self.table_tr = ManyWebElements(page, 'table tr')

        # СЕЛЕКТЫ

        self.first_value = WebElement(page, '.foundItemsName')

        self.date_one = WebElement(page, "//*[text() = ' 1 ']")

        self.quit = WebElement(page, '.exitIcon')

        self.cross = WebElement(page, '.mts-input__suffix-box')

        # Подтверждение выхода
        self.quit_confirm = WebElement(page, '.btn')

        self.avatar = WebElement(page, '.safeAvatar')

        # Таб Все входящие
        self.all_tab = WebElement(page, "//*[text() = ' Все входящие ']")
        # Таб Взятые в работу
        self.take_to_work_tab = WebElement(page, "//*[text() = ' Взятые в работу ']")
        # Таб Опубликованы
        # Таб Отклонены
        # Таб Ошибки при записи

        # ДОБАВЛЕНИЯ ДОКУМЕНТА

        # Кнопка "Добавить файл"
        self.addFile = WebElement(page, "//*[text() = ' Добавить документ ']")

        # Документ
        self.doc_item = WebElement(page, '.buttonInner .name')

        # Добавление файла инпут
        self.input_file = WebElement(page, "div[class='productDocuments'] div input[type='file']")

        # Радиобаттон в фроме прикрепления документа
        self.radiobutton_public = WebElement(page, "//*[text() = ' Публичный ']")

        # Радиобаттон в фроме прикрепления документа
        self.radiobutton_closed = WebElement(page, "//*[text() = ' Закрытый ']")

        # Радиобаттон в фроме прикрепления документа
        self.radiobutton_file = WebElement(page, "//*[text() = ' Файл ']")

        # Радиобаттон в фроме прикрепления документа
        self.radiobutton_link = WebElement(page, "//*[text() = ' Ссылка ']")

        # Инпут названия документа
        self.doc_name = WebElement(page, '.container .name .pp-input__inner')

        # Публичный
        self.public_doc = WebElement(page, "//*[text() = ' Публичный ']")

        # Закрытый
        self.closed_doc = WebElement(page, "//*[text() = ' Закрытый ']")

        # Файл
        self.file = WebElement(page, "//*[text() = ' Файл ']")

        # ссылка
        self.link = WebElement(page, "//*[text() = ' Ссылка ']")

        # Инпут ссылки
        self.add_link_input = WebElement(page, '.in .pp-input .pp-input__inner')

        # Кнопка "Отправить заявку"
        self.addDoc = WebElement(page, "//*[text() = ' Отправить заявку ']")

        # Кнопка "Добавить документ"
        self.add_doc_button = WebElement(page, "//*[text() = 'Добавить']")

        # Заголовок на превью странице заявки
        self.header_add_doc = WebElement(page, '.pageHeader')

        # Кнопка корзины
        self.delete_doc = WebElement(page, '#remove-button')

        # Кнопка Удалить (корзина) все
        self.delete_doc_many = ManyWebElements(page, '.comment .chevron')

        # Подтверждение удаления
        self.delete_confirmation = WebElement(
            page, "//button[@class='mts-button mts-button_m']//span[@class='mts-button__inner']")

        # Кнопка Перейти к заявке
        self.go_to_application = WebElement(page, "//*[text() = 'Перейти к заявке']")

        # Кнопка Удалить на странице продукта
        self.delete_product_button = WebElement(page, '.removeButton .mts-button')

        # Инпут причины удаления
        self.reason_deleted_input = WebElement(page, "//*[@class='pp-input__inner pp-textarea__inner']")

        # Кнопка удалить в модалке удаления
        self.delete_in_modal_button = WebElement(page, '//*[@class="deleteProduct"]/*[@class="buttons"]/button[2]')

        # РЕДАКТИРОВАНИЕ

        self.replace_button = WebElement(
            page, "button[class='pp-button pp-button_l pp-button_theme_dark'] span[class='pp-button__inner']")

        # Значек редактирования на Жизненном цикле
        self.edit_button_lc = WebElement(page, '.lifeCycle .edit')

        # РМ Юзера

        self.my_briefs = WebElement(page, "//*[text() = 'Мои заявки']")
        self.closed_tab = WebElement(page, "//*[text() = ' Завершённые ']")
        self.repeat = WebElement(page, "//*[text() = 'Повторить']")

        # ПОЛЯ В ФОРМАХ СОЗДАНИЯ
        self.fields = ManyWebElements(page, '.field')

        self.required_fields = ManyWebElements(page, '.required')

        self.name = WebElement(page, '#name .pp-input__inner')

        self.description = WebElement(page, '#description .pp-input__inner')

        self.PPinfo_status = WebElement(page, '#PPinfo_status')

        self.employee_business_owner = WebElement(page, '#employee_business_owner .selectedField')

        self.employee_tech_lead = WebElement(page, '#employee_tech_lead .selectedField')

        self.employee_chief_PO = WebElement(page, '#employee_chief_PO .selectedField')

        self.employee_product_owner = WebElement(page, '#employee_product_owner .selectedField')

        self.PPInfo_qbrmemo_link = WebElement(page, '#PPInfo_qbrmemo_link .pp-input__inner')

        self.employee_senior_PO = WebElement(page, '#employee_senior_PO .selectedField')

        self.PPinfo_web_app = WebElement(page, '#PPinfo_web_app .selectedField')

        self.PPinfo_delta_Appstore = WebElement(page, '#PPinfo_delta_Appstore .pp-input__inner')

        self.PPinfo_GooglePlay_delta = WebElement(page, '#PPinfo_GooglePlay_delta .pp-input__inner')

        self.PPInfo_activity_oracle_code = WebElement(page, '#PPInfo_activity_oracle_code .pp-radio-button')

        self.PPInfo_atomic_product = WebElement(page, '#PPInfo_atomic_product .pp-input__inner')

        self.PPInfo_EPP_bm = WebElement(page, '#PPInfo_EPP_bm .pp-input__inner')

        self.PPInfo_business_vertical = WebElement(page, '#PPInfo_business_vertical .pp-input__inner')

        self.PPInfo_product_block = WebElement(page, '#PPInfo_product_block .selectedField')

        self.PPinfo_MTS_Brand = WebElement(page, '#PPinfo_MTS_Brand .selectedField')

        self.PPInfo_order_advertising = WebElement(page, '#PPInfo_order_advertising .pp-input__inner')

        self.PPInfo_ECO_version_And = WebElement(page, '#PPInfo_ECO_version_And .pp-input__inner')

        self.PPInfo_ECO_version_iOS = WebElement(page, '#PPInfo_ECO_version_iOS .pp-input__inner')

        self.employee_sponsor = WebElement(page, '#employee_sponsor .selectedField')

        self.PPInfo_product_com = WebElement(page, '#PPInfo_product_com .pp-input__inner')

        self.PPinfo_close_date = WebElement(page, '#PPinfo_close_date .pp-input__inner')

        self.PPinfo_execution_date = WebElement(page, '#PPinfo_execution_date .pp-input__inner')

        self.PPinfo_start_date_MVP = WebElement(page, '#PPinfo_start_date_MVP .pp-input__inner')

        self.PPinfo_start_close_date = WebElement(page, '#PPinfo_start_close_date .pp-input__inner')

        self.PPinfo_finish_date_MVP = WebElement(page, '#PPinfo_finish_date_MVP .pp-input__inner')

        self.PPInfo_date_In_progress = WebElement(page, '#PPInfo_date_In_progress .pp-input__inner')

        self.PPInfo_date_Idea_formation = WebElement(page, '#PPInfo_date_Idea_formation .pp-input__inner')

        self.PPInfo_dashboard_BFI = WebElement(page, '#PPInfo_dashboard_BFI .pp-input__inner')

        self.PPInfo_detailed_description = WebElement(page, '#PPInfo_detailed_description .pp-input__inner')

        self.PPInfo_Team_adequacy = WebElement(page, '#PPInfo_Team_adequacy .pp-input__inner')

        self.PPInfo_order_quality = WebElement(page, '#PPInfo_order_quality .pp-input__inner')

        self.PPinfo_start_close = WebElement(page, '#PPinfo_start_close .pp-radio-button')

        self.PPInfo_Eco_Integration_Andr = WebElement(page, '#PPInfo_Eco_Integration_Andr .pp-input__inner')

        self.PPInfo_Eco_Integration_Web = WebElement(page, '#PPInfo_Eco_Integration_Web .pp-input__inner')

        self.PPInfo_Eco_Integration_iOS = WebElement(page, '#PPInfo_Eco_Integration_iOS .pp-input__inner')

        self.PPinfo_EPP = WebElement(page, '#PPinfo_EPP .pp-radio-button')

        self.PPInfo_ois_card = WebElement(page, '#PPInfo_ois_card .pp-input__inner')

        self.PPInfo_card_SOL = WebElement(page, '#PPInfo_card_SOL .pp-input__inner')

        self.PPinfo_category_product = WebElement(page, '#PPinfo_category_product .selectedField')

        self.PPInfo_HFMplanning_desc = WebElement(page, '#PPInfo_HFMplanning_desc .pp-input__inner')

        self.PPInfo_Team = WebElement(page, '#PPInfo_Team .pp-input__inner')

        self.PPInfo_control_DUT = WebElement(page, '#PPInfo_control_DUT .pp-input__inner')

        self.PPinfo_mvp = WebElement(page, '#PPinfo_mvp .selectedField')

        self.PPInfo_external_user = WebElement(page, '#PPInfo_external_user .pp-input__inner')

        self.PPinfo_revenue = WebElement(page, '#PPinfo_revenue .pp-radio-button')

        self.PPinfo_konkurent = WebElement(page, '#PPinfo_konkurent .pp-input__inner')

        self.PPInfo_Monetization = WebElement(page, '#PPInfo_Monetization .pp-input__inner')

        self.PPInfo_business_area = WebElement(page, '#PPInfo_business_area .pp-input__inner')

        self.PPInfo_new_oracle_code = WebElement(page, '#PPInfo_new_oracle_code .pp-input__inner')

        self.PPInfo_main_product = WebElement(page, '#PPInfo_main_product .pp-input__inner')

        self.PPinfo_appstore_rate = WebElement(page, '#PPinfo_appstore_rate .pp-input__inner')

        self.PPinfo_GooglePlay_rate = WebElement(page, '#PPinfo_GooglePlay_rate .pp-input__inner')

        self.PPInfo_type_external = WebElement(page, '#PPInfo_type_external .pp-input__inner')

        self.PPInfo_product_group = WebElement(page, '#PPInfo_product_group .pp-input__inner')

        self.PPinfo_fix_HFM = WebElement(page, '#PPinfo_fix_HFM .selectedField')

        self.PPinfo_telecom_sign = WebElement(page, '#PPinfo_telecom_sign .pp-radio-button')

        self.PPInfo_Vitrina = WebElement(page, '#PPInfo_Vitrina .pp-input__inner')

        self.PPInfo_Materiality = WebElement(page, '#PPInfo_Materiality .pp-input__inner')

        self.PPinfo_partner_sign = WebElement(page, '#PPinfo_partner_sign .pp-radio-button')

        self.PPInfo_reason_close = WebElement(page, '#PPInfo_reason_close .pp-input__inner')

        self.PPinfo_product_problem = WebElement(page, '#PPinfo_product_problem .pp-input__inner')

        self.PPInfo_product_vertical = WebElement(page, '#PPInfo_product_vertical .pp-input__inner')

        self.PPinfo_product_service = WebElement(page, '#PPinfo_product_service .pp-radio-button')

        self.PPinfo_product_aim = WebElement(page, '#PPinfo_product_aim .pp-input__inner')

        self.PPInfo_Public_Description = WebElement(page, '#PPInfo_Public_Description .pp-input__inner')

        self.PPInfo_order_contract = WebElement(page, '#PPInfo_order_contract .pp-input__inner')

        self.PPinfo_resolution = WebElement(page, '#PPinfo_resolution .pp-input__inner')

        self.PPinfo_market = WebElement(page, '#PPinfo_market .selectedField')

        self.PPinfo_metrics = WebElement(page, '#PPinfo_metrics .pp-radio-button')

        self.PPinfo_order_link = WebElement(page, '#PPinfo_order_link .pp-input__inner')

        self.PPInfo_product_direction = WebElement(page, '#PPInfo_product_direction .pp-input__inner')

        self.PPinfo_StructuralProductType = WebElement(page, '#PPinfo_StructuralProductType .pp-input__inner')

        self.PPInfo_essense_product = WebElement(page, '#PPInfo_essense_product .pp-input__inner')

        self.PPInfo_tags = WebElement(page, '#PPInfo_tags .pp-input__inner')

        self.PPInfo_type_develop = WebElement(page, '#PPInfo_type_develop .selectedField')

        self.PPinfo_market_sign = WebElement(page, '#PPinfo_market_sign .selectedField')

        self.employee_tribe = WebElement(page, '#employee_tribe .selectedField')

        self.PPInfo_level_QBR = WebElement(page, '#PPInfo_level_QBR .pp-input__inner')

        self.PPinfo_GosSector_ch = WebElement(page, '#PPinfo_GosSector_ch .pp-radio-button')

        self.PPinfo_values = WebElement(page, '#PPinfo_values .pp-input__inner')

        self.PPInfo_cost_center = WebElement(page, '#PPInfo_cost_center .pp-input__inner')

        self.PPinfo_frequency = WebElement(page, '#PPinfo_frequency .pp-radio-button')

        self.PPInfo_employee_plan = WebElement(page, '#PPInfo_employee_plan .pp-input__inner')

        self.PPInfo_employee_fact = WebElement(page, '#PPInfo_employee_fact .pp-input__inner')

        self.PPinfo_expert_estimate_web = WebElement(page, '#PPinfo_expert_estimate_web .pp-input__inner')

        self.PPinfo_expert_estimate_android = WebElement(page, '#PPinfo_expert_estimate_android .pp-input__inner')

        self.PPinfo_expert_estimate_ios = WebElement(page, '#PPinfo_expert_estimate_ios .pp-input__inner')

        self.PPInfo_IsEcosystem = WebElement(page, '#PPInfo_IsEcosystem .pp-radio-button')

        self.PPinfo_EPM = WebElement(page, '#PPinfo_EPM .pp-radio-button')

        self.PPInfo_MPV_product = WebElement(page, '#PPInfo_MPV_product .pp-radio-button')

        # ПОЛЯ В ФОРМАХ РЕДАКТИРОВАНИЯ

        self.name_replace = WebElement(page, '#name')

        self.description_replace = WebElement(page, '#description')

        self.PPinfo_status_replace = WebElement(page, '#PPinfo_status')

        self.employee_business_owner_replace = WebElement(page, '#employee_business_owner')

        self.employee_tech_lead_replace = WebElement(page, '#employee_tech_lead')

        self.employee_chief_PO_replace = WebElement(page, '#employee_chief_PO')

        self.employee_product_owner_replace = WebElement(page, '#employee_product_owner')

        self.PPInfo_qbrmemo_link_replace = WebElement(page, '#PPInfo_qbrmemo_link')

        self.employee_senior_PO_replace = WebElement(page, '#employee_senior_PO')

        self.PPinfo_web_app_replace = WebElement(page, '.attributeTable #gr_PPinfo_web_app .edit')

        self.gr_PPInfo_product_block = WebElement(page, '.attributeTable #gr_PPInfo_product_block .edit')

        self.PPinfo_web_app_field = WebElement(page, '#gr_PPinfo_web_app')

        self.PPinfo_delta_Appstore_replace = WebElement(page, '#PPinfo_delta_Appstore')

        self.PPinfo_GooglePlay_delta_replace = WebElement(page, '#PPinfo_GooglePlay_delta')

        self.PPInfo_activity_oracle_code_replace = WebElement(page, '#PPInfo_activity_oracle_code')

        self.PPInfo_atomic_product_replace = WebElement(page, '#PPInfo_atomic_product .pp-input__inner')

        self.PPInfo_EPP_bm_replace = WebElement(page, '#PPInfo_EPP_bm .pp-input__inner')

        self.PPInfo_business_vertical_replace = WebElement(page, '#PPInfo_business_vertical .pp-input__inner')

        self.PPInfo_product_block_replace = WebElement(page, '#PPInfo_product_block .pp-input__inner')

        self.PPinfo_MTS_Brand_replace = WebElement(page, '#PPinfo_MTS_Brand .pp-radio-button')

        self.PPInfo_order_advertising_replace = WebElement(page, '#PPInfo_order_advertising .pp-input__inner')

        self.PPInfo_ECO_version_And_replace = WebElement(page, '#PPInfo_ECO_version_And .pp-input__inner')

        self.PPInfo_ECO_version_iOS_replace = WebElement(page, '#PPInfo_ECO_version_iOS .pp-input__inner')

        self.employee_sponsor_replace = WebElement(page, '#employee_sponsor .selectedField')

        self.PPInfo_product_com_replace = WebElement(page, '#PPInfo_product_com .pp-input__inner')

        self.PPinfo_close_date_replace = WebElement(page, '#PPinfo_close_date .pp-input__inner')

        self.PPinfo_execution_date_replace = WebElement(page, '#PPinfo_execution_date .pp-input__inner')

        self.PPinfo_start_date_MVP_replace = WebElement(page, '#PPinfo_start_date_MVP .pp-input__inner')

        self.PPinfo_start_close_date_replace = WebElement(page, '#PPinfo_start_close_date .pp-input__inner')

        self.PPinfo_finish_date_MVP_replace = WebElement(page, '#PPinfo_finish_date_MVP .pp-input__inner')

        self.PPInfo_date_In_progress_replace = WebElement(page, '#PPInfo_date_In_progress .pp-input__inner')

        self.PPInfo_date_Idea_formation_replace = WebElement(page, '#PPInfo_date_Idea_formation .pp-input__inner')

        self.PPInfo_dashboard_BFI_replace = WebElement(page, '#PPInfo_dashboard_BFI .pp-input__inner')

        self.PPInfo_detailed_description_replace = WebElement(page, '#PPInfo_detailed_description')

        self.PPInfo_Team_adequacy_replace = WebElement(page, '#PPInfo_Team_adequacy .pp-input__inner')

        self.PPInfo_order_quality_replace = WebElement(page, '#PPInfo_order_quality .pp-input__inner')

        self.PPinfo_start_close_replace = WebElement(page, '#PPinfo_start_close .pp-radio-button')

        self.PPInfo_Eco_Integration_Andr_replace = WebElement(page, '#PPInfo_Eco_Integration_Andr .pp-input__inner')

        self.PPInfo_Eco_Integration_Web_replace = WebElement(page, '#PPInfo_Eco_Integration_Web .pp-input__inner')

        self.PPInfo_Eco_Integration_iOS_replace = WebElement(page, '#PPInfo_Eco_Integration_iOS .pp-input__inner')

        self.PPinfo_EPP_replace = WebElement(page, '#PPinfo_EPP .pp-radio-button')

        self.PPInfo_ois_card_replace = WebElement(page, '#PPInfo_ois_card .pp-input__inner')

        self.PPInfo_card_SOL_replace = WebElement(page, '#PPInfo_card_SOL .pp-input__inner')

        self.PPinfo_category_product_replace = WebElement(page, '#PPinfo_category_product .pp-input__inner')

        self.PPInfo_HFMplanning_desc_replace = WebElement(page, '#PPInfo_HFMplanning_desc .pp-input__inner')

        self.PPInfo_Team_replace = WebElement(page, '#PPInfo_Team .pp-input__inner')

        self.PPInfo_control_DUT_replace = WebElement(page, '#PPInfo_control_DUT .pp-input__inner')

        self.PPinfo_mvp_replace = WebElement(page, '#PPinfo_mvp .pp-input__inner')

        self.PPInfo_external_user_replace = WebElement(page, '#PPInfo_external_user .pp-input__inner')

        self.PPinfo_revenue_replace = WebElement(page, '#PPinfo_revenue .pp-radio-button')

        self.PPinfo_konkurent_replace = WebElement(page, '#PPinfo_konkurent .pp-input__inner')

        self.PPInfo_Monetization_replace = WebElement(page, '#PPInfo_Monetization .pp-input__inner')

        self.PPInfo_business_area_replace = WebElement(page, '#PPInfo_business_area .pp-input__inner')

        self.PPInfo_new_oracle_code_replace = WebElement(page, '#PPInfo_new_oracle_code .pp-input__inner')

        self.PPInfo_main_product_replace = WebElement(page, '#PPInfo_main_product .pp-input__inner')

        self.PPinfo_appstore_rate_replace = WebElement(page, '#PPinfo_appstore_rate .pp-input__inner')

        self.PPinfo_GooglePlay_rate_replace = WebElement(page, '#PPinfo_GooglePlay_rate .pp-input__inner')

        self.PPInfo_type_external_replace = WebElement(page, '#PPInfo_type_external .pp-input__inner')

        self.PPInfo_product_group_replace = WebElement(page, '#PPInfo_product_group .pp-input__inner')

        self.PPinfo_fix_HFM_replace = WebElement(page, '#PPinfo_fix_HFM .pp-radio-button')

        self.PPinfo_telecom_sign_replace = WebElement(page, '#PPinfo_telecom_sign .pp-radio-button')

        self.PPInfo_Vitrina_replace = WebElement(page, '#PPInfo_Vitrina .pp-input__inner')

        self.PPInfo_Materiality_replace = WebElement(page, '#PPInfo_Materiality .pp-input__inner')

        self.PPinfo_partner_sign_replace = WebElement(page, '#PPinfo_partner_sign .pp-radio-button')

        self.PPInfo_reason_close_replace = WebElement(page, '#PPInfo_reason_close .pp-input__inner')

        self.PPinfo_product_problem_replace = WebElement(page, '#PPinfo_product_problem .pp-input__inner')

        self.PPInfo_product_vertical_replace = WebElement(page, '#PPInfo_product_vertical .pp-input__inner')

        self.PPinfo_product_service_replace = WebElement(page, '#PPinfo_product_service .pp-radio-button')

        self.PPinfo_product_aim_replace = WebElement(page, '#PPinfo_product_aim .pp-input__inner')

        self.PPInfo_Public_Description_replace = WebElement(page, '#gr_PPInfo_Public_Description .edit')

        self.PPInfo_order_contract_replace = WebElement(page, '#PPInfo_order_contract .pp-input__inner')

        self.PPinfo_resolution_replace = WebElement(page, '#PPinfo_resolution .pp-input__inner')

        self.PPinfo_market_replace = WebElement(page, '#PPinfo_market .pp-input__inner')

        self.PPinfo_metrics_replace = WebElement(page, '#PPinfo_metrics .pp-radio-button')

        self.PPinfo_order_link_replace = WebElement(page, '#PPinfo_order_link .pp-input__inner')

        self.PPInfo_product_direction_replace = WebElement(page, '#PPInfo_product_direction .pp-input__inner')

        self.PPinfo_StructuralProductType_replace = WebElement(page, '#PPinfo_StructuralProductType .pp-radio-button')

        self.PPInfo_essense_product_replace = WebElement(page, '#PPInfo_essense_product .pp-input__inner')

        self.PPInfo_tags_replace = WebElement(page, '#PPInfo_tags .pp-input__inner')

        self.PPInfo_type_develop_replace = WebElement(page, '#PPInfo_type_develop .pp-radio-button')

        self.PPinfo_market_sign_replace = WebElement(page, '#PPinfo_market_sign .pp-radio-button')

        self.employee_tribe_replace = WebElement(page, '#employee_tribe .selectedField')

        self.PPInfo_level_QBR_replace = WebElement(page, '#PPInfo_level_QBR .pp-input__inner')

        self.PPinfo_GosSector_ch_replace = WebElement(page, '#PPinfo_GosSector_ch .pp-radio-button')

        self.PPinfo_values_replace = WebElement(page, '#PPinfo_values .pp-input__inner')

        self.PPInfo_cost_center_replace = WebElement(page, '#PPInfo_cost_center .pp-input__inner')

        self.PPinfo_frequency_replace = WebElement(page, '#PPinfo_frequency .pp-radio-button')

        self.PPInfo_employee_plan_replace = WebElement(page, '#PPInfo_employee_plan .pp-input__inner')

        self.PPInfo_employee_fact_replace = WebElement(page, '#PPInfo_employee_fact .pp-input__inner')

        self.PPinfo_expert_estimate_web_replace = WebElement(page, '#PPinfo_expert_estimate_web')

        self.PPinfo_expert_estimate_android_replace = WebElement(page, '#PPinfo_expert_estimate_android')

        self.PPinfo_expert_estimate_ios_replace = WebElement(page, '#PPinfo_expert_estimate_ios')

        self.PPInfo_IsEcosystem_replace = WebElement(page, '#PPInfo_IsEcosystem')

        self.PPinfo_EPM_replace = WebElement(page, '#PPinfo_EPM')

        self.PPInfo_MPV_product_replace = WebElement(page, '#PPInfo_MPV_product')
