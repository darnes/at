import time
import json

import psutil
from kafka import KafkaProducer, SimpleClient, KafkaConsumer

TOPIC_NAME = 'numt'


def main_test_producer():

    producer = KafkaProducer(
        bootstrap_servers=['localhost:9092'], value_serializer=lambda x: json.dumps(x).encode('utf-8')
    )

    while True:
        # todo: ignore first value of cpu_usage
        cpu_usage = psutil.cpu_percent()
        mem_usage = psutil.virtual_memory()
        data = {'number': cpu_usage}
        producer.send(TOPIC_NAME, value=data)
        producer.flush()
        print(cpu_usage, mem_usage.available, mem_usage.total)
        time.sleep(1.0)


if __name__ == '__main__':
    main_test_producer()
