import time

import allure
import pytest

from API.models.cache.cache import Cache
from API.models.ppinfo.product_v1 import ProductV1
from API.models.ppinfo.rest import Rest


@pytest.mark.last
@pytest.mark.api
@allure.feature("Кэш категории, каунтеры")
class TestCache(Rest, ProductV1):

    @allure.title("При создание продукта он попадает в 'Новые'")
    @pytest.mark.parametrize("product_type", ["Vneshnii", "Vnutrennii"])
    def test_new_cache_add(self, cache_client, ppinfo_client, product_type):
        with allure.step("Добавляем новый продукт"):
            data = self.get_data_for_product_creation(product_type, status="(PPinfo_status)Pilot")
            product_id = self.create_product(ppinfo_client, data)
            time.sleep(30)
            new_products = self.get_new_products(cache_client)
        with allure.step("Есть ли новый продукт на главной странице"):
            assert any(product["code"] == product_id for product in new_products), f"Продукта {product_id} нет в ответе API New"

    @allure.title("Сравнение id созданного продукта (архив) с id продукта API Cache Close")
    @allure.issue("https://jira.mts.ru/browse/PPI-3272", "PPInfo - Отображение продуктов, которые закрылись за последние 30 дней")
    @pytest.mark.parametrize("product_type", ["Vneshnii", "Vnutrennii"])
    def test_close_cache_add_archive(self, cache_client, ppinfo_client, product_type, clear_db_products):
        with allure.step("Добавляем новый продукт"):
            product_id = self.create_product(ppinfo_client, self.get_data_for_product_creation(product_type, status='Arkhiv'))
            time.sleep(40)
            close_products = self.get_close_products(cache_client)
        with allure.step("Есть ли новый продукт на главной странице"):
            products_in_close = []
            for product in close_products:
                assert product["properties"][
                    "isArchive"
                ], f'В продукте {product["name"]} атрибут isArchive = {product["properties"]["isNew"]}'
                products_in_close.append(product["code"])

            assert product_id in products_in_close, f"Созданного продукта {product_id} нет в ответе API Categories {products_in_close}"

    @allure.title("Создание хаба категории 'Идея' и проверка его отображения в Новых идеях")
    def test_idea_cache_add_idea(self, cache_client, ppinfo_client):
        with allure.step("Готовим данные для создания хаба"):
            name = self.text
            data = self.get_data_for_hub_creation(name)

        with allure.step("Создание хаба"):
            self.create_hub(ppinfo_client, data)

        time.sleep(30)

        with allure.step("Проверяем, что Идея отобразился в Новых идеях"):
            hubs = self.get_new_idea_hubs(cache_client)

            assert any(hub['name'] == name for hub in hubs), f"Идея '{name}' не найдена в Новых идеях"

    @allure.title("Удаленный продукт не отображается в Новых")
    @allure.issue(
        "https://jira.mts.ru/browse/PPI-3266",
        'PPInfo - Доработка замечаний блока "Новое в PPInfo"',
    )
    @pytest.mark.parametrize("product_type", ["Vneshnii", "Vnutrennii"])
    def test_new_cache_add_deleted(
            self, cache_client, ppinfo_client, pmd_internal_gw_client, product_type
    ):
        with allure.step("Добавляем новый продукт"):
            data = self.get_data_for_product_creation(
                product_type, status="(PPinfo_status)Pilot"
            )
            product_id = self.create_product(ppinfo_client, data)
            time.sleep(40)
            new_products = self.get_new_products(cache_client)
        with allure.step("Есть ли новый продукт на главной странице"):
            assert any(
                product["code"] == product_id for product in new_products), 'Созданный продукт не отображается в Новых'

        with allure.step("Удаляем продукт и смотрим, есть ли он в API New"):
            self.delete_product(pmd_internal_gw_client, bi=product_id)
            time.sleep(40)
            assert not any(product["code"] == product_id for product in
                           self.get_close_products(cache_client)), 'Удаленный продукт не отображается в Закрытых'

            assert not any(product["code"] == product_id for product in
                           self.get_new_products(cache_client)), 'Удаленный продукт не отображается в Новых'

    @allure.title("Сортировка на странице Продукты")
    @pytest.mark.parametrize(
        "direction",
        [
            "Все направления",
            "Телеком",
            "Финтех",
            "Медиа",
            "Ad-teh",
            "MWS",
            "Юрент",
            "УК Экосистемы МТС",
        ],
    )
    @pytest.mark.parametrize(
        "group", ["Maintenance_R&D", "Growth_R&D", "Venchurnoe_R&D"]
    )
    def test_sort_on_product_page(self, cache_client, direction, group):

        products = []

        direction = self.get_sections_codes[direction]

        for i in self.get_products_on_main_page(cache_client, direction)["sections"]:
            if i["code"] == "all":
                for action in i["subSections"]:
                    if action["code"] == group:
                        for product in action["products"]:
                            name = product["name"]
                            isInitClose = product["properties"].get(
                                "isInitClose", False
                            )
                            isEcosystemProduct = product["properties"].get(
                                "isEcosystemProduct", False
                            )
                            products.append((name, isInitClose, isEcosystemProduct))

        sorted_products = sorted(products, key=lambda x: (x[1], (not x[2], x[0]) if not x[1] else x[0]))

        assert products == sorted_products, "Сортировка на странице продуктов некорректная"

    @allure.title("Сортировка на странице Хабы")
    @pytest.mark.parametrize(
        "direction",
        [
            "Все направления",
            "Телеком",
            "Финтех",
            "Медиа",
            "Ad-teh",
            "MWS",
            "Юрент",
            "УК Экосистемы МТС",
        ],
    )
    def test_sort_on_hubs_page(self, cache_client, direction):

        products = []

        direction = self.get_sections_codes[direction]

        for i in self.get_hubs_on_main_page(cache_client, direction)["sections"]:
            if i["code"] == "all":
                for product in i["products"]:
                    name = product["name"]
                    isInitClose = product["properties"].get("isInitClose", False)
                    isEcosystemProduct = product["properties"].get(
                        "isEcosystemProduct", False
                    )
                    products.append((name, isInitClose, isEcosystemProduct))

        sorted_products = sorted(products, key=lambda x: (x[1], (not x[2], x[0]) if not x[1] else x[0]))

        assert products == sorted_products, "Сортировка на странице продуктов некорректная"

    @allure.title("Сортировка на странице Архивные")
    @pytest.mark.parametrize("group", ["archive", "deleted"])
    def test_sort_on_archive_page(self, cache_client, group):

        products = []

        for i in self.get_archive_on_main_page(cache_client):
            if i["code"] == group:
                for product in i["products"]:
                    name = product["name"]
                    products.append(name)

        sorted_products = sorted(products)

        assert (products == sorted_products), "Сортировка на странице продуктов некорректная"

    @allure.title("При создание продукта/хаба/архивного продукта тотал увеличивается")
    @pytest.mark.parametrize("product_type", ["product", "hub", 'archive'])
    def test_counter_cache_with_add(self, cache_client, ppinfo_client, product_type):
        with allure.step("Запрос на кеш тотал до создания продукта"):
            total_before = self.total(cache_client)

        with allure.step("Добавляем новый продукт"):
            if product_type == "product":
                data = self.get_data_for_product_creation('Vneshnii', status="(PPinfo_status)Waiting_decision")
            if product_type == "hub":
                data = self.get_data_for_hub_creation(self.text)
            if product_type == "archive":
                data = self.get_data_for_product_creation('Vneshnii')

            self.create_product(ppinfo_client, data)
            time.sleep(30)

        with allure.step("Запрос на кеш тотал после создания продукта"):
            total_after = self.total(cache_client)

        with allure.step("Проверка увеличения количества продуктов"):
            before = total_before[product_type]
            after = total_after[product_type]

            assert after > before, f"Ожидалось увеличение количества продуктов. Было: {before}, стало: {after}"

    @allure.title("Проверка изменения count в фильтре SYSTEM_ProductType после добавления внешнего продукта")
    @pytest.mark.parametrize("is_product", ["product", "hub"])
    @pytest.mark.parametrize("product_type", ["Vneshnii", "Vnutrennii"])
    def test_product_filter_count_value_change_after_add(self, cache_client, ppinfo_client, clear_db_products,
                                                         product_type, is_product):

        with allure.step("Получаем кол-во продуктов в фильтре до добавления продукта"):
            total_before = self.get_filter_count(cache_client, product_type, is_product)

        with allure.step("Добавляем новый продукт"):
            if is_product == "product":
                data = self.get_data_for_product_creation(product_type, status="(PPinfo_status)Waiting_decision")
            if is_product == "hub":
                data = self.get_data_for_hub_creation(self.text, product_type)

            self.create_product(ppinfo_client, data)
        with allure.step("Получаем кол-во продуктов в фильтре после добавления продукта"):
            self.wait_for_count_change(cache_client, product_type, is_product, total_before)

    @allure.title('Проверка, что в фильтре "Тип продукта" нет значения "Не определено" при includeAtomic=true')
    @allure.issue("https://jira.mts.ru/browse/PPI-3370","PPinfo - В фильтрах у атомарных продуктов тип продукта отображен как Не определено")
    def test_system_product_type_filter_no_blank(self, cache_client):
        filters = self.get_products_on_main_page(
            cache_client, direction="all", with_atomic="true")["filters"]

        for f in filters:
            if f["code"] == "SYSTEM_ProductType":
                for value in f["values"]:
                    assert value["code"] in ["Vneshnii", "Vnutrennii"], f'Значение в фильтре SYSTEM_ProductType: {value["code"]} не равно "Vneshnii" или "Vnutrennii"'

    @allure.title("При включении тогла атомарные, архивные продукты не приходят в фильтрах")
    @allure.issue("https://jira.mts.ru/browse/PPI-4225", "PPinfo - При включении тогла Атомарные в фильтрах также видны архивные/удалённые атомарные продукты")
    def test_filter_archived_atomic_absence(self, cache_client):
        filters = self.get_products_on_main_page(cache_client, "all", "true")["filters"]

        statuses_in_filter = []
        for item in filters:
            if item["code"] == "PPinfo_status":
                for status in item["values"]:
                    statuses_in_filter.append(status["code"])

        assert "Arkhiv" not in statuses_in_filter, "При включении тогла атомарных в фильтры попали архивные продукты"

    @allure.title('При включение тогла "Включая атомарные" в фильтрах происходит пересчет продуктов')
    @pytest.mark.parametrize("is_product", ["product", "hub"])
    def test_filter_counts_with_atomic_toggle(self, cache_client, ppinfo_client, is_product):

        atomic_len = None
        total = self.total(cache_client)[is_product]
        filters = None

        if is_product == "product":
            filters = self.get_products_on_main_page(cache_client, "all", "true")["filters"]
            atomic_len = len(self.get_only_active_atomics(ppinfo_client))

        if is_product == "hub":
            filters = self.get_hubs_on_main_page(cache_client, "all", "true")["filters"]
            atomic_len = len(self.get_only_active_hub_atomics(ppinfo_client))

        for item in filters:
            expected = total + atomic_len
            assert item["total"] == expected, f'Для {is_product}: ожидалось {expected}, а получили {item["total"]} в фильтре {item["code"]}'


###########################################################################Тесты с редисом


@pytest.mark.last
@pytest.mark.api
@allure.feature("Редис")
class TestRedis(Cache, ProductV1):
    @allure.title("Проверка изменения Бренда в кеш сервисе при изменении значения в продукте")
    @allure.issue("https://jira.mts.ru/browse/PPI-1037","PPInfo - Добавление карточки продукта в распределенный кэш")
    def test_redis_brand(self, ppinfo_client):
        try:

            if "PPinfo_MTS_Brand" in self.get_info_from_redis()["properties"]:
                assert self.get_info_from_redis()["properties"]["PPinfo_MTS_Brand"] == [
                    {"code": "(PPinfo_MTSBrand)MTSBrand_yes", "value": "Старый бренд "}
                ], "Информация в редис неверная"

            data = {
                "id": "BI_2769",
                "attributes": [
                    {
                        "id": "PPinfo_MTS_Brand",
                        "values": [
                            {
                                "code": "Brend_MTS_ekosistema",
                                "value": "Бренд МТС экосистема",
                            }
                        ],
                    }
                ],
                "notification": False,
                "type": "",
            }

            self.change_product(ppinfo_client, data)

            time.sleep(15)

            if "PPinfo_MTS_Brand" in self.get_info_from_redis()["properties"]:
                assert self.get_info_from_redis()["properties"]["PPinfo_MTS_Brand"] == [
                    {"code": "Brend_MTS_ekosistema", "value": "Бренд МТС экосистема"}
                ], "Информация в редис неверная"
        finally:

            data = {
                "id": "BI_2769",
                "attributes": [
                    {
                        "id": "PPinfo_MTS_Brand",
                        "values": [
                            {
                                "code": "(PPinfo_MTSBrand)MTSBrand_yes",
                                "value": "Старый бренд ",
                            }
                        ],
                    }
                ],
                "notification": False,
                "type": "",
            }

            self.change_product(ppinfo_client, data)

    @allure.title("Проверка изменения продукт овнера в кеш сервисе при изменерия значения в продукте")
    @allure.issue("https://jira.mts.ru/browse/PPI-1037","PPInfo - Добавление карточки продукта в распределенный кэш")
    def test_redis_po(self):

        assert self.get_info_from_redis()["properties"]["employee_product_owner"], "Продукт Овнер не пришел в свойствах"

    @allure.title("При синхронизации по продукту зависимости появляются")
    @allure.issue("https://jira.mts.ru/browse/PPI-4123","PPInfo - Отображение и создание зависимостей на продукте")
    def test_get_dependency_by_product(self, cache_client):

        self.delete_dependence_from_redis()

        self.get_dependencies_by_product_code_404(cache_client)

        self.sync_dependencies_by_product_code(cache_client, "BI_2201")

        dependence_after_delete = self.get_dependencies_by_product_code(cache_client)
        if_dependence_exist = False
        for dependency in dependence_after_delete.values():
            if isinstance(dependency, list):
                for quarter in dependency:
                    if quarter["dependencies"]:
                        if_dependence_exist = True

        assert if_dependence_exist, "В продукте не появились зависимости после синхронизации"

    @allure.title("При синхронизации по продукту зависимости появляются")
    @allure.issue("https://jira.mts.ru/browse/PPI-4123","PPInfo - Отображение и создание зависимостей на продукте")
    def test_get_dependency_all_products(self, cache_client):

        self.delete_dependence_from_redis(delete_all=True)

        self.get_dependencies_by_product_code_404(cache_client)

        self.sync_dependencies_all_products(cache_client)

        dependence_after_delete = self.get_dependencies_by_product_code(cache_client)
        if_dependence_exist = False
        for dependency in dependence_after_delete.values():
            if isinstance(dependency, list):
                for quarter in dependency:
                    if quarter["dependencies"]:
                        if_dependence_exist = True

        assert if_dependence_exist, "В продукте не появились зависимости после синхронизации"
