import time

import psycopg2

from API.utils.sql_requests import DELETE_ATTR, DELETE_SPEC, DELETE_ROLE, DELETE_SOURCE, DELETE_DOCS, \
    DELETE_CRITICALITY_CLASS_MESSAGE, DELETE_PRODUCTS, DELETE_BRIEFS, DELETE_NOTI_NOTIFICATION_BD, \
    DELETE_NOTI_PRODUCTSTORAGE_BD, DELETE_NOTI_PRODBOARD_BD, DELETE_ACTION, DELETE_BRIEFS_V2, DELETE_TOOLS_AND_GROUPS, \
    DELETE_DEMOS, DELETE_DEMOS_CATEGORIES, DELETE_INTEGRATION_MESSAGE
from DBcm import UseDataBase

REQS_PRODUCT_STORAGE = (
    DELETE_ATTR, DELETE_SPEC, DELETE_ROLE, DELETE_SOURCE, DELETE_DOCS, DELETE_CRITICALITY_CLASS_MESSAGE,
    DELETE_PRODUCTS,
    DELETE_NOTI_PRODUCTSTORAGE_BD, DELETE_ACTION, DELETE_TOOLS_AND_GROUPS, DELETE_DEMOS, DELETE_DEMOS_CATEGORIES, DELETE_INTEGRATION_MESSAGE)

REQS_PRODBOARD = (DELETE_BRIEFS, DELETE_NOTI_PRODBOARD_BD, DELETE_BRIEFS_V2)

REQS_NOTIFICATION = (DELETE_NOTI_NOTIFICATION_BD,)


def execute_requests(database: str, requests: tuple, max_retries: int = 3):
    with UseDataBase(database) as cursor:
        for req in requests:
            retries = 0
            while retries < max_retries:
                try:
                    cursor.execute(req)
                    print(f"Запрос выполнен успешно: {req}")
                    break
                except psycopg2.Error as e:
                    retries += 1
                    print(f"Ошибка при выполнении запроса {req} для базы данных {database}: {e}. Попытка {retries} из {max_retries}")
                    if retries == max_retries:
                        print(f"Превышено максимальное количество попыток для запроса {req}. Ошибка сохраняется.")
                        raise
                time.sleep(3)




if __name__ == '__main__':
    execute_requests('pmd', REQS_PRODUCT_STORAGE)
    execute_requests('pb', REQS_PRODBOARD)
    execute_requests('ntf', REQS_NOTIFICATION)
