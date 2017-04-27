import kiskadee.model
import kiskadee.queue

running = True


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
    plugins = kiskadee.load_plugins()
    for plugin in plugins:
        packages = plugin.watch()
        for package in packages:
            kiskadee.queue.enqueue(package)


if __name__ == "__main__":
    # TODO: improve with start/stop system
    while running:
        monitor()
    # cleanup goes here
