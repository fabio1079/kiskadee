import queue

analysis_queue = queue.Queue()
package_queue = queue.Queue()


def analysis_enqueue(package):
    analysis_queue.put(package)


def analysis_dequeue():
    return analysis_queue.get()


def analysis_done():
    analysis_queue.task_done()

def is_empty():
    return analysis_queue.empty()

def package_enqueue(package):
    package_queue.put(package)


def package_dequeue():
    return package_queue.get()


def package_done():
    package_queue.task_done()
