import kiskadee.model
import kiskadee.queue

running = True
watchers = []  # functions decorated with watcher()


def sync_analyses():
    """enqueues package versions without analyses in the db for analysis"""
    # sweep db for versions without analyses
    # if queue empty
    # enqueue all
    # else: check the queue for each package version and running jobs?
    # run analysis on the one not in queue nor under analysis
    # we could also empty the queue in the very begining of this task
    pass


def monitor():
    kiskadee.load_plugins()
    for watch in watchers:
        watch()


def watcher(watch):
    watchers.append(watch)

    def wrapper(*args, **kwargs):
        packages = watch(*args, **kwargs)
        for package in packages:
            kiskadee.queue.enqueue(package)
    return wrapper

if __name__ == "__main__":
    # TODO: improve with start/stop system
    while running:
        monitor()
    # cleanup goes here
