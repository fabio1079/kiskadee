import docker


def run(analyzer, sources):
    """ Runs a static analyzer on a given package

    analyzer: name of the static analyzer container to run
    sources: absolute path for the uncompressed package
    return: analysis results
    """
    volume = {sources: {'bind': '/src', 'mode': 'ro'}}
    client = docker.from_env()
    # FIXME: Since we are using only cppcheck for now, we only care about stderr
    return client.containers.run(analyzer, '/src', volumes=volume, stdout=False, stderr=True)
