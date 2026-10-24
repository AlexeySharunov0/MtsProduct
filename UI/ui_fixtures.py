import logging
import os
from datetime import datetime

import allure
import pytest
from playwright.sync_api import Playwright, Browser

from API.utils.vault_client import VaultClient
from UI.utils.EnvProvider import EnvProvider
from UI.utils.my_decorators import retry_on_timeout

# Paths

client = VaultClient()
# Credentials
USER_PASSWORD = client.get_creds("main")['default_password']
USER_LOGIN = client.get_creds("main")['default_login']

TECH_USER_LOGIN_1 = client.get_creds("main")['tech_1_login']
TECH_USER_PASSWORD_1 = client.get_creds("main")['tech_1_password']

TECH_USER_LOGIN_2 = client.get_creds("main")['tech_2_login']
TECH_USER_PASSWORD_2 = client.get_creds("main")['tech_2_password']

logger = logging.getLogger(__name__)

IS_HEADLESS = False if os.getenv('IS_HEADLESS') == 'FALSE' else True


# ===================================================== Авторизация ====================================================
@pytest.fixture
@retry_on_timeout(max_retries=3, retry_delay=5)
def authorize(page):
    # with page.wait_for_event("load"):
    page.goto(EnvProvider.getBaseUrl())
    with allure.step("В поле логина вводим корректный логин тех.пользователя"):
        page.locator("#username").fill(USER_LOGIN)
    with allure.step("В поле пароля вводим корректный пароль тех.пользователя"):
        page.locator("#password").fill(USER_PASSWORD)
    with allure.step("Нажимаем кнопку логина"):
        page.locator('.btn').click()

    return page


@pytest.fixture
@retry_on_timeout(max_retries=3, retry_delay=5)
def authorize_tech_user_1(page_user):
    page_user.goto(EnvProvider.getBaseUrl())
    with allure.step("В поле логина вводим корректный логин тех.пользователя"):
        page_user.locator("#username").fill(TECH_USER_LOGIN_1)
    with allure.step("В поле пароля вводим корректный пароль тех.пользователя"):
        page_user.locator("#password").fill(TECH_USER_PASSWORD_1)
    with allure.step("Нажимаем кнопку логина"):
        page_user.locator('.btn').click()

    return page_user


@pytest.fixture
@retry_on_timeout(max_retries=3, retry_delay=5)
def authorize_tech_user_2(page_user):
    page_user.goto(EnvProvider.getBaseUrl())
    with allure.step("В поле логина вводим корректный логин тех.пользователя"):
        page_user.locator("#username").fill(TECH_USER_LOGIN_2)
    with allure.step("В поле пароля вводим корректный пароль тех.пользователя"):
        page_user.locator("#password").fill(TECH_USER_PASSWORD_2)
    with allure.step("Нажимаем кнопку логина"):
        page_user.locator('.btn').click()

    return page_user


# ====================================================== Настройки =====================================================

@pytest.fixture(scope="session")
def browser_context_args(browser_context_args) -> dict:
    return {**browser_context_args, "viewport": {"width": 1920, "height": 1080}, "ignore_https_errors": True,
            "locale": "ru-Ru", "timezone_id": "Europe/Moscow",
            "http_credentials": {"username": USER_LOGIN, "password": USER_PASSWORD}}


@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args) -> dict:
    return {**browser_type_launch_args, "headless": IS_HEADLESS, "slow_mo": 400,
            "args": ["--no-sandbox", "--disable-setuid-sandbox", "--disable-dev-shm-usage"]}
    # headless True если не нужен запуск браузера
    # slow_mo - время между действиями в мс


@pytest.fixture(scope="session")
def browser(playwright: Playwright, browser_type_launch_args: dict) -> Browser:
    return playwright.chromium.launch(**browser_type_launch_args)


@pytest.fixture(scope="function")
def browser_context(playwright: Playwright, browser_type_launch_args: dict, browser_context_args: dict):
    browser = playwright.chromium.launch(**browser_type_launch_args)
    context = browser.new_context(**browser_context_args)
    yield context
    context.close()
    browser.close()


# TODO: придумать, как не плодить пейджи
@pytest.fixture(scope="function")
def page(browser_context, request):
    page = browser_context.new_page()
    page.set_default_timeout(10000)
    yield page
    page.close()


@pytest.fixture(scope="function")
def page_user(browser_context, request):
    page = browser_context.new_page()
    page.set_default_timeout(10000)
    yield page
    page.close()


# ====================================================== Debugging =====================================================
def screenshot_on_failure(page, request):
    if request.session.testsfailed:
        screenshots_dir = os.path.join(os.path.dirname(__file__), '.', 'screenshots')
        if not os.path.exists(screenshots_dir):
            os.makedirs(screenshots_dir)

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        screenshot_path = os.path.join(screenshots_dir, f"{request.function.__name__}_{timestamp}.png")

        page.screenshot(path=screenshot_path)

        with open(screenshot_path, 'rb') as image_file:
            allure.attach(image_file.read(),
                          name=request.function.__name__,
                          attachment_type=allure.attachment_type.PNG)
