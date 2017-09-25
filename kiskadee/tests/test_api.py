import json
import unittest
from sqlalchemy.orm import sessionmaker

import kiskadee.model as model
from kiskadee.model import Fetcher
import kiskadee
from kiskadee.api.app import kiskadee as kiskadee_api
import kiskadee.api.app
from kiskadee.database import Database


class ApiTestCase(unittest.TestCase):

    def setUp(self):
        kiskadee_api.testing = True
        self.engine = Database('db_test').engine
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        self.app = kiskadee_api.test_client()
        model.create_analyzers(self.session)
        fetcher = model.Fetcher(
                name='kiskadee-fetcher', target='university'
        )
        self.session.add(fetcher)
        self.session.commit()

    def tearDown(self):
        self.session.close()
        model.Base.metadata.drop_all()

    def test_get_fetchers(self):
        def mock_kiskadee_db_session():
            return self.session

        print(self.session.query(Fetcher).all())
        kiskadee.api.app.kiskadee_db_session = mock_kiskadee_db_session
        response = self.app.get("/fetchers")
        self.assertIn("fetchers", json.loads(response.data.decode("utf-8")))

    def test_get_activated_fetcher(self):

        def mock_kiskadee_db_session():
            return self.session

        kiskadee.api.app.kiskadee_db_session = mock_kiskadee_db_session
        response = self.app.get("/fetchers")
        response_as_json = json.loads(response.data.decode("utf-8"))
        fetcher_name = response_as_json["fetchers"][0]["name"]
        self.assertEqual("kiskadee-fetcher", fetcher_name)


if __name__ == '__main__':
    unittest.main()
