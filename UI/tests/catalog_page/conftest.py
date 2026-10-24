import pytest

from UI.pages.catalog_page.catalog.catalog import CatalogPage
from UI.ui_fixtures import screenshot_on_failure, authorize_tech_user_1


# Paths


# =========================================== Главная страница продукта ================================================


@pytest.fixture
def catalog_page(authorize, request) -> CatalogPage:
    if hasattr(request, 'param'):
        page = CatalogPage(authorize, request.param)
    else:
        page = CatalogPage(authorize)

    yield page

    screenshot_on_failure(authorize, request)


@pytest.fixture
def user_catalog_page(authorize_tech_user_1, request) -> CatalogPage:
    if hasattr(request, 'param'):
        page = CatalogPage(authorize_tech_user_1, request.param)
    else:
        page = CatalogPage(authorize_tech_user_1)

    yield page

    screenshot_on_failure(authorize_tech_user_1, request)
