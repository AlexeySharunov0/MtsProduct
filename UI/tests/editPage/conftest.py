import pytest

from UI.pages.add_replace_page.add_replace import AddReplacePage
from UI.ui_fixtures import screenshot_on_failure, authorize_tech_user_1


# Paths


# =========================================== Главная страница продукта ================================================


@pytest.fixture
def add_replace_page(authorize, request) -> AddReplacePage:
    if hasattr(request, 'param'):
        page = AddReplacePage(authorize, request.param)
    else:
        page = AddReplacePage(authorize)

    yield page

    screenshot_on_failure(authorize, request)


@pytest.fixture
def user_add_replace_page(authorize_tech_user_1, request) -> AddReplacePage:
    if hasattr(request, 'param'):
        page = AddReplacePage(authorize_tech_user_1, request.param)
    else:
        page = AddReplacePage(authorize_tech_user_1)

    yield page

    screenshot_on_failure(authorize_tech_user_1, request)


@pytest.fixture
def user_2_add_replace_page(authorize_tech_user_2, request) -> AddReplacePage:
    if hasattr(request, 'param'):
        page = AddReplacePage(authorize_tech_user_2, request.param)
    else:
        page = AddReplacePage(authorize_tech_user_2)

    yield page

    screenshot_on_failure(authorize_tech_user_2, request)
