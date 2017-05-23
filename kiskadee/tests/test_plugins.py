from unittest import TestCase
import unittest
import kiskadee
import sys
import os
from os import path, listdir
import shutil
import socket
import tempfile
from kiskadee.queue import dequeue_package
import kiskadee.plugins.debian


def is_connected():
    try:
        # connect to the host -- tells us if the host is actually
        # reachable
        socket.create_connection(("www.google.com", 80))
        return True
    except OSError:
        pass
    return False


class TestPlugins(TestCase):
    def test_loading(self):
        kiskadee.load_plugins()
        plugins_path = path.join('kiskadee', 'plugins')
        plugins_pkg_files = [f for f in listdir(plugins_path) if
                             path.isfile(path.join(plugins_path, f))]
        plugins_pkg_files.remove('__init__.py')
        if '__init__.pyc' in plugins_pkg_files:
            plugins_pkg_files.remove('__init__.pyc')
        for plugin in plugins_pkg_files:
            plugin_name, file_ext = path.splitext(plugin)
            self.assertTrue('kiskadee.plugins.' + plugin_name in sys.modules)


class TestDebianPlugin(TestCase):

    def setUp(self):
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
        some_pkg = dequeue_package()
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
                          'directory': 'pool/main/0/0ad'}
        url = self.debian_plugin._dsc_url(sample_package)
        self.assertEqual(expected_dsc_url, url)
