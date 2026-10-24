from __future__ import annotations

import logging
import os
import time
import warnings
from typing import Any

import allure
import curlify
import requests
from requests import Response

from API.utils.my_decorators import retry_on_timeout


class BaseRequest:
    def __init__(self, base_url: str, service: str) -> None:
        self.base_url = base_url
        self.service = service
        self.token = None
        self.cookies = None
        self.logger = logging.getLogger(__name__)
        self._timeout = 10
        self.session = None
        self.login = None
        self.grpc_login = None


    def update_timeout(self, new_timeout: int) -> None:
        self._timeout = new_timeout

    def _prepare_headers(self, is_json=True) -> dict[str, str]:
        headers = {}
        if is_json:
            headers['Content-Type'] = 'application/json'
        if self.token:
            headers['Authorization'] = f'Bearer {self.token}'
        if self.cookies:
            headers['Cookie'] = self.cookies
        if self.login:
            headers['Login'] = self.login
        if self.grpc_login:
            headers['grpc-metadata-login'] = self.grpc_login
        return headers

    def authorize_cookies(self, role_cookie):
        self.cookies = role_cookie

    def authorize(self, client_id: str, client_secret: str, username: str, password: str, login: bool = True) -> None:
        warnings.simplefilter('ignore')
        auth_url = os.getenv(
            'AUTH_TOKEN_URL',
            'https://auth.example.com/auth/realms/autotests/protocol/openid-connect/token',
        )
        auth_data = {
            'grant_type': 'client_credentials',
            'client_id': client_id,
            'client_secret': client_secret,
            'username': username,
            'password': password,
        }
        try:
            response = requests.post(auth_url, data=auth_data, verify=False)
            response.raise_for_status()
            auth_response = response.json()
            self.token = auth_response['access_token']
            if login:
                self.login = os.getenv('AUTH_LOGIN')
                self.grpc_login = os.getenv('AUTH_LOGIN')
            self.logger.info('\033[32m Авторизация прошла успешно \033[0m')
        except requests.exceptions.RequestException as e:
            self.logger.error(f'\033[31m Ошибка при авторизации: {e} \033[0m')
            raise

    @retry_on_timeout(max_retries=5, delay=2)
    def _request(self, method: str, endpoint: str, expected_status_code: int | list, session, **kwargs) -> Response:
        url = f'{self.base_url}/{self.service}/{endpoint}' if self.service else f'{self.base_url}/{endpoint}'
        is_json = not ('files' in kwargs and kwargs['files'] is not None)
        headers = self._prepare_headers(is_json=is_json)
        self.logger.info(f'Запрос: {method} {url}, args: {kwargs}, expected status code - {expected_status_code}')
        if isinstance(expected_status_code, int):
            expected_status_code = [expected_status_code]
        try:
            with allure.step('Отправляем запрос'):
                for _ in range(5):
                    response = session.request(method, url, headers=headers, verify=False, timeout=self._timeout,
                                               **kwargs)
                    # print(curlify.to_curl(response.request))
                    response.encoding = 'utf-8'
                    if response.status_code in expected_status_code:
                        break
                    else:
                        time.sleep(2)

            with allure.step('Проверяем код ответа'):
                assert response.status_code in expected_status_code, f'Ожидаемый статус код {expected_status_code} != Полученный статус код {response.status_code} \n Тело ответа - {response.text}'

            try:
                json_data = response.json()
                body = str(json_data)[:500] + '...(log limit)'
            except ValueError:
                body = str(response.text)[:500] + '...(log limit)'

            self.logger.info(f'\033[32m Успешный запрос: {method} {url}. Тело ответа: {body} \033[0m')
            return response

        except AssertionError as e:
            try:
                json_data = response.json()
                body = str(json_data)[:1000] + '...(log limit)'
            except ValueError:
                body = str(response.text)[:1000] + '...(log limit)'

            self.logger.error(f'\033[31m Ошибка при запросе:{method} {url}. Тело ответа: {body} \033[0m')
            raise e

        except requests.Timeout as e:
            self.logger.error(f'\033[31m Нет ответа >10 секунд по запросу:{method} {url} \033[0m')
            raise e

    def get(self, endpoint: str, params: dict[str, Any] = None, expected_status_code: int | list = 200,
            raw_format: bool = False) -> Response:

        self.session = requests.Session()
        response = self._request('GET', endpoint, params=params, expected_status_code=expected_status_code,
                                 session=self.session)
        return response.json() if not raw_format else response

    def post(self, endpoint: str, json: dict[str, Any] = None, expected_status_code: int | list = 200,
             raw_format: bool = False, files: dict[str, Any] = None, params: dict[str, Any] = None) -> dict[str, Any]:

        self.session = requests.Session()
        if not files:
            response = self._request('POST', endpoint, expected_status_code=expected_status_code, json=json,
                                     session=self.session, files=files, params=params)
        else:
            response = self._request('POST', endpoint, expected_status_code=expected_status_code, data=json,
                                     session=self.session, files=files, params=params)
        return response.json() if not raw_format else response

    def put(self, endpoint: str, json: dict[str, Any] = None, expected_status_code: int | list = 200,
            raw_format: bool = False, files: dict[str, Any] = None) -> dict[str, Any]:

        self.session = requests.Session()
        response = self._request('PUT', endpoint, expected_status_code=expected_status_code, json=json,
                                 session=self.session, files=files)
        return response.json() if not raw_format else response

    def patch(self, endpoint: str, json: dict[str, Any] = None, expected_status_code: int | list = 200,
              raw_format: bool = False, params: dict[str, Any] = None) -> dict[str, Any]:

        self.session = requests.Session()
        response = self._request('PATCH', endpoint, expected_status_code=expected_status_code, json=json,
                                 session=self.session, params=params)
        return response.json() if not raw_format else response

    def delete(self, endpoint: str, params: dict[str, Any] = None, expected_status_code: int | list = 200):

        self.session = requests.Session()
        return self._request('DELETE', endpoint, expected_status_code=expected_status_code,
                             session=self.session, params=params)
