from UI.base.WebElement import WebElement, ManyWebElements


class ExternalProductLocators:

    def __init__(self, page):
        # ТАБЫ -------------------------------------------------------------------------------------------------------------

        # ГРУППЫ ХАРАКТЕРИСТИК -----------------------------

        # Таб Порядок групп
        self.group_order_tab = WebElement(page, '#groupAttribute')

        # Таб Общие
        self.common_tab = WebElement(page, '#groupGeneral')

        # ВНЕШНИЕ ПРОДУКТЫ ---------------------------------

        # Таб действия
        self.actions_tab = WebElement(page, '#linkActionsCommercial')

        # Таб Ключевые свойства внешних продуктов
        self.ext_key_prop_tab = WebElement(page, '#headerCommercial')

        # Таб Ссылки о продукте внешних продуктов
        self.ext_links_about_tab = WebElement(page, '#linkDescriptionCommercial')

        # Таб Полезные ссылки и сервисы внешних продуктов
        self.ext_links_tab = WebElement(page, '#linksCommercial')

        # Таб Руководство внешних продуктов
        self.ext_owners_tab = WebElement(page, '#usersCommercial')

        # Таб Эко модули
        self.eco_modules_tab = WebElement(page, '#commercialEco')

        # ЭЛЕМЕНТЫ АТРИБУТОВ -----------------------------------------------------------------------------------------------

        # Выбранные переключатели
        self.is_checked = ManyWebElements(page, '.is-checked')

        # Draggable элементы
        self.draggables = ManyWebElements(page, '.draggableAttribute .collectionItem')

        # Draggable элементы текст
        self.draggables_text = ManyWebElements(page, '.draggableAttribute .collectionItem span.title')

        # Draggable элементы заголовки
        self.draggable_titles = ManyWebElements(page, '.draggableAttribute .collectionItem .title')
