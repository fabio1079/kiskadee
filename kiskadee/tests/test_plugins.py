from unittest import TestCase
import os
import shutil
import tempfile
import kiskadee.queue


class TestPlugins(TestCase):
    def test_loading(self):
        _config = kiskadee.config
        _config['debian_plugin'] = {'active': 'no'}
        _config['juliet_plugin'] = {'active': 'yes'}
        _config['example_plugin'] = {'active': 'yes'}
        kiskadee.config = _config
        plugins = kiskadee.load_plugins()
        for plugin in plugins:
            name = plugin.__name__.split('.')\
            [len(plugin.__name__.split('.')) - 1]
            self.assertTrue(name != 'debian')


class TestDebianPlugin(TestCase):

    def setUp(self):
        import kiskadee.plugins.debian
        self.debian_plugin = kiskadee.plugins.debian.Plugin()
        self.data = self.debian_plugin.config

    def mock_download_sources_gz(self):
        path = tempfile.mkdtemp()
        source = 'kiskadee/tests/test_source/Sources.gz'
        shutil.copy2(source, path)
        return path

    def test_mount_sources_gz_url(self):
        mirror = self.data['target']
        release = self.data['release']
        url = self.debian_plugin._sources_gz_url()
        expected_url = "%s/dists/%s/main/source/Sources.gz" % (mirror, release)
        self.assertEqual(url, expected_url)

    def test_uncompress_sources_gz(self):
        temp_dir = tempfile.mkdtemp()
        self.debian_plugin._download_sources_gz = self.mock_download_sources_gz
        temp_dir = self.debian_plugin._download_sources_gz()
        self.debian_plugin._uncompress_gz(temp_dir)
        files = os.listdir(temp_dir)
        shutil.rmtree(temp_dir)
        self.assertTrue('Sources' in files)

    def test_enqueue_a_valid_pkg(self):
        temp_dir = tempfile.mkdtemp()
        self.debian_plugin._download_sources_gz = self.mock_download_sources_gz
        temp_dir = self.debian_plugin._download_sources_gz()
        self.debian_plugin._uncompress_gz(temp_dir)
        self.debian_plugin._queue_sources_gz_pkgs(temp_dir)
        shutil.rmtree(temp_dir)
        some_pkg = kiskadee.queue.dequeue_package()
        self.assertTrue(isinstance(some_pkg, dict))
        self.assertIn('name', some_pkg)
        self.assertIn('version', some_pkg)
        self.assertIn('plugin', some_pkg)
        self.assertIn('meta', some_pkg)
        self.assertIn('directory', some_pkg['meta'])

    def test_mount_dsc_url(self):
        expected_dsc_url = "http://ftp.us.debian.org/debian/pool/main/0/0ad/0ad_0.0.21-2.dsc"
        sample_package = {'name': '0ad',
                          'version': '0.0.21-2',
                          'meta': {'directory': 'pool/main/0/0ad'}}
        url = self.debian_plugin._dsc_url(sample_package)
        self.assertEqual(expected_dsc_url, url)

    def test_compare_gt_version(self):
        new = '1.1.1'
        old = '1.1.0'
        result = self.debian_plugin.compare_versions(new, old)
        self.assertTrue(result)

    def test_compare_smallest_version(self):
        new = '8.5-2'
        old = '8.6-0'
        result = self.debian_plugin.compare_versions(new, old)
        self.assertFalse(result)

    def test_compare_equal_version(self):
        new = '3.3.3-0'
        old = '3.3.3-0'
        result = self.debian_plugin.compare_versions(new, old)
        self.assertFalse(result)
