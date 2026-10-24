import pytest

from UI.pages.SettingsPage.curators_page.curators import CuratorPage
from UI.pages.SettingsPage.edit_page.edit import EditPage
from UI.pages.SettingsPage.external_product_page.external_product import ExternalProductPage
from UI.pages.SettingsPage.forms_page.forms import FormsPage
from UI.pages.SettingsPage.internal_product_page.internal_product import InternalProductPage
from UI.pages.SettingsPage.main_page.main import MainPage
from UI.pages.SettingsPage.pg_page.pg import PGPage
from UI.ui_fixtures import screenshot_on_failure


# Paths


# =========================================== Страница настройки кураторов ================================================


@pytest.fixture
def curators_page(authorize, request) -> CuratorPage:
    if hasattr(request, 'param'):
        page = CuratorPage(authorize, request.param)
    else:
        page = CuratorPage(authorize)

    yield page

    screenshot_on_failure(authorize, request)


# =========================================== Страница настроек PG =====================================================


@pytest.fixture
def pg_page(authorize, request) -> PGPage:
    if hasattr(request, 'param'):
        page = PGPage(authorize, request.param)
    else:
        page = PGPage(authorize)

    yield page

    screenshot_on_failure(authorize, request)


# ============================================ Страница настроек  уведомлениям =========================================


@pytest.fixture
def edit_page(authorize, request) -> EditPage:
    if hasattr(request, 'param'):
        page = EditPage(authorize, request.param)
    else:
        page = EditPage(authorize)

    yield page

    screenshot_on_failure(authorize, request)


# ============================================== Страница настроек форм добавления =====================================


@pytest.fixture
def forms_page(authorize, request) -> FormsPage:
    if hasattr(request, 'param'):
        page = FormsPage(authorize, request.param)
    else:
        page = FormsPage(authorize)

    yield page

    screenshot_on_failure(authorize, request)


# ============================================== Страница настроек форм добавления =====================================


@pytest.fixture
def main_page(authorize, request) -> MainPage:
    if hasattr(request, 'param'):
        page = MainPage(authorize, request.param)
    else:
        page = MainPage(authorize)

    yield page

    screenshot_on_failure(authorize, request)


# ============================================== Страница настроек внешнего продукта ===================================


@pytest.fixture
def external_product_page(authorize, request) -> ExternalProductPage:
    if hasattr(request, 'param'):
        page = ExternalProductPage(authorize, request.param)
    else:
        page = ExternalProductPage(authorize)

    yield page

    screenshot_on_failure(authorize, request)


# ============================================== Страница настроек внутреннего продукта ================================

@pytest.fixture
def internal_product_page(authorize, request) -> InternalProductPage:
    if hasattr(request, 'param'):
        page = InternalProductPage(authorize, request.param)
    else:
        page = InternalProductPage(authorize)

    yield page

    screenshot_on_failure(authorize, request)
