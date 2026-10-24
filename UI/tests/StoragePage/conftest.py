import pytest

from UI.pages.StoragePage.attributes.attributes import AttributesPage
from UI.pages.StoragePage.specification.specification import SpecificationPage
from UI.ui_fixtures import screenshot_on_failure


# Paths


# =========================================== Страница атрибутов ================================================


@pytest.fixture
def attributes_page(authorize, request) -> AttributesPage:
    if hasattr(request, 'param'):
        page = AttributesPage(authorize, request.param)
    else:
        page = AttributesPage(authorize)

    yield page

    screenshot_on_failure(authorize, request)


# ============================================ Страница спецификаций ===================================================


@pytest.fixture
def specification_page(authorize, request) -> SpecificationPage:
    if hasattr(request, 'param'):
        page = SpecificationPage(authorize, request.param)
    else:
        page = SpecificationPage(authorize)

    yield page

    screenshot_on_failure(authorize, request)
