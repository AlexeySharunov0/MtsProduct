import os

import requests

from API.utils.helpers import assert_status_code
from API.utils.vault_client import VaultClient

client = VaultClient()
TOKEN_URL = os.getenv(
    'AUTH_TOKEN_URL',
    'https://auth.example.com/auth/realms/autotests/protocol/openid-connect/token',
)


def bearer_token():
    data = {
        "grant_type": "client_credentials",
        "client_id": client.get_creds("main")['client_id'],
        "client_secret": client.get_creds("main")['client_secret'],
    }
    response = requests.post(TOKEN_URL, data=data,
                             verify=False, timeout=15)
    assert_status_code(response)
    return response.json()['access_token']


def super_bearer_token():
    data = {
        "grant_type": "password",
        "client_id": client.get_creds("main")['client_id'],
        "client_secret": client.get_creds("main")['client_secret'],
        "username": client.get_creds("main")['default_login'],
        "password": client.get_creds("main")['default_password']
    }
    response = requests.post(TOKEN_URL, data=data,
                             verify=False, timeout=15)
    assert_status_code(response)
    return response.json()['access_token']


if __name__ == "__main__":
    print(bearer_token())
