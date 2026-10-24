import psycopg2

from API.utils.vault_client import VaultClient

client = VaultClient()

dbconfig = {
    'host': client.get_creds("main")['host_db'],
    'database': client.get_creds("main")['database_db'],
    'user': client.get_creds("main")['user_db'],
    'password': client.get_creds("main")['password_db']
}

dbconfig_notification = {
    'host': client.get_creds('main')['host_db'],
    'database': client.get_creds('main')['notification_db_name'],
    'user': client.get_creds('main')['notification_db_user'],
    'password': client.get_creds('main')['notification_db_password']
}

dbconfig_prodboard = {
    'host': client.get_creds("main")['host_db'],
    'database': client.get_creds("main")['prodboard_db_name'],
    'user': client.get_creds("main")['prodboard_db_user'],
    'password': client.get_creds("main")['prodboard_db_password']
}


class UseDataBase:
    """
    Контекстный менеджер для работы с базой данных
    """

    def __init__(self, config: str = 'pmd') -> None:
        if config == 'pmd':
            config = dbconfig
        if config == 'ntf':
            config = dbconfig_notification
        if config == 'pb':
            config = dbconfig_prodboard
        self.configuration = config

    def __enter__(self):
        try:
            print("Пробуем подклбчиться")
            self.conn = psycopg2.connect(**self.configuration)
            print("Подключились")
        except psycopg2.OperationalError as e:
            print('Не удалось выполнить запрос', e)
        self.cursor = self.conn.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.conn.commit()
        count = self.cursor.rowcount
        print(f'Потрогали {count} записей')
        self.cursor.close()
        self.conn.close()
