import unittest
from datetime import datetime

from dshw.common import MonitorMessage, MessageSerializer


class TestMessageSerializer(unittest.TestCase):
    def test_serializer(self):
        m = MonitorMessage(cpu_usage=12.0, mem_usage=44.0, timestamp=datetime.utcnow())
        flat_message = MessageSerializer.serialize(m)
        mr = MessageSerializer.deserialize(flat_message)

        self.assertEqual(m.cpu_usage, mr.cpu_usage)
        self.assertEqual(m.mem_usage, mr.mem_usage)
        self.assertEqual(m.timestamp, mr.timestamp)

