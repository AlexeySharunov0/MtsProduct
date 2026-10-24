import allure
import pytest

from UI.tests.settingsPage.conftest import edit_page


@allure.feature("Настройки")
@allure.feature("Нотификации")
@pytest.mark.ui
class TestEditSettings:

    @allure.title(f"Настройки добавления и изменения")
    @allure.story(f"Я, как администратор, хочу управлять группой опрос через настройки")
    def test_sostav_opros(self, edit_page):
        edit_page.opros_sostav_tab.click()
        assert 'activeItem' in edit_page.opros_sostav_tab.get_attribute('class')

    @allure.title(f"Настройки добавления и изменения")
    @allure.story(f"Я, как администратор, хочу управлять составом группы опрос и нотификациями через настройки")
    def test_ext_opros(self, edit_page):
        edit_page.opros_external_products_tab.click()
        assert 'activeItem' in edit_page.opros_external_products_tab.get_attribute('class')

    @allure.title(f"Настройки добавления и изменения")
    @allure.story(f"Я, как администратор, хочу управлять составом группы опрос и нотификациями через настройки")
    def test_inner_opros(self, edit_page):
        """ Активный таб внутренние опрос"""

        edit_page.opros_internal_products_tab.click()
        assert 'activeItem' in edit_page.opros_internal_products_tab.get_attribute('class')

    @allure.title(f"Настройки добавления и изменения")
    @allure.story(f"Я, как администратор, хочу управлять составом группы опрос и нотификациями через настройки")
    def test_noti_po(self, edit_page):
        """ Информирование о добавлении продукта - о создании для руководства - активный таб"""

        edit_page.create_notification_po_tab.click()
        assert 'activeItem' in edit_page.create_notification_po_tab.get_attribute('class')

    @allure.title(f"Настройки добавления и изменения")
    @allure.story(f"Я, как администратор, хочу управлять составом группы опрос и нотификациями через настройки")
    def test_noti_ext(self, edit_page):
        """ Информирование о добавлении продукта - внешние - активный таб"""
        edit_page.create_external_tab.click()
        assert 'activeItem' in edit_page.create_external_tab.get_attribute('class')

    @allure.title(f"Настройки добавления и изменения")
    @allure.story(f"Я, как администратор, хочу управлять составом группы опрос и нотификациями через настройки")
    def test_noti_inner(self, edit_page):
        """ Информирование о добавлении продукта - внутренние - активный таб"""
        edit_page.create_intenal_tab.click()
        assert 'activeItem' in edit_page.create_intenal_tab.get_attribute('class')

    @allure.title(f"Настройки добавления и изменения")
    @allure.story(f"Я, как администратор, хочу управлять составом группы опрос и нотификациями через настройки")
    def test_noti_closed_product_tab(self, edit_page):
        """ Информирование о редактировании продукта - инициировано закрытие - активный таб"""
        edit_page.closed_product_tab.click()
        assert 'activeItem' in edit_page.closed_product_tab.get_attribute('class')

    @allure.title(f"Настройки добавления и изменения")
    @allure.story(f"Я, как администратор, хочу управлять составом группы опрос и нотификациями через настройки")
    def test_noti_closed_cpo_tab(self, edit_page):
        """ Информирование о редактировании продукта - CPO - активный таб"""

        edit_page.closed_cpo_tab.click()
        assert 'activeItem' in edit_page.closed_cpo_tab.get_attribute('class')

    @allure.title(f"Настройки добавления и изменения")
    @allure.story(f"Я, как администратор, хочу управлять составом группы опрос и нотификациями через настройки")
    def test_noti_closed_po_tab(self, edit_page):
        """ Информирование о редактировании продукта - PO - активный таб"""
        edit_page.closed_po_tab.click()
        assert 'activeItem' in edit_page.closed_po_tab.get_attribute('class')
