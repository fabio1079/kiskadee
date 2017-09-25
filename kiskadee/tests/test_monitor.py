import unittest
from sqlalchemy.orm import sessionmaker

from kiskadee import model
from kiskadee.monitor import Monitor
from kiskadee.queue import packages_queue
from kiskadee.model import Package, Fetcher, create_analyzers
import kiskadee.queue
import kiskadee.fetchers.debian
from kiskadee.database import Database


class MonitorTestCase(unittest.TestCase):

    def setUp(self):
        self.engine = Database('db_test').engine
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        self.monitor = Monitor(self.session)
        model.Base.metadata.create_all(self.engine)
        create_analyzers(self.session)
        self.pkg1 = {
                'name': 'curl',
                'version': '7.52.1-5',
                'fetcher': kiskadee.fetchers.debian,
                'meta': {'directory': 'pool/main/c/curl'},
                'results': {
                    'cppcheck': '<>',
                    'flawfinder': '><'},
                'fetcher_id': 1}

        self.pkg2 = {'name': 'urlscan',
                     'version': '0.8.2',
                     'fetcher': kiskadee.fetchers.debian,
                     'meta': {'directory': 'pool/main/u/urlscan'},
                     'results': {
                            'cppcheck': '<>',
                            'flawfinder': '><'},
                     'fetcher_id': 1}

        self.pkg3 = {'name': 'curl',
                     'version': '7.52.2-5',
                     'fetcher': kiskadee.fetchers.debian,
                     'meta': {'directory': 'pool/main/c/curl'},
                     'results': {
                            'cppcheck': '<>',
                            'flawfinder': '><'},
                     'fetcher_id': 1}

    def tearDown(self):
        self.session.close()
        model.Base.metadata.drop_all()

    def test_dequeue_package(self):
        packages_queue.put(self.pkg1)
        _pkg = self.monitor.dequeue_package()
        self.assertTrue(isinstance(_pkg, dict))

    def test_return_fetcher_name(self):
        fetcher = kiskadee.fetchers.debian.Fetcher()
        self.assertEqual(fetcher.name, 'debian')

    def test_save_some_fetcher(self):
        fetcher = kiskadee.fetchers.debian.Fetcher()
        self.monitor._save_fetcher(fetcher)
        _fetchers = self.monitor.session.query(Fetcher).all()
        self.assertEqual(len(_fetchers), 1)
        self.assertEqual(_fetchers[0].name, 'debian')
        self.assertEqual(_fetchers[0].description,
                         fetcher.config['description'])

    def test_save_package(self):
        self.monitor._save_fetcher(kiskadee.fetchers.debian.Fetcher())
        packages_queue.put(self.pkg1)
        packages_queue.put(self.pkg2)

        _pkg = self.monitor.dequeue_package()
        self.monitor._save_analyzed_pkg(_pkg)
        _pkgs = self.monitor.session.query(Package).all()
        self.assertEqual(len(_pkgs), 1)
        self.assertEqual(_pkgs[0].name, _pkg['name'])

        _pkg = self.monitor.dequeue_package()
        self.monitor._save_analyzed_pkg(_pkg)
        _pkgs = self.monitor.session.query(Package).all()
        self.assertEqual(len(_pkgs), 2)
        self.assertEqual(_pkgs[1].name, _pkg['name'])

    def test_save_version(self):
        self.monitor._save_fetcher(kiskadee.fetchers.debian.Fetcher())
        self.monitor._save_analyzed_pkg(self.pkg1)
        _pkgs = self.monitor.session.query(Package).all()
        _version = _pkgs[0].versions[0].number
        self.assertEqual(_version, self.pkg1['version'])

    def test_update_version(self):
        self.monitor._save_fetcher(kiskadee.fetchers.debian.Fetcher())
        packages_queue.put(self.pkg1)
        packages_queue.put(self.pkg3)

        _pkg = self.monitor.dequeue_package()
        self.monitor._save_analyzed_pkg(_pkg)

        _pkg = self.monitor.dequeue_package()
        self.monitor._save_analyzed_pkg(_pkg)

        _pkgs = self.monitor.session.query(Package).all()
        self.assertEqual(len(_pkgs), 1)

        _pkg_versions = self.monitor._query(Package).\
            filter(Package.name == _pkg['name']).first().versions

        _first_version = _pkg_versions[0].number
        _current_version = _pkg_versions[-1].number
        self.assertEqual(self.pkg1['version'], _first_version)
        self.assertEqual(_pkg['version'], _current_version)


if __name__ == '__main__':
    unittest.main()
