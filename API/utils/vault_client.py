import json
import logging
import os

import hvac
import pytest
import urllib3

urllib3.disable_warnings()


class VaultClient:
    client = None
    text = 'Клиент Vault не прошел авторизацию'
    logger = logging.getLogger(__name__)
    _template_result = {'login': None, 'password': None, 'pkey': None}
    full_result = dict()
    _data = 'data'

    def __init__(self, remote: bool = True, url: str = os.getenv('VAULT_URL', 'https://vault.example.com/'),
                 mount_point=os.getenv('VAULT_MOUNT_POINT', 'autotests')):
        self.mount_point = mount_point
        self.mode = bool(remote)
        self.logger.info(f"Vault client mode: {self.mode}, mount_point: {self.mount_point}, url: {url}")
        self.client = hvac.Client(url=url, verify=False)
        if self.mode:
            self._get_envs()
            if not self.client.is_authenticated():
                self.logger.info(self.text + " пробуем аутентифицировать клиент")
                self.auth()
        else:
            self.full_result = json.loads(os.getenv("VAULT_CREDS"))

    def _get_envs(self):
        self.role = os.getenv("ROLE_VAULT")
        self.secret = os.getenv("SECRET_VAULT")
        if not self.role or not self.secret:
            self.logger.error("нет переменных окружения roleId и secretId, клиент vault не сможет авторизоваться")

    def auth(self):
        """
        Аутентификация клиента
        :return:
        """
        try:
            response = self.client.auth.approle.login(role_id=self.role, secret_id=self.secret)
            self.client.token = response['auth']['client_token']
        except Exception as ex:
            pytest.exit(self.text + "\tmessage: " + ex.__str__())

    def _update_full_result(self, target: str, result: dict):
        """
        Метод кэширует данные
        :param target:
        :param result:
        :return:
        """
        cred = dict()
        for key in self._template_result:
            if key in result:
                cred[key] = result[key]
        if not cred:
            cred = result
        self.full_result[target] = cred

    def get_creds(self, target):
        """
        Метод отдает данные для авторизации, в формате dict

        :param target: данные от чего мы ищем креды
        """
        if not self.mode:
            return self.full_result.get(target)
        if target in self.full_result.keys():
            return self.full_result.get(target)
        if not self.client.is_authenticated():
            self.logger.info(self.text + " пробуем аутентифицировать клиент")
            self.auth()
        self.logger.info(f'target: {target}')
        creds = self.client.secrets.kv.v2.read_secret(target, mount_point=self.mount_point)
        self._update_full_result(target, creds[self._data][self._data])
        return self.full_result.get(target)

    @property
    def get_all_creds(self):

        return self.full_result
