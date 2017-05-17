import abc
import kiskadee
import inspect


class Plugin():
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        full_name = inspect.getmodule(self).__name__
        self.name = full_name.split('.')[-1]
        config_section = self.name + '_plugin'
        self.config = kiskadee.config[config_section]

    @abc.abstractmethod
    def get_sources(self, name, version, *args, **kwargs):
        """Returns the absolute path for a compressed file
        containing the package source code
        """
        raise NotImplementedError('get_sources must be defined by plugin')

    @abc.abstractmethod
    def watch(self):
        raise NotImplementedError('watch must be defined by plugin')

    def analyzers(self):
        """Get active analyzers for current plugin

        This information should live in kiskadee's configuration file as
        the name of each analyzer separated by spaces.
        """
        if not self.config['analyzers']:
            return kiskadee.config['analyzers'].split()
        else:
            return self.config['analyzers'].split()
