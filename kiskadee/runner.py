import os
import shutil
import kiskadee
import kiskadee.queue
import kiskadee.analyzers
import kiskadee.model
import kiskadee.database
import kiskadee.helpers
import xml.etree.ElementTree

running = True


def runner():
    """Runner entry point
    """
    database = kiskadee.database.Database()
    engine = database.engine
    session = database.session
    kiskadee.model.Base.metadata.create_all(engine)
    kiskadee.model.Base.metadata.bind = engine
    while running:
        if not kiskadee.queue.is_empty():
            kiskadee.logger.debug('RUNNER: dequeuing...')
            package = kiskadee.queue.dequeue_analysis()
            kiskadee.logger.debug('RUNNER: dequeued %s-%s from %s'
                                  % (package['name'],
                                     package['version'],
                                     package['plugin'].__name__))
            analysis_reports = analyze(package)
            kiskadee.logger.debug('RUNNER: Saving analysis')
            all_analyses = '\n'.join(analysis_reports)
            plugin = kiskadee.model.Plugin(name=package['plugin'].__name__)
            package = kiskadee.model.Package(name=package['name'])
            version = kiskadee.model.Version(number=package['version'],
                                             analysis=all_analyses,
                                             has_analysis=True)
            session.merge(package)
            session.merge(plugin)
            session.merge(version)
            session.commit()


def analyze(package):
    """ The package dict is in the queue. The keys are:
        plugin: the plugin module itself
        name: the package name
        version: the package version
        path: plugin default path for packages
        return: list with firehose reports
    """
    base_dir = kiskadee.config['analyses']['path']
    sources = os.path.join(base_dir,
                           package['plugin'].__name__,
                           package['name'],
                           package['version'])
    # shutil.rmtree(sources)
    if not os.path.exists(sources):
        os.makedirs(sources)

    plugin = package['plugin'].Plugin()
    kiskadee.logger.debug('ANALYSIS: Downloading...')
    compressed_sources = plugin.get_sources(package['name'],
                                            package['version'])
    kiskadee.logger.debug('ANALYSIS: Downloaded!')
    kiskadee.logger.debug('ANALYSIS: Unpacking...')
    shutil.unpack_archive(compressed_sources, sources)
    kiskadee.logger.debug('ANALYSIS: Unpacked!')

    analyzers = plugin.analyzers()
    reports = []
    for analyzer in analyzers:
        kiskadee.logger.debug('ANALYSIS: running %s ...' % analyzer)
        analysis = kiskadee.analyzers.run(analyzer, sources)
        firehose_report = kiskadee.helpers.to_firehose(analysis, analyzer)
        reports.append(xml.etree.ElementTree.tostring(firehose_report))
        kiskadee.logger.debug('ANALYSIS: DONE running %s' % analyzer)
    # TODO: remove compressed files and uncompressed files after the analysis
    return reports
