import allure
import pytest

from API.models.hyperion.hyperion import Hyperion


@pytest.mark.api
@allure.feature('Hyperion')
class TestHyperion(Hyperion):

    @allure.title('Получение проектов Хайпиреон по коду Oracle')
    @pytest.mark.parametrize('code', ['MLib', 'MAAS', 'MAfi'])
    def test_hyperion_api(self, hyperion_client, code):
        self.get_hyperion_projects(hyperion_client, code)

    @allure.title('Получение проектов Хайпиреон с неправильным кодом Oracle')
    @pytest.mark.parametrize('code', ['qqweqweqweqweqweqweqwe', '1233123123', '@#$$%%'])
    def test_hyperion_api_error(self, hyperion_client, code):
        self.get_hyperion_projects_error(hyperion_client, code)