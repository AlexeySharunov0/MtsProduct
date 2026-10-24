from UI.base.WebElement import WebElement


class MetricsPageLocators:

    def __init__(self, page):
        # МЕТРИКИ ----------------------------------------------------------------------------------------------------------

        # Таб метрик
        self.metrics_tab = WebElement(page, '#menu_metrics')

        # Заголовок на странице Метрики
        self.metrics_header = WebElement(page, '#metrics')

        # Кнопка "Запросить доступ" на странице метрик
        self.get_access_button_metrics = WebElement(page, '.linkLimit')

        # Анимация загрузки iframe на странице метрик
        self.metrics_iframe = WebElement(page, '.greenPlumContent')

        # Текст при отсутствии метрик у продукта на станице метрик
        self.metrics_iframe_none = WebElement(page, '.typeReport')

        # Другие витрины
        self.metrics_other_showcase = WebElement(page, '.content .productLinksAndServices')

        # Первая ссылка в Другие витрины
        self.metrics_other_showcase_first_link = WebElement(page, '#Vychisliaemaia_ssylka')

        # Вторая ссылка в Другие витрины
        self.metrics_other_showcase_second_link = WebElement(page, '#Vych_ssylka_4')

        # Описание страницы
        self.tab_description = WebElement(page, '.descriptionTab')
