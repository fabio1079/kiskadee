from importlib import import_module
import sys

def main():
    """ Here we will load all the plugins passed by
    configuration file to kiskadee.
    """
    # TODO: Move this method to other module, cli
    # will be responsable only to parse kiskadee's input
    # TODO: Make this code more generic, in order to enable
    # run the same setup code to several plugins. Maybe create a
    # interface that define the behavior of the plugins.
    from kiskadee.plugins.debian import debian
    requested_source = sys.argv[1]
    debian.watch(requested_source)
