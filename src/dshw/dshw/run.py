#!python

import time

import psutil


def main_test_producer():
    while True:
        # todo: ignore first value of cpu_usage
        cpu_usage = psutil.cpu_percent()
        mem_usage = psutil.virtual_memory()
        print(cpu_usage, mem_usage.available, mem_usage.total)
        time.sleep(1.0)

# kafka experiments
import json

from kafka import KafkaProducer, SimpleClient, KafkaConsumer

TOPIC_NAME = 'numt'


def main_producer():
    client = SimpleClient(['localhost:9092'])
    # todo: reconsider - works with the auto topic creation enabled
    # client.ensure_topic_exists(TOPIC_NAME)
    producer = KafkaProducer(
        bootstrap_servers=['localhost:9092'], value_serializer=lambda x: json.dumps(x).encode('utf-8')
    )

    for e in range(1000):
        data = {'number': e}
        producer.send(TOPIC_NAME, value=data)
        producer.flush()
        print('message sent')
        time.sleep(0.1)


def main_consumer():
    consumer = KafkaConsumer(
        TOPIC_NAME,
        bootstrap_servers=['localhost:9092'],
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )
    for message in consumer:
        message = message.value
        print('{} received '.format(message))


# database connection
from sqlalchemy import create_engine
from sqlalchemy import Column, String, SmallInteger, DateTime, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database
from datetime import datetime

db_string = "postgresql+psycopg2://postgres:docker@localhost:5432/monitor"
db = create_engine(db_string)
base = declarative_base()


class Metric(base):
    __tablename__ = 'metric'
    pk = Column('id', Integer, primary_key=True)
    value = Column(SmallInteger)
    time_stamp = Column(DateTime)


def create_db():
    if not database_exists(db_string):
        create_database(db_string)


def main_pg():
    create_db()
    db = create_engine(db_string)

    Session = sessionmaker(db)
    session = Session()
    base.metadata.create_all(db)

    new_val = Metric(value=11, time_stamp=datetime.now())
    session.add(new_val)
    session.commit()


def main_proto_consumer():
    consumer = KafkaConsumer(
        TOPIC_NAME,
        bootstrap_servers=['localhost:9092'],
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )
    Session = sessionmaker(db)
    session = Session()
    base.metadata.create_all(db)

    for message in consumer:
        new_val = Metric(value=message.value['number'], time_stamp=datetime.now())
        session.add(new_val)
        session.commit()
        print('{} received '.format(message))


def main():
    # main_producer()
    # main_consumer()
    # main_pg()
    main_proto_consumer()


if __name__ == '__main__':
    main()
