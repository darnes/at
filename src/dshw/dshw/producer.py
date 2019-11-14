import time
from datetime import datetime
import logging

import psutil

from dshw.common import (
    MessageSerializer, MonitorMessage, get_env_var,
    SysVar, connect_kafka_retrying, log_to_output
)

MAX_RETRIES = 30

log = logging.getLogger(__name__)
log_to_output()


def get_system_info() -> MonitorMessage:
    return MonitorMessage(
        cpu_usage=psutil.cpu_percent(0.1),
        mem_usage=psutil.virtual_memory().percent,
        timestamp=datetime.now()
    )


def producer_main():
    """Producer entry point"""
    client = connect_kafka_retrying(MAX_RETRIES)
    kafka_topic_name = get_env_var(SysVar.KAFKA_TOPIC).encode('utf-8')
    topic = client.topics[kafka_topic_name]
    log.info('starting to produce messages')
    with topic.get_sync_producer() as producer:
        while True:
            info = get_system_info()
            log.debug('producing message %s', info.timestamp)
            producer.produce(
                MessageSerializer.serialize(info)
            )
            time.sleep(1.0)
