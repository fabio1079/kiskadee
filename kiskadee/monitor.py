import kiskadee.model
from kiskadee.queue import enqueue_analysis, dequeue_package, \
        enqueue_package
import threading
from threading import Thread
from multiprocessing import Process
from kiskadee.model import Package, Plugin, Version, Base
from kiskadee.database import Database


class Monitor:

    def __init__(self):
        self.engine = None
        self.session = None


    def sync_analyses(self):
        """enqueues package versions without analyses in the db for analysis"""
        # sweep db for versions without analyses
        # if queue empty
        # enqueue all
        # else: check the queue for each package version and running jobs?
        # run analysis on the one not in queue nor under analysis
        # we could also empty the queue in the very begining of this task
        pass


    def initialize(self):
        """ Starts all the threads involves with the monitoring process.
        This includes all the plugins, that queuing packages in the packages_queue,
        and the monitor() method, that retrieve  packages from the packages_queue,
        and makes the necessary database operations """

        try:
            database = Database()
            self.engine = database.engine
            self.session = database.session
            self._start(self.monitor, False)
            plugins = kiskadee.load_plugins()
            for plugin in plugins:
                name = self._plugin_name(plugin)
                self._create_plugin(name, plugin)
                self._start(plugin.watch, True)
        except Exception:
            print("Database not found")



    def _start(self, module, joinable=False):
        module_as_a_thread = Thread(target=module)
        module_as_a_thread.daemon = True
        module_as_a_thread.start()
        if joinable:
            module_as_a_thread.join()


    def monitor(self):
        """ Continuous dequeue packages from packages_queue """
        Base.metadata.create_all(self.engine)
        Base.metadata.bind = self.engine
        while True:
            if not kiskadee.queue.packages_queue.empty():
                pkg = dequeue_package()
                self._save_or_update_pkgs(pkg)


    def _save_or_update_pkgs(self, pkg):
        name = self._plugin_name(pkg['plugin'])
        queue_file = "%s_queue_output" % name
        _plugin = self.session.query(Plugin).filter(Plugin.name==name).first()
        if _plugin:
            if not self.session.query(Package).filter(Package.name==pkg['name']).first():
                _package = Package(name=pkg['name'],
                                plugin_id=_plugin.id)
                _version = Version(number=pkg['version'],
                                package_id=_package.id,
                                has_analysis=False)
                _package.versions.append(_version)
                self.session.add(_package)
                print("Writing output in %s file" % queue_file)
                with open(queue_file, 'w+') as target:
                    # In the future we will use some logging tool to do this.
                    target.write("dequed package: %s \n" % str(pkg))

                self.session.commit()


    def _plugin_name(self, plugin):
        return plugin.__name__.split('.')[len(plugin.__name__.split('.')) - 1]

    def _create_plugin(self, name, plugin):
        if not self.session.query(Plugin).filter(Plugin.name==name).first():
            _plugin = Plugin(name=name,
                    target=plugin.PLUGIN_DATA['target'],
                    description=plugin.PLUGIN_DATA['description'])
            self.session.add(_plugin)
            self.session.commit()


def daemon():
    """ Entry point to the monitor module """
    # TODO: improve with start/stop system
    monitor = Monitor()
    p = Process(target=monitor.initialize())
    p.daemon = True
    p.start()
    p.join()
    # cleanup goes here
