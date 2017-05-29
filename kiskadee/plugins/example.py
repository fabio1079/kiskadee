import kiskadee
import shutil
import os.path
import tempfile
import sys


class Plugin(kiskadee.plugins.Plugin):
    def get_sources(self, name, version, *args, **kwargs):
        return 'kiskadee/tests/test_source/test_source.tar.gz'

    def watch(self):
        """There is no proper API to inspect new example versions.
        It should not matter, since example will not receive updates.
        """
        example = {}
        example['plugin'] = sys.modules[__name__]
        example['name'] = 'example'
        example['version'] = '0.1'
        # this should be queued to the other queue first
        kiskadee.queue.enqueue_analysis(example)

    def comprare_versions(v1, v2):
        """Example has only one version
        
        This method does not matter here, let's just pass
        """
        return 0
