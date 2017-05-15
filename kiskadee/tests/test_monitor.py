from unittest import TestCase
from kiskadee.monitor import Monitor
from kiskadee import model
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import kiskadee
from kiskadee.queue import enqueue_analysis, dequeue_package, \
        enqueue_package
from kiskadee.helpers import _start
from time import sleep
from kiskadee.model import Package, Plugin, Version, Base


class TestMonitor(TestCase):

    def setUp(self):
        self.monitor = Monitor()
        self.monitor.engine = create_engine('sqlite:///:memory:')
        Session = sessionmaker(bind=self.monitor.engine)
        self.monitor.session = Session()
        # model.metadata.create_all(self.engine)
        model.Base.metadata.create_all(self.monitor.engine)

    def tearDown(self):
        # model.metadata.drop_all(self.engine)
        model.Base.metadata.drop_all(self.monitor.engine)

    def test_sync_analyses(self):
        self.monitor.sync_analyses()

    def test_dequeue_package_values(self):
        def mock_download_source_gz(url):
            return 'kiskadee/tests/test_source'

        plugins = kiskadee.load_plugins()
        for plugin in plugins:
            plugin.download_sources_gz = mock_download_source_gz
            plugin.collect()
            pkg = dequeue_package()
            self.assertTrue(isinstance(pkg, dict))

    def test_save_dequeued_pkg(self):
        def mock_download_source_gz(url):
            return 'kiskadee/tests/test_source'

        def mock_save_or_update_pkgs(pkg):
            return {}

        debian_plugin = kiskadee.plugins.debian
        debian_plugin.download_sources_gz = mock_download_source_gz
        debian_plugin.collect()
        pkg = self.monitor.dequeue()
        self.assertTrue(isinstance(pkg, dict))

    def test_return_plugin_name(self):

        plugin = kiskadee.plugins.debian
        self.assertEqual(self.monitor._plugin_name(plugin), 'debian')

    def test_save_plugin(self):
        plugin = kiskadee.plugins.debian
        self.monitor._save_plugin(plugin)
        _plugins = self.monitor.session.query(Plugin).all()
        self.assertEqual(len(_plugins), 1)
        self.assertEqual(_plugins[0].name, 'debian')
        self.assertEqual(_plugins[0].description,
                         plugin.PLUGIN_DATA['description'])

    def test_save_package(self):
        plugin = kiskadee.plugins.debian
        self.monitor._save_plugin(plugin)
        pkg = {'name': 'curl',
               'version': '1.5-1',
               'plugin': kiskadee.plugins.debian,
               'meta': { 'directory': 'pool/main/c/curl'}
              }
        self.monitor._save_or_update_pkgs(pkg)
        _pkgs = self.monitor.session.query(Package).all()
        self.assertEqual(len(_pkgs), 1)
        self.assertEqual(_pkgs[0].name, 'curl')

    def test_save_version(self):
        plugin = kiskadee.plugins.debian
        self.monitor._save_plugin(plugin)
        pkg = {'name': 'curl',
               'version': '1.5-1',
               'plugin': kiskadee.plugins.debian,
               'meta': { 'directory': 'pool/main/c/curl'}
              }
        self.monitor._save_or_update_pkgs(pkg)
        _pkgs = self.monitor.session.query(Package).all()
        _version = _pkgs[0].versions[0].number
        self.assertEqual(_version, '1.5-1')
