""" Continous static analysis package.

kiskadee runs different static analyzers ona set of pre-defined software
repositories. When the kiskadee package is loaded, we load all the plugin names
in the pligins subpackages.
"""
from os import listdir, path

kiskadee_plugins = []
plugins_path = path.join('kiskadee', 'plugins')
plugins_pkg_files = [f for f in listdir(plugins_path) if
                     path.isfile(path.join(plugins_path, f))]
plugins_pkg_files.remove('__init__.py')
for plugin in plugins_pkg_files:
    plugin_name, file_ext = path.splitext(plugin)
    kiskadee_plugins.append(plugin_name)
