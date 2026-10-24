from UI.base.WebElement import WebElement, ManyWebElements


class DependencyLocators:

    def __init__(self, page):
        # ДЕМО -------------------------------------------------------------------------------------------------------------

        # Таб Зависмости
        self.dependency_tab = WebElement(page, "#menu_dependencies")

        # Кнопка "Связаться с командой"
        self.contact_the_team = WebElement(page, "#callToAction .link")

        # Кнопка "Создать зависмость"
        self.create_a_dependency = WebElement(page, "#create_dependecy_link")
