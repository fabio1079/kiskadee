"""Run each static analyzer in each package marked for analysis."""

import shutil
import tempfile
import os

import kiskadee.queue
import kiskadee.analyzers
import kiskadee.model
import kiskadee.database
import kiskadee.util
import kiskadee.converter
from kiskadee.model import Analyzer

RUNNING = True


def runner():
    """Run static analyzers.

    Continuously dequeue packages from `analyses_queue` and call the
    :func:`analyze` method, passing the dequeued package. After the analysis,
    updates the status of this package on the database.
    """
    kiskadee.logger.debug('Starting runner component')
    session = kiskadee.database.Database().session
    create_analyzers(session)
    while RUNNING:
        if not kiskadee.queue.is_empty():
            kiskadee.logger.debug('RUNNER: dequeuing...')
            source_to_analysis = kiskadee.queue.dequeue_analysis()
            kiskadee.logger.debug('RUNNER: dequeued %s-%s from %s'
                                  % (source_to_analysis['name'],
                                     source_to_analysis['version'],
                                     source_to_analysis['plugin'].__name__))

            call_analyzers(source_to_analysis)


def call_analyzers(source_to_analysis):
    """Iterate over the package analyzers.

    For each analyzer defined to analysis the source, call
    the function :func:`analyze`, passing the source dict, the analyzer
    to run the analysis, and the path to a compressed source.
    """
    plugin = source_to_analysis['plugin'].Plugin()
    source_path = _path_to_uncompressed_source(
            source_to_analysis, plugin
    )
    if not source_path:
        return None

    analyzers = plugin.analyzers()
    source_to_analysis['results'] = {}
    for analyzer in analyzers:
        firehose_report = analyze(
                source_to_analysis, analyzer, source_path
        )
        if firehose_report:
            source_to_analysis['results'][analyzer] = firehose_report

    if source_to_analysis['results']:
        kiskadee.logger.debug(
                "RUNNER: Sending {}-{} to Monitor"
                .format(source_to_analysis["name"],
                        source_to_analysis["version"])
            )
        kiskadee.queue.enqueue_result(source_to_analysis)
    shutil.rmtree(source_path)


def analyze(source_to_analysis, analyzer, source_path):
    """Run each analyzer on a source_to_analysis.

    The `source_to_analysis` dict is in the queue. The keys are:
        - plugin: the plugin module itself
        - name: the package name
        - version: the package version
        - path: plugin default path for packages
        - return: list with firehose reports
    The `analyzer` is the name of a static analyzer already created on the
    database.
    The `source_path` is the directory to a uncompressed source, returned
    by the :func:`_path_to_uncompressed_source`.
    """
    if source_path is None:
        return None

    kiskadee.logger.debug('ANALYSIS: running {} ...'.format(analyzer))
    try:
        analysis = kiskadee.analyzers.run(analyzer, source_path)
        firehose_report = kiskadee.converter.to_firehose(analysis,
                                                         analyzer)
        kiskadee.logger.debug('ANALYSIS: DONE {} analysis'.format(analyzer))
        return firehose_report
    except Exception as err:
        kiskadee.logger.debug('RUNNER: could not generate analysis')
        kiskadee.logger.debug(err)
        return None
# TODO: remove compressed/uncompressed files after the analysis


def _path_to_uncompressed_source(package, plugin):

    if not plugin or not package:
        return None

    kiskadee.logger.debug(
            'ANALYSIS: Downloading {} '
            'source...'.format(package['name'])
    )

    compressed_source = plugin.get_sources(package)

    if compressed_source:
        kiskadee.logger.debug(
                'ANALYSIS: Downloaded {} source in {} path'
                .format(package['name'], os.path.dirname(compressed_source))
                )
        uncompressed_source_path = tempfile.mkdtemp()
        shutil.unpack_archive(compressed_source, uncompressed_source_path)
        kiskadee.logger.debug(
                'ANALYSIS: Unpacking {} source in {} path'
                .format(package['name'], uncompressed_source_path)
                )
        if not compressed_source.find("kiskadee/tests") > -1:
            shutil.rmtree(os.path.dirname(compressed_source))
        kiskadee.logger.debug(
                'ANALYSIS: Unpacked {} source'.format(package['name'])
                )
        kiskadee.logger.debug(
                'ANALYSIS: Remove {} temp directory'
                .format(os.path.dirname(compressed_source))
            )
        return uncompressed_source_path
    else:
        kiskadee.logger.debug('RUNNER: invalid compressed source')
        return None


def create_analyzers(_session):
    """Create the analyzers on database.

    The kiskadee analyzers are defined on the section `analyzers` of the
    kiskadee.conf file. The `_session` argument represents a sqlalchemy
    session.
    """
    list_of_analyzers = dict(kiskadee.config._sections["analyzers"])
    for name, version in list_of_analyzers.items():
        if not (_session.query(Analyzer).filter(Analyzer.name == name).
                filter(Analyzer.version == version).first()):
            new_analyzer = kiskadee.model.Analyzer()
            new_analyzer.name = name
            new_analyzer.version = version
            _session.add(new_analyzer)
    _session.commit()
