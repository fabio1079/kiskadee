from unittest import TestCase
from kiskadee.monitor import Monitor
from kiskadee import model
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import kiskadee
from kiskadee.queue import enqueue_analysis, dequeue_package, \
        enqueue_package


class TestMonitor(TestCase):

    def setUp(self):
        self.engine = create_engine('sqlite:///:memory:')
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        # model.metadata.create_all(self.engine)
        model.Base.metadata.create_all(self.engine)
        self.monitor = Monitor()

    def tearDown(self):
        # model.metadata.drop_all(self.engine)
        model.Base.metadata.drop_all(self.engine)

    def test_sync_analyses(self):
        self.monitor.sync_analyses()

    def test_dequeue_package(self):
        def mock_download_source_gz(url):
            return 'kiskadee/tests/test_source'

        plugins = kiskadee.load_plugins()
        for plugin in plugins:
            plugin.download_sources_gz = mock_download_source_gz
            plugin.collect()
            pkg = dequeue_package()
            self.assertTrue(isinstance(pkg, dict))
