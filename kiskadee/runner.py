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
        print('in loop')
        if not kiskadee.queue.is_empty():
            print('dequeuing')
            package = kiskadee.queue.dequeue_analysis()
            print('dequeued')
            print('running analysis')
            analysis_reports = analyze(package)
            print('DONE running analysis')
            # TODO: save reports in DB
            print(analysis_reports)
            print('end run')
        time.sleep(5)


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
    compressed_sources = plugin.get_sources(package['name'],
                                            package['version'])
    print('Downloaded!')
    print('Unpacking...')
    shutil.unpack_archive(compressed_sources, sources)
    print('Unpacked!')

    analyzers = plugin.analyzers()
    reports = []
    for analyzer in analyzers:
        analysis = kiskadee.analyzers.run(analyzer, sources)
        firehose_report = kiskadee.helpers.to_firehose(analysis, analyzer)
        reports.append(firehose_report)
    # TODO: remove compressed files and uncompressed files after the analysis
    return reports
