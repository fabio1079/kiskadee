from unittest import TestCase

from kiskadee.runner import _analyze, _path_to_uncompressed_source
from kiskadee.runner import _save_source_analysis
import kiskadee.plugins.example
from kiskadee.runner import _create_analyzers
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from kiskadee import model


class TestAnalyzers(TestCase):

    def setUp(self):
        self.engine = create_engine('sqlite:///:memory:')
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        model.Base.metadata.create_all(self.engine)
        _create_analyzers(self.session)
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
        firehose_report = _analyze(self.deb_pkg, "cppcheck", source_path)
        self.assertIsNotNone(firehose_report)

    def test_save_source_analysis(self):

        source_to_analysis = {
                'name': 'test',
                'version': '1.0.0',
                'plugin': kiskadee.plugins.example
        }

        package = model.Package(
                name='test',
                plugin_id=self.plugin.id
                )

        package_version = model.Version(
                number='1.0.0',
                package_id=package.id
                )

        package.versions.append(package_version)

        self.session.add(package)
        self.session.add(package_version)
        self.session.commit()

        firehose_report = "<>"
        _save_source_analysis(
                source_to_analysis,
                firehose_report,
                "cppcheck",
                self.session
        )

        saved_analysis = (
                self.session.query(model.Analysis)
                .filter(model.Analysis.raw == firehose_report).first()
        )

        self.assertIsNotNone(saved_analysis)

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
