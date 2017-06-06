Common interface to kiskadee plugins
====================================

The Plugin class, define a common behavior to all plugins in kiskadee. This
is useful to easly integrates to kiskadee new targets to be monitored. A
target is some source code that the plugin will check for new packages, and
make the download of the source code when necessary. When creating a new
plugin, you must heritage from `kiskadee.plugins.Plugin`, in order to follow
the required interface. Each of the behaviors defined in `kiskadee.plugins.Plugin`
can be implemented according to the target that will be monitored by the
new plugin.

The class defines the following behaviors:

.. py:class:: Plugin

    .. py:method:: compare_versions(new, old)

        Returns *true* if `new` is greater then `old`. `new` and `old` will
        be the versions of packages monitored by your plugin.

    .. py:method:: get_sources(source_data)

        Returns the absolute path for a compressed file
        containing the package source code. `source_data` will be a dict
        previously created by the plugin. `source_data` will have at least
        two obrigatory keys: `name` and `version` of the package that have
        to be downloaded.

    .. py:method:: watch()

        Continuously monitors some target repository. This method will be called
        as a thread, and will run concurrently with the main kiskadee thread.
        This method must enqueue packages using the
        `@kiskadee.queue.package_enqueuer` decorator.

Plugin example
-----------------------

A simple example of a kiskadee plugin

.. code-block:: python

    import kiskadee
    import sys
    import kiskadee.queue
    class Plugin(kiskadee.plugins.Plugin):
        def get_sources(self, source_data):
            return 'kiskadee/tests/test_source/test_source.tar.gz'

        @kiskadee.queue.package_enqueuer
        def watch(self):
            """There is no proper API to inspect new example versions.
            It should not matter, since example will not receive updates.
            """
            example = {}
            example['plugin'] = sys.modules[__name__]
            example['version'] = '0.1'
            example['name'] = 'example'
            return example

        def compare_versions(self, new, old):
            """Example has only one version

            This method does not matter here, let's just pass
            """
            return 0
