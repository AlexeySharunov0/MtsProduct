import allure
import pytest

from UI.data.assertions_data import ProductsAsserts as assertions
from UI.tests.productPage.conftest import atomic_page, product_page


@pytest.mark.ui
@allure.feature("Вкладка Атомарные продукты")
class TestAtomic:
    @allure.title("Проверка кликабельности и отображения таба Атомарные продукты у продуктов с атомарным")
    @pytest.mark.parametrize("atomic_page", assertions.linkToProductsWithAtomic, indirect=True)
    def test_atomic_tab_check_with_atomic(self, atomic_page):
        with allure.step("Проверяем, что таб есть в боковом меню"):
            assert atomic_page.atomic_tab.is_visible(), 'Таба нет в меню'
        with allure.step('Проверяем, что таб Атомарные кликабельный'):
            assert atomic_page.atomic_tab.is_clickable(), 'Таб некликабельный'
        with allure.step("Проверяем, что таб отмечен как активный (черный)"):
            assert atomic_page.atomic_tab.get_attribute('class') == 'content', 'Таб окрашен серым'

    @allure.title("Проверка кликабельности и отображения таба Атомарные продукты у продуктов без атомарных")
    @pytest.mark.parametrize("atomic_page", assertions.linkToProductsWithNoAtomic, indirect=True)
    def test_atomic_tab_check_no_atomic(self, atomic_page):
        with allure.step("Проверяем, что таб есть в боковом меню"):
            assert atomic_page.atomic_tab.is_visible(), 'Таба нет в меню'
        with allure.step('Проверяем, что таб Атомарные кликабельный'):
            assert atomic_page.atomic_tab.is_clickable(), 'Таб некликабельный'
        with allure.step("Проверяем, что таб отмечен как активный (черный)"):
            assert atomic_page.atomic_tab.get_attribute('class') == 'content empty', 'Таб окрашен черным'

    @allure.title("Проверка отсутствия таба Атомарные продукты у атомарных продуктов")
    @pytest.mark.parametrize("product_page", assertions.linkToAtomicProduct, indirect=True)
    def test_atomic_tab_check_atomic(self, product_page):
        with allure.step("Проверяем, что таба нет в боковом меню"):
            assert product_page.atomic_tab.is_not_visible(), 'Таба есть в меню'

    @allure.title("Проверка заголовков на странице атомарных")
    @pytest.mark.parametrize("atomic_page", assertions.linkToDifferentAtomic, indirect=True)
    def test_check_atomic_headers(self, atomic_page):
        with allure.step("Проверяем, что заголовок страницы отображается корректно"):
            assert atomic_page.atomic_header.is_visible(), 'Заголовка нет'
            assert atomic_page.atomic_header.get_text() == 'Атомарные продукты', 'Текст заголовка не совпадает'
        with allure.step("Проверяем, что описание страницы отображается корректно"):
            assert atomic_page.atomic_description.is_visible(), 'Описания нет'
            assert atomic_page.atomic_description.get_text() == assertions.atomic_description, 'Текст описания не совпадает'

    @allure.title("Проверка текста при отсутствии атомарных продуктов")
    @pytest.mark.parametrize("atomic_page", assertions.linkToProductsWithNoAtomic, indirect=True)
    def test_check_text_atomic_no_products(self, atomic_page):
        with allure.step("Проверяем, что текст при отсутствии атомарных отображается корректно"):
            assert atomic_page.atomic_none.is_visible(), 'Заголовка нет'
            assert atomic_page.atomic_none.get_text() == assertions.atomic_error, 'Текст ошибки не совпадает'

    @allure.title("Проверка отображения продукта в Атомарных продуктах")
    @pytest.mark.parametrize("atomic_page", assertions.linkToProductsWithAtomic, indirect=True)
    def test_check_product_display(self, atomic_page):
        with allure.step("Проверяем, что название продукта отображается"):
            assert atomic_page.first_atomic_product.is_visible(), 'Названия продукта нет'
        with allure.step("Проверяем, что описание продукта отображается"):
            assert atomic_page.first_atomic_description.is_visible(), 'Описания продукта нет'
        with allure.step("Проверяем, что product owner отображается"):
            assert atomic_page.first_atomic_job_title.is_visible(), 'Надпись product owner нет'
            assert atomic_page.first_atomic_job_name.is_visible(), 'Имени руководителя нет'
            assert atomic_page.first_atomic_job_photo.is_visible(), 'Фото product owner нет'
        with allure.step("Проверяем, что иконка статусов отображается"):
            assert atomic_page.first_atomic_status_icon.is_visible(), 'Иконки статуса продукта нет'

    @allure.title("Проверка, что если есть архивные продукты в атомарных, то отображается хедер Архивные")
    @pytest.mark.parametrize("atomic_page", assertions.linkToProductsWithAtomic, indirect=True)
    def test_atomic_archive(self, atomic_page):
        with allure.step("Проверяем, что если у продукта есть архивные атомарные, то отображается заголовок"):
            if atomic_page.atomic_archive_block.is_visible():
                assert atomic_page.atomic_archive_header.is_visible(), 'Нет заголовка Архивные'

    @allure.title("Проверка корректного перехода из родительского продукта на страницу атомарного")
    @pytest.mark.parametrize("atomic_page", assertions.linkToMainForAtomicProduct, indirect=True)
    def test_go_to_parent_page(self, atomic_page):
        with allure.step('Кликаем на первый атомарный продукт из списка'):
            atomic_page.first_atomic_product.click()
        with allure.step('Проверяем, что url текущей страницы совпадает с ожидаемым'):
            assert atomic_page.url == 'https://stage.prodboard.mts.ru/product/BI_1883/main', 'Ссылка не совпадает'

    @allure.title("Проверка кликабельности ФИО product owner на вкладке атомарные продукты")
    @pytest.mark.parametrize("atomic_page", assertions.linkToProductsWithAtomic, indirect=True)
    def test_open_atomic_product_owner_closed_clickable(self, atomic_page):
        with allure.step('Проверяем кликабельность ФИО у product owner'):
            assert atomic_page.owner_atomic.is_clickable(), 'ФИО у product owner не кликабельно'

    @allure.title("Проверка кликабельности названия продукта на вкладке атомарные продукты")
    @pytest.mark.parametrize("atomic_page", assertions.linkToProductsWithAtomic, indirect=True)
    def test_open_atomic_product_name_closed_clickable(self, atomic_page):
        with allure.step('Проверяем кликабельность названия продукта'):
            assert atomic_page.first_atomic_product.is_clickable(), 'Названия продукта не кликабельно'

    @allure.title('Открытие карточки уволенного сотрудника в атомарных продуктах, проверка наличия статуса "Уволен"')
    @pytest.mark.parametrize('atomic_page', ['https://stage.prodboard.mts.ru/product/BI_105/atomic'], indirect=True)
    def test_fired_owner_atomic(self, product_page, atomic_page):
        with allure.step('Кликаем на product owner Бирюков'):
            product_page.fired_user_biryukov.click()
        with allure.step('Проверяем наличие чипса "уволен" на карточке product owner'):
            assert product_page.fired_status.is_visible(), 'Чипс "уволен" отсутсвует'

    @allure.title("Проверка перехода со страницы атомарного продукта на страницу родительского")
    @pytest.mark.parametrize("product_page", assertions.linkToAtomicProduct, indirect=True)
    def test_go_to_atomic_page(self, product_page):
        expected_main_product_title = product_page.main_product_link.get_text()
        with allure.step('Кликаем на ссылку родительского продукта'):
            product_page.main_product_link.click()
            product_page.wait_force(1)
        with allure.step('Проверяем, что название родительского продукта совпадает с ожидаемым'):
            assert product_page.product_name.get_text() == expected_main_product_title, 'Название не совпадает'
        with allure.step('Проверяем, что таб Атомарные продукты появился'):
            assert product_page.atomic_tab.is_visible(), 'Таб не появился'

    @allure.title("Нажатие на название возвращает к основной информации о текущем продукте (с таба атомарных)")
    @pytest.mark.parametrize("atomic_page", assertions.linkToDifferentAtomic, indirect=True)
    def test_name_returns_to_main_info_from_atomic(self, product_page, atomic_page):
        with allure.step("Кликаем на название продукта"):
            product_page.product_name.click()
        with allure.step("Проверяем, что мы вернулись на главную страницу продукта"):
            assert atomic_page.atomic_header.is_not_visible(), 'Заголовок с Атомарные продукты остался'

    @allure.title("Нажатие на лого возвращает к основной информации о текущем продукте (с таба атомарных)")
    @pytest.mark.parametrize("atomic_page", assertions.linkToDifferentAtomic, indirect=True)
    def test_logo_returns_to_main_info_from_atomic(self, product_page, atomic_page):
        with allure.step("Кликаем на лого продукта"):
            product_page.product_logo.click()
        with allure.step("Проверяем, что мы вернулись на главную страницу продукта"):
            assert atomic_page.atomic_header.is_not_visible(), 'Заголовок с Атомарные продукты остался'
