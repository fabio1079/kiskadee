import os
import shutil
import kiskadee
import kiskadee.queue
import kiskadee.analyzers
import kiskadee.helpers

running = True


def runner():
    """Runner entry point
    """
    while running:
        if not kiskadee.queue.is_empty():
            package = kiskadee.queue.dequeue_analysis()
            analysis_reports = analyze(package)
            # TODO: save reports in DB
            print(analysis_reports)


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
    shutil.rmtree(sources)
    if not os.path.exists(sources):
        os.makedirs(sources)

    plugin = package['plugin'].Plugin()
    compressed_sources = plugin.get_sources(package['name'],
                                            package['version'])
    shutil.unpack_archive(compressed_sources, sources)

    analyzers = plugin.analyzers
    reports = []
    for analyzer in analyzers:
        analysis = kiskadee.analyzers.run(analyzer, sources)
        firehose_report = kiskadee.helpers.to_firehose(analysis, analyzer)
        reports.append(firehose_report)
    # TODO: remove compressed files and uncompressed files after the analysis
    return reports
