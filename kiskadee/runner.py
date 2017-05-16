import os
import shutil
import tarfile
import kiskadee.queue
import kiskadee.analyzers
import kiskadee.model
import kiskadee.helpers
import kiskadee.database

running = True


def runner():
    """Runner entry point
    """
    while running:
        if not kiskadee.queue.is_empty():
            package = kiskadee.queue.dequeue_analysis()
            analysis_reports = analyze(package)
            # TODO: save reports in DB


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

    compressed_sources = package['plugin'].get_sources(package['name'],
                                                       package['version'])
    with tarfile.open(fileobj=compressed_sources) as tarball:
        tarball.extractall(path=sources)

    analyzers = package['plugin'].analyzers
    reports = []
    for analyzer in analyzers:
        analysis = kiskadee.analyzers.run(analyzer, sources)
        firehose_report = kiskadee.helpers.to_firehose(analysis, analyzer)
        reports.append(firehose_report)
    return reports
