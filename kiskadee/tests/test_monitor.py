from unittest import TestCase
from kiskadee import monitor


class TestMonitor(TestCase):
    def test_sync_db_cache(self):
        monitor.sync_db_cache()
