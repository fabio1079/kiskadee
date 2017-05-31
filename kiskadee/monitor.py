import kiskadee
import kiskadee.database
import kiskadee.runner
import kiskadee.queue
import threading
from multiprocessing import Process
from kiskadee.model import Package, Plugin, Version, Base
import time


class Monitor:

    def __init__(self):
        self.engine = None
        self.session = None
        self.running = True
        self.logger = kiskadee.logger

    def initialize(self):
        """ Starts all the threads involved with the monitoring process.
        This includes all plugins that queue packages in the packages_queue,
        and the monitor() method, which retrieves packages from packages_queue,
        and makes the necessary database operations """

        database = kiskadee.database.Database()
        self.engine = database.engine
        self.session = database.session
        Base.metadata.create_all(self.engine)
        Base.metadata.bind = self.engine
        _start(self.monitor)
        plugins = kiskadee.load_plugins()
        for plugin in plugins:
            self._save_plugin(plugin)
            _start(plugin.Plugin().watch)
            time.sleep(1)
        _start(kiskadee.runner.runner, True)

    def monitor(self):
        """ Continuosly check new packages and save it in db """
        while self.running:
            pkg = self.dequeue()
            if pkg:
                self._save_or_update_pkg(pkg)

    def dequeue(self):
        """ dequeue packages from packages_queue """
        if not kiskadee.queue.packages_queue.empty():
            pkg = kiskadee.queue.dequeue_package()
            kiskadee.queue.package_done()
            self.logger.info("Dequed Package: {}".format(str(pkg)))
            time.sleep(1)
            return pkg
        return {}

    def _save_or_update_pkg(self, pkg):
        _name = self._plugin_name(pkg['plugin'])
        _plugin = self._query(Plugin).filter(Plugin.name == _name).first()
        if _plugin:
            if not self._query(Package).\
                    filter(Package.name == pkg['name']).first():
                self._save_pkg(pkg, _plugin)
            else:
                self._update_pkg_version(pkg)

    def _save_pkg(self, pkg, _plugin):
        _package = Package(name=pkg['name'],
                           plugin_id=_plugin.id)
        _version = Version(number=pkg['version'],
                           package_id=_package.id,
                           has_analysis=False)
        _package.versions.append(_version)
        self.session.add(_package)
        self.logger.info("Saving package in db: {}".format(str(pkg)))
        self.session.commit()
        self.logger.info("Enqueue package {}_{} "
                         " for analysis".format(pkg['name'], pkg['version']))
        kiskadee.queue.enqueue_analysis(pkg)


    def _update_pkg_version(self, pkg):
        _pkg = self._query(Package).filter(Package.name == pkg['name']).first()
        current_pkg_version = _pkg.versions[-1].number

        try:
            if pkg['plugin'].Plugin().compare_versions(pkg['version'], current_pkg_version) == 1:
                _new_version = Version(number=pkg['version'],
                                       package_id=_pkg.id,
                                       has_analysis=False)
                _pkg.versions.append(_new_version)
                self.session.add(_pkg)
                self.session.commit()
                self.logger.info("Enqueue package {}_{}"
                                 "for analysis".format(pkg['name'], pkg['version']))
                kiskadee.queue.enqueue_analysis(pkg)
            else:
                return {}
        except ValueError:
            self.logger.info("Could not compare versions")

    def _plugin_name(self, plugin):
        return plugin.__name__.split('.')[len(plugin.__name__.split('.')) - 1]

    def _save_plugin(self, plugin):
        plugin = plugin.Plugin()
        name = plugin.name
        self.logger.info("Saving {} plugin in database".format(name))
        if not self.session.query(Plugin).filter(Plugin.name == name).first():
            _plugin = Plugin(name=name,
                             target=plugin.config['target'],
                             description=plugin.config['description'])
            self.session.add(_plugin)
            #self.session.commit()

    def _query(self, arg):
        return self.session.query(arg)


def _start(module, joinable=False, timeout=None):
    module_as_a_thread = threading.Thread(target=module)
    module_as_a_thread.daemon = True
    module_as_a_thread.start()
    if joinable or timeout:
        module_as_a_thread.join(timeout)


def daemon():
    """ Entry point to the monitor module """
    # TODO: improve with start/stop system
    monitor = Monitor()
    p = Process(target=monitor.initialize())
    p.daemon = True
    p.start()
    p.join()
    # cleanup goes here
