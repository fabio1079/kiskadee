import json
import unittest
from sqlalchemy.orm import sessionmaker

import kiskadee
from kiskadee.runner import Runner
from kiskadee.monitor import Monitor
import kiskadee.api.app
import kiskadee.fetchers.example


class ApiTestCase(unittest.TestCase):

    def setUp(self):
        kiskadee.api.app.kiskadee.testing = True
        self.engine = kiskadee.database.Database('db_test').engine
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        self.app = kiskadee.api.app.kiskadee.test_client()
        kiskadee.model.create_analyzers(self.session)
        fetcher = kiskadee.model.Fetcher(
                name='kiskadee-fetcher', target='university'
        )
        model.Base.metadata.create_all(self.engine)
        model.create_analyzers(self.session)
        fetcher = kiskadee.model.Fetcher(
                name='kiskadee-fetcher', target='university', id=1
        )
        pkg = kiskadee.model.Package(
                name='kiskadee-package', fetcher_id=1, id=1
        )
        version = kiskadee.model.Version(
                number='7.23', package_id=1, id=1
        )
        analysis = kiskadee.model.Analysis(
                version_id=1, analyzer_id=1,
                raw="{\"metadata\": \"test\"}"
        )
        report = model.Reports(
            analysis_id=1, warnings=1, styles=1, errors=1
        )
        self.session.add(fetcher)
        self.session.add(pkg)
        self.session.add(version)
        self.session.add(analysis)
        self.session.add(report)
        self.session.commit()
        self.runner = Runner()
        self.monitor = Monitor(self.session)
        self.runner.kiskadee_queue = kiskadee.queue.KiskadeeQueue()

    def tearDown(self):
        self.session.close()
        kiskadee.model.Base.metadata.drop_all()

    def test_get_fetchers(self):
        def mock_kiskadee_db_session():
            return self.session

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

    def test_get_analysis_as_json(self):
        source_to_analysis = {
                'name': 'test',
                'version': '1.0.0',
                'fetcher_id': '1',
                'fetcher': kiskadee.fetchers.example.Fetcher()
        }

        def mock_kiskadee_db_session():
            return self.session

        self.runner.call_analyzers(source_to_analysis)
        analyzed_pkg = self.runner.kiskadee_queue.dequeue_result()
        self.monitor._save_analyzed_pkg(analyzed_pkg)
        kiskadee.api.app.kiskadee_db_session = mock_kiskadee_db_session
        response = self.app.get("/analysis/test/1.0.0")
        response_data = json.loads(response.data.decode("utf-8"))
        self.assertIsNotNone(response_data["analysis"]["raw"])
        pkg_first_analysis = response_data["analysis"]["raw"]["results"][0]
        self.assertIn('location', pkg_first_analysis)
        self.assertIn('cwe', pkg_first_analysis)
        self.assertIn('message', pkg_first_analysis)

    def test_get_specific_analysis(self):

        def mock_kiskadee_db_session():
            return self.session

        kiskadee.api.app.kiskadee_db_session = mock_kiskadee_db_session
        response = self.app.get("/analysis/kiskadee-package/7.23/")
        response_as_json = json.loads(response.get_data(as_text=True))
        self.assertIn("analysis", response_as_json)
        #  On the first analysis of response,
        #  check if exists some report attribute
        self.assertIn("report", response_as_json['analysis'][0])


if __name__ == '__main__':
    unittest.main()
