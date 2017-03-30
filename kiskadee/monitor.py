import kiskadee.model
import kiskadee.queue


def sync_analyses():
    """enqueues package versions without analyses in the db for analysis"""
    # sweep db for versions without analyses
    # if queue empty
    # enqueue all
    # else: check the queue for each package version and running jobs?
    # run analysis on the one not in queue nor under analysis
    # we could also empty the queue in the very begining of this task
    pass


def monitor_repository():
    pass
    # for plugin in plugins:
    #   #  plugin.watch() # background?
    # how to receive messages and enqueue?
    # use decorators to jeep runing the function and enqueuing stuff?


def enqueue_new_package(package_version):
    kiskadee.queue.enqueue(package_version)
