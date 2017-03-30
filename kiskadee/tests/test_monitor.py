from unittest import TestCase
from kiskadee import monitor
from kiskadee import model
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class TestMonitor(TestCase):

    def setUp(self):
        self.engine = create_engine('sqlite:///:memory:')
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        # model.metadata.create_all(self.engine)
        model.Base.metadata.create_all(self.engine)

    def tearDown(self):
        # model.metadata.drop_all(self.engine)
        model.Base.metadata.drop_all(self.engine)

    def test_sync_analyses(self):
        monitor.sync_analyses()
