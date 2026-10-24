from UI.base.WebElement import WebElement, ManyWebElements


class HealthPageLocators:

    def __init__(self, page):
        # Здоровье -----------------------------------------------------------------------------------------------------

        # Таб здоровье
        self.health_tab = WebElement(page, '//*[@id="menu_health"]')

        # Описание раздела здоровье
        self.health_description = WebElement(page,'//*[@id="main"]/div/div[2]/div[2]/div/div[2]/div/div')


        # PQI ----------------------------------------------------------------------------------------------------------

        # Блок PQI
        self.pqi_block = WebElement(page, '(//*[@class="quatityIndicator"])')

        # Блок PQI - заголовок
        self.pqi_block_title = WebElement(page, '(//*[@class="healthCaption"])[1]')

        # Блок PQI - квартал 2
        self.pqi_block_quarter_2 = WebElement(page, '(//*[@class="captionCell"])[1]')

        # Блок PQI - квартал 3
        self.pqi_block_quarter_3 = WebElement(page, '(//*[@class="captionCell"])[2]')

        # Ссылка на PQI - показатель качества
        self.pqi = WebElement(page, '//a[contains(@href, "example.com/product_dashboard")]')


        # NSAT/tNPS ----------------------------------------------------------------------------------------------------

        # Блок NSAT/tNPS
        self.nsat_tnps_block = WebElement(page, '//*[@id="main"]/div/div[2]/div[2]/div/div[3]/div[2]')

        # Блок NSAT/tNPS - заголовок
        self.nsat_tnps_block_title = WebElement(page, '(//*[@class="healthCaption"])[2]')

        # Блок NSAT/tNPS - текст внутри блока
        self.nsat_tnps_block_text = WebElement(page, '(//*[@class="oneCell"])')


        # Класс критичности --------------------------------------------------------------------------------------------

        # Блок Класс критичности
        self.criticality_class_block = WebElement(page, '(//*[@class="criticalityClass"])')

        # Блок Класс критичности - заголовок
        self.criticality_class_block_title = WebElement(page, '(//*[@class="healthCaption"])[3]')

        # Блок Класс критичности - атрибут "Класс критичности"
        self.criticality_class_block_attribute = WebElement(page, '(//*[@class ="captionCell"])[3]')

        # Блок Класс критичности - значение "Класс критичности"
        self.criticality_class_block_value = WebElement(page, '(//*[@class ="valueCell"])[1]')

        # Блок Класс критичности - Дата прохождения
        self.criticality_class_block_date = WebElement(page, '(//*[@class="captionCell"])[4]')

        # Чипсик "Класс критичности систем не соответствует классу продукта"
        self.criticality_class_chip = WebElement(page, '(//*[@class="criticalityClassNotMatch"])')

        # Чипсик "Класс критичности систем соответствует классу продукта"
        self.criticality_class_chip_match = WebElement(page, '(//*[@class="match"])')

        # Иконка подсказки для чипсика "Класс критичности систем соответствует классу продукта"
        self.criticality_class_suggestion_icon = WebElement(page, '(//*[@class="ppTooltip"])[19]')

        # Текст из подсказки
        self.criticality_class_suggestion_text = WebElement(page, '(//*[@class="tooltipContentMatch"])')


        # Технологическая зрелость -------------------------------------------------------------------------------------

        # Блок Технологическая зрелость
        self.technology_maturity_block = WebElement(page, '(//*[@class="technologicalMaturity"])')

        # Блок Технологическая зрелость - заголовок
        self.technology_maturity_block_title = WebElement(page, '(//*[@class="healthCaption"])[4]')

        # Блок Технологическая зрелость - Индекс
        self.technology_maturity_block_index = WebElement(page, '(//*[@class="captionCell"])[5]')

        # Блок Технологическая зрелость - Дата оценки
        self.technology_maturity_block_date = WebElement(page, '(//*[@class="captionCell"])[6]')

        # Ссылка на тех. зрелость (selfe)
        self.tech_maturity = WebElement(page, '//a[contains(text(), "Технологическая зрелость")]')


        # Свойства продукта --------------------------------------------------------------------------------------------

        # Показать все свйоства продукта
        self.show_all_properties = WebElement(page, '(//*[@class="link"])[12]')

        # Класс критичности
        self.criticality_class = WebElement(page, '(//*[@class ="description"])[102]')

        # Класс криичности ИС
        self.criticality_class_is = WebElement(page, '(//*[@class ="description"])[103]')

