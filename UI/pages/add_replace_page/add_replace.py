import logging
import time
from datetime import datetime

import allure
from playwright.sync_api import Page

from API.utils.generate import Gen
from UI.base.WebPage import WebPage
from UI.pages.add_replace_page.add_replace_locators import AddPageLocators
from UI.ui_fixtures import USER_LOGIN, USER_PASSWORD, TECH_USER_PASSWORD_1, \
    TECH_USER_LOGIN_1, TECH_USER_LOGIN_2, TECH_USER_PASSWORD_2
from paths import ROOT

logger = logging.getLogger(__name__)


class AddReplacePage(WebPage, AddPageLocators):
    def __init__(self, page: Page, url: str = None):
        WebPage.__init__(self, page)  # Явный вызов инициализатора WebPage
        AddPageLocators.__init__(self, page)  # Явный вызов инициализатора CanvasPageLocators
        self._page = page
        self.base_url = url if url else 'https://stage.prodboard.example.com/add-product'
        self.get_page(self.base_url)

    @allure.step('Выбор типа продукта')
    def start_work(self, product_type: str = 'commercial', clear_draft: bool = True):
        if product_type == 'commercial':
            with allure.step('Выбираем внешний продукт'):
                self.choose_type_button.get_items()[0].click()
        else:
            with allure.step('Выбираем внутренний продукт'):
                self.choose_type_button.get_items()[-1].click()
        if clear_draft:
            with allure.step('Очищаем черновик'):
                self.clear_button.click()

    @allure.step('Заполняем обязательные поля формы')
    def fill_required_fields(self):
        required_amount = self.required_fields.count()

        count = 0
        for field in self.fields:
            if count == required_amount:
                break
            if field.get_child('PPLabel').get_child('required'):
                self.fill_any_field(field.get_attribute('data-type'), field)
            count += 1

    @allure.step('Заполняем все поля определенного типа')
    def fill_all_fields(self, field_type: str, to_remove: list = None):
        for field in self.fields.get_items():
            if field.get_attribute('data-type') == field_type:
                if to_remove:
                    if any(i in field.get_text() for i in to_remove):
                        continue
                self.fill_any_field(field.get_attribute('data-type'), field)

    @allure.step('Заполняем поле любого формата')
    def fill_any_field(self, field_type: str, element):
        match field_type:
            case 'user':
                self.scroll_page_down(300)
                self.find_user(element)
            case 'time':
                self.data_input(element.get_child('.pp-input__inner'))
            case 'text':
                self.text_input(element.get_child('pp-input__inner'))
            case 'string':
                if element.get_child('fieldUniversal'):
                    self.many_select(element)
                else:
                    self.text_input(element.get_child('.has-suffix'))
            case _:
                assert False, f'Элемента с типом {field_type} нет'

    @allure.step('Заполняем форму: юзер')
    def find_user(self, element, user: str = 'admin_user'):
        element.click()
        with allure.step(f'Ищем пользователя {user}'):
            self.po_input.fill(user)
            self.find.click()
            self.user.click()

    @allure.step('Заполняем форму: мультивыбор')
    def many_select(self, web_input):
        web_input.click()
        self.first_value.click()

    @allure.step('Заполняем форму: строка')
    def text_input(self, input_element):
        input_element.fill('test ' + Gen.generate_text(length=5))

    @allure.step('Заполняем форму: дата')
    def data_input(self, input_element):
        input_element.click()
        input_element.press_key("ArrowLeft")

    @allure.step('Проверяем значок возле шага в добавлении продукта')
    def check_step_marks(self, element, state: str) -> bool:
        states = {
            'accept': "/images/checkCircle.svg",
            'deny': "/images/briefFalture.svg",
            'in_work': "/images/BriefInWork.svg",
            'registered': "/images/BriefIsWaiting.svg"
        }
        try:
            element.get_child(f'//*[@src="{states[state]}"]')
            return True
        except Exception:
            return False

    @allure.step('Перезаходим админом')
    def login_admin(self):
        with allure.step('Выходим с сайта'):
            self.avatar.click()
            self.quit.click()
            self.quit_confirm.click()

            self.get_page("https://stage.prodboard.example.com/")
            with allure.step("В поле логина вводим корректный логин тех.пользователя"):
                self.login_input.fill(USER_LOGIN)
            with allure.step("В поле пароля вводим корректный пароль тех.пользователя"):
                self.password_input.fill(USER_PASSWORD)
            with allure.step("Нажимаем кнопку логина"):
                self.login_button.click()

    @allure.step('Перезаходим пользователем')
    def login_user(self):
        with allure.step('Выходим с сайта'):
            self.avatar.click()
            self.quit.click()
            self.quit_confirm.click()
            # self.cross.click()

            self.get_page("https://stage.prodboard.example.com/")
            with allure.step("В поле логина вводим корректный логин тех.пользователя"):
                self.login_input.fill(TECH_USER_LOGIN_1)
            with allure.step("В поле пароля вводим корректный пароль тех.пользователя"):
                self.password_input.fill(TECH_USER_PASSWORD_1)
            with allure.step("Нажимаем кнопку логина"):
                self.login_button.click()

    @allure.step('Перезаходим пользователем')
    def login_user_2(self):
        with allure.step('Выходим с сайта'):
            self.avatar.click()
            self.quit.click()
            self.quit_confirm.click()
            # self.cross.click()

            self.get_page("https://stage.prodboard.example.com/")
            with allure.step("В поле логина вводим корректный логин тех.пользователя"):
                self.login_input.fill(TECH_USER_LOGIN_2)
            with allure.step("В поле пароля вводим корректный пароль тех.пользователя"):
                self.password_input.fill(TECH_USER_PASSWORD_2)
            with allure.step("Нажимаем кнопку логина"):
                self.login_button.click()

    @allure.step('Заменяем содержимое формы')
    def replace_input(self, input_type: str, input_element):
        if input_type == "string":

            input_element.fill('https://' + Gen.generate_text(7))

        elif input_type == "many select":

            input_element.click()
            self.first_value.click()

        elif input_type == "user":

            input_element.click()
            self.po_input.fill('dashkerdin')
            self.find.click()
            self.user.click()

        elif input_type == "data":

            input_element.input_element()
            self.date_one.click()

    @allure.step('Удаление продукта')
    def delete_product(self):
        with allure.step('Жмем на кнопку удалить'):
            self.delete_product_button.click()
        with allure.step('Вводим причину удаления'):
            self.reason_deleted_input.fill(datetime.now().strftime("%d:%m:%Y"))
        with allure.step('Подтверждаем удаление'):
            self.delete_in_modal_button.click()

    @allure.step("Добавляем документ через заявку")
    def add_doc(self, access_type: str = 'public'):

        self.get_page('https://stage.prodboard.example.com/product/BI_3266/docs')

        doc_name = '/UI/data/test_file.docx'
        doc_full_name = ROOT + doc_name
        with allure.step("Нажимаем кнопку 'Добавить файл...'"):
            self.addFile.click()
        with allure.step('Заполняем поле Название'):
            self.doc_name.fill(doc_name)
        with allure.step("Выбираем публичность"):
            if access_type == 'public':
                self.public_doc.click()
            else:
                self.closed_doc.click()
        with allure.step("Добавляем файл"):
            self.file.click()
            self.input_file.input_file(doc_full_name)
        with allure.step("Жмем кнопу Добавить"):
            self.addDoc.click()
        time.sleep(2)
        self.go_to_application.click()
        time.sleep(2)

        assert self.url.startswith(
            'https://stage.prodboard.example.com/brief/'), 'Мы не перешли на страницу заявки'

    @allure.step("Добавляем документ админом")
    def add_doc_without_brief(self, access_type: str = 'public'):
        doc_name = 'UI_TEST_DOC'
        doc_full_name = ROOT + '/UI/data/test_file.docx'
        with allure.step("Нажимаем кнопку 'Добавить файл...'"):
            self.addFile.click()
        with allure.step('Заполняем поле Название'):
            self.doc_name.fill(doc_name)
        with allure.step("Выбираем публичность"):
            if access_type == 'public':
                self.public_doc.click()
            else:
                self.closed_doc.click()
        with allure.step("Добавляем файл"):
            self.file.click()
            self.input_file.input_file(doc_full_name)
        with allure.step("Жмем кнопу Добавить"):
            self.add_doc_button.click()

    @allure.step("Добавляем ссылку админом")
    def add_link_without_brief(self, access_type: str = 'public'):
        with allure.step("Нажимаем кнопку 'Добавить файл...'"):
            self.addFile.click()
        with allure.step('Заполняем поле Название'):
            self.doc_name.fill('UI_TEST_LINK')
        with allure.step("Выбираем публичность"):
            if access_type == 'public':
                self.public_doc.click()
            else:
                self.closed_doc.click()
        with allure.step("Добавляем ссылку"):
            self.link.click()
            self.add_link_input.fill('https://stage.prodboard.example.com/preset/archive')
        with allure.step("Жмем кнопу Добавить"):
            self.add_doc_button.click()

    @allure.step("Добавляем ссылку пользователем")
    def add_link(self, access_type: str = 'public'):

        self.get_page('https://stage.prodboard.example.com/product/BI_3266/docs')

        with allure.step("Нажимаем кнопку 'Добавить файл...'"):
            self.addFile.click()
        with allure.step('Заполняем поле Название'):
            self.doc_name.fill('UI_TEST_LINK')
        with allure.step("Выбираем публичность"):
            if access_type == 'public':
                self.public_doc.click()
            else:
                self.closed_doc.click()
        with allure.step("Добавляем ссылку"):
            self.link.click()
            self.add_link_input.fill('https://stage.prodboard.example.com/preset/archive')
        with allure.step("Жмем кнопу Добавить"):
            self.addDoc.click()
        self.go_to_application.click()
        self.wait()

        assert self.url.startswith(
            'https://stage.prodboard.example.com/brief/'), 'Мы не перешли на страницу заявки'
