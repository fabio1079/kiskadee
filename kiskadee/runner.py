import os
import shutil
import kiskadee
import kiskadee.queue
import kiskadee.analyzers
import kiskadee.helpers
import time

running = True


def runner():
    """Runner entry point
    """
    while running:
        kiskadee.logger.debug('RUNNER: entering loop')
        if not kiskadee.queue.is_empty():
            kiskadee.logger.debug('RUNNER: dequeuing')
            package = kiskadee.queue.dequeue_analysis()
            kiskadee.logger.debug('RUNNER: dequeued')
            analysis_reports = analyze(package)
            kiskadee.logger.debug('DONE running analysis')
            # TODO: save reports in DB
            kiskadee.logger.debug(analysis_reports)
            kiskadee.logger.debug('end run')
        time.sleep(5)
        kiskadee.logger.debug('RUNNER: loop ended')


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
        reports.append(firehose_report)
        kiskadee.logger.debug('ANALYSIS: DONE running %s' % analyzer)
    # TODO: remove compressed files and uncompressed files after the analysis
    return reports
