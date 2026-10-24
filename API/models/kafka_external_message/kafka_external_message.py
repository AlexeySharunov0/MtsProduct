import base64

from API.utils.kafka import message_get_from_kafka, message_send_to_kafka
from API.utils.vault_client import VaultClient


class KafkaConfigs:
    client = VaultClient()

    # Kafka external user
    KAFKA_USER = client.get_creds('main')['kafka_external_user']

    # Kafka external pass base64
    KAFKA_PASSWORD = client.get_creds('main')['kafka_external_password_base64']

    KAFKA_GET_LOGIN = client.get_creds('main')['kafka_login']

    KAFKA_GET_PASSWORD = client.get_creds('main')['kafka_password']

    DECODED_PASSWORD = base64.b64decode(KAFKA_PASSWORD).decode('utf-8')
    DECODED_PASSWORD_FOR_GET = base64.b64decode(KAFKA_GET_PASSWORD).decode('utf-8')

    # Конфиг для отправки сообщения
    CONFIG_TO_SEND_MESSAGE = {
        'bootstrap.servers': '11.217.101.138:9094',  # Адрес брокера Kafka
        'client.id': 'python-producer',  # Идентификатор клиента
        'security.protocol': 'SASL_PLAINTEXT',  # Протокол безопасности (SASL)
        'sasl.mechanisms': 'SCRAM-SHA-512',  # Механизм аутентификации
        'sasl.username': KAFKA_USER,  # Ваше имя пользователя из Vault
        'sasl.password': DECODED_PASSWORD  # Ваш декодированный пароль из Vault
    }

    # Конфиг для получения сообщения из external кафки
    CONF_TO_GET_MESSAGE_EXTERNAL = {
        'bootstrap.servers': '11.217.101.138:9094',
        'group.id': 'test_consumer_group1',
        'auto.offset.reset': 'latest',
        'enable.auto.commit': False,
        'security.protocol': 'SASL_PLAINTEXT',
        'sasl.mechanism': 'SCRAM-SHA-512',
        'sasl.username': KAFKA_USER,
        'sasl.password': DECODED_PASSWORD,
    }

    # Конфиг для получения сообщения из internal кафки products
    CONF_TO_GET_MESSAGE_INTERNAL_PRODUCTS = {
        'bootstrap.servers': '11.217.101.140:9094',
        'group.id': 'test_consumer_group2',
        'auto.offset.reset': 'latest',
        'enable.auto.commit': False,
        'security.protocol': 'SASL_PLAINTEXT',
        'sasl.mechanism': 'SCRAM-SHA-512',
        'sasl.username': KAFKA_GET_LOGIN,
        'sasl.password': DECODED_PASSWORD_FOR_GET,
    }

    # Топик, в который будем отправлять сообщение
    TOPIC_MONETIZATION_CONSOLE = 'monetization-console-integration'
    TOPIC_TO_GET = 'external_pmd_products'
    TOPIC_TO_GET_PRODUCTS = 'pmd-product-event'


class KafkaExternal(KafkaConfigs):
    def get_message(self, date: str = '2022-12-14', attribute_id: str = 'PPinfo_start_date_MVP',
                    product_code: str = 'BI_56907') -> dict:
        message = {
            'dates': [
                {
                    'date': date,
                    'attributeId': attribute_id,
                    'documentLink': 'https://bossreferent.example.com/br/rd?unid=F996D27CD19C7ACD4325889F002E66DA',
                    'documentName': '434324 от 2022-04-27 test test test'
                }
            ],
            'productCode': product_code
        }
        return message

    def message_send_to_kafka_monetization_console(self, attribute_id: str):
        message_send_to_kafka(conf=self.CONFIG_TO_SEND_MESSAGE, message=self.get_message(attribute_id=attribute_id),
                              topic=self.TOPIC_MONETIZATION_CONSOLE)

    def message_get_from_kafka_external(self, required_key=None):
        return message_get_from_kafka(conf=self.CONF_TO_GET_MESSAGE_EXTERNAL, topic=self.TOPIC_TO_GET, required_key=required_key)

    def message_get_from_kafka_internal_products(self, required_key=None):
        return message_get_from_kafka(conf=self.CONF_TO_GET_MESSAGE_INTERNAL_PRODUCTS, topic=self.TOPIC_TO_GET_PRODUCTS, required_key=required_key)
