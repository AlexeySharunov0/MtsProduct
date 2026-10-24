from UI.base.WebElement import WebElement, ManyWebElements


class ProductGuidePageLocators:

    def __init__(self, page):
        # PRODUCT GUIDE -------------------------------------------------------------------------------------------------

        # Таб Product Guide
        self.product_guide_tab = WebElement(page, "#menu_guide")

        # Чипс NEW у Product Guide
        self.new_chips = WebElement(page, ".newMenuItem")

        # Хедер продукт гайда
        self.product_guide_header = WebElement(page, "#productGuide")

        # Строка поиска в продукт гайде
        self.product_guide_search_line = WebElement(page, "//*[@placeholder='Название или описание шага']")

        # Крестик в строке поиска продукт гайда
        self.pg_search_cross = WebElement(page, ".pp-input .close")

        # Сообщение о том, что ничего не найдено
        self.pg_search_error = WebElement(page, ".searchMessage")

        # Вкладки групп в режиме схемы
        self.product_guide_groups_schemes = ManyWebElements(page, ".columnHeader")

        # Вкладки групп в режиме списка
        self.product_guide_groups_list = ManyWebElements(page, ".groupTabs .pp-tab")

        # Каунтеры групп
        self.product_guide_group_counters = ManyWebElements(page, ".tabWrapper .count")

        # Шаги PG
        self.steps_pg = ManyWebElements(page, ".step")

        # Описание страницы
        self.tab_description = WebElement(page, '.descriptionTab')

        # Каунтеры шагов
        self.step_counters = ManyWebElements(page, ".serialNumber")

        # Плашка Обязательный
        self.step_required_chips = ManyWebElements(page, ".required")

        # Имя шага
        self.step_name = ManyWebElements(page, ".nameAndRequired .name")

        # Описание шага
        self.step_description = ManyWebElements(page, ".content .description")

        # Блок ссылок
        self.step_link_block = WebElement(page, ".links")

        # Ссылки в шаге
        self.step_links = ManyWebElements(page, "//*[@class='links']/span/a")

        # Блок сотрудников
        self.step_employee_block = WebElement(page, ".employees")

        # Сотрудники в шаге
        self.step_employees = ManyWebElements(page, ".employee")

        # Блок файлов
        self.step_files_block = WebElement(page, ".files")

        # Файлы в шаге
        self.step_files = ManyWebElements(page, ".link")

        # Шаги не добавлены
        self.pg_error = WebElement(page, "//*[text()=' Шаги пока не добавлены ']")

        # Редиректы в поиске
        self.search_redirect_links = ManyWebElements(page, ".redirectMessage .link")

        # Чипс обязательность у вложенного шага
        self.required_cheeps_in_internal_step = WebElement(page, ".subStep .required")

        # Чипс повторяемости у вложенного шага
        self.repeatable_cheeps_in_internal_step = WebElement(page, ".subStep .repeatable")

        # Чипсы на шаге
        self.cheeps_in_step = ManyWebElements(page, ".step .badges")

        # Чипсы на подшаге
        self.cheeps_in_substep = ManyWebElements(page, ".subStepName")

        # Фильтр Обязательные
        self.required_filter = WebElement(page, "#filter_required")

        # Фильтр Повторяемые
        self.repeatable_filter = WebElement(page, "#filter_repeatable")

        # Фильтр PO
        self.po_filter = WebElement(page, "#filter_po")

        # Фильтр Тех лид
        self.techlead_filter = WebElement(page, "#filter_techlead")

        # Режимы отображения
        self.display_mode = ManyWebElements(page, '.headerRow .pp-tab')  # 1 - схема, 2 - список

        # Кнопка фильтров
        self.filters_btn = WebElement(page, ".headerRow .ppDropdown")

        # Выпадашка выборов фильтров
        self.filters_dropdown = WebElement(page, ".attributesField .selectedField")

        # Фильтры в выпадашке
        self.filters_in_dropdown_filters = ManyWebElements(page, ".foundItemsName")

        # Кнопка Применить
        self.filters_apply_btn = WebElement(page, ".buttons .mts-button")

        # Карточка сотрудника
        self.user_card = WebElement(page, '.userCard')

        # Название столбца в режиме схемы
        self.column_name_in_scheme_mode = ManyWebElements(page, ".columnHeader .name")

        # Каунтеры столбца в режиме схемы
        self.column_counter_in_scheme_mode = ManyWebElements(page, ".columnHeader .count")

        # Всплывающее окно шага
        self.side_window_in_scheme_mode = WebElement(page, ".sideWindow")

        # Список подшагов
        self.substep_list = WebElement(page, ".substepsList")

        # Подшаги в списке подшагов
        self.steps_in_substep_list = ManyWebElements(page, ".substepsList .step")

        # Схема шагов
        self.schema = WebElement(page, ".schema")

        # Тогл вложенных шагов
        self.toggle_substeps = WebElement(page, ".toggleSubsteps")

        # Кнопка в шаге
        self.action_button = WebElement(page, '.actionButton')

