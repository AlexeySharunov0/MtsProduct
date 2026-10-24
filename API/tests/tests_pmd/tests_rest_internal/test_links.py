import warnings

import allure
import pytest

from API.models.pmd.rest_internal_modules.links import Links

warnings.filterwarnings('ignore', message='numpy.dtype size changed')


#### LINKS
@pytest.mark.api
@allure.feature('Лого')
class TestPublicLinks(Links):
    @allure.title('Получение лого по BI коду')
    @pytest.mark.parametrize('code', ['BI_60', 'BI_1561', 'BI_1288', 'BI_1921'])
    def test_get_docs(self, public_rest_client, code):
        self.get_logo_by_code(public_rest_client, code)
