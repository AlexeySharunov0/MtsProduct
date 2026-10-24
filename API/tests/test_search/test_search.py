import allure
import pytest

from API.models.search.search import Search
from API.utils.helpers import translate_text

eng_layout = "qwertyuiop[]asdfghjkl;'\zxcvbnm,."
rus_layout = "йцукенгшщзхъфывапролджэёячсмитьбю"


@pytest.mark.api
@allure.label('priority', 'Высокий')
@allure.feature("Поиск")
@allure.issue('https://jira.mts.ru/browse/PPI-4516', 'PPInfo - Поиск: выдача результатов')
class TestSearch(Search):

    @allure.title("Проверка поиска по названию")
    @pytest.mark.parametrize("pattern",
                             ["Маркетолог", 'Марк', 'марк', 'АТС', 'Умный', '8-800', 'АОН', 'Бизнес', '*зве', 'Скоринг',
                              'RCS\RBM', 'библиотека'])
    def test_search_name(self, search_client, pattern):

        self.make_search(search_client, pattern=pattern, category='name')

    @allure.title("Проверка поиска по названию с английской раскладкой")
    @pytest.mark.parametrize("pattern", ['vfhr', 'vfhrtnjkju', 'FNC', 'vfhr'])
    def test_search_name_eng(self, search_client, pattern):

        self.make_search(search_client, pattern=pattern, category='name', translate=True)

    @allure.title("Проверка поиска по названию с русской раскладкой")
    @pytest.mark.parametrize("pattern", ['сфырифсл', 'дшму', 'ьгышс', 'ФИЦ', 'сфдд', 'Ашт'])
    def test_search_name_rus(self, search_client, pattern):

        self.make_search(search_client, pattern=pattern, category='name', translate=True)

    @allure.title("Проверка поиска по старому названию")
    @pytest.mark.parametrize("pattern, result",
                             [('test ctujvso', 'Новое название'), ('test fqvxtna', 'Новое название1'),
                              ('test oalxxlb', 'Новое название2')])
    def test_search_old_name(self, search_client, pattern, result):

        self.make_search(search_client, pattern=pattern, category='oldName', result=result)

    @allure.title("Проверка поиска по витрине")
    @pytest.mark.parametrize("pattern, result",
                             [('Марс', 'МТС Поиск'),
                              ('Юпитер', 'МТС Music'),
                              ('Уран', 'Сайт МТС')]
                             )
    def test_search_showcase(self, search_client, pattern, result):

        self.make_search(search_client, pattern=pattern, category='window', result=result)

    @allure.title("Проверка поиска по коду BI")
    @pytest.mark.parametrize("pattern, result",
                             [('BI_1287', 'E-sensor'),
                              ('BI_60', 'МТС Маркетолог'),
                              ('BI_1883', 'MTS Social ads'),
                              ('BI_1921', '1C')])
    def test_search_bi_code(self, search_client, pattern, result):

        self.make_search(search_client, pattern=pattern, category='code.keyword', result=result)

    @allure.title("Проверка поиска по части кода")
    @pytest.mark.parametrize("pattern, result",
                             [('1287', 'E-sensor'),
                              ('1285', 'Skytracking security'),
                              ('1883', 'MTS Social ads'),
                              ('1921', '1C')])
    def test_search_num_code(self, search_client, pattern, result):

        self.make_search(search_client, pattern=pattern, category='code.keyword', result=result)

    @allure.title("Проверка поиска по пользователю")
    @pytest.mark.parametrize("pattern, result",
                             [('Всезнаковый', 'Автотесты_поиск'),
                              ('user-with.all_signs123', 'Автотесты_поиск')]
                             )
    def test_search_users(self, search_client, pattern, result):

        self.make_search(search_client, pattern=pattern, category=['fioEmployees', 'loginEmployees'], result=result)

    @allure.title("Проверка поиска по коду Oracle")
    @pytest.mark.parametrize("pattern, result",
                             [('UDom', 'МТС Умный дом'), ('mMTS', 'Мой МТС'), ('MTSP', 'МТС Premium')])
    def test_search_oracle(self, search_client, pattern, result):

        self.make_search(search_client, pattern=pattern, category='oracleCode', result=result)

    @allure.title("Проверка поиска по приложениям")
    @pytest.mark.parametrize("pattern, result",
                             [('SSO mobile', 'МТС Умный дом'), ('PRO.501', 'МТС Умный дом'),
                              ('PRO501', 'МТС Умный дом')])
    def test_search_app(self, search_client, pattern, result):

        self.make_search(search_client, pattern=pattern, category=['applications_names', 'applications_codes'],
                         result=result)

    @allure.title("Проверка поиска по системе")
    @allure.issue('https://jira.mts.ru/browse/PPI-4498', 'PPInfo - Поиск продукта по названию, команде поддержки ИС')
    @pytest.mark.parametrize("pattern, result", [('mts-cb-dev', 'МТС Cashback'), ('mts-cb', 'МТС Cashback'),
                                                 ('cb-dev', 'МТС Cashback'), ('C/PRM', 'МТС Cashback')])
    def test_search_system(self, search_client, pattern, result):

        self.make_search(search_client, pattern=pattern, category='info_system_names',
                         result=result)

    @allure.title("Поиск по Команде поддержки ИС")
    @allure.issue('https://jira.mts.ru/browse/PPI-4498', 'PPInfo - Поиск продукта по названию, команде поддержки ИС')
    @pytest.mark.parametrize("pattern, result", [('КЦ ИТ Поддержка МТС Cashback', 'МТС Cashback'),
                                                 ('КЦ ВП Stream MaaS', 'МТС Маркетолог')])
    def test_search_help_team_is(self, search_client, pattern, result):

        self.make_search(search_client, pattern=pattern, category='info_system_teams',
                         result=result)

    @allure.title("В поиске удаленные продукты отображаются с корзиной")
    @pytest.mark.parametrize("pattern",
                             ['библиотека'])
    @allure.issue('https://jira.mts.ru/browse/PPI-1081', 'PPInfo - Удаленные продукты в поисковой выдаче')
    def test_search_deleted(self, search_client, pattern):

        products = []
        for product in self.search(search_client, pattern):
            if 'name' in product['highlight']:
                if not product['properties']["isDeleted"] and not product['properties']["isArchive"]:
                    products.append(product["name"])
        with allure.step("Проверяем результаты поиска"):
            assert not products, f"{products=} появились по паттерну {pattern}"

    @allure.title("В поиске у хабов отображается тип Хаб")
    @allure.issue('https://jira.mts.ru/browse/PPI-3674',
                  'PPInfo - Отображать в поиске у хабов текст "Хаб"')
    def test_search_hub_type(self, search_client):

        for product in self.search(search_client, 'хаб'):
            if 'name' in product['highlight']:
                assert product["properties"]["Tip_obieekta_ucheta"][
                           'value'] == 'Хаб', "У продукта не приходит информация что он хаб"

    @allure.title("Сортировка в поисковой выдаче")  # TODO Написать тест нормально
    @pytest.mark.xfail
    def test_sort_in_search_results(self, search_client):

        products = []
        for product in self.search(search_client, 'мтс'):
            if 'name' in product['highlight']:
                name = product['name']
                isInitClose = product['properties'].get('isInitClose', False)
                isArchive = product['properties'].get('isArchive', False)

                if isArchive:
                    p = 3
                elif isInitClose:
                    p = 2
                else:
                    p = 1

                products.append((p, name, isInitClose, isArchive))

        sorted_products = sorted(products, key=lambda x: (x[0], x[1]))

        assert products == sorted_products, 'В поисковой выдаче корректная сортировка'

    @allure.title("Проверка подсказок при поиске")
    @pytest.mark.parametrize("pattern",
                             ['Маркетолог', 'Марк', 'марк', 'Умный', 'мой коннект', '8-800', 'АОН', 'Бизнес',
                              'Скоринг', 'RCS\RBM'])
    def test_suggestion(self, search_client, pattern):

        suggestions = []
        for suggestion, hint_count in zip(self.suggestion(search_client, pattern)["suggestions"], range(3)):
            if hint_count >= 3:
                break
            if pattern.lower() not in suggestion["name"].lower() and 'test' not in suggestion["name"].lower():
                suggestions.append(suggestion["name"])
        with allure.step("Проверяем результаты поиска"):
            assert not suggestions, f"{suggestions=} появились по паттерну {pattern}"

    @allure.title("Проверка количества подсказок при поиске")
    @pytest.mark.parametrize("pattern",
                             ['мтс'])
    def test_suggestion_count(self, search_client, pattern):

        response = self.suggestion(search_client, pattern)
        with allure.step("Проверяем, что подсказки есть"):
            assert response['suggestions'], "Поиск не дал результатов"
        with allure.step("Проверяем количество подсказок"):
            assert len(response['suggestions']) == 7, "Количество подсказок не равно 7"

    @allure.title("Проверка подсказок при поиске по BI коду")
    @pytest.mark.parametrize("pattern, result",
                             [('BI_1287', 'E-sensor'),
                              ('BI_60', 'МТС Маркетолог'),
                              ('BI_1883', 'MTS Social ads'),
                              ('BI_1921', '1C')])
    def test_suggestion_bi_code(self, search_client, pattern, result):

        self.check_suggestions(search_client, pattern=pattern, expected_result=result)

    @allure.title("Проверка подсказок при поиске по части кода")
    @pytest.mark.parametrize("pattern, result",
                             [('1287', 'E-sensor'),
                              ('1285', 'Skytracking security'),
                              ('1883', 'MTS Social ads'),
                              ('1921', '1C')])
    def test_suggestion_num_code(self, search_client, pattern, result):

        self.check_suggestions(search_client, pattern=pattern, expected_result=result)

    @allure.title("Проверка подсказок при поиске по юзеру")
    @pytest.mark.parametrize("pattern, result",
                             [('Всезнаковый', 'Автотесты_поиск'),
                              ('user-with.all_signs123', 'Автотесты_поиск'),
                              ('Никифоров', 'Автотесты_поиск')]
                             )
    def test_suggestion_user(self, search_client, pattern, result):
        with allure.step("Проверям, что нужный продукт найден"):
            assert any(result.lower() in product["name"].lower() for product in
                       self.suggestion(search_client, pattern)["suggestions"]), "Поиск не дал результатов"

    @allure.title("Проверка подсказок при поиске по названию с русской раскладкой")
    @pytest.mark.parametrize("pattern", ['ьгышс', 'ФИЦ'])
    def test_suggestion_name_rus(self, search_client, pattern):

        self.check_suggestions(search_client, pattern=pattern, translate=True)

    @allure.title("Проверка подсказок при поиске по названию с английской раскладкой")
    @pytest.mark.parametrize("pattern", ['vfhrtnjkju', "pdjybn", "fynbahjl"])
    def test_suggestion_name_eng(self, search_client, pattern):

        self.check_suggestions(search_client, pattern=pattern, translate=True)

    @allure.title("Проверка подсказок по поиску по витрине")
    @pytest.mark.parametrize("pattern, result",
                             [('Марс', 'МТС Поиск'),
                              ('Юпитер', 'МТС Music'),
                              ('Уран', 'Сайт МТС')]
                             )
    def test_suggestion_showcase(self, search_client, pattern, result):

        self.check_suggestions(search_client, pattern=pattern, expected_result=result)

    @allure.title("Проверка подсказок по поиску по старому названию")
    @pytest.mark.parametrize("pattern, result",
                             [('test ctujvso', 'Новое название'), ('test fqvxtna', 'Новое название1'),
                              ('test oalxxlb', 'Новое название2')])
    def test_suggestion_old_name(self, search_client, pattern, result):

        self.check_suggestions(search_client, pattern=pattern, expected_result=result)

    @allure.title("Проверка подсказок по поиску по Oracle")
    @pytest.mark.parametrize("pattern, result",
                             [('UDom', 'МТС Умный дом'), ('mMTS', 'Мой МТС')])
    def test_suggestion_oracle(self, search_client, pattern, result):

        self.check_suggestions(search_client, pattern=pattern, expected_result=result)

    @allure.title("Проверка подсказок по поиску по приложениям")
    @pytest.mark.parametrize("pattern, result",
                             [('SSO mobile', 'МТС Умный дом'), ('PRO.501', 'МТС Умный дом'),
                              ('PRO501', 'МТС Умный дом'), ('CB_ACC', 'МТС Cashback')])
    def test_suggestion_app(self, search_client, pattern, result):

        self.check_suggestions(search_client, pattern=pattern, expected_result=result)

    @allure.title("Подсказки по системе")
    @allure.issue('https://jira.mts.ru/browse/PPI-4498', 'PPInfo - Поиск продукта по названию, команде поддержки ИС')
    @pytest.mark.parametrize("pattern, result", [('mts-cb-dev', 'МТС Cashback'), ('mts-cb', 'МТС Cashback'),
                                                 ('cb-dev', 'МТС Cashback'), ('C/PRM', 'МТС Cashback')])
    def test_suggestion_system(self, search_client, pattern, result):

        self.check_suggestions(search_client, pattern=pattern, expected_result=result)

    @allure.title("Подсказки по Команде поддержки ИС")
    @allure.issue('https://jira.mts.ru/browse/PPI-4498', 'PPInfo - Поиск продукта по названию, команде поддержки ИС')
    @pytest.mark.parametrize("pattern, result", [('КЦ ИТ Поддержка МТС Cashback', 'МТС Cashback'),
                                                 ('BIM Virtual Group', 'МТС Тестировани')])
    def test_suggestion_help_team_is(self, search_client, pattern, result):

        self.check_suggestions(search_client, pattern=pattern, expected_result=result)

    @allure.title("Проверка наличия подсказон 'Архив' и 'Удалён' в поиске")
    @allure.issue("https://jira.mts.ru/browse/PPI-4603", "PPInfo - В подсказках в поиске отображать, что продукт архивный ")
    @pytest.mark.parametrize(
        "search_text, expected_archive, expected_deleted",
        [
            ("1100", True, False),
            ("тест 1108", False, True),
        ]
    )
    def test_search_suggestions_have_archive_and_deleted_api(self, search_client, search_text, expected_archive,
                                                         expected_deleted):
        with allure.step(f"Отправляем запрос на поиск: '{search_text}'"):
            response = self.suggestion(search_client, pattern=search_text)

        with allure.step("Проверяем флаги 'isStatusArchive' и 'isDeleted' в результатах"):
            for suggestion in response["suggestions"]:
                assert suggestion["isStatusArchive"] == expected_archive, \
                    f"Флаг 'isStatusArchive' имеет значение {suggestion['isStatusArchive']}, ожидалось {expected_archive}"
                assert suggestion["isDeleted"] == expected_deleted, \
                    f"Флаг 'isDeleted' имеет значение {suggestion['isDeleted']}, ожидалось {expected_deleted}"

    @allure.title("Проверка подсказок по коду сервиса")
    @allure.issue("https://jira.mts.ru/browse/PPI-3819", "PPInfo - Поиск продукта по коду и названию сервиса")
    @pytest.mark.parametrize("pattern, expected_result", [
        ("SBS.2111", "Apple Music"),
        ("SBS.2112", "Apple Music"),
    ])
    def test_suggestion_by_service_code(self, search_client, pattern, expected_result):
        with allure.step(f"Отправляем запрос на поиск: '{pattern}'"):
            response = self.suggestion(search_client, pattern)

        with allure.step("Проверяем, что есть хотя бы одна подходящая подсказка"):
            assert any(expected_result in suggestion["name"] for suggestion in response["suggestions"]), \
                f"Подсказка с '{expected_result}' не найдена по паттерну '{pattern}'"

    @allure.title("Проверка подсказок по названию сервиса")
    @allure.issue("https://jira.mts.ru/browse/PPI-3819", "PPInfo - Поиск продукта по коду и названию сервиса")
    @pytest.mark.parametrize("pattern, expected_result", [
        ("[Инфраструктура] Apple Music", "Apple Music"),
        ("[Временный] Apple Music", "Apple Music"),
    ])
    def test_suggestion_by_service_name(self, search_client, pattern, expected_result):
        with allure.step(f"Отправляем запрос на поиск: '{pattern}'"):
            response = self.suggestion(search_client, pattern)

        with allure.step("Проверяем, что есть хотя бы одна подходящая подсказка"):
            assert any(expected_result in suggestion["name"] for suggestion in response["suggestions"]), \
                f"Подсказка с '{expected_result}' не найдена по паттерну '{pattern}'"

    @allure.title("Проверка нового поиска по названию")
    @pytest.mark.parametrize('pattern',
                             ['Маркетолог', 'Марк', 'марк', 'АТС', 'Умный', '8-800', 'АОН', 'Бизнес', '*зве', 'Скоринг',
                              r'RCS\RBM', 'библиотека'])
    def test_external_search_name(self, search_external_client, search_client, pattern):

        self.compare_external_search_results(search_external_client, search_client, pattern)

    @allure.title("Проверка нового поиска по названию с английской раскладкой")
    @pytest.mark.parametrize("pattern", ['vfhr', 'vfhrtnjkju', 'FNC', 'vfhr'])
    def test_external_search_name_eng(self, search_external_client, search_client, pattern):

        self.compare_external_search_results(search_external_client, search_client, pattern, translate=True)

    @allure.title("Проверка нового поиска по названию с русской раскладкой")
    @pytest.mark.parametrize("pattern", ['сфырифсл', 'дшму', 'ьгышс', 'ФИЦ', 'сфдд', 'Ашт'])
    def test_external_search_name_rus(self, search_external_client, search_client, pattern):

        self.compare_external_search_results(search_external_client, search_client, pattern, translate=True)

    @allure.title("Проверка нового поиска по старому названию")
    @pytest.mark.parametrize("pattern, result",
                             [('test ctujvso', 'Новое название'), ('test fqvxtna', 'Новое название1'),
                              ('test oalxxlb', 'Новое название2')])
    def test_external_search_old_name(self, search_external_client, search_client, pattern, result):

        self.compare_external_search_results(search_external_client, search_client, pattern, result=result)

    @allure.title("Проверка нового поиска по витрине")
    @pytest.mark.parametrize("pattern, result",
                             [('Марс', 'МТС Поиск'),
                              ('Юпитер', 'МТС Music'),
                              ('Уран', 'Сайт МТС')]
                             )
    def test_external_search_showcase(self, search_external_client, search_client, pattern, result):

        self.compare_external_search_results(search_external_client, search_client, pattern, result=result)

    @allure.title("Проверка нового поиска по коду BI")
    @pytest.mark.parametrize("pattern, result",
                             [('BI_1287', 'E-sensor'),
                              ('BI_60', 'МТС Маркетолог'),
                              ('BI_1883', 'MTS Social ads'),
                              ('BI_1921', '1C')])
    def test_external_search_bi_code(self, search_external_client, search_client, pattern, result):

        self.compare_external_search_results(search_external_client, search_client, pattern, result=result)

    @allure.title("Проверка нового поиска по части кода")
    @pytest.mark.parametrize("pattern, result",
                             [('1287', 'E-sensor'),
                              ('1285', 'Skytracking security'),
                              ('1883', 'MTS Social ads'),
                              ('1921', '1C')])
    def test_external_search_num_code(self, search_external_client, search_client, pattern, result):

        self.compare_external_search_results(search_external_client, search_client, pattern, result=result)

    @allure.title("Проверка нового поиска по пользователю")
    @pytest.mark.parametrize("pattern, result",
                             [('Всезнаковый', 'Автотесты_поиск'),
                              ('user-with.all_signs123', 'Автотесты_поиск'),
                              ('Никифоров', 'Автотесты_поиск')]
                             )
    def test_external_search_users(self, search_external_client, search_client, pattern, result):

        self.compare_external_search_results(search_external_client, search_client, pattern, result=result)

    @allure.title("Проверка нового поиска по коду Oracle")
    @pytest.mark.parametrize("pattern, result",
                             [('UDom', 'МТС Умный дом'), ('mMTS', 'Мой МТС'), ('MTSP', 'МТС Premium')])
    def test_external_search_oracle(self, search_external_client, search_client, pattern, result):

        self.compare_external_search_results(search_external_client, search_client, pattern, result=result)

    @allure.title("Проверка нового поиска по приложениям")
    @pytest.mark.parametrize("pattern, result",
                             [('SSO mobile', 'МТС Умный дом'), ('PRO.501', 'МТС Умный дом'),
                              ('PRO501', 'МТС Умный дом')])
    def test_external_search_app(self, search_external_client, search_client, pattern, result):

        self.compare_external_search_results(search_external_client, search_client, pattern, result=result)

    @allure.title("Проверка нового поиска по системе")
    @allure.issue('https://jira.mts.ru/browse/PPI-4498', 'PPInfo - Поиск продукта по названию, команде поддержки ИС')
    @pytest.mark.parametrize("pattern, result", [('mts-cb-dev', 'МТС Cashback'), ('mts-cb', 'МТС Cashback'),
                                                 ('cb-dev', 'МТС Cashback'), ('C/PRM', 'МТС Cashback')])
    def test_external_search_system(self, search_external_client, search_client, pattern, result):

        self.compare_external_search_results(search_external_client, search_client, pattern, result=result)

    @allure.title("Проверка нового поиска по Команде поддержки ИС")
    @allure.issue('https://jira.mts.ru/browse/PPI-4498', 'PPInfo - Поиск продукта по названию, команде поддержки ИС')
    @pytest.mark.parametrize("pattern, result", [('КЦ ИТ Поддержка МТС Cashback', 'МТС Cashback'),
                                                 ('КЦ ВП Stream MaaS', 'МТС Маркетолог')])
    def test_external_search_help_team_is(self, search_external_client, search_client, pattern, result):

        self.compare_external_search_results(search_external_client, search_client, pattern, result=result)

    @allure.title('Проверка нового поиска с параметрами limit')
    @allure.issue('https://jira.mts.ru/browse/PPI-2506',
                  'PPInfo - Добавить параметры limit, offset в метод /search/ в External API')
    @pytest.mark.parametrize('limit', [1, 5, 10])
    def test_external_search_limit(self, search_external_client, limit):
        assert len(self.search_v1(search_external_client, pattern='test',
                                  limit=limit)) == limit, 'Итоговый результат не совпадает с ожидаемым'

    @allure.title('Проверка нового поиска с параметрами offset')
    @allure.issue('https://jira.mts.ru/browse/PPI-2506',
                  'PPInfo - Добавить параметры limit, offset в метод /search/ в External API')
    @pytest.mark.parametrize('offset', [0, 5, 10])
    def test_external_search_offset(self, search_external_client, offset):
        products_before = self.search_v1(search_external_client, 'тест')
        products_after = self.search_v1(search_external_client, pattern='тест', offset=offset)
        with allure.step('Проверяем, что сдвиг работает'):
            assert products_before[offset] == products_after[0], 'Элементы не сдвинулись'

    @allure.title("Проверка нового поиска по полному названию сервиса")
    @allure.issue("https://jira.mts.ru/browse/PPI-3819", "PPInfo - Поиск продукта по коду и названию сервиса")
    @pytest.mark.parametrize("pattern, result", [
        ("[Инфраструктура] Apple Music", "Apple Music"),
        ("[Временный] Apple Music", "Apple Music")
    ])
    def test_external_search_by_service_full_name(self, search_external_client, search_client, pattern, result):
        products = []
        if search_result := self.search_v1(search_external_client, pattern):
            for product in search_result:
                products.append(product["name"])
        with allure.step("Проверяем результаты поиска"):
            assert self.get_all_result(search_client, pattern) == products, \
                f"Результат нового поиска {products=} отличается от результатов старого поиска"

    @allure.title("Проверка нового поиска по коду сервиса")
    @allure.issue("https://jira.mts.ru/browse/PPI-3819", "PPInfo - Поиск продукта по коду и названию сервиса")
    @pytest.mark.parametrize("pattern, result",
                             [("SBS.2111", "Apple Music"), ("SBS.2112", "Apple Music")])
    def test_external_search_by_service_code(self, search_external_client, search_client, pattern, result):
        products = []
        if search_result := self.search_v1(search_external_client, pattern):
            for product in search_result:
                products.append(product["name"])
        with allure.step("Проверяем результаты нового поиска"):
            assert self.get_all_result(search_client, pattern) == products, \
                f"Результат нового поиска {products=} отличается от результатов старого поиска"

    @allure.title("Проверка поиска по коду сервиса")
    @allure.issue("https://jira.mts.ru/browse/PPI-3819", "PPInfo - Поиск продукта по коду и названию сервиса")
    @pytest.mark.parametrize("pattern, result",
                             [("SBS.2111", "Apple Music"), ("SBS.2112", "Apple Music")])
    def test_search_by_service_code_api(self, search_client, pattern, result):
        self.make_search(search_client, pattern=pattern, category='codes_realizes_service', result=result)

    @allure.title("Проверка поиска по полному названию сервиса")
    @allure.issue("https://jira.mts.ru/browse/PPI-3819", "PPInfo - Поиск продукта по коду и названию сервиса")
    @pytest.mark.parametrize("pattern, result",
                             [("[Инфраструктура] Apple Music", "Apple Music"),
                              ("[Временный] Apple Music", "Apple Music")])
    def test_search_by_service_full_name_api(self, search_client, pattern, result):
        self.make_search(search_client, pattern=pattern, category='names_realizes_service', result=result)
