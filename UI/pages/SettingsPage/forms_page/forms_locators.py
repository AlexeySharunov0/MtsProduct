from UI.base.WebElement import WebElement


class FormsLocators:

    def __init__(self, page):
        # Поля для администраторов. Внешние
        self.external_admin = WebElement(page, '#optionalAdminCommercialColumn')

        # Поля для администраторов. Внутренние
        self.internal_admin = WebElement(page, '#optionalAdminInternalColumn')

        # Обязательные поля для пользователя. Внешние
        self.required_external_user = WebElement(page, '#requiredUserCommercialColumn')

        # Обязательные поля для пользователя. Внутренние
        self.required_internal_user = WebElement(page, '#requiredUserInternalColumn')

        # Необязательные поля для пользователя. Внешние
        self.optional_external_user = WebElement(page, '#optionalUserCommercialColumn')

        # Необязательные поля для пользователя. Внутренние
        self.optional_internal_user = WebElement(page, '#optionalUserInternalColumn')

        # Колонки тоглов атрибутов
        self.columns_attributes = WebElement(page, '.columns')
