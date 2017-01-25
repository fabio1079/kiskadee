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
        self.slave = None
        self.master = None
        self.pg = None
        self.data = None
        self.http = None

    def watch(self):
        pass

    def callback(self):
        pass

    def container_id(self):
        call(['docker', 'ps -aqf "name=debile-pg"'], shell=True)

    def retrieve_container(self, container_name):
        try:
            container = self.containers().get('debile-%s' % container_name)
            setattr(self, container_name, container)
            self.start_container(container)
        except Exception:
            print("Something went wrong and " +
                  "container was not properly started")
            method_call = getattr(self, "run_%s" % container_name)
            method_call()

    def start_container(self, container):
        try:
            container.start()
            return container
        except Exception:
            print('Container already runnin')
            return container

    def check(self):
        containers = ['data', 'pg', 'http',
                      'master', 'slave']
        for container in containers:
            self.retrieve_container(container)
            self.start_container(container)

    def run_master(self):
            print('Starting debile master')
            self.master = self.containers().run("debile-master-pkg",
                                                "debile-master --config " +
                                                "/etc/debile/master.yaml " +
                                                "--auth simple",
                                                name='debile-master',
                                                links={'debile-pg': 'debile-pg'},
                                                volumes_from=['debile-data'],
                                                detach=True)

    def run_slave(self):
            print('Starting debile slave')
            self.slave = self.containers().run("debile-slave-pkg",
                                               "tail -f /dev/null",
                                               links={'debile-http': 'debile-http',
                                                      'debile-master': 'debile-master'},
                                               name='debile-slave',
                                               detach=True)

    def run_pg(self):
            self.pg = self.containers().run("clemux/debile-pg",
                                            "tail -f /dev/null",
                                            name='debile-pg',
                                            ports={'5432': '5432'},
                                            detach=True)
    def run_data(self):
            self.pg = self.containers().run("clemux/debile-data",
                                            "tail -f /dev/null",
                                            name='debile-data',
                                            detach=True)

    def run_http(self):
            self.http = self.containers().run("clemux/debile-http",
                                              "tail -f /dev/null",
                                              name='debile-http',
                                              volumes_from=['debile-data'],
                                              ports={'80': '80'},
                                              detach=True)

    def upload(self):
        print(self.slave.exec_run("debile-upload --dist=unstable " +
                                  "--source=mutt --version=1.7.1-5 " +
                                  "--group=default"))

    def containers(self):
        return self.client.containers

if __name__ == "__main__":
    debile = Runner()
    debile.check()
    debile.upload()
