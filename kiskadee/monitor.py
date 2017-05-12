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

def initialize():
    start(monitor);
    plugins = kiskadee.load_plugins()
    for plugin in plugins:
        name = plugin_name(plugin)
        create_plugin(name, plugin)
        start(plugin.watch)


def start(module):
    module_as_a_thread = Thread(target=module)
    module_as_a_thread.daemon = True
    module_as_a_thread.start()
    module_as_a_thread.join()


def monitor():
    while True:
        if not kiskadee.queue.packages_queue.empty():
            pkg = dequeue_package()
            save_or_update_pkgs(pkg)


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


def save_or_update_pkgs(pkg):
    name = plugin_name(pkg['plugin'])
    queue_file = "%s_queue_output" % name
    print("Writing output in %s file" % queue_file)
    _plugin = session.query(Plugin).filter(Plugin.name==name).first()
    if _plugin:
        if not session.query(Package).filter(Package.name==pkg['name']).first():
            _package = Package(name=pkg['name'],
                               plugin_id=_plugin.id)
            _version = Version(number=pkg['version'],
                               package_id=_package.id,
                               has_analysis=False)
            _package.versions.append(_version)
            session.add(_package)
            with open(queue_file, 'w+') as target:
                # In the future we will use some logging tool to do this.
                target.write("dequed package: %s \n" % str(pkg))

            session.commit()

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
    p = Process(target=initialize)
    p.daemon = True
    p.start()
    p.join()
    # cleanup goes here
