import abc
import kiskadee


class Plugin():
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        self.name = __name__
        config_section = self.name + '_plugin'
        self.config = kiskadee.config[config_section]

    @abc.abstractmethod
    def get_sources(self):
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
