import pytest

from UI.pages.main_page.main_page.main_page import MainPage
from UI.pages.main_page.news_page.news import NewsPage
from UI.ui_fixtures import screenshot_on_failure, authorize_tech_user_1


# Paths


# =========================================== Главная страница продукта ================================================


@pytest.fixture
def main_page(authorize, request) -> MainPage:
    if hasattr(request, 'param'):
        page = MainPage(authorize, request.param)
    else:
        page = MainPage(authorize)

    yield page

    screenshot_on_failure(authorize, request)


@pytest.fixture
def user_main_page(authorize_tech_user_1, request) -> MainPage:
    if hasattr(request, 'param'):
        page = MainPage(authorize_tech_user_1, request.param)
    else:
        page = MainPage(authorize_tech_user_1)

    yield page

    screenshot_on_failure(authorize_tech_user_1, request)


# =========================================== Новости ================================================


@pytest.fixture
def news_page(authorize, request) -> NewsPage:
    if hasattr(request, 'param'):
        page = NewsPage(authorize, request.param)
    else:
        page = NewsPage(authorize)

    yield page

    screenshot_on_failure(authorize, request)
