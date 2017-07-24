from unittest import TestCase
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from kiskadee import model
from kiskadee.monitor import Monitor
from kiskadee.queue import enqueue_package
from kiskadee.model import Package, Plugin
import kiskadee.queue
import kiskadee.plugins.debian
from kiskadee.runner import create_analyzers


class TestMonitor(TestCase):

    def setUp(self):
        self.engine = create_engine('sqlite:///:memory:')
        Session = sessionmaker(bind=self.engine)
        session = Session()
        self.monitor = Monitor(session)
        model.Base.metadata.create_all(self.engine)
        create_analyzers(self.monitor.session)
        self.pkg1 = {
                'name': 'curl',
                'version': '7.52.1-5',
                'plugin': kiskadee.plugins.debian,
                'meta': {'directory': 'pool/main/c/curl'},
                'results': {
                    'cppcheck': '<>',
                    'flawfinder': '><'},
                'plugin_id': 1}

        self.pkg2 = {'name': 'urlscan',
                     'version': '0.8.2',
                     'plugin': kiskadee.plugins.debian,
                     'meta': {'directory': 'pool/main/u/urlscan'},
                     'results': {
                            'cppcheck': '<>',
                            'flawfinder': '><'},
                     'plugin_id': 1}

        self.pkg3 = {'name': 'curl',
                     'version': '7.52.2-5',
                     'plugin': kiskadee.plugins.debian,
                     'meta': {'directory': 'pool/main/c/curl'},
                     'results': {
                            'cppcheck': '<>',
                            'flawfinder': '><'},
                     'plugin_id': 1}

    def tearDown(self):
        # model.metadata.drop_all(self.engine)
        model.Base.metadata.drop_all(self.engine)

    def test_dequeue_package(self):
        enqueue_package(self.pkg1)
        _pkg = self.monitor.dequeue_package()
        self.assertTrue(isinstance(_pkg, dict))

    def test_return_plugin_name(self):
        plugin = kiskadee.plugins.debian
        self.assertEqual(self.monitor._plugin_name(plugin), 'debian')

    def test_save_some_plugin(self):
        plugin = kiskadee.plugins.debian.Plugin()
        self.monitor._save_plugin(kiskadee.plugins.debian)
        _plugins = self.monitor.session.query(Plugin).all()
        self.assertEqual(len(_plugins), 1)
        self.assertEqual(_plugins[0].name, 'debian')
        self.assertEqual(_plugins[0].description,
                         plugin.config['description'])

    def test_save_package(self):
        plugin = kiskadee.plugins.debian
        self.monitor._save_plugin(plugin)
        enqueue_package(self.pkg1)
        enqueue_package(self.pkg2)

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
        plugin = kiskadee.plugins.debian
        self.monitor._save_plugin(plugin)
        self.monitor._save_analyzed_pkg(self.pkg1)
        _pkgs = self.monitor.session.query(Package).all()
        _version = _pkgs[0].versions[0].number
        self.assertEqual(_version, self.pkg1['version'])

    def test_update_version(self):
        plugin = kiskadee.plugins.debian
        self.monitor._save_plugin(plugin)
        enqueue_package(self.pkg1)
        enqueue_package(self.pkg3)

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
