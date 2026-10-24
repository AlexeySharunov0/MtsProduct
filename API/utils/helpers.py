from datetime import datetime, timedelta
import logging

import allure
import psycopg2
from requests import Response

from API.utils.DBcm import UseDataBase
from API.utils.sql_requests import GET_ATOMIC

logger = logging.getLogger(__name__)


@allure.step("Проверяем код ответа")
def assert_status_code(response: Response, expected_status_code: int | None = 200) -> None:
    """
    Проверка статус кода ответа
    Args:
        response: Необработанный ответ от сервера
        expected_status_code: Ожидаемый статус кода ответа
    """
    assert response.status_code == expected_status_code, (f"Ошибка: Ожидаемый статус код {expected_status_code}, "
                                                          f"получен {response.status_code} \n Тело ответа - {response.json()}")



@allure.step("Проверяем все поля в объекте не пустые")
def is_json_empty(json_data):
    """
    Проверяем все поля в объекте не пустые
    Args:
        json_data: Словарь объекта

    Returns:
        bool: True, если все поля заполнены, иначе False
    """
    if isinstance(json_data, dict):
        for key, value in json_data.items():
            if value is None or value == '' or value == []:
                allure.attach(f"Ошибка: ключ '{key}' содержит пустое значение: {value}", name="Пустое значение",
                              attachment_type=allure.attachment_type.TEXT)
                return False
            if isinstance(value, (dict, list)):
                if not is_json_empty(value):
                    allure.attach(f"Ошибка: ключ '{key}' содержит пустое значение: {value}", name="Пустое значение",
                                  attachment_type=allure.attachment_type.TEXT)
                    return False
    elif isinstance(json_data, list):
        for index, item in enumerate(json_data):
            if not is_json_empty(item):
                allure.attach(f"Ошибка: элемент списка с индексом '{index}' содержит пустое значение",
                              name="Пустое значение", attachment_type=allure.attachment_type.TEXT)
                return False
    return True


@allure.step("Переводим текст")
def translate_text(pattern, lang_1, lang_2):
    """
    Переводит текст
    Args:
        pattern: Текст, который надо перевести
        lang_1: Текущий язык
        lang_2: Язык на который надо перевести
    Returns:
        Переведённый текст

    """
    translation = str.maketrans(lang_1, lang_2)
    return pattern.lower().translate(translation)


@allure.step('Получение атомарных продуктов')
def get_atomic_products():
    """
    Получение атомарных продуктов
    Returns:
        Список атомарных продуктов
    """
    with UseDataBase() as cursor:
        try:
            cursor.execute(GET_ATOMIC)
            return [product[0] for product in cursor.fetchall()]
        except psycopg2.OperationalError as e:
            print('Не удалось выполнить запрос', e)


@allure.step('Декодирование строк в словаре/списке/строке')
def decode_unicode_in_collection(data: dict) -> dict | list | str | dict[dict]:
    """
    Декодирование строк в словаре
    Args:
        data: Словарь где будем искать закодированные строки и декодировать их
    Returns:
        Преобразованный словарь
    """
    if isinstance(data, dict):
        return {k: decode_unicode_in_collection(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [decode_unicode_in_collection(i) for i in data]
    elif isinstance(data, str):
        try:
            return bytes(data, "utf-8").decode("unicode_escape").encode('latin1').decode('utf-8')
        except UnicodeDecodeError:
            return data
    else:
        return data

@allure.step('Проверка является ли значение ссылкой')
def is_url(value):
    try:
        if isinstance(value, str) and (value.startswith('http://') or value.startswith('https://')):
            return True
        else:
            return False
    except:
        return False

def get_previous_and_current_quarter_start_dates():
    """
    Возвращает даты начала предыдущего и текущего кварталов.

    Возвращает список с двумя элементами, где первый элемент — это дата начала предыдущего квартала,
    а второй элемент — это дата начала текущего квартала.

    Returns:
        list: Список с двумя элементами, каждый из которых является объектом datetime.
    """
    now = datetime.now()
    current_year = now.year
    current_month = now.month
    current_quarter = (current_month - 1) // 3 + 1
    current_quarter_start = datetime(current_year, (current_quarter - 1) * 3 + 1, 1)

    prev_quarter = current_quarter - 1
    prev_year = current_year

    if prev_quarter < 1:
        prev_quarter = 4
        prev_year -= 1

    prev_quarter_start = datetime(prev_year, (prev_quarter - 1) * 3 + 1, 1)

    return [prev_quarter_start, current_quarter_start]