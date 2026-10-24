from UI.base.WebElement import WebElement, ManyWebElements


class EcoModulesPageLocators:

    def __init__(self, page):
        # ЭКОСИСТЕМНЫЕ МОДУЛИ ----------------------------------------------------------------------------------------------

        # Таб экосистемных модулей / Продуктов ЕПМ
        self.eco_tab = WebElement(page, '#menu_eco')

        # Хедер на странице экосистемных модулей
        self.eco_header = WebElement(page, '#eco')

        # Хедер ЭПМ
        self.epm_header = WebElement(page, "//*[@id='eco' and text() = 'Продукты с ЭПМ ']")

        # Описание ЭПМ
        self.epm_description = WebElement(page, '#epm-description')

        # Таблица экосистемных модулей
        self.eco_table = WebElement(page, '.tableWithIndicators')

        # Ссылки на продукты в эко модулях
        self.eco_prod_links = ManyWebElements(page, '.inlineBlock .link')

        # Ячейки в таблице Экосистемных модулей
        self.eco_cells = ManyWebElements(page, '.inte')

        # Текст при отсутствии экосистемных связей
        self.eco_error = WebElement(page,
                                    "//*[text() = ' Интеграция с Экосистемными продуктовыми модулями отсутствует ']")

        # Описание страницы
        self.tab_description = WebElement(page, '.descriptionTab')
