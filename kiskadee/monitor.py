import kiskadee.model
from kiskadee.queue import enqueue_analysis, dequeue_package, \
        enqueue_package
import threading
from multiprocessing import Process
from kiskadee.model import Package, Plugin, Version, Base
from kiskadee.database import Database
from kiskadee.helpers import _start
import logging


class Monitor:

    def __init__(self):
        self.engine = None
        self.session = None
        self.running = True
        self.logger = logging.getLogger()


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

        database = Database()
        self.engine = database.engine
        self.session = database.session
        _start(self.monitor, False)
        plugins = kiskadee.load_plugins()
        for plugin in plugins:
            self._save_plugin(plugin)
            _start(plugin.watch, True)

    def monitor(self):
        """ Continuosly check new packages and save it in db """
        Base.metadata.create_all(self.engine)
        Base.metadata.bind = self.engine
        while self.running:
            pkg = self.dequeue()
            if pkg:
                self._save_or_update_pkgs(pkg)

    def dequeue(self):
        """ dequeue packages from packages_queue """
        if not kiskadee.queue.packages_queue.empty():
            pkg = dequeue_package()
            self.logger.debug("Dequed Package: %s"  % str(pkg))
            return pkg
        return {}


    def _save_or_update_pkgs(self, pkg):
        name = self._plugin_name(pkg['plugin'])
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

                self.logger.debug("Saving package in db: %s"  % str(pkg))
                self.session.commit()


    def _plugin_name(self, plugin):
        return plugin.__name__.split('.')[len(plugin.__name__.split('.')) - 1]

    def _save_plugin(self, plugin):
        name = self._plugin_name(plugin)
        self.logger.debug("Saving %s plugin in database" % name)
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
