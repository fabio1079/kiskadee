import kiskadee.queue
import kiskadee.analyzers
import kiskadee.model

running = True


def runner():
    while running:
        if not kiskadee.queue.is_empty():
            package = kiskadee.queue.dequeue()
            analyze(package)


def analyze(package):
    """ The package dict is in the queue. The keys are:
        plugin: the plugin module itself
        name: the package name
        version: the package version
    """
    # get source of specific version
    sources = package['plugin'].get_sources(package['name'], package['version'])
    # get list of analyzers
    # this list should come from a config file. if we have a class for the plugins to inherit from,
    # we can get this superclass to read the global config file for each specific plugin
    analyzers = package['plugin'].analyzers
    # run each analyzer
    for analyzer in analyzers:
        # run container/have thread waiting for analysis OR container itself should store result!
        kiskadee.analyzers.run(analyzer, sources)
    # store analysis in DB (another function?)
