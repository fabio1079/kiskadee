"""Provide kiskadee queues and operations on them."""
import time
import queue
from multiprocessing import Queue

import kiskadee

packages_queue = queue.Queue()

class KiskadeeQueue():

    def __init__(self):
        self.analysis = Queue()
        self.results = Queue()

    def enqueue_analysis(self, pkg):
        return self.analysis.put(pkg)

    def dequeue_analysis(self):
        return self.analysis.get()

    def dequeue_result(self):
        return self.results.get()

    def enqueue_result(self, pkg):
        return self.results.put(pkg)

    def results_empty(self):
        return self.results.empty()

def source_enqueuer(func):
    """Decorate functions to queue return values with enqueue_analysis."""
    def wrapper(*args, **kwargs):
        source = func(*args, **kwargs)
        enqueue_analysis(source)
    return wrapper

def package_enqueuer(func):
    """Decorate functions to queue return values with enqueue_package."""
    def wrapper(*args, **kwargs):
        package = func(*args, **kwargs)
        packages_queue.put(package)
        plugin = package['plugin'].name
        kiskadee.logger.debug(
                "{} plugin: Sending package {}_{} for monitor"
                .format(plugin, package['name'], package['version'])
            )
        time.sleep(2)
    return wrapper
