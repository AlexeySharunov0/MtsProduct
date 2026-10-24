import logging

import allure
from playwright.sync_api import Page

from UI.base.WebPage import WebPage
from UI.pages.product_page.product_guide.pg_locators import ProductGuidePageLocators

logger = logging.getLogger(__name__)


class PGPage(WebPage, ProductGuidePageLocators):
    def __init__(self, page: Page, url: str = None):
        WebPage.__init__(self, page)  # Явный вызов инициализатора WebPage
        ProductGuidePageLocators.__init__(self, page)  # Явный вызов инициализатора CanvasPageLocators
        self._page = page

        self.base_url = url if url else 'https://stage.prodboard.example.com/product/BI_60/guide'
        self.get_page(self.base_url)

    @allure.step("Выбор фильтра")
    def choice_filter(self, query: str):

        self.filters_btn.click()
        self.filters_dropdown.click()
        for fil in self.filters_in_dropdown_filters:
            if fil.get_text().strip() == query:
                fil.click()
                self.filters_dropdown.click()
                self.filters_apply_btn.click()
                break

    @allure.step("Поиск чипсов в основных шагах по query")
    def find_cheeps_in_step(self, query: str) -> bool:
        """
        Пробегаемся по всем основным шагам и смотрим все чипсы, хотя бы один чипс у каждого шага должен соответствовать query
        Args:
            query: Обязательный, повторяемый, для ПО, для СТС, только кодами
        Returns:
            Если найдено, то True, иначе False
        """
        result = None
        for chip in self.cheeps_in_step:
            result = any(elem.get_attribute('class').split()[-1] == query for elem in
                         chip.get_children('chipPg'))

        return result

    @allure.step("Поиск чипсов в подшагах по query")
    def find_cheeps_in_substep(self, query: str) -> None:
        """
         Пробегаемся по всем подшагам и смотрим все чипсы, хотя бы один чипс у каждого шага должен соответствовать query
        Args:
            query:  Обязательный, повторяемый, для ПО, для СТС, только кодами
        """
        for chip in self.cheeps_in_substep:
            assert any(elem.get_attribute('class').split()[-1] == query for elem in
                       chip.get_children('chipPg')), 'Шаги не отфильтрованы'

    @allure.step("Ищем чипс в шагах и подшагах")
    def assert_chips(self, query: str) -> bool:
        """
        Пробегаемся по всем основным шагам и смотрим все чипсы, ищем хотя бы один чипс соответствующий критериям, если его нет то пробегаем по всем подшагам, так же еще хотя бы одни шаг тс чипсом по критериям, если ничего не найдено, то False
        Args:
            query: Обязательный, повторяемый, для ПО, для СТС, только кодами
        Returns:
            Если найдено, то True, иначе False
        """

        result = True

        for step in self.steps_pg:
            for chip in step.get_children('badges'):
                chips_names = [elem.get_attribute('class').split()[-1] for elem in chip.get_children('chipPg')]
                if query in chips_names:
                    break
            else:
                for elem in step.get_children('subSteps'):
                    for sub_step in elem.get_children('subStepName'):
                        if sub_step.get_children('chipPg', timeout=500):

                            chips_names = [chip.get_attribute('class').split()[-1] for chip in
                                           sub_step.get_children('chipPg')]
                            print(chips_names)
                            if query.split()[-1] not in chips_names:
                                result = False

        return result
