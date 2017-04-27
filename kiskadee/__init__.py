""" Continous static analysis package.

kiskadee runs different static analyzers on a set of pre-defined software
repositories. When the kiskadee package is loaded, we load all the plugin names
in the plugins subpackages.
"""
from os import listdir, path
import os
import importlib

my_path = os.path.dirname(os.path.realpath(__file__))
kiskadee_plugins = []
plugins_path = path.join(my_path, 'plugins')
plugins_pkg_files = [f for f in listdir(plugins_path) if
                     path.isfile(path.join(plugins_path, f))]
plugins_pkg_files.remove('config.json')
plugins_pkg_files.remove('__init__.py')
for plugin in plugins_pkg_files:
    plugin_name, file_ext = path.splitext(plugin)
    kiskadee_plugins.append(plugin_name)


def load_plugins():
    plugins = []
    for plugin in kiskadee_plugins:
        plugins.append(importlib.import_module('kiskadee.plugins.' + plugin))
    return plugins
