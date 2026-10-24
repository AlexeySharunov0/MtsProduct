import pytest

from UI.pages.product_page.atomic_page.atomic import AtomicPage
from UI.pages.product_page.dependency.dependency import DependencyPage
from UI.pages.product_page.documents.documents import DocumentsPage
from UI.pages.product_page.eco_modules.eco_modules import EcoModulesPage
from UI.pages.product_page.main.main_page import MainPage
from UI.pages.product_page.metrics.metrics import MetricsPage
from UI.pages.product_page.product_guide.pg import PGPage
from UI.pages.product_page.projects.projects import ProjectsPage
from UI.pages.product_page.technological_composition.techno import TechnoPage
from UI.pages.product_page.health.health import HealthPage
from UI.ui_fixtures import screenshot_on_failure, authorize_tech_user_1, authorize


# Paths


# =========================================== Главная страница продукта ================================================


@pytest.fixture
def product_page(authorize, request) -> MainPage:
    if hasattr(request, 'param'):
        page = MainPage(authorize, request.param)
    else:
        page = MainPage(authorize)

    yield page

    screenshot_on_failure(authorize, request)


@pytest.fixture
def product_page_user_1(authorize_tech_user_1, request) -> MainPage:
    if hasattr(request, 'param'):
        page = MainPage(authorize_tech_user_1, request.param)
    else:
        page = MainPage(authorize_tech_user_1)

    yield page

    screenshot_on_failure(authorize_tech_user_1, request)


# =========================================== Атомарные продукты =======================================================

@pytest.fixture
def atomic_page(authorize, request) -> AtomicPage:
    if hasattr(request, 'param'):
        page = AtomicPage(authorize, request.param)
    else:
        page = AtomicPage(authorize)

    yield page

    screenshot_on_failure(authorize, request)


# =========================================== Страница документов ======================================================

@pytest.fixture
def docs_page(authorize, request) -> DocumentsPage:
    if hasattr(request, 'param'):
        page = DocumentsPage(authorize, request.param)
    else:
        page = DocumentsPage(authorize)

    yield page

    screenshot_on_failure(authorize, request)


@pytest.fixture
def docs_page_user(authorize_tech_user_1, request) -> DocumentsPage:
    if hasattr(request, 'param'):
        page = DocumentsPage(authorize_tech_user_1(), request.param)
    else:
        page = DocumentsPage(authorize_tech_user_1)

    yield page

    screenshot_on_failure(authorize_tech_user_1, request)


# =========================================== Экосистемные модули ======================================================

@pytest.fixture
def eco_modules_page(authorize, request) -> EcoModulesPage:
    if hasattr(request, 'param'):
        page = EcoModulesPage(authorize, request.param)
    else:
        page = EcoModulesPage(authorize)

    yield page

    screenshot_on_failure(authorize, request)


# ================================================ Метрики =============================================================

@pytest.fixture
def metrics_page(authorize, request) -> MetricsPage:
    if hasattr(request, 'param'):
        page = MetricsPage(authorize, request.param)
    else:
        page = MetricsPage(authorize)

    yield page

    screenshot_on_failure(authorize, request)


# ================================================ Product Guide =======================================================

@pytest.fixture
def pg_page(authorize, request) -> PGPage:
    if hasattr(request, 'param'):
        page = PGPage(authorize, request.param)
    else:
        page = PGPage(authorize)

    yield page

    screenshot_on_failure(authorize, request)


# ================================================ Проекты =============================================================

@pytest.fixture
def projects_page(authorize, request) -> ProjectsPage:
    if hasattr(request, 'param'):
        page = ProjectsPage(authorize, request.param)
    else:
        page = ProjectsPage(authorize)

    yield page

    screenshot_on_failure(authorize, request)


# ========================================== Технологический состав ====================================================

@pytest.fixture
def techno_page(authorize, request) -> TechnoPage:
    if hasattr(request, 'param'):
        page = TechnoPage(authorize, request.param)
    else:
        page = TechnoPage(authorize)

    yield page

    screenshot_on_failure(authorize, request)

# ================================================ Зависмости ==========================================================

@pytest.fixture
def dependency_page(authorize, request) -> DependencyPage:
    if hasattr(request, 'param'):
        page = DependencyPage(authorize, request.param)
    else:
        page = DependencyPage(authorize)

    yield page

    screenshot_on_failure(authorize, request)

# =========================================== Здоровье =================================================================
@pytest.fixture
def health_page(authorize, request) -> HealthPage:
    if hasattr(request, 'param'):
        page = HealthPage(authorize, request.param)
    else:
        page = HealthPage(authorize)

    yield page

    screenshot_on_failure(authorize, request)