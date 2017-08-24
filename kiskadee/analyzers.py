"""This module provides functions to run static analyzers."""

import subprocess
import os

def run(analyzer, sources):
    """Run a static analyzer on a given package.

    `analyzer` is the name of the static analyzer container to run.
    `sources` is the absolute path for the uncompressed package. Returns
    a analysis results.
    """
    volume = ''.join([sources, ':', '/src'])
    uid = os.getuid()
    return subprocess.check_output(
            "docker run -e KISKADEE_UID={} "
            "-v {} {}".format(uid, volume, analyzer),
            shell=True, stderr=subprocess.STDOUT)
