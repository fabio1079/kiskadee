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
        example['name'] = 'example'
        example['version'] = '0.1'
        return example

    def comprare_versions(v1, v2):
        """Example has only one version

        This method does not matter here, let's just pass
        """
        return 0
