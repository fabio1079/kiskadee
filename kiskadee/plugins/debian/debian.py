from kiskadee.plugins.debian.analyzers import cppcheck

def init():
    """TODO: Docstring for init.

    :arg1: TODO
    :returns: TODO

    """
    print(cppcheck.version())

def download_source_package(pkg_name, pkg_version):
    """Download packages from some debian mirror.

    :pkg_name: package name (a.g mutt)
    :pkg_version: package version (a.g 1.7.5-1)
    :returns: source package

    OBS: Other plugins may have this behavior,
    find a better place (module) to this method.
    """
    pass
