from unittest import TestCase
import kiskadee
from kiskadee.plugins.debian import debian as debian_plugin
import importlib
import sys
import os
from os import path, listdir
import shutil


def load_plugins():
    for plugin in kiskadee.kiskadee_plugins:
        importlib.import_module('kiskadee.plugins.' + plugin)


class TestPlugins(TestCase):
    def test_loading(self):
        load_plugins()
        plugins_path = path.join('kiskadee', 'plugins')
        plugins_pkg_files = [f for f in listdir(plugins_path) if
                             path.isfile(path.join(plugins_path, f))]
        plugins_pkg_files.remove('__init__.py')
        for plugin in plugins_pkg_files:
            plugin_name, file_ext = path.splitext(plugin)
            self.assertTrue('kiskadee.plugins.' + plugin_name in sys.modules)


class TestDebianPlugin(TestCase):

    def test_generate_randomfile(self):
        path = debian_plugin.extracted_source_path()
        self.assertTrue(isinstance(path, str))

    def test_copy_source_to_path(self):
        source = 'kiskadee/tests/test_source/test_source.tar.gz'
        path = debian_plugin.extracted_source_path()
        debian_plugin.copy_source(source, path)
        files = os.listdir(path)
        self.assertTrue('test_source.tar.gz' in files)
        shutil.rmtree(path)

    def test_extract_source(self):
        source = 'kiskadee/tests/test_source/test_source.tar.gz'
        path = debian_plugin.extracted_source_path()
        debian_plugin.copy_source(source, path)
        debian_plugin.extract_source(source, path)
        files = os.listdir(path)
        self.assertTrue('source' in files)
        shutil.rmtree(path)

    def test_run_cppcheck(self):
        source = 'kiskadee/tests/test_source/test_source.tar.gz'
        path = debian_plugin.extracted_source_path()
        debian_plugin.copy_source(source, path)
        debian_plugin.extract_source(source, path)
        debian_plugin.analyzers().cppcheck(path)
        files = os.listdir('reports')
        self.assertTrue('cppcheck_report.xml' in files)

