from UI.base.WebElement import WebElement, ManyWebElements


class EditLocators:

    def __init__(self, page):
        # ДОБАВЛЕНИЕ В ГРУППУ ОПРОС ----------------------------------------------------------------------------------------

        # Кнопка "Добавить сотрудника" в группу опрос
        self.add_user_in_opros = WebElement(page, '.buttons .mts-button')

        # Строка для ввода данных юзера для добавления в группу опрос
        self.add_user_input = WebElement(page, '.mts-input__inner')

        # Кнопка "Найти сотрудника"
        self.find_user_button = WebElement(page, '.background .mts-button__inner')

        # Кнопка "Добавить в группу" когда пользователь уже найден
        self.add_ingroup_button = WebElement(page, '.background .remove-button')

        # Юзеры, состоящие в группе опрос
        self.opros_users = ManyWebElements(page, '.employee .fullName')

        # ТАБЫ -------------------------------------------------------------------------------------------------------------

        # Таб "Состав" для настройки нотификаций для группы опрос
        self.opros_sostav_tab = WebElement(page, '#PoolSender')

        # Таб "Внешние продукты"
        self.opros_external_products_tab = WebElement(page, '#groupOPROSCommercial')

        # Таб "Внутренние продукты"
        self.opros_internal_products_tab = WebElement(page, '#groupOPROSInternal')

        # Таб "Уведомления о создании для руководства"
        self.create_notification_po_tab = WebElement(page, '#CreateProductOwner')

        # Таб "Внешние продукты"
        self.create_external_tab = WebElement(page, '#CreateProductCommercial')

        # Таб "Внутренние продукты"
        self.create_intenal_tab = WebElement(page, '#CreateProductInternal')

        # Таб "Инициировано закрытие"
        self.closed_product_tab = WebElement(page, '#closeProductCommercial')

        # Таб "CPO"
        self.closed_cpo_tab = WebElement(page, '#cpoSender')

        # Таб "PO"
        self.closed_po_tab = WebElement(page, '#poSender')

        # ЭЛЕМЕНТЫ АТРИБУТОВ -----------------------------------------------------------------------------------------------

        # Таб "Внешние продукты"
        self.required_external_tab = WebElement(page, '#requiredCommercialColumn')

        # Таб "Внутренние продукты"
        self.required_internal_tab = WebElement(page, '#requiredInternalColumn')

        # Выбранные переключатели
        self.is_checked = ManyWebElements(page, '.is-checked')
