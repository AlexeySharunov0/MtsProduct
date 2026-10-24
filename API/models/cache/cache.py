import json
import time
from typing import Any

import allure
import redis

from API.api_fixtures import vault
from API.data.cache import Total, New, Close, Idea
from API.models.ppinfo.product_v1 import ProductV1


class CacheUrls:
    '''
    https://stage.prodboard.example.com/cache/swagger/index.html
    '''

    # Отображение продуктов, добавленных за последние 30 дней
    NEW = 'v2/new'

    # Отображение продуктов, закрытых за последние 30 дней
    CLOSE = 'v2/close'

    # Новые идеи на главной странице
    IDEAS = "v2/hub"

    # Каунтеры количества продуктов на главной странице согласно Типам продукта
    TOTAL = 'v2/total'

    # Получение Продуктов для главной страницы
    MAIN_PAGE_PRODUCTS = 'v1/tab/product'

    # Получение Продуктов для главной страницы
    MAIN_PAGE_HUBS = 'v1/tab/hub'

    # Получение Продуктов для главной страницы
    MAIN_PAGE_ARCHIVE = 'v1/tab/archive'

    # Ручка для раздела 'Мой портфель' на сайте
    # Пока НЕ тестируем
    PORTFOLIO = 'rest/api/v1/portfolio'

    # Синхронизация зависимостей по всем продуктам
    SYNC_ALL_PRODUCTS = 'v1/dependency'

    # Синхронизация зависимостей по конкретному продукту
    SYNC_BY_PRODUCT_CODE = 'v1/dependency/{}'

    # Получение зависимостей по конкретному продукту
    GET_DEPENDENCY_BY_PRODUCT_CODE = 'v1/dependency/{}'


class Cache(CacheUrls, ProductV1):

    @allure.step("Получаем count для типа продукта")
    def get_filter_count(self, cache_client: Any, product_type: str, is_product: str) -> int:
        """
        Получает текущее значение count для указанного типа продукта из фильтра SYSTEM_ProductType.

        Args:
            is_product: Флаг, указывающий на то, работаем с хабами или продуктами.
            cache_client (Any): Клиент для взаимодействия с кешем.
            product_type (str): Код типа продукта, для которого нужно получить count.

        Returns:
            int: Текущее значение count для указанного типа продукта.
    """
        if is_product == 'hub':
            filters = self.get_hubs_on_main_page(cache_client, direction='all', with_atomic='true')['filters']
        else:
            filters = self.get_products_on_main_page(cache_client, direction='all', with_atomic='true')['filters']

        for f in filters:
            if f['code'] == 'SYSTEM_ProductType':
                for v in f['values']:
                    if v['code'] == product_type:
                        return v['count']

    @allure.step('Запрос на кеш тотал')
    def total(self, client) -> dict[str, Any]:
        with allure.step('Получаем кеш тотал всех типов продуктов'):
            total = client.get(self.TOTAL)
            Total(**total)
            return total

    @allure.step('Запрос на кеш New')
    def get_new_products(self, client) -> list[dict[str, Any]]:
        with allure.step('Получаем кеш New'):
            response = client.get(self.NEW)
        with allure.step('Проверяем модель ответа и статус код'):
            New(news=response)
            return response

    @allure.step('Запрос на кеш Close')
    def get_close_products(self, client) -> list[dict[str, Any]]:
        with allure.step('Получаем кеш Close'):
            response = client.get(self.CLOSE)
        with allure.step('Проверяем модель ответа и статус код'):
            Close(close=response)
            return response

    @allure.step('Получение хабов из раздела "Новые идеи"')
    def get_new_idea_hubs(self, client) -> list[dict[str, Any]]:
        with allure.step('Получаем кеш Ideas'):
            response = client.get(self.IDEAS)
        with allure.step('Проверяем модель ответа и статус код'):
            Idea(close=response)
            return response

    @allure.step('Ожидание изменения count в фильтре')
    def wait_for_count_change(self, cache_client: Any, product_type: str, is_product: str, total_before: int):
        start_time = time.time()
        timeout = 60
        interval = 5
        while time.time() - start_time < timeout:
            total_after = self.get_filter_count(cache_client, product_type, is_product)
            if total_after > total_before:
                break
            time.sleep(interval)
        else:
            raise AssertionError(f"Каунтер не изменился за {timeout} секунд")

    @allure.step('Связь с редисом')
    def get_info_from_redis(self) -> dict[str, Any]:
        '''
        Получает и возвращает информацию о продукте из Redis.

        Метод подключается к Redis с использованием параметров доступа из vault,
        затем извлекает значение из хэш-таблицы с ключом 'productCards' и полем '2769',
        декодирует полученную строку и преобразует её из формата JSON в словарь Python.

        Returns:
            Dict[str, Any]: Словарь с данными продукта, полученными из Redis.
        '''
        with allure.step('Получаем данные из Редиса'):
            redis_client = redis.Redis(
                host=vault.get_creds('main')['redis_host'],
                port=vault.get_creds('main')['redis_port'],
                client_name=vault.get_creds('main')['redis_client_name'],
                password=vault.get_creds('main')['redis_password'],
            )

            product = redis_client.hget('productCards', '2769').decode()

            return json.loads(product)

    @allure.step('Синхронизация зависимостей по всем продуктам')
    def sync_dependencies_all_products(self, client) -> None:
        client.post(self.SYNC_ALL_PRODUCTS, raw_format=True)

    @allure.step('Синхронизация зависимостей по конкретному продукту')
    def sync_dependencies_by_product_code(self, client, product_id: str) -> None:
        client.post(self.SYNC_BY_PRODUCT_CODE.format(product_id), raw_format=True)

    @allure.step('Получение зависимостей по продукту')
    def get_dependencies_by_product_code(self, client, bi_code: str = 'BI_2201') -> dict[str, dict[str, Any]]:
        response = client.get(self.SYNC_BY_PRODUCT_CODE.format(bi_code))

        return response

    @allure.step('Получение зависимостей по продукту, при отсутствии зависимостей')
    def get_dependencies_by_product_code_404(self, client, bi_code: str = 'BI_2201', ) -> None:
        client.get(self.SYNC_BY_PRODUCT_CODE.format(bi_code), expected_status_code=404)

    @allure.step('Удаление зависимостей из редиса')
    def delete_dependence_from_redis(self, bi_code: str = 'BI_2201', delete_all: bool = False):
        '''
            Удаляет зависимости из Redis по ключу 'dependency'.

            Если параметр delete_all установлен в True, метод удаляет все поля
            (все зависимости) из хэша 'dependency'. В противном случае удаляется
            зависимость только по конкретному bi_code.

        Args:
            bi_code (str): Код зависимости, которую нужно удалить. Используется только,
                если delete_all=False. По умолчанию 'BI_2201'.
            delete_all (bool): Флаг, указывающий на необходимость удалить все зависимости.
                Если True — удаляются все поля из 'dependency'. По умолчанию False.

        Returns:
            None
        '''
        redis_client = redis.Redis(
            host=vault.get_creds('main')['redis_host'],
            port=vault.get_creds('main')['redis_port'],
            client_name=vault.get_creds('main')['redis_client_name'],
            password=vault.get_creds('main')['redis_password'],
        )

        if delete_all:
            fields = redis_client.hkeys('dependency')

            if fields:
                redis_client.hdel('dependency', *fields)
            return

        product = redis_client.hget('dependency', bi_code)
        if product is not None:
            redis_client.hdel('dependency', bi_code)

    @property
    def get_sections_codes(self):
        return {
            'Все направления': 'all',
            'Телеком': 'Telekom',
            'Финтех': 'Fintekh',
            'Медиа': 'Media',
            'Ad-teh': 'Ad-teh',
            'MWS': 'MWS',
            'Юрент': 'Iurent',
            'УК Экосистемы МТС': 'Ekosistema',
        }

    @allure.step('Получение Продуктов на главной странице')
    def get_products_on_main_page(self, client, direction, with_atomic: str = 'false') -> dict[str, Any]:
        params = {
            'direction': direction,
        }

        if with_atomic == 'true':
            params['includeAtomic'] = 'true'

        response = client.get(self.MAIN_PAGE_PRODUCTS, params=params)

        return response

    @allure.step('Получение Хабов на главной странице')
    def get_hubs_on_main_page(self, client, direction, with_atomic: str = 'false') -> dict[str, Any]:
        params = {
            'direction': direction,
        }

        if with_atomic == 'true':
            params['includeAtomic'] = 'true'

        response = client.get(self.MAIN_PAGE_HUBS, params=params)

        return response

    @allure.step('Получение хабов из раздела "Новые идеи"')
    def get_new_idea_hubs(self, client) -> dict[str, Any]:
        response = client.get(self.IDEAS)
        return response

    @allure.step('Получение Архива на главной странице')
    def get_archive_on_main_page(self, client) -> list[dict[str, Any]]:

        response = client.get(self.MAIN_PAGE_ARCHIVE)

        return response
