from enum import Enum
import time
import os
import sys
import json
from datetime import datetime
import logging

from pykafka import KafkaClient, exceptions

log = logging.getLogger(__name__)


def log_to_output():
    logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)


class ConfigMissingException(BaseException):
    """
    Raised in case of required configuration is missing
    """
    pass


class MonitorMessage(object):
    cpu_usage: float
    mem_usage: float
    timestamp: datetime

    def __init__(self, cpu_usage: float, mem_usage: float,  timestamp: datetime):
        self.cpu_usage = cpu_usage
        self.mem_usage = mem_usage
        self.timestamp = timestamp


class MessageSerializer(object):
    """Serializer for Monitor Message"""

    _dt_format = '%Y-%m-%d %H:%M:%S.%f'

    @classmethod
    def serialize(cls, mes: MonitorMessage) -> bytes:
        return json.dumps({
            'cpu_usage': mes.cpu_usage,
            'mem_usage': mes.mem_usage,
            'timestamp': datetime.strftime(mes.timestamp, cls._dt_format),
        }).encode('utf-8')

    @classmethod
    def deserialize(cls, data: bytes) -> MonitorMessage:
        dict_data = json.loads(data.decode('utf-8'))
        dict_data.update(
            {'timestamp': datetime.strptime(dict_data['timestamp'], cls._dt_format)}
        )
        return MonitorMessage(**dict_data)


class SysVar(Enum):
    KAFKA_ADDRESS = 'KAFKA_ADDRESS'
    KAFKA_TOPIC = 'KAFKA_TOPIC'
    PG_CONNECTION_STR = 'PG_CONNECTION_STR'


def get_env_var(var: SysVar) -> str:
    """
    Read value form environment. Raise ConfigMissingException if var is not set.

    :param var: variable name
    :return: variable value
    """
    try:
        return os.environ[var.value]
    except KeyError:
        raise ConfigMissingException('System variable `{name}` is not set.'.format(name=var.value))


def connect_kafka_retrying(retry_num) -> KafkaClient:
    current_retry = 0
    while current_retry < retry_num:
        try:
            return KafkaClient(get_env_var(SysVar.KAFKA_ADDRESS))
        except exceptions.NoBrokersAvailableError:
            log.warning('connection failed retry #%s', current_retry)
            time.sleep(3.0)
            current_retry += 1
