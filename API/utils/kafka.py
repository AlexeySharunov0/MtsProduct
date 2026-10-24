import json
import logging
import uuid

import allure
from confluent_kafka import Producer, Consumer, KafkaException, KafkaError, TopicPartition


@allure.step('Проверяем доставку сообщения')
def delivery_report(err, msg):
    logger = logging.getLogger(__name__)
    """
    Вызывается для каждого сообщения, чтобы подтвердить его доставку.
    """
    if err is not None:
        logger.error(f'Ошибка отправки сообщения: {err}')
    else:
        logger.info(f'Сообщение отправлено к {msg.topic()}')


@allure.step('Отправляем сообщение в Kafka')
def message_send_to_kafka(conf: dict, message: dict, topic: str):
    # Создаем объект Producer
    producer = Producer(conf)

    # Сообщение, которое нужно отправить
    message = json.dumps(message)

    try:
        # Отправляем сообщение в Kafka
        producer.produce(topic, message.encode('utf-8'), callback=delivery_report, key=uuid.uuid4().__str__())

        # Ждем завершения доставки всех сообщений
        producer.flush(timeout=5)

    except Exception as e:
        print(f'Не получилось создать сообщение: {e}')


@allure.step('Забираем сообщение из kafka с определенным ключом')
def message_get_from_kafka(topic: str, conf: dict, required_key: str):
    # Создаем потребителя
    consumer = Consumer(conf)

    # Подписываемся на топик
    consumer.subscribe([topic])

    # Получаем список разделов для топика
    partitions = consumer.list_topics(topic, timeout=10).topics[topic].partitions.keys()
    topic_partitions = [TopicPartition(topic, p) for p in partitions]

    # Определяем смещения для конца каждого раздела
    for tp in topic_partitions:
        low, high = consumer.get_watermark_offsets(tp)
        tp.offset = high - 1  # Устанавливаем смещение на последний элемент
        logging.info(f'Раздел {tp.partition}: смещение {tp.offset}')

    # Назначаем разделы с обновленными смещениями
    consumer.assign(topic_partitions)
    attempts = 0
    try:
        while attempts < 4:
            # Получаем сообщение из топика
            msg = consumer.poll(timeout=1)
            if msg is None:
                attempts += 1
                logging.warning('Нет сообщений, повторная попытка...')
                continue
            if msg.error():
                # Обрабатываем ошибки
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    # Достигнут конец раздела
                    assert False, 'Достигнут конец раздела в Кафка. Сообщения по ключу не были найдены'
                else:
                    raise KafkaException(msg.error())

            if msg.key() and msg.key().decode('utf-8') == required_key and required_key:
                # Если ключ совпадает, обрабатываем JSON
                try:
                    json_data = json.loads(msg.value().decode('utf-8'))
                    return json_data
                except json.JSONDecodeError as e:
                    print(f'Error decoding JSON: {e}')
            else:
                json_data = json.loads(msg.value().decode('utf-8'))
                return json_data

        raise Exception(f'Не удалось получить сообщение после 3 попыток')

    except KeyboardInterrupt:
        pass
    finally:
        # Закрываем потребителя
        consumer.close()
