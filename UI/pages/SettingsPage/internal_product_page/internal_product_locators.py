from UI.base.WebElement import WebElement, ManyWebElements


class InternalProductLocators:

    def __init__(self, page):
        # ГРУППЫ ХАРАКТЕРИСТИК -----------------------------

        # Таб Порядок групп
        self.group_order_tab = WebElement(page, '#groupAttributeInternal')

        # Таб Общие
        self.common_tab = WebElement(page, '#cce0c5f8-8004-4d96-8987-fc52ddc178c3')

        # ВНУТРЕННИЕ ПРОДУКТЫ -------------------------------

        # Таб действия
        self.int_actions_tab = WebElement(page, '#linkActionsInternal')

        # Таб Ключевые свойства внутренних продуктов
        self.int_key_prop_tab = WebElement(page, '#headerInternal')

        # Таб Ссылки о продукте внутренних продуктов
        self.int_links_about_tab = WebElement(page, '#linkDescriptionInternal')

        # Таб Ссылки внутренних продуктов
        self.int_links_tab = WebElement(page, '#linksInternal')

        # Таб Руководство внутренних продуктов
        self.int_owners_tab = WebElement(page, '#usersInternal')

        # ЭЛЕМЕНТЫ АТРИБУТОВ -----------------------------------------------------------------------------------------------

        # Выбранные переключатели
        self.is_checked = ManyWebElements(page, '.is-checked')

        # Draggable элементы
        self.draggables = ManyWebElements(page, '.draggableAttribute .collectionItem')

        # Draggable элементы текст
        self.draggables_text = ManyWebElements(page, '.draggableAttribute .collectionItem span.title')

        # Draggable элементы заголовки
        self.draggable_titles = ManyWebElements(page, '.draggableAttribute .collectionItem span.title')
