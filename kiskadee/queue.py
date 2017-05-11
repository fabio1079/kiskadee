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
