import os
import time
import dotenv

import psycopg2
import pytest
from psycopg2 import DatabaseError

from API.utils.DBcm import UseDataBase
from API.utils.api_client import BaseRequest
from API.utils.routes import APIRoutes
from API.utils.sql_requests import DELETE_ATTR, DELETE_SPEC, DELETE_TOOLS_AND_GROUPS, DELETE_PRODUCTS
from API.utils.vault_client import VaultClient

vault = VaultClient()

# HOST = "http://localhost:8080"  #
# HOST = "https://dev.prodboard.example.com"  #
# HOST = "https://stage.prodboard.example.com"  #


# HOST = "https://dev-pmd.prodboard.example.com"


######## CACHE

@pytest.fixture
def cache_client(request):
    client = BaseRequest(APIRoutes.BASE, service=APIRoutes.CACHE)
    # Аутентификация OAuth 2.0
    admin_cookie = vault.get_creds("main")["admin_user_cookie"]
    client.authorize_cookies(admin_cookie)

    yield client


####### PMD

@pytest.fixture
def rest_internal_client(request):
    client = BaseRequest(APIRoutes.BASE, service=APIRoutes.PMD_REST_INTERNAL)
    # Аутентификация OAuth 2.0
    admin_cookie = vault.get_creds("main")["admin_user_cookie"]
    client.authorize_cookies(admin_cookie)

    yield client


@pytest.fixture
def rest_internal_user_client(request):
    client = BaseRequest(APIRoutes.BASE, service=APIRoutes.PMD_REST_INTERNAL)
    # Аутентификация OAuth 2.0
    user_cookie = vault.get_creds("main")["regular_user_cookie"]
    client.authorize_cookies(user_cookie)

    yield client

@pytest.fixture
def rest_internal_user2_client(request):
    client = BaseRequest(APIRoutes.BASE, service=APIRoutes.PMD_REST_INTERNAL)
    # Аутентификация OAuth 2.0
    user_cookie = vault.get_creds("main")["service_user_cookie"]
    client.authorize_cookies(user_cookie)

    yield client


@pytest.fixture
def public_rest_client(request):
    client = BaseRequest(APIRoutes.BASE, service=APIRoutes.PMD_PUBLIC_REST)
    # Аутентификация OAuth 2.0
    user_cookie = vault.get_creds("main")["regular_user_cookie"]
    client.authorize_cookies(user_cookie)

    yield client

@pytest.fixture
def public_gw_client(request):
    client = BaseRequest(APIRoutes.BASE, service=APIRoutes.PMD_PUBLIC_GW)
    # Аутентификация OAuth 2.0
    client_id = vault.get_creds("main")['client_id']
    client_secret = vault.get_creds("main")['client_secret']
    username = vault.get_creds("main")['default_login']
    password = vault.get_creds("main")['default_password']
    client.authorize(client_id, client_secret, username, password, login=True)

    yield client

@pytest.fixture
def pmd_admin_gw_client(request):
    client = BaseRequest(APIRoutes.BASE, service=APIRoutes.PMD_ADMIN_GW)
    # Аутентификация OAuth 2.0
    admin_cookie = vault.get_creds("main")["admin_user_cookie"]
    client.authorize_cookies(admin_cookie)

    yield client


@pytest.fixture
def rest_external_client(request):
    client = BaseRequest(APIRoutes.BASE, service=APIRoutes.PMD_EXTERNAL_REST)
    # Аутентификация OAuth 2.0
    client_id = vault.get_creds("main")['client_id']
    client_secret = vault.get_creds("main")['client_secret']
    username = vault.get_creds("main")['default_login']
    password = vault.get_creds("main")['default_password']
    client.authorize(client_id, client_secret, username, password)

    yield client


@pytest.fixture
def pmd_admin_rest_client(request):
    client = BaseRequest(APIRoutes.BASE, service=APIRoutes.PMD_ADMIN_REST)
    # Аутентификация OAuth 2.0
    admin_cookie = vault.get_creds("main")["admin_user_cookie"]
    client.authorize_cookies(admin_cookie)

    yield client


@pytest.fixture
def pmd_internal_api_gw_client(request):
    client = BaseRequest(APIRoutes.BASE, service=APIRoutes.PMD_INTERNAL_API_GW)
    # Аутентификация OAuth 2.0
    admin_cookie = vault.get_creds("main")["admin_user_cookie"]
    client.authorize_cookies(admin_cookie)

    yield client


@pytest.fixture
def pmd_internal_gw_client(request):
    client = BaseRequest(APIRoutes.BASE, service=APIRoutes.PMD_INTERNAL_GW)
    # Аутентификация OAuth 2.0
    admin_cookie = vault.get_creds("main")["admin_user_cookie"]
    client.authorize_cookies(admin_cookie)

    yield client


#######  PPINFO
@pytest.fixture
def ppinfo_client(request):
    client = BaseRequest(APIRoutes.BASE, service=APIRoutes.PPINFO_GW)
    # Аутентификация OAuth 2.0
    admin_cookie = vault.get_creds("main")["admin_user_cookie"]
    client.authorize_cookies(admin_cookie)

    yield client

@pytest.fixture
def ppinfo_user_client(request):
    client = BaseRequest(APIRoutes.BASE, service=APIRoutes.PPINFO_GW)
    # Аутентификация OAuth 2.0
    user_cookie = vault.get_creds("main")["regular_user_cookie"]
    client.authorize_cookies(user_cookie)

    yield client

@pytest.fixture
def ppinfo_api_client(request):
    client = BaseRequest(APIRoutes.BASE, service=APIRoutes.PPINFO)
    # Аутентификация OAuth 2.0
    admin_cookie = vault.get_creds("main")["admin_user_cookie"]
    client.authorize_cookies(admin_cookie)

    yield client

@pytest.fixture
def ppinfo_user_api_client(request):
    client = BaseRequest(APIRoutes.BASE, service=APIRoutes.PPINFO)
    # Аутентификация OAuth 2.0
    user_cookie = vault.get_creds("main")["regular_user_cookie"]
    client.authorize_cookies(user_cookie)

    yield client


####### USER SERVICE

@pytest.fixture
def user_service_client(request):
    client = BaseRequest(APIRoutes.BASE, service=APIRoutes.USER_SERVICE)
    # Аутентификация OAuth 2.0
    admin_cookie = vault.get_creds("main")["admin_user_cookie"]
    client.authorize_cookies(admin_cookie)

    yield client


######## HYPERION

@pytest.fixture
def hyperion_client(request):
    client = BaseRequest(APIRoutes.BASE, service=APIRoutes.HYPERION)
    # Аутентификация OAuth 2.0
    admin_cookie = vault.get_creds("main")["admin_user_cookie"]
    client.authorize_cookies(admin_cookie)

    yield client


###### MOBILE
@pytest.fixture
def mobil_client(request):
    client = BaseRequest(APIRoutes.BASE, service=APIRoutes.MOBILE)
    # Аутентификация OAuth 2.0
    client_id = vault.get_creds("main")['client_id']
    client_secret = vault.get_creds("main")['client_secret']
    username = vault.get_creds("main")['default_login']
    password = vault.get_creds("main")['default_password']
    client.authorize(client_id, client_secret, username, password)

    yield client


###### NEWS

@pytest.fixture
def news_public_client(request):
    client = BaseRequest(APIRoutes.BASE, service=APIRoutes.NEWS_PUBLIC)
    # Аутентификация OAuth 2.0
    admin_cookie = vault.get_creds("main")["admin_user_cookie"]
    client.authorize_cookies(admin_cookie)

    yield client


@pytest.fixture
def news_admin_client(request):
    client = BaseRequest(APIRoutes.BASE, service=APIRoutes.NEWS_ADMIN)
    # Аутентификация OAuth 2.0
    admin_cookie = vault.get_creds("main")["admin_user_cookie"]
    client.authorize_cookies(admin_cookie)

    yield client

###### SEARCH

@pytest.fixture
def search_client(request):
    client = BaseRequest(APIRoutes.BASE, service=APIRoutes.SEARCH_INTERNAL)
    # Аутентификация OAuth 2.0
    admin_cookie = vault.get_creds("main")["admin_user_cookie"]
    client.authorize_cookies(admin_cookie)

    yield client

@pytest.fixture
def search_external_client(request):
    client = BaseRequest(APIRoutes.BASE, service=APIRoutes.SEARCH_EXTERNAL)
    # Аутентификация OAuth 2.0
    client_id = vault.get_creds("main")['client_id']
    client_secret = vault.get_creds("main")['client_secret']
    username = vault.get_creds("main")['default_login']
    password = vault.get_creds("main")['default_password']
    client.authorize(client_id, client_secret, username, password)

    yield client



@pytest.fixture
def clear_excel():
    yield
    file_path = "filename_excel.xlsx"
    if os.path.exists(file_path):
        os.remove(file_path)


@pytest.fixture
def clear_db_notifications():
    for i in range(5):
        db_config = {
            'pmd': ('pmd', 'delete from pmd.message_outbox'),
            'ntf': ('ntf', 'delete from ntf.email_history'),
            'pb': ('pb', 'delete from pb.message_outbox')
        }

        for db in ['pmd', 'ntf', 'pb']:
            db_name, query = db_config[db]

            try:
                with UseDataBase(db_name) as cursor:
                    cursor.execute(query)
            except psycopg2.OperationalError as e:
                raise DatabaseError(f"Не удалось выполнить запрос для базы данных {db}: {e}")

        time.sleep(1)

    yield

    for i in range(5):
        db_config = {
            'pmd': ('pmd', 'delete from pmd.message_outbox'),
            'ntf': ('ntf', 'delete from ntf.email_history'),
            'pb': ('pb', 'delete from pb.message_outbox')
        }

        for db in ['pmd', 'ntf', 'pb']:
            db_name, query = db_config[db]

            try:
                with UseDataBase(db_name) as cursor:
                    cursor.execute(query)
            except psycopg2.OperationalError as e:
                raise DatabaseError(f"Не удалось выполнить запрос для базы данных {db}: {e}")

        time.sleep(1)



@pytest.fixture
def clear_db_attribute():
    yield
    try:
        with UseDataBase('pmd') as cursor:
            cursor.execute(DELETE_ATTR)
    except psycopg2.OperationalError as e:
        raise DatabaseError(f"Не удалось выполнить запрос для базы данных pmd: {e}")


@pytest.fixture
def clear_db_tools():
    try:
        with UseDataBase('pmd') as cursor:
            cursor.execute(DELETE_TOOLS_AND_GROUPS)
    except psycopg2.OperationalError as e:
        raise DatabaseError(f"Не удалось выполнить запрос для базы данных pmd: {e}")
    yield

@pytest.fixture
def clear_db_products():
    try:
        with UseDataBase('pmd') as cursor:
            cursor.execute(DELETE_PRODUCTS)
    except psycopg2.OperationalError as e:
        raise DatabaseError(f"Не удалось выполнить запрос для базы данных pmd: {e}")
    yield


@pytest.fixture
def clear_db_spec():
    yield
    try:
        with UseDataBase('pmd') as cursor:
            cursor.execute(DELETE_SPEC)
    except psycopg2.OperationalError as e:
        raise DatabaseError(f"Не удалось выполнить запрос для базы данных pmd: {e}")


