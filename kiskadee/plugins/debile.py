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

    def watch(self):
        pass

    def callback(self):
        pass

    def container_id(self):
        call(['docker', 'ps -aqf "name=debile-pg"'], shell=True)

    def check_debile(self, container):
        try:
            debile_container = self.client.containers.get('debile-%s' % container)
            debile_container.start()
            setattr(self, container, debile_container)
            return True
        except Exception:
            print('Container not created')
            return False

    def start_master(self):
        if not (self.check_debile('master')):
            print('Starting debile master')
            self.master = self.client.containers.run("debile-master-pkg",
                                                    "debile-master --config /etc/debile/master.yaml" \
                                                    "--sign simple",
                    name='debile-master', links={'debile-pg':'debile-pg'},
                    volumes_from=['debile-data'])

    def start_slave(self):
        if not (self.check_debile('slave')):
            print('Starting debile slave')
            self.slave = self.client.containers.run("debile-slave-pkg", "tail -f /dev/null",
                                   name='debile-slave', detach=True)

    def start_pg(self):
        if not(self.check_debile('pg')):
            self.pg = self.client.containers.run("clemux/debile-pg", "tail -f /dev/null",
                                   name='debile-pg', detach=True)
    def start_data(self):
        if not(self.check_debile('data')):
            self.pg = self.client.containers.run("clemux/debile-data", "tail -f /dev/null",
                                   name='debile-data', detach=True)

    def start_debile(self):
        self.start_pg()
        self.start_data()
        self.start_master()
        self.start_slave()

    def call(self):
        print(self.slave.exec_run("debile-upload --dist=unstable --source=vim --version=7.3.547-7 --group=test"))

        #TODO: docker python lib cannot stop container properly
        call(['docker', 'stop', 'debile-master'])

if __name__ == "__main__":
    runner = Runner()
    runner.start_debile()
    runner.call()
