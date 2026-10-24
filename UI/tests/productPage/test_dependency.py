import allure
import pytest

from UI.data.assertions_data import ProductsAsserts as assertions
from UI.tests.productPage.conftest import dependency_page


@pytest.mark.ui
@allure.feature("Вкладка Зависмости")
@allure.issue('https://jira.mts.ru/browse/PPI-4123', 'PPInfo - Отображение и создание зависимостей на продукте')
class TestDependency:

    @allure.title("Если не установлен основной проект, то вкладка зависмостей не отображается")
    def test_if_not_set_project_main(self, dependency_page):

        dependency_page.get_page('https://stage.prodboard.mts.ru/product/BI_0/dependencies')
        assert dependency_page.dependency_tab.get_attribute('class') == 'content empty', 'Вкладка отображены черный текстом, хотя основной проект не установлен'

        assert dependency_page.contact_the_team.is_clickable(), 'Нет кнопки Связаться с командой или она некликабельна'

    @allure.title("Если установлен основной проект, то вкладка зависмостей активна")
    def test_dependency_tab_active(self, dependency_page):
        assert dependency_page.dependency_tab.get_attribute(
            'class') == 'content', 'Вкладка отображены черный текстом, хотя основной проект не установлен'

        assert dependency_page.contact_the_team.is_not_visible(), 'Кнопка Связаться с командой видима'

    @allure.title("Корректная ссылка у кнопки Создать зависмость")
    def test_create_dependency_button(self, dependency_page):
        dependency_page.wait_force(1)
        assert dependency_page.create_a_dependency.get_attribute('href') == 'https://jira.mts.ru/secure/CreateIssueDetails!init.jspa?pid=19606&issuetype=11304&customfield_19514=29457', 'Ссылка некорректна'




