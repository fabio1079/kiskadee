"""Provide kiskadee monitoring capabilities.

kiskadee monitors repositories checking for new package versions to be
analyzed. This module provides such capabilities.
"""
import threading
from multiprocessing import Process
import time

import kiskadee.database
import kiskadee.runner
import kiskadee.queue
from kiskadee.model import Package, Plugin, Version
from kiskadee.util import _plugin_name

RUNNING = True


class Monitor:
    """Provide kiskadee monitoring objects."""

    def __init__(self, _session):
        """Return a non initialized Monitor."""
        self.session = _session

    def initialize(self):
        """Start all threads related to the monitoring process.

        This includes all plugins that enqueue packages in the packages_queue,
        and the monitor() method, which retrieves packages from packages_queue,
        and makes the necessary database operations

        .. warning::

            If a plugin does not enqueue the packages in the packages_queue,
            the analysis will never be performed. You can use thee decorator
            `@kiskadee.queue.package_enqueuer` to easiliy enqueue a package.
        """
        _start(self.monitor)
        plugins = kiskadee.load_plugins()
        for plugin in plugins:
            self._save_plugin(plugin)
            _start(plugin.Plugin().watch)
            time.sleep(1)
        _start(kiskadee.runner.runner, True)

    def monitor(self):
        """Dequeue packages and check if they need to be analyzed.

        The packages are dequeued from the `package_queue`. When a package
        needs to be analyzed, this package is enqueued in the `analyses_queue`
        queue so the runner component can trigger an analysis. Each plugin must
        enqueue its packages in the `packages_queue`.
        """
        while RUNNING:
            pkg = self.dequeue_package()
            if pkg:
                self._send_to_runner(pkg)
            time.sleep(2)
            package_to_save = self.dequeue_result()
            self._save_analyzed_pkg(package_to_save)

    def dequeue_package(self):
        """Dequeue packages from packages_queue."""
        if not kiskadee.queue.packages_queue.empty():
            pkg = kiskadee.queue.dequeue_package()
            kiskadee.queue.package_done()
            kiskadee.logger.debug(
                    "MONITOR: Dequed Package: {}_{}"
                    .format(pkg["name"], pkg["version"])
                )
            return pkg
        return {}

    def dequeue_result(self):
        """Dequeue analyzed packages from result_queue."""
        if not kiskadee.queue.result_queue.empty():
            pkg = kiskadee.queue.dequeue_result()
            kiskadee.logger.debug(
                    "MONITOR: Dequed result for package : {}_{}"
                    .format(pkg["name"], pkg["version"])
                )
            return pkg
        return {}

    def _send_to_runner(self, pkg):
        _name = _plugin_name(pkg['plugin'])
        _plugin = self._query(Plugin).filter(Plugin.name == _name).first()
        _package = (
                self._query(Package)
                .filter(Package.name == pkg['name']).first()
            )

        if _plugin:
            pkg["plugin_id"] = _plugin.id
            if not _package:
                kiskadee.logger.debug(
                        "MONITOR: Sending package {}_{} "
                        " for analysis".format(pkg['name'], pkg['version'])
                )
                kiskadee.queue.enqueue_analysis(pkg)
            else:
                new_version = pkg['version']
                analysed_version = _package.versions[-1].number
                plugin = pkg['plugin'].Plugin()
                if (plugin.compare_versions(new_version, analysed_version)):
                    kiskadee.queue.enqueue_analysis(pkg)

    def _save_analyzed_pkg(self, pkg):
        if not pkg:
            return {}

        _package = (
                self._query(Package)
                .filter(Package.name == pkg['name']).first()
            )
        if not _package:
            _package = self._save_pkg(pkg)
        if _package:
            _package = self._update_pkg(_package, pkg)

        for analyzer, result in pkg['results'].items():
            self._save_analysis(pkg, analyzer, result, _package.versions[-1])

    def _update_pkg(self, package, pkg):

        if(package.versions[-1].number == pkg['version']):
            return package
        try:
            _new_version = Version(
                    number=pkg['version'],
                    package_id=package.id
                    )
            package.versions.append(_new_version)
            self.session.add(package)
            self.session.commit()
            kiskadee.logger.debug(
                    "MONITOR: Sending package {}_{}"
                    "for analysis".format(pkg['name'], pkg['version'])
                    )
            return package
        except ValueError:
            kiskadee.logger.debug("MONITOR: Could not compare versions")
            return None

    def _save_pkg(self, pkg):
        _package = Package(name=pkg['name'],
                           plugin_id=pkg['plugin_id'])
        self.session.add(_package)
        self.session.commit()
        _version = Version(number=pkg['version'],
                           package_id=_package.id)
        self.session.add(_version)
        self.session.commit()
        return _package

    def _save_analysis(self, pkg, analyzer, result, version):
        _analysis = kiskadee.model.Analysis()
        try:
            _analyzer = self._query(kiskadee.model.Analyzer).\
                    filter(kiskadee.model.Analyzer.name == analyzer).first()
            _analysis.analyzer_id = _analyzer.id
            _analysis.version_id = version.id
            _analysis.raw = result
            self.session.add(_analysis)
            self.session.commit()
            kiskadee.logger.debug(
                    "MONITOR: Saved analysis for package: {}_{}"
                    .format(pkg["name"], pkg["version"])
                )
        except Exception as err:
            kiskadee.logger.debug(
                    "MONITOR: The required analyzer was" +
                    "not registered in kiskadee"
                )
            kiskadee.logger.debug(err)
            return None


    def _save_plugin(self, plugin):
        name = _plugin_name(plugin)
        plugin = plugin.Plugin()
        kiskadee.logger.debug(
                "MONITOR: Saving {} plugin in database".format(name)
            )
        if not self.session.query(Plugin).filter(Plugin.name == name).first():
            _plugin = Plugin(name=name,
                             target=plugin.config['target'],
                             description=plugin.config['description'])
            self.session.add(_plugin)
            self.session.commit()

    def _query(self, arg):
        return self.session.query(arg)


def _start(module, joinable=False, timeout=None):
    module_as_a_thread = threading.Thread(target=module)
    module_as_a_thread.daemon = True
    module_as_a_thread.start()
    if joinable or timeout:
        module_as_a_thread.join(timeout)


def daemon():
    """Entry point to the monitor module."""
    # TODO: improve with start/stop system
    session = kiskadee.database.Database().session
    monitor = Monitor(session)
    p = Process(target=monitor.initialize())
    p.daemon = True
    p.start()
    p.join()
