"""This module provides functions to run static analyzers."""

import docker
from subprocess import check_output

def run(analyzer, sources):
    """Run a static analyzer on a given package.

    `analyzer` is the name of the static analyzer container to run.
    `sources` is the absolute path for the uncompressed package. Returns
    a analysis results.
    """
    volume = {sources: {'bind': '/src', 'mode': 'Z'}}
    client = docker.from_env(version='auto')
    uid = int(check_output("echo $UID", shell=True))
    return client.containers.run(analyzer, '/src', volumes=volume,
                                 environment={'KISKADEE_UID': uid},
                                 stderr=True, stdout=True, tty=True)
