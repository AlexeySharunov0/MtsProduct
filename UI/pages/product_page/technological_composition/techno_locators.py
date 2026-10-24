from UI.base.WebElement import WebElement, ManyWebElements


class TechnoPageLocators:

    def __init__(self, page):
        # ТЕХНИЧЕСКИЙ СОСТАВ -------------------------------------------------------------------------------------------

        # Добавить приложение в ArchOps
        self.archops_add = WebElement(page, "//*[text() = 'Добавить приложение в Archops ']/../..")

        # Создать систему в IMS
        self.ims_create_system = WebElement(page, "//*[text() = 'Создать систему в IMS ']/../..")

        # Таб ПО
        self.software_tab = WebElement(page, "#menu_software")

        # Хедер ПО
        self.software_header = WebElement(page, "#software")

        # Стрелочки открытия Программного обеспечения
        self.software_opening = ManyWebElements(page, ".marker")

        # Содержание Техно продукта
        self.software_info_inside = WebElement(page, ".simple")

        # Описание пустого продукта
        self.software_empty_product = WebElement(page, ".description")

        # Чипс Тип разработки
        self.software_development_type = WebElement(page, ".development")

        # Текст при отсутствии технологических продуктов
        self.techno_none = WebElement(page, ".soft")

        # Кнопка изменить связи
        self.change_links_button = WebElement(page, ".notes")

        # Блок Руководство в Технический состав
        self.software_people = WebElement(page, ".management")

        # Блок Контент в Техническом составе
        self.software_content = WebElement(page, ".content")

        # Технический лидер технологических продуктов
        self.techno_lead = WebElement(page, ".owner .link")

        # Столбец класса критичности
        self.cc_column = WebElement(page, ".criticalClass")

        # Значение в столбце класса критичности
        self.cc_column_value = WebElement(page, ".criticalClass .content_is")

        # Столбец ИС
        self.inf_system_column = WebElement(page, ".lineName")

        # Столбец Статус
        self.status_column = WebElement(page, ".status")

        # Столбец Команда поддержки
        self.team_column = WebElement(page, ".team")

        # Чипсы основного ПО
        self.main_po = WebElement(page, "//*[text() = ' Основное ']")

        # Описание страницы
        self.tab_description = WebElement(page, '.descriptionTab')

        # Кнопка Тех учетки
        self.tech_users_button = ManyWebElements(page, ".imsButton .linkButton")
