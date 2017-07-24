import unittest

from kiskadee.runner import analyze, _path_to_uncompressed_source
from kiskadee.runner import create_analyzers, call_analyzers
import kiskadee.plugins.example
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from kiskadee import model


class TestAnalyzers(unittest.TestCase):

    def setUp(self):
        self.engine = create_engine('sqlite:///:memory:')
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        model.Base.metadata.create_all(self.engine)
        create_analyzers(self.session)
        self.plugin = kiskadee.plugins.debian.Plugin()
        self.deb_pkg = {'name': 'test',
                        'version': '1.0.0',
                        'plugin': kiskadee.plugins.debian
                        }
        self.plugin = model.Plugin(name='kiskadee-plugin', target='university')
        self.session.add(self.plugin)
        self.session.commit()

    def test_run_analyzer(self):

        source_to_analysis = {
                'name': 'test',
                'version': '1.0.0',
                'plugin': kiskadee.plugins.example
        }

        source_path = _path_to_uncompressed_source(
                source_to_analysis, kiskadee.plugins.example.Plugin()
        )
        firehose_report = analyze(self.deb_pkg, "cppcheck", source_path)
        self.assertIsNotNone(firehose_report)

    def test_generate_a_firehose_report(self):
        source_to_analysis = {
                'name': 'test',
                'version': '1.0.0',
                'plugin': kiskadee.plugins.example
        }

        call_analyzers(source_to_analysis)

        analyzed_pkg = kiskadee.queue.dequeue_result()

        self.assertEqual(analyzed_pkg['name'], source_to_analysis['name'])
        self.assertIn('cppcheck', analyzed_pkg['results'])
        self.assertIn('flawfinder', analyzed_pkg['results'])

    def test_path_to_uncompressed_source(self):

        source_to_analysis = {
                'name': 'test',
                'version': '1.0.0',
                'plugin': kiskadee.plugins.example
        }

        source_path = _path_to_uncompressed_source(
                source_to_analysis, kiskadee.plugins.example.Plugin()
        )

        self.assertIsNotNone(source_path)

    def test_invalid_path_to_uncompressed_source(self):

        source_to_analysis = {
                'name': 'test',
                'version': '1.0.0',
                'plugin': kiskadee.plugins.example
        }

        source_path = _path_to_uncompressed_source(
                source_to_analysis, None
        )

        self.assertIsNone(source_path)
