import warnings

import allure

warnings.filterwarnings("ignore", message="numpy.dtype size changed")

HOST = 'https://stage.prodboard.example.com'


class LinksUrls:
    """
    https://stage.prodboard.example.com/pmd/swagger/rest/internal/index.html#/
    """
    #### LINKS

    # Получение лого по коду продукта
    GET_LOGO_BY_CODE = 'v1/product/{}/logo'


class Links(LinksUrls):
    #### LINKS
    @allure.step('Получение лого продукта по коду')
    def get_logo_by_code(self, client, file_id: str) -> bytes:
        response = client.get(self.GET_LOGO_BY_CODE.format(file_id), raw_format=True)

        return response.content
