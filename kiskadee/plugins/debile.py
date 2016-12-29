from subprocess import call
import os
import docker
message = 'message structure goes here'

# Debile submodule
runner_name = 'debian_runner'

base_docker_dir = '/contrib/clemux/docker'
runner_dir = runner_name + base_docker_dir


class Runner():

    def __init__(self):
        self.client = docker.from_env()
        self.docker_root = os.path.dirname(os.path.realpath(__file__)) + "/../%s" % runner_dir
        self.synced_root = os.path.dirname(os.path.realpath(__file__)) + "/../%s" % runner_name
        self.container = None

    def watch(self):
        pass

    def callback(self):
        pass

    def valid_env(self):
        env_docker = call('docker', shell=True)
        return env_docker <= 0

    def container_id(self):
        call(['docker', 'ps -aqf "name=debile-pg"'], shell=True)

    def check_master(self):
        try:
            self.container = self.client.containers.get('debile-master')
            self.container.start()
            return self.container
        except Exception:
            print('Container not created')
            return False
        pass

    def start_master(self):
        if not (self.check_master()):
            print('Creating container')
            self.container = self.client.containers.run("clemux/debile-master", "tail -f /dev/null",
                name='debile-master',detach=True,
                volumes={self.synced_root: {'bind': '/srv/debile/sync_repo', 'mode': 'rw'}})

        return self.container

    def run(self):
        print(self.container.exec_run("ls"))

        #TODO: docker python lib cannot stop container properly
        call(['docker', 'stop', 'debile-master'])

if __name__ == "__main__":
    runner = Runner()
    container = runner.start_master()
    runner.run()
