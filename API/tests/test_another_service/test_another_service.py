import datetime

import allure
import pytest

from API.utils.DBcm import UseDataBase
from API.utils.vault_client import VaultClient

client = VaultClient()


@pytest.mark.api
@allure.label('priority', 'Высокий')
@allure.feature("Внешние системы")
class TestAnotherService:

    @allure.title("Взаимодействие с внешними системами")
    def test_internal_system_connect(self):
        current_datetime = datetime.datetime.now()

        with UseDataBase() as cursor:
            try:
                cursor.execute(
                    "SELECT created_at FROM pmd.v_external_request_statistic ORDER BY created_at DESC LIMIT 1;")
            except Exception as e:
                print('Не удалось выполнить запрос', e)
            results = cursor.fetchall()

            db_datetime = results[0][0]

            current_date_db = db_datetime.strftime('%Y-%m-%d')
            current_datetime = current_datetime.strftime('%Y-%m-%d')

        with allure.step("Проверяем что последняя дата интеграции была сегодня"):
            assert current_date_db == current_datetime
