import os
import shutil
import tarfile
import kiskadee.queue
import kiskadee.analyzers
import kiskadee.model

running = True


def runner():
    while running:
        if not kiskadee.queue.is_empty():
            package = kiskadee.queue.dequeue_analysis()
            analyze(package)


def analyze(package):
    """ The package dict is in the queue. The keys are:
        plugin: the plugin module itself
        name: the package name
        version: the package version
        path: plugin default path for packages
    """
    # TODO: Base dir must be set in kiskadee config file as the directory that holds all packages to be analyzed
    base_dir = '/tmp/kiskadee'
    sources = os.path.join(base_dir, package['plugin'].__name__, package['name'], package['version'])
    shutil.rmtree(sources)
    if not os.path.exists(sources):
        os.makedirs(sources)

    compressed_sources = package['plugin'].get_sources(package['name'], package['version'])
    with tarfile.open(fileobj=compressed_sources) as tarball:
        tarball.extractall(path=sources)

    analyzers = package['plugin'].analyzers
    for analyzer in analyzers:
        analysis = kiskadee.analyzers.run(analyzer, sources)
        # TODO: store analysis in DB
