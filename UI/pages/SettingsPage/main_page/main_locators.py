from UI.base.WebElement import WebElement, ManyWebElements


class MainLocators:

    def __init__(self, page):
        # ТАБЫ -------------------------------------------------------------------------------------------------------------

        # Таб "Карточка продукта"
        self.card_tab = WebElement(page, '#chips')

        # Таб "Категории внешних продуктов"
        self.categories_tab = WebElement(page, '#commercialCategory')

        # Таб "Статусы" внешние
        self.statuses_tab = WebElement(page, '#StatusBar')

        # Таб "Статусы" внутренние
        self.statuses_tab_int = WebElement(page, '#internalStatus')

        # Таб "Столбцы excel" внешние
        self.excel_tab = WebElement(page, '#includeIntoXlsxReport')

        # Таб "Столбцы excel" внутренние
        self.excel_tab_int = WebElement(page, '#internalExcel')

        # Выбранные переключатели
        self.is_checked = ManyWebElements(page, '.is-checked')

        # Таб фильтры - пункт внешние
        self.vneshii_filters = WebElement(page, '#mainFilter')

        # Таб фильтры - пункт внутренние
        self.vnutrennii_filters = WebElement(page, '#mainFilter')

        # Таб фильтры - пункт архивные
        self.archival_filters = WebElement(page, '#mainFilter')

        # АТРИБУТЫ ---------------------------------------------------------------------------------------------------------

        # Draggable элементы
        self.draggables = ManyWebElements(page, '.draggableAttribute .collectionItem .title')
        self.draggable_titles = ManyWebElements(page, '.draggableAttribute .collectionItem .title')
