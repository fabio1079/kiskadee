import kiskadee.model
from kiskadee.queue import enqueue_analysis, dequeue_package, \
        enqueue_package
import threading
from threading import Thread
from multiprocessing import Process
from kiskadee.model import Package, Plugin, Version, session


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
        name = plugin_name(plugin)
        create_plugin(name, plugin)
        print("Starting %s plugin" % name)
        consumer_queue = Thread(target=save_or_update_pkgs,
                                args=(name,))
        consumer_queue.daemon = True
        consumer_queue.start()
        plugin_thread = Thread(target=plugin.watch)
        plugin_thread.daemon = True
        plugin_thread.start()
        plugin_thread.join()


def enqueue_source(func):
    def wrapper(*args, **kwargs):
        sources = func(*args, **kwargs)
        for source in sources:
            enqueue_analysis(source)
    return wrapper


def enqueue_pkg(func):
    def wrapper(*args, **kwargs):
        package = func(*args, **kwargs)
        enqueue_package(package)
    return wrapper


def save_or_update_pkgs(plugin_name):
    queue_file = "%s_queue_output" % plugin_name
    print("Writing output in %s file" % queue_file)
    with open(queue_file, '+w') as target:
        while True:
            # In the future we will use some logging tool to do this.
            pkg = dequeue_package()
            target.write("dequed package: %s \n" % str(pkg))

            # Database stuff here.

def plugin_name(plugin):
    return plugin.__name__.split('.')[len(plugin.__name__.split('.')) - 1]

def create_plugin(name, plugin):
    if not session.query(Plugin).filter(Plugin.name==name).first():
        _plugin = Plugin(name=name,
                target=plugin.PLUGIN_DATA['target'],
                description=plugin.PLUGIN_DATA['description'])
        session.add(_plugin)
        session.commit()

def daemon():
    # TODO: improve with start/stop system
    p = Process(target=monitor)
    p.daemon = True
    p.start()
    p.join()
    # cleanup goes here
