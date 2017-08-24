"""Fetcher package.

Each kiskadee fetcher must be a module in this package that implements the
Fetcher class here defined.
"""

import abc
import kiskadee
import inspect


class Fetcher():
    """Abstract Fetcher class."""

    __metaclass__ = abc.ABCMeta

    def __init__(self):
        """Return a new kiskadee Fetcher.

        The fetcher name is the module name.
        There MUST be a [FETCHER_NAME_fetcher] section in kiskadee.conf
        for each fetcher. Refer to the configuration file documentation
        for more information.
        """
        full_name = inspect.getmodule(self).__name__
        self.name = full_name.split('.')[-1]
        config_section = self.name + '_fetcher'
        self.config = kiskadee.config[config_section]

    @abc.abstractmethod
    def get_sources(package):
        """Return the absolute path of compressed package source code.

        `source_data` will be a dictionary previously created by the fetcher.
        `source_data` will have at least two obrigatory keys: `name` and
        `version` of the package that have to be downloaded.
        """
        raise NotImplementedError('get_sources must be defined by fetcher')

    @abc.abstractmethod
    def watch(self):
        """Continuously monitor some target repository.

        This method will be called as a thread, and will run concurrently with
        the main kiskadee thread.  This method must enqueue packages using the
        `@kiskadee.queue.package_enqueuer` decorator.
        """
        raise NotImplementedError('watch must be defined by fetcher')

    @abc.abstractmethod
    def compare_versions(self, new, old):
        """Return *true* if `new` is greater then `old`.

        `new` and `old` will be the versions of packages monitored by your
        fetcher.
        """
        raise NotImplementedError(
                'compare_versions must be defined by fetcher'
            )

    def analyzers(self):
        """Get active analyzers for current fetcher.

        This information should live in kiskadee's configuration file as
        the name of each analyzer separated by spaces.
        """
        if not self.config.get('analyzers'):
            fetcher_name = self.name + '_fetcher'
            return kiskadee.config[fetcher_name].get('analyzers').split()
        else:
            return self.config.get('analyzers').split()