import queue

analysis_queue = queue.Queue


def enqueue(package):
    analysis_queue.put(package)


def dequeue():
    return analysis_queue.get()
