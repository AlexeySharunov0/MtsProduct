import allure
import pytest

from UI.tests.main_page.conftest import main_page


@pytest.mark.ui
@pytest.mark.action
@allure.feature("Переход по ссылке из главной")
class TestGoToProductPage:

    @allure.title(f"Переход из главной на страницу продукта")
    def test_go_to_first_product(self, main_page):
        main_page.get_page('https://stage.prodboard.mts.ru/preset2/products/all')
        with allure.step('Кликаем на карточку продукта'):
            main_page.products[0].click()
        with allure.step('Проверяем, что попали на страницу продукта'):
            assert "https://stage.prodboard.mts.ru/product/" in main_page.url, 'Урл не соответствует урлу страницы продукта'

    @allure.title(f"Переход из главной на страницу избранного продукта")
    def test_go_to_saved_product(self, main_page):
        with allure.step('Кликаем на значок избранных продуктов'):
            main_page.favorites_button.click()
        with allure.step('Кликаем на первый продукт в избранных'):
            main_page.first_favorite.click()
            main_page.wait()
            main_page.switch_to_tab(1)
        with allure.step('Проверяем, что попали на страницу продукта'):
            assert "https://stage.prodboard.mts.ru/product/" in main_page.url, 'Урл не соответствует урлу страницы продукта'

    @allure.title(f"Переход из главной на страницу Мой портфель")
    @allure.issue('https://jira.mts.ru/browse/PPI-2831', 'PPInfo - Мой Портфель - Проекты')
    def test_go_to_my_briefcase(self, main_page):
        with allure.step('Кликаем на значок Мой портфель'):
            main_page.my_briefcase.click()
        with allure.step('Переход на табл проектов'):
            main_page.projects.click()
        with allure.step('Проверяем, что у iframe правельна ссылка'):
            assert main_page.iframe_in_projects.get_attribute(
                'src') == 'https://finportal.mts.ru/reports/powerbi/%D0%A3%D0%BF%D1%80%D0%B0%D0%B2%D0%BB%D0%B5%D0%BD%D1%87%D0%B5%D1%81%D0%BA%D0%B0%D1%8F%20%D0%BE%D1%82%D1%87%D0%B5%D1%82%D0%BD%D0%BE%D1%81%D1%82%D1%8C/%D0%A0%D0%B0%D0%B1%D0%BE%D1%87%D0%B5%D0%B5%20%D0%BC%D0%B5%D1%81%D1%82%D0%BE%20%D1%80%D1%83%D0%BA%D0%BE%D0%B2%D0%BE%D0%B4%D0%B8%D1%82%D0%B5%D0%BB%D1%8F_%D0%BF%D1%80%D0%BE%D0%B5%D0%BA%D1%82%D1%8B?rc:toolbar=false', 'Ссылка на iframe некорректная'


@pytest.mark.ui
@allure.feature("Переход по ссылке из главной")
class TestGoToSettingsPage:

    @allure.title(f"Переход из главной в настройки главной страницы")
    def test_go_to_main_settings(self, main_page):
        main_page.dropdown_menu.click()
        with allure.step('Кликаем на настройки Главной страницы'):
            main_page.main_page_menu_item.click()
        with allure.step('Проверяем, что попали в настройки Главной страницы'):
            assert main_page.url == "https://stage.prodboard.mts.ru/prefs/main_settings", 'Урл не соответствует урлу настроек Главной страницы'

    @allure.title(f"Переход из главной в настройки внешнего продукта")
    def test_go_to_product_settings_commercial(self, main_page):
        main_page.dropdown_menu.click()
        with allure.step('Кликаем на "Страница внешнего продукта"'):
            main_page.product_page_menu_item_commercial.click()
        with allure.step('Проверяем, что попали в настройки страницы внешнего продукта'):
            assert main_page.url == "https://stage.prodboard.mts.ru/prefs/product_commercial", 'Урл не соответствует урлу настроек страницы внешнего продукта'

    @allure.title(f"Переход из главной в настройки внутреннего продукта")
    def test_go_to_product_settings_internal(self, main_page):
        main_page.dropdown_menu.click()
        with allure.step('Кликаем на "Страница внутреннего продукта"'):
            main_page.product_page_menu_item_internal.click()
        with allure.step('Проверяем, что попали в настройки страницы внутреннего продукта'):
            assert main_page.url == "https://stage.prodboard.mts.ru/prefs/product_internal", 'Урл не соответствует урлу настроек страницы внутреннего продукта'

    @allure.title('Переход из главной в настройку обязательных полей для формы добавления продукта')
    def test_required_fields_settings(self, main_page):
        main_page.dropdown_menu.click()
        with allure.step('Переходим на страницу настройки обязательных поле в форме создания с главной страницы'):
            main_page.required_fields_settings.click()
        with allure.step('Проверяем что действительно находимся на верной странице'):
            assert main_page.url == 'https://stage.prodboard.mts.ru/prefs/form_create', 'Урл не соответствует урлу настроек формы добавления'

    @allure.title(f"Переход из главной в настройки  уведомлений")
    def test_go_to_edit_settings(self, main_page):
        main_page.dropdown_menu.click()
        with allure.step('Кликаем на "Управление уведомлениями"'):
            main_page.notifications_menu_item.click()
        with allure.step('Проверяем, что попали в Управление уведомлениями'):
            assert main_page.url == "https://stage.prodboard.mts.ru/prefs/edit_settings", 'Урл не соответсвует урлу управления уведомлениями'


@pytest.mark.ui
@allure.feature(f"Переход по ссылке из главной")
class TestGoToAdminPage:

    @allure.title(f"Переход из главной в заявки")
    def test_go_to_aplications(self, main_page):
        main_page.dropdown_menu.click()
        with allure.step('Кликаем на "Заявки"'):
            main_page.applications_menu_item.click()
        with allure.step('Проверяем, что попали на страницу заявок'):
            assert main_page.url == "https://stage.prodboard.mts.ru/my-briefs/statusPublished", 'Урл не соответствует урлу заявок'

    @allure.title(f'Переход из главной к Сотрудникам')
    def test_go_to_fired(self, main_page):
        main_page.dropdown_menu.click()
        with allure.step('Кликаем на "Уволенные сотрудники"'):
            main_page.fired_menu_item.click()
        with allure.step('Проверяем, что попали на страницу уволенных сотрудников'):
            assert main_page.url == 'https://stage.prodboard.mts.ru/adsemployees/adsemployeeslist', 'Урл не соответствует урлу уволенных сотрудников'

    @allure.title(f"Переход из главной в хранилище")
    def test_go_to_storage(self, main_page):
        main_page.dropdown_menu.click()
        with allure.step('Кликаем на "Хранилище"'):
            main_page.storage_menu_item.click()
        with allure.step('Проверяем, что попали на страницу хранилища'):
            assert main_page.url == "https://stage.prodboard.mts.ru/catalogue/attributes/", 'Урл не соответствует урлу хранилища'

    @allure.title(f"Переход из главной в массовые операции")
    def test_go_to_bulk(self, main_page):
        main_page.dropdown_menu.click()
        with allure.step('Кликаем на "Массово изменение продуктов"'):
            main_page.bulk_ops_menu_item.click()
        with allure.step('Проверяем, что попали на страницу массовых операций'):
            assert main_page.url == "https://stage.prodboard.mts.ru/excel/get/", 'Урл не соответствует урлу массовых операций'

    @allure.title(f"Переход из главной в группы пользователей")
    def test_go_to_groups(self, main_page):
        main_page.dropdown_menu.click()
        with allure.step('Кликаем на "Группы пользователей"'):
            main_page.user_groups_menu_item.click()
        with allure.step('Проверяем, что попали на страницу групп пользователей'):
            assert main_page.url == "https://stage.prodboard.mts.ru/roles-and-rights/ea23b49c-ed52-4baa-a20d-86873e1954de", 'Урл не соответствует урлу групп пользователей'

    @allure.title(f"Переход из главной в изменение статусов")
    def test_go_to_statuses(self, main_page):
        main_page.dropdown_menu.click()
        with allure.step('Кликаем на "Изменение статусов"'):
            main_page.change_statuses_menu_item.click()
        with allure.step('Проверяем, что попали на страницу изменений статусов'):
            assert main_page.url == "https://stage.prodboard.mts.ru/changes/statuses", 'Урл не соответствует урлу изменений статусов'

    @allure.title(f"Переход из главной в изменение Класса критичности")
    @allure.issue('https://jira.mts.ru/browse/PPI-2195', 'PPInfo - Раздел "Изменение класса критичности"')
    def test_go_to_criticality_class(self, main_page):
        main_page.dropdown_menu.click()
        with allure.step('Кликаем на "Изменение статусов"'):
            main_page.change_statuses_menu_item.click()
        with allure.step('Переход в изменение класса критичности'):
            main_page.change_criticality_class.click()
        with allure.step('Проверяем, что попали на страницу изменений статусов'):
            assert main_page.url == "https://stage.prodboard.mts.ru/changes/critical", 'Урл не соответствует урлу изменений Класса критичности'

    @allure.title(f"Переход со страницы добавления продукта в страницу добавления внешнего")
    @allure.issue('https://jira.mts.ru/browse/PPI-416', 'PPInfo - Доработать страницу добавления продукта')
    def test_go_to_add_external(self, main_page):
        with allure.step('Переходим на страницу добавления продукта'):
            main_page.add_product.click()
        with allure.step('Нажимаем на кнопку добавления внешнего продукта'):
            main_page.add_product_on_page[0].click()
        with allure.step('Проверяем урл страницы, мы должны находиться на странице добавления внешнего продукта'):
            assert main_page.url == "https://stage.prodboard.mts.ru/add/Commercial", 'Урл не соответствует урлу добавления внешнего'

    @allure.title(f"Переход со страницы добавления продукта в страницу добавления внутреннего")
    @allure.issue('https://jira.mts.ru/browse/PPI-416', 'PPInfo - Доработать страницу добавления продукта')
    def test_go_to_add_internal(self, main_page):
        with allure.step('Переходим на страницу добавления продукта'):
            main_page.add_product.click()
        with allure.step('Нажимаем на кнопку добавления внутреннего продукта'):
            main_page.add_product_on_page[1].click()
        with allure.step('Проверяем урл страницы, мы должны находиться на странице добавления внутреннего продукта'):
            assert main_page.url == "https://stage.prodboard.mts.ru/add/Internal", 'Урл не соответствует урлу добавления внутреннего'


@pytest.mark.ui
@allure.feature("Выход")
class TestSignOut:

    def test_sign_out(self, main_page):
        main_page.dropdown_menu.click()
        with allure.step('Кликаем на "Выйти"'):
            main_page.quit_menu_item.click()
        with allure.step('Проверяем, что попали на страницу аутентификации'):
            assert "https://isso-dev.mts.ru/" in main_page.url, 'Урл не соответствует урлу страницы аутентификации'


@pytest.mark.ui
@allure.feature('Переход с главной страницы в Каталог продуктов')
@allure.issue('https://jira.mts.ru/browse/PPI-3558', 'Предложение перехода из блока "Новое в PPInfo" в "Каталог"')
class TestGoToCatalogue:
    @allure.title('Переход из новое в каталог')
    def test_go_to_catalogue_from_new(self, main_page):
        with allure.step('Кликаем на кнопку Перейти в каталог'):
            main_page.catalogue_button.click()
        with allure.step('Проверяем, что попали на страницу каталога'):
            assert 'https://stage.prodboard.mts.ru/preset2/products/all' == main_page.url, (
                f'Урл не соответствует урлу в каталоге продуктов \n'
                f'https://stage.prodboard.mts.ru/preset2/products/all != {main_page.url}')

    @allure.title('Переход из закрытые в каталог')
    def test_go_to_catalogue_from_closed(self, main_page):
        with allure.step('Кликаем на кнопку закрытые продукты'):
            main_page.closed_products.click()
        with allure.step('Кликаем по кнопке Архив продуктов'):
            main_page.archive_catalogue_button.click()
        with allure.step('Проверяем, что попали в архив продуктов'):
            assert 'https://stage.prodboard.mts.ru/preset2/archive/archive' == main_page.url, (
                f'Урл не соответствует урлу в архиве продуктов \n'
                f'https://stage.prodboard.mts.ru/preset2/archive/archive != {main_page.url}')
