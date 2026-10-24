from typing import Dict, Any, List

import allure

from API.data.pmd import DemosInSearch
from API.data.search import SearchModel, Suggestions, NewSearchResult
from API.utils.helpers import translate_text

HOST = 'https://stage.prodboard.example.com'


class SearchUrls:
    """
    https://stage.prodboard.example.com/search/swagger/rest/index.html
    """
    # Поиск
    SEARCH = 'v1/product'

    # Поиск external
    SEARCH_V1 = 'v1/product'

    # Подсказки
    SUGGESTIONS = 'v1/product/suggestion'

    # Поиск Демо
    SEARCH_DEMO = 'v1/demo/search'

    # Подсказки Демо
    SUGGESTIONS_DEMO = 'v1/demo/suggestion'


class Search(SearchUrls):

    @allure.step('Поиск')
    def search(self, client, pattern: str) -> list[dict]:
        params = {
            "pattern": f"{pattern}"
        }

        response = client.get(self.SEARCH, params=params)

        SearchModel(search=response)

        return response

    @allure.step('Получение всех результатов поиска со всех категорий')
    def get_all_result(self, client, pattern: str) -> List[str]:

        product_names = []

        for product in self.search(client, pattern):
            product_names.append(product["name"])

        return product_names

    @allure.step('Поиск v1')
    def search_v1(self, client, pattern: str, limit: int = 1000, offset: int = 0) -> List[Dict[str, Any]]:
        params = {
            "pattern": f"{pattern}",
            "limit": limit,
            "offset": offset
        }

        response = client.get(self.SEARCH_V1, params=params)

        NewSearchResult(search_result=response)

        return response

    @allure.step('Подсказки')
    def suggestion(self, client, pattern: str) -> Dict[str, Any]:
        params = {
            "pattern": f"{pattern}"
        }

        response = client.get(self.SUGGESTIONS, params=params)

        Suggestions(**response)

        return response

    @allure.step('Поиск демо')
    def search_demo(
            self,
            client,
            pattern: str = None,
            category_list: list[str] | None = None,
            date_from: int = None,
            date_to: int = None
    ) -> list[dict[str, Any]]:

        params = [
        ]
        if pattern:
            params += [('pattern', pattern)]
        if category_list:
            params += [('category', category) for category in category_list]
        if date_from:
            params += [('dateFrom', date_from)]
        if date_to:
            params += [('dateTo', date_to)]

        response = client.get(self.SEARCH_DEMO, params=params)

        DemosInSearch(demos=response)

        return response

    @allure.step('Производим поиск')
    def make_search(self, search_client, pattern: str, category: str | list, translate: bool = False, result: str = None):
        """
        Осуществляет поиск по заданному патерну и в указанной категории,
        предоставляет возможность перевода патерна и осуществляет проверку результата в зависимости от заданных условий.

    Args:
        search_client: АПИ клиент
        pattern (str): Патерн для поиска.
                       Если указан параметр translate, шаблон может быть переведен на другой язык.
        category (str | list): Категория или список категорий, в которых нужно выполнить поиск. Если категория одна он ищет продукт в ней, если несколько, то в любой из них
                               Если результат поиска принадлежит заданной категории, он учитывается.
        translate (bool, optional): Опция перевода патерна на другой язык.
                                    Если True, патерна переводится перед поиском. По умолчанию False. Если патерн на русском, то перевод будет на английсикй и наоборот
        result (str, optional): Ожидаемый результат поиска.
                                Если указан, возвращаются только те продукты,
                                которые содержат ожидаемый результат в своем названии.
                                Если не указан, то проверяем поисковую выдачу с патерном

        """
        eng_layout = "qwertyuiop[]asdfghjkl;'\zxcvbnm,."
        rus_layout = "йцукенгшщзхъфывапролджэёячсмитьбю"

        products = []
        found = 0
        search_result = self.search(search_client, pattern)
        if translate:
            pattern = translate_text(pattern.lower(), eng_layout, rus_layout) if pattern[
                                                                             0].lower() in eng_layout else translate_text(
                pattern.lower(), rus_layout, eng_layout)



        for product in search_result:
            is_presence_category = any(categ in product['highlight'] for categ in category) if isinstance(category, list) else category in product['highlight']
            if is_presence_category:
                found += 1
                if result:
                    if result.lower() not in product["name"].lower():
                        products.append(product["name"])
                else:
                    if pattern.lower() not in product["name"].lower() and 'test' not in product["name"].lower():
                        products.append(product["name"])
        with allure.step("Проверяем результаты поиска"):
            assert found, 'Нет совпадений в нужной категории'
            assert not products, f"{products=} появились по паттерну {pattern}"

    @allure.step('Проверка подсказок')
    def check_suggestions(self, search_client, pattern, expected_result=None, translate=False):
        """
                Выполняет поиск подсказок по заданному паттерну и проверяет их соответствие ожидаемому результату.

                Args:
                    search_client: Объект клиента для выполнения HTTP-запросов.
                    pattern (str): Строка, по которой выполняется поиск подсказок.
                    expected_result (str, optional): Ожидаемый результат в названии продукта.
                                                     Если указан, проверяется, что все подсказки содержат это значение.
                                                     Если не указан, проверяется, что все подсказки содержат исходный паттерн.
                    translate (bool, optional): Флаг перевода паттерна между русской и английской раскладкой.
                                                По умолчанию False.
        """
        eng_layout = "qwertyuiop[]asdfghjkl;'\zxcvbnm,."
        rus_layout = "йцукенгшщзхъфывапролджэёячсмитьбю"

        if translate and isinstance(pattern, str):
            if pattern[0].lower() in rus_layout:
                pattern = translate_text(pattern.lower(), rus_layout, eng_layout)
            else:
                pattern = translate_text(pattern.lower(), eng_layout, rus_layout)

        response = self.suggestion(search_client, pattern)
        suggestions = []

        for suggestion in response["suggestions"]:
            if expected_result:
                if expected_result.lower() not in suggestion["name"].lower():
                    suggestions.append(suggestion["name"])
            else:
                if pattern.lower() not in suggestion["name"].lower():
                    suggestions.append(suggestion["name"])

        with allure.step("Проверяем результаты подсказок"):
            assert not suggestions, f"{suggestions=} появились по паттерну {pattern}"

    @allure.step('Сравнение результатов поиска')
    def compare_external_search_results(self, search_external_client, search_client, pattern: str, translate: bool = False, result: str = None):
        """
        Сравнивает результаты нового поиска v1 с результатами старого поиска.

        Args:
            search_external_client: клиент для нового поиска v1
            search_client: клиент для старого поиска
            pattern: строка поиска
            translate: требуется ли транслитерация паттерна
            result: ожидаемый результат поиска
        """
        with allure.step("Применяем транслитрацию при необходимости"):
            if translate:
                eng_layout = "qwertyuiop[]asdfghjkl;'\zxcvbnm,."
                rus_layout = "йцукенгшщзхъфывапролджэёячсмитьбю"
                if pattern[0].lower() in eng_layout:
                    pattern = translate_text(pattern.lower(), eng_layout, rus_layout)
                else:
                    pattern = translate_text(pattern.lower(), rus_layout, eng_layout)

        with allure.step("Получаем результаты нового поиска v1"):
            new_search_result = self.search_v1(search_external_client, pattern)
            new_products = []
            for product in new_search_result:
                new_products.append(product["name"])

        with allure.step("Получаем результаты старого поиска"):
            old_products = self.get_all_result(search_client, pattern)

        with allure.step("Сравниваем результаты"):
            assert sorted(new_products) == sorted(old_products), \
                f"Результаты нового поиска отличаются от старого: {new_products} vs {old_products}"






