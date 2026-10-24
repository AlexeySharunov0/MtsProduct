import os
from enum import Enum


class APIRoutes(str, Enum):
    BASE = os.getenv('API_BASE_URL', 'https://stage.prodboard.example.com')
    CACHE = 'cache/rest/api'
    PMD_REST_INTERNAL = 'pmd/internal/rest/api'
    PMD_PUBLIC_REST = 'pmd/public/rest/api'
    PMD_PUBLIC_GW = 'pmd/public/gw/api'
    PMD_ADMIN_GW = 'pmd/admin/gw/api'
    PMD_EXTERNAL_REST = 'pmd/external/rest/api'
    PMD_ADMIN_REST = 'pmd/admin/rest/api'
    PMD_INTERNAL_API_GW = 'pmd/internal_api/gw/api'
    PMD_INTERNAL_GW = 'pmd/internal/gw/api'
    PPINFO_GW = 'ppinfo/gw/api'
    PPINFO = 'ppinfo/api'
    USER_SERVICE = 'user-service/internal/rest/api'
    HYPERION = 'hyperion/internal/rest/api'
    MOBILE = 'mobile/rest/api'
    NEWS_PUBLIC = 'news-service/api/public/rest'
    NEWS_ADMIN = 'news-service/api/admin/rest'
    SEARCH_INTERNAL = 'search/internal/rest/api'
    SEARCH_EXTERNAL = 'search/external/rest/api'

    def __str__(self) -> str:
        return self.value
