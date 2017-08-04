"""Provide kiskadee queues and operations on them."""
import time
import queue
from multiprocessing import Queue

import kiskadee

packages_queue = queue.Queue()


class KiskadeeQueue():
    """Provide kiskadee queues objects."""

    def __init__(self):
        """Initialize a kiskadee queue object."""
        self.analysis = Queue()
        self.results = Queue()

    def enqueue_analysis(self, pkg):
        """Put a analysis on the analysis queue."""
        return self.analysis.put(pkg)

    def dequeue_analysis(self):
        """Get a analysis from the analysis queue."""
        return self.analysis.get()

    def dequeue_result(self):
        """Get a result from the results queue."""
        return self.results.get()

    def enqueue_result(self, pkg):
        """Put a result on the results queue."""
        return self.results.put(pkg)

    def results_empty(self):
        """Check if the results queue is empty."""
        return self.results.empty()


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
