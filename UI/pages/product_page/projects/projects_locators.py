from UI.base.WebElement import WebElement


class ProjectsPageLocators:

    def __init__(self, page):
        # ПРОЕКТЫ ----------------------------------------------------------------------------------------------------------

        # DaVinci запустить легкий старт
        self.davinci_easy_start_button = WebElement(page, "//*[text() = 'Запустить лёгкий старт ']/../..")

        # DaVinci Начать защиту инвестиций по продукту
        self.davinci_protect_investments = WebElement(page,
                                                      "//*[text() = 'Начать защиту инвестиций по продукту ']/../..")

        # RMS Создать проект
        self.rms_create_project = WebElement(page, "//*[text() = 'Создать проект ']/../..")

        # Таб проектов
        self.project_tab = WebElement(page, "#menu_projects")

        # Хедер проектов
        self.project_header = WebElement(page, "#projects .caption.large.withPadding")

        # Таб Хайпиреон на табе проекты
        self.hyperion_tab_project_tab = WebElement(page, "//*[text() = 'Hyperion']")

        # Таб Давинчи на табе проекты
        self.davinci_tab_project_tab = WebElement(page, "//*[text() = 'DaVinci']")

        # Таб RMS на табе проекты
        self.rms_tab_project_tab = WebElement(page, "//*[text() = 'RMS']")

        # Таб OEBS на табе проекты
        self.oebs_tab_project_tab = WebElement(page, "//*[text() = ' OEBS.Активы ']")

        # Таблица проектов Hyperion
        self.table_hype = WebElement(page, "#projects-hyperion-full .projectsTable")

        # Таблица проектов Davinci
        self.davinci_table = WebElement(page, "#projects-davinci-full .projectsTable")

        # Таблица проектов RMS
        self.table_rms = WebElement(page, "#projects-rms-full .projectsTable")

        # Таблица проектов OEBS
        self.table_oebs = WebElement(page, "#projects-oebs-full .projectsTable")

        # Строка поиска на странице проектов Hyperion
        self.search_projects_hyperion = WebElement(page, "#projects-hyperion-search .pp-input__inner")

        # Строка поиска на странице проектов RMS
        self.search_projects_rms = WebElement(page, "#projects-rms-search .pp-input__inner")

        # Строка поиска на странице проектов DaVinci
        self.search_projects_davinci = WebElement(page, "#projects-davinci-search .pp-input__inner")

        # Проект MVP_Гео-онлайн триггеры на фемтосотах для МТС Маркетолог
        self.project_first = WebElement(page,
                                        "//*[text() = 'MVP_Гео-онлайн триггеры на фемтосотах для МТС Маркетолог']")

        # Проект Инжектор МТС
        self.project_inzhector = WebElement(page, "//*[text() = 'Инжектор МТС']")

        # Проект новый проект
        self.project_new_project = WebElement(page, "//*[text() = 'новый проект']")

        # Проект R04933
        self.project_R04933 = WebElement(page, "//*[text() = 'R04933_SWAP_MTS_Communicator']")

        # Проект R05037
        self.project_R05037 = WebElement(page, "//*[text() = 'R05037_CAPEX_MTS Marketolog from 10.01.2022']")

        # Описание страницы
        self.tab_description = WebElement(page, '.descriptionTab')
