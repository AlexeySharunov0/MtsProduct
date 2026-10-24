import allure

from API.data.hyperion import ListHyperion

HOST = 'https://stage.prodboard.example.com'


class HyperionUrls:
    """
    https://stage.prodboard.example.com/hyperion/swagger/rest/index.html#/
    """
    # Получение проектов по коду Oracle внутри карточки продукта
    HYPERION = 'v1/project/{}'


class Hyperion(HyperionUrls):

    @allure.step('Получение проектов Хайпиреон')
    def get_hyperion_projects(self, client, oracle_code):
        with allure.step(f'Получение проектов по коду Oracle: {oracle_code}'):
            response = client.get(self.HYPERION.format(oracle_code))
        with allure.step('Проверка модели ответа и статус кода'):
            ListHyperion(hyperion=response)
            assert response, f'В ответе нет ни одного проекта {response["projects"]}'

    @allure.step('Получение проектов по невалидному коду Oracle')
    def get_hyperion_projects_error(self, client, oracle_code: str):
        with allure.step(f'Получение проектов Хайпиреон по несуществующему коду оракл: {oracle_code}'):
            response = client.get(self.HYPERION.format(oracle_code))
        with allure.step('Проверка модели ответа и статус кода'):
            assert not response, f'Ожидался пустой список, но получено: {response}'


