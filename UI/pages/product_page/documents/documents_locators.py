from UI.base.WebElement import WebElement, ManyWebElements


class DocumentsPageLocators:

    def __init__(self, page):
        # ДОКУМЕНТЫ --------------------------------------------------------------------------------------------------------

        # Таб документов
        self.docs_tab = WebElement(page, "#menu_docs")

        # Хедер документов
        self.docs_header = WebElement(page, "#docs")

        # Текст при отсутствии документов
        self.docs_empty = WebElement(page, "#docs-error")

        # Таблица документов
        self.docs_table = WebElement(page, ".documentsTable")

        # Документы
        self.doc = ManyWebElements(page, ".buttonInner .name")

        # Дата документа
        self.docs_data = WebElement(page, ".docDate")

        # Ссылка на документе
        self.doc_link = WebElement(page, "//*[@class='link matomo_download']")

        # Строка поиска в документе
        self.docs_search = WebElement(page, ".pp-input__inner")

        # Текст при пустом поиске
        self.docs_empty_search = WebElement(page, "#filter-error")

        # Значок лупы в строке поиска
        self.search_icon_docs = WebElement(page, ".prefixIcon")

        # Описание страницы
        self.tab_description = WebElement(page, '.descriptionTab')

        # Кнопка Удалить (корзина) все
        self.delete_doc_many = ManyWebElements(page, "#remove-button")  # Такое есть в add page

        # Кнопка корзины
        self.delete_doc = WebElement(page, '#remove-button')  # Такое есть в add page

        # Подтверждение удаления
        self.delete_confirmation = WebElement(
            page,
            "//button[@class='mts-button mts-button_m']//span[@class='mts-button__inner']")  # Такое есть в add page

        # Кнопка скачивания на странице предпросмотра
        self.download_button_in_preview = WebElement(page, '.wrapper .link')

        # Кнопка закрытия модального окна предпросмотра
        self.close_modal_button = WebElement(page, '.captionModal .closeButton')
