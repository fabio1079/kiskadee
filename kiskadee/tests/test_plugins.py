from unittest import TestCase
import kiskadee
import importlib
import sys
import os
from os import path, listdir
import shutil


class TestPlugins(TestCase):
    def test_loading(self):
        kiskadee.load_plugins()
        plugins_path = path.join('kiskadee', 'plugins')
        plugins_pkg_files = [f for f in listdir(plugins_path) if
                             path.isfile(path.join(plugins_path, f))]
        plugins_pkg_files.remove('config.json')
        plugins_pkg_files.remove('__init__.py')
        for plugin in plugins_pkg_files:
            plugin_name, file_ext = path.splitext(plugin)
            self.assertTrue('kiskadee.plugins.' + plugin_name in sys.modules)


class TestDebianPlugin(TestCase):

    def setUp(self):
        plugins = kiskadee.load_plugins()
        self.debian_plugin = kiskadee.plugins.debian

    def test_generate_randomfile(self):
        path = self.debian_plugin.extracted_source_path()
        self.assertTrue(isinstance(path, str))

    def test_copy_source_to_path(self):
        source = 'kiskadee/tests/test_source/test_source.tar.gz'
        path = self.debian_plugin.extracted_source_path()
        self.debian_plugin.copy_source(source, path)
        files = os.listdir(path)
        self.assertTrue('test_source.tar.gz' in files)
        shutil.rmtree(path)

    def test_uncompress_tar_gz(self):
        source = 'kiskadee/tests/test_source/test_source.tar.gz'
        path = self.debian_plugin.extracted_source_path()
        self.debian_plugin.copy_source(source, path)
        self.debian_plugin.uncompress_tar_gz(source, path)
        files = os.listdir(path)
        self.assertTrue('source' in files)
        shutil.rmtree(path)

    def test_run_cppcheck(self):
        source = 'kiskadee/tests/test_source/test_source.tar.gz'
        path = self.debian_plugin.extracted_source_path()
        self.debian_plugin.copy_source(source, path)
        self.debian_plugin.uncompress_tar_gz(source, path)
        self.debian_plugin.analyzers().cppcheck(path)
        files = os.listdir('reports')
        self.assertTrue('firehose_cppcheck_report.xml' in files)
