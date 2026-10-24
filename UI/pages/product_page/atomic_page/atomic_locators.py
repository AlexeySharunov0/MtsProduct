from UI.base.WebElement import WebElement


class AtomicPageLocators:

    def __init__(self, page):
        # АТОМАРНЫЕ ПРОДУКТЫ -----------------------------------------------------------------------------------------------

        # Таб атомарных продуктов
        self.atomic_tab = WebElement(page, '#menu_atomic')

        # Заголовок в атомарных продуктах
        self.atomic_header = WebElement(page, '#atomic')

        # Описание раздела в атомарных продуктах
        self.atomic_description = WebElement(page, '.descriptionTab')

        # Первый по счету атомарный продукт
        self.first_atomic_product = WebElement(page, '.atomicHeader .header')

        # Первое по счету описание продукта
        self.first_atomic_description = WebElement(page, '.content .description')

        # Первая по счету надпись Product Owner
        self.first_atomic_job_title = WebElement(page, '.jobAndName .jobTitle')

        # Первое по счету имя руководителя
        self.first_atomic_job_name = WebElement(page, '.jobAndName .link')

        # Первое по счету фото руководителя
        self.first_atomic_job_photo = WebElement(page, '.avatarAndName .avatarImage')

        # Первая по счету иконка статуса
        self.first_atomic_status_icon = WebElement(page, '.status')

        # Блок архивные на странице атомарных
        self.atomic_archive_block = WebElement(page, '.archive')

        # Заголовок Архивные на странице атомарных
        self.atomic_archive_header = WebElement(page, '.caption.medium.withPadding')

        # Руководитель центра в атомарном продукте
        self.owner_atomic = WebElement(page, '.avatarAndName')

        # Текст при отсутствии атомарных продуктов
        self.atomic_none = WebElement(page, '#atomicError')
