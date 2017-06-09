"""This module provides functions to run static analyzers."""

import docker


def run(analyzer, sources):
    """Run a static analyzer on a given package.

    `analyzer` is the name of the static analyzer container to run.
    `sources` is the absolute path for the uncompressed package. Returns
    a analysis results.
    """
    volume = {sources: {'bind': '/src', 'mode': 'ro'}}
    client = docker.from_env()
    # FIXME: Since we are using only cppcheck for now, we only want stderr
    return client.containers.run(analyzer, '/src', volumes=volume,
                                 stdout=False, stderr=True)
