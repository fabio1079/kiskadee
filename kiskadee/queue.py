import queue

analyses_queue = queue.Queue()
packages_queue = queue.Queue()


def enqueue_analysis(package):
    analyses_queue.put(package)


def dequeue_analysis():
    return analyses_queue.get()


def analysis_done():
    analyses_queue.task_done()


def is_empty():
    return analyses_queue.empty()


def enqueue_package(package):
    packages_queue.put(package)


def dequeue_package():
    return packages_queue.get()


def package_done():
    packages_queue.task_done()


def source_enqueuer(func):
    """ Decorator to add the behavior of
    queue in the enqueue_analysis,
    some random value. """
    def wrapper(*args, **kwargs):
        source = func(*args, **kwargs)
        enqueue_analysis(source)
    return wrapper


def package_enqueuer(func):
    """ Decorator to add the behavior of
    queue in the enqueue_package,
    some random value. """
    def wrapper(*args, **kwargs):
        package = func(*args, **kwargs)
        enqueue_package(package)
    return wrapper
