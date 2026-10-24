import functools
import time

import psycopg2
import requests

from API.utils.DBcm import UseDataBase


def retry_on_timeout(max_retries=5, delay=2):
    """
    Декоратор для повторной попытки выполнения функции при возникновении таймаута.

    :param max_retries: Максимальное количество попыток.
    :param delay: Задержка между попытками в секундах.
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except (requests.exceptions.ReadTimeout, requests.exceptions.ConnectTimeout) as e:
                    if attempt == max_retries - 1:
                        raise
                    if hasattr(args[0], 'logger'):
                        args[0].logger.warning(
                            f'\033[33m Таймаут, попытка {attempt + 1} из {max_retries}: {str(e)} \033[0m'
                        )
                    if hasattr(args[0], 'session'):
                        args[0].session.close()
                        args[0].session = requests.Session()
                    time.sleep(delay)
        return wrapper
    return decorator


def retry_on_exception_db(max_retries: int = 3):
    def decorator(func):
        def wrapper(*args, **kwargs):
            retries = 0
            while retries < max_retries:
                try:
                    with UseDataBase(args[0]) as cursor:
                        return func(cursor, *args[1:], **kwargs)
                except psycopg2.Error as e:
                    retries += 1
                    print(f"Ошибка при выполнении запроса для базы данных {args[0]}: {e}. Попытка {retries} из {max_retries}")
                    if retries == max_retries:
                        print(f"Превышено максимальное количество попыток для запроса. Ошибка сохраняется.")
                        raise
                time.sleep(1)
        return wrapper
    return decorator
