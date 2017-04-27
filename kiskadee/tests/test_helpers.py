from unittest import TestCase
import kiskadee
from kiskadee.helpers import to_firehose
import importlib
import sys
import os
import xml.etree.ElementTree as ET

class TestHelpers(TestCase):

    @classmethod
    def setUpClass(cls):
        """ Prepare environment to run tests
        """
        plugins = kiskadee.load_plugins()
        debian_plugin = kiskadee.plugins.debian
        source = 'kiskadee/tests/test_source/test_source.tar.gz'
        path = debian_plugin.extracted_source_path()
        debian_plugin.extract_source(source, path)
        cls.analyzer_report = debian_plugin.analyzers().cppcheck(path)


    def test_parse_cppcheck_report(self):
        root_tree = to_firehose(self.analyzer_report, 'cppcheck').getroot()
        generator = root_tree.find('metadata').find('generator')
        results = root_tree.find('results')
        self.assertIsNotNone(generator)
        self.assertEqual(generator.get('name'), 'cppcheck')
        self.assertIsNotNone(results)
        self.assertIsNotNone(root_tree.find('metadata'))
