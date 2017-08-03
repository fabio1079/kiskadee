"""Example kiskadee plugin implementation."""

import sys
import kiskadee.queue


class Plugin(kiskadee.plugins.Plugin):
    """Example kiskadee plugin implementation."""

    def get_sources(self, source_data):
        """Use sources from test suite."""
        return 'kiskadee/tests/test_source/test_source.tar.gz'

    @kiskadee.queue.package_enqueuer
    def watch(self):
        """There is no proper API to inspect new example versions.

        It should not matter, since example will not receive updates.
        """
        example = {}
        example['plugin'] = kiskadee.plugins.example.Plugin()
        example['version'] = '0.1'
        example['name'] = 'example'
        return example

    def compare_versions(self, new, old):
        """Compare package versions.

        Example has only one version. This method does not matter here, let's
        just pass.
        """
        return 0
