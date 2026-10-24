from UI.base.WebElement import WebElement


class ServiceAndCapabilitiesPageLocators:

    def __init__(self, page):
        # СЕРВИСЫ И КАПАБИЛИТИ -------------------------------------------------------------------------------------------

        # Таб сервисов и капабилити
        self.services_tab = WebElement(page, '#menu_services')

        # Сервисы
        self.services = WebElement(page, "//*[text() = 'Сервисы ']")

        # Капабилити
        self.capabilities = WebElement(page, "//*[text() = 'Капабилити ']")

        # Текст при отсутствии сервисов
        self.no_text = WebElement(page, '.noServives')
