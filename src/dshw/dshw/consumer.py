import logging

from sqlalchemy import Column, create_engine, Float, DateTime, Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils import database_exists, create_database


from dshw.common import get_env_var, SysVar, MessageSerializer, connect_kafka_retrying, log_to_output

log = logging.getLogger(__name__)
log_to_output()


base = declarative_base()


class Metric(base):
    __tablename__ = 'metric'
    pk = Column('id', Integer, primary_key=True)
    cpu_usage = Column(Float)
    mem_usage = Column(Float)
    timestamp = Column(DateTime)


def create_db(conn_str):
    if not database_exists(conn_str):
        create_database(conn_str)


def consumer_main():
    pg_connection_str = get_env_var(SysVar.PG_CONNECTION_STR)
    create_db(pg_connection_str)
    db = create_engine(pg_connection_str)

    session_class = sessionmaker(db)
    session = session_class()
    base.metadata.create_all(db)

    client = connect_kafka_retrying(30)
    kafka_topic_name = get_env_var(SysVar.KAFKA_TOPIC).encode('utf-8')
    topic = client.topics[kafka_topic_name]
    consumer = topic.get_simple_consumer()
    log.info('starting to consume messages')
    for message in consumer:
        if message is not None:
            val = MessageSerializer.deserialize(message.value)
            log.debug('cpu: %s, time %s, fullmsg: %s', val.cpu_usage, val.timestamp, message.value)
            metric = Metric(cpu_usage=val.cpu_usage, mem_usage=val.mem_usage, timestamp=val.timestamp)
            session.add(metric)
            session.commit()
