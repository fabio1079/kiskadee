import os
from unittest import TestCase

from kiskadee.runner import analyze
import kiskadee.plugins.debian


class TestAnalyzers(TestCase):

    def setUp(self):
        self.plugin = kiskadee.plugins.debian.Plugin()
        self.deb_pkg = {'name': 'test',
                        'version': '1.0.0',
                        'plugin': kiskadee.plugins.debian
                        }

    def test_run_analyzer(self):

        def mock_get_sources(arg1, arg2):
            base_path = os.path.dirname(os.getcwd())
            return ''.join([base_path,
                            '/kiskadee/kiskadee/tests/test_source/'
                            'test_source.tar.gz'])

        kiskadee.plugins.debian.Plugin.get_sources = mock_get_sources
        self.deb_pkg = {'name': 'test',
                        'version': '1.0.0',
                        'plugin': kiskadee.plugins.debian
                        }

        result = analyze(self.deb_pkg)
        self.assertTrue(isinstance(result, list))
        self.assertTrue(len(result) == 1)
