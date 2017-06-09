"""Provide kiskadee queues and operations on them."""

import queue

analyses_queue = queue.Queue()
packages_queue = queue.Queue()


def enqueue_analysis(package):
    """Enqueue a package for analysis.

    A package abstraction is a dict with the following key, value pairs:
        - plugin: the module object of a kiskadee plugin.
        - name: package name.
        - version: package version.
    """
    analyses_queue.put(package)


def dequeue_analysis():
    """Dequeue a package for analysis.

    A package abstraction is a dict with the following key, value pairs:
        - plugin: the module object of a kiskadee plugin.
        - name: package name.
        - version: package version.
    """
    return analyses_queue.get()


def analysis_done():
    """Anounce analysis is finished."""
    analyses_queue.task_done()


def is_empty():
    """Check if `analyses_queue is empty`.

    Returns True if the queue is empty and False otherwise.
    """
    return analyses_queue.empty()


def enqueue_package(package):
    """Enqueue a package for monitoring purposes.

    A package abstraction is a dict with the following key, value pairs:
        - plugin: the module object of a kiskadee plugin.
        - name: package name.
        - version: package version.
    """
    packages_queue.put(package)


def dequeue_package():
    """Dequeue a package for monitoring purposes.

    A package abstraction is a dict with the following key, value pairs:
        - plugin: the module object of a kiskadee plugin.
        - name: package name.
        - version: package version.
    """
    return packages_queue.get()


def package_done():
    """Anounce package was verified."""
    packages_queue.task_done()


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
        enqueue_package(package)
    return wrapper
