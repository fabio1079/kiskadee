from unittest import TestCase
import kiskadee
import importlib
import sys
from os import path, listdir


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
