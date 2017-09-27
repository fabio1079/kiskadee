"""Provide kiskadee monitoring capabilities.

kiskadee monitors repositories checking for new package versions to be
analyzed. This module provides such capabilities.
"""
import threading
from multiprocessing import Process
import time
import os
import json

import kiskadee.database
from kiskadee.report import CppcheckReport, FlawfinderReport
from kiskadee.runner import Runner
import kiskadee.queue
from kiskadee.model import Package, Fetcher, Version, Report

RUNNING = True

REPORTERS = {
    'cppcheck': CppcheckReport,
    'flawfinder': FlawfinderReport
}


class Monitor:
    """Provide kiskadee monitoring objects."""

    def __init__(self, _session):
        """Return a non initialized Monitor."""
        self.session = _session
        self.kiskadee_queue = None

    def monitor(self, kiskadee_queue):
        """Dequeue packages and check if they need to be analyzed.

        The packages are dequeued from the `package_queue`. When a package
        needs to be analyzed, this package is enqueued in the `analyses_queue`
        so the runner component can trigger an analysis.  Each fetcher must
        enqueue its packages in the `packages_queue`.
        """
        kiskadee.logger.debug('kiskadee PID: {}'.format(os.getppid()))
        kiskadee.logger.debug('Starting monitor subprocess')
        kiskadee.logger.debug('monitor PID: {}'.format(os.getpid()))
        fetchers = kiskadee.load_fetchers()
        for fetcher in fetchers:
            self._save_fetcher(fetcher.Fetcher())
            _start_fetcher(fetcher.Fetcher().watch)

        while RUNNING:
            self.kiskadee_queue = kiskadee_queue
            pkg = self.dequeue_package()
            if pkg:
                self._send_to_runner(pkg)
            time.sleep(2)
            package_to_save = self.dequeue_result()
            self._save_analyzed_pkg(package_to_save)

    def dequeue_package(self):
        """Dequeue packages from packages_queue."""
        if not kiskadee.queue.packages_queue.empty():
            pkg = kiskadee.queue.packages_queue.get()
            kiskadee.logger.debug(
                    "MONITOR: Dequed Package: {}_{}"
                    .format(pkg["name"], pkg["version"])
                )
            return pkg
        return {}

    def dequeue_result(self):
        """Dequeue analyzed packages from result_queue."""
        if not self.kiskadee_queue.results_empty():
            pkg = self.kiskadee_queue.dequeue_result()
            kiskadee.logger.debug(
                    "MONITOR: Dequed result for package : {}_{}"
                    .format(pkg["name"], pkg["version"])
                )
            return pkg
        return {}

    def _send_to_runner(self, pkg):
        _name = pkg['fetcher'].name
        _fetcher = self._query(Fetcher).filter(Fetcher.name == _name).first()
        _package = (
                self._query(Package)
                .filter(Package.name == pkg['name']).first()
            )

        if _fetcher:
            pkg["fetcher_id"] = _fetcher.id
            if not _package:
                kiskadee.logger.debug(
                        "MONITOR: Sending package {}_{} "
                        " for analysis".format(pkg['name'], pkg['version'])
                )
                self.kiskadee_queue.enqueue_analysis(pkg)
            else:
                new_version = pkg['version']
                analysed_version = _package.versions[-1].number
                fetcher = pkg['fetcher']
                if (fetcher.compare_versions(new_version, analysed_version)):
                    self.kiskadee_queue.enqueue_analysis(pkg)

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
                           fetcher_id=pkg['fetcher_id'])
        self.session.add(_package)
        self.session.commit()
        _version = Version(number=pkg['version'],
                           package_id=_package.id)
        self.session.add(_version)
        self.session.commit()
        return _package

    def _save_reports(self, analysis, pkg, analyzer_name):
        try:
            results = analysis['results']
            analyzer_report = REPORTERS[analyzer_name](results)
            _reports = Report()
            _reports.results = json.dumps(
                    analyzer_report
                    ._compute_reports(analyzer_name)
                )
            _reports.analysis_id = analysis['id']
            self.session.add(_reports)
            self.session.commit()
            kiskadee.logger.debug(
                    "MONITOR: Saved analysis reports for {} package"
                    .format(pkg["name"])
                )
        except KeyError as key:
            kiskadee.logger.debug(
                    "ERROR: There's no reporter " +
                    "to get reports from {} analyzer. ".format(key) +
                    "Make shure to import or implement them."
                )
        except Exception as err:
            kiskadee.logger.debug(
                    "MONITOR: Failed to get analysis reports to {} package"
                    .format(pkg["name"])
                )
            kiskadee.logger.debug(err)
        return

    def _save_analysis(self, pkg, analyzer, result, version):
        _analysis = kiskadee.model.Analysis()
        try:
            _analyzer = self._query(kiskadee.model.Analyzer).\
                    filter(kiskadee.model.Analyzer.name == analyzer).first()
            _analysis.analyzer_id = _analyzer.id
            _analysis.version_id = version.id
            _analysis.raw = json.loads(result)
            self.session.add(_analysis)
            self.session.commit()
            dict_analysis = {
                    'results': _analysis.raw['results'],
                    'id': _analysis.id
                }
            self._save_reports(dict_analysis, pkg, _analyzer.name)
            kiskadee.logger.debug(
                    "MONITOR: Saved analysis done by {} for package: {}_{}"
                    .format(analyzer, pkg["name"], pkg["version"])
                )
            return
        except Exception as err:
            kiskadee.logger.debug(
                    "MONITOR: The required analyzer was " +
                    "not registered in kiskadee"
                )
            kiskadee.logger.debug(err)
            return None

    def _save_fetcher(self, fetcher):
        name = fetcher.name
        kiskadee.logger.debug(
                "MONITOR: Saving {} fetcher in database".format(name)
            )
        if not self.session.query(Fetcher)\
                .filter(Fetcher.name == name).first():
            _fetcher = Fetcher(
                    name=name,
                    target=fetcher.config['target'],
                    description=fetcher.config['description']
                )
            self.session.add(_fetcher)
            self.session.commit()

    def _query(self, arg):
        return self.session.query(arg)


def _start_fetcher(module, joinable=False, timeout=None):
    module_as_a_thread = threading.Thread(target=module)
    module_as_a_thread.daemon = True
    module_as_a_thread.start()
    if joinable or timeout:
        module_as_a_thread.join(timeout)


def daemon():
    """Entry point to the monitor module."""
    # TODO: improve with start/stop system
    _kiskadee_queue = kiskadee.queue.KiskadeeQueue()
    session = kiskadee.database.Database().session
    monitor = Monitor(session)
    runner = Runner()
    monitor_process = Process(
            target=monitor.monitor,
            args=(_kiskadee_queue,)
        )
    runner_process = Process(
            target=runner.runner,
            args=(_kiskadee_queue,)
        )
    monitor_process.start()
    runner_process.start()
    runner_process.join()
