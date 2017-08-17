# kiskadee

kiskadee is a continuous static analysis tool which writes the analysis results
into a Firehose database.

## Running

To run kiskadee, you must have docker installed and running. Use the
dockerfiles in the `util` directory to build the images for each static
analyzer. The name of the image must be equal of the analyzer name.
You can accomplish that by doing

    docker build . -t cppcheck

With the Docker images build, create a virtualenv to kiskadee

    sudo dnf install virtualenv
    virtualenv -p /usr/bin/python3
    source bin/activate

Install some package dependencies. The name of the dependencies are compatible
with the Fedora distribution. If you use another distribution, you will have
to find the compatible name for the dependencies. The `redhat-rpm-config` 
package, is a specific Fedora dependency. If you are not in Fedora (or a
Red Hat distribution), maybe you will not have to install it.

    sudo dnf install openssl-devel python3-devel gcc redhat-rpm-config

Kiskadee use postgresql as database. You will need to create a database named
kiskadee, with a role kiskadee as owner.

Install python dependencies and run kiskadee

    pip install -e .
    pip install "fedmsg[consumers]"


If you are using distribution with selinux, be aware that you must set
permissions so the container can access external files.

Kiskadee looks for its configuration file under `util/kiskadee.conf`. 
If everything goes well till now, open the kiskadee.conf file, and set as
active only the example fetcher. Now run kiskadee by typing `kiskadee` on
the terminal. If the Docker images was properly build, and the Docker client
was properly configured on your machine, kiskadee will be able to analysis a
exemple source code. This code is in the kiskadee/tests/test\_source/ directory.

To run the API just run the command `kiskadee_api`.

### Anitya Fetcher
If you intend to run the anitya fetcher, you will have to install fedmsg-hub,
in order to kiskadee be able to consume the fedmsg events.
To install fedmsg-hub follow this steps inside the kiskadee root path:

    # Run this inside the kiskadee's virtualenv
    sudo mkdir -p /etc/fedmsg.d/
    sudo cp util/base.py util/endpoints.py  /etc/fedmsg.d/
    sudo cp util/anityaconsumer.py /etc/fedmsg.d/
    PYTHONPATH=`pwd` fedmsg-hub

With this steps, fedmsg-hub will instantiate `AnityaConsumer` and publish
the monitored events using ZeroMQ. When kiskadee starts it will consume
the messages published by the consumer, and will run the analysis.

The events that comes to the anitya fetcher are published by Anitya, on this
[page](https://apps.fedoraproject.org/datagrepper/raw?category=anitya.)

For more info about the Anitya service, read kiskadee documentation.

### Debian Fetcher
If you intend to use the debian fetcher, you will have to install the
`devscripts` package, in order use the necessary Debian tools to run the
fetcher.

## Development

Kiskadee daemon and API development are hosted at [pagure](https://pagure.io/kiskadee).

Kiskadee frontend is hosted at [pagure](https://pagure.io/kiskadee/kiskadee_ui).
Feel free to open issues and pull requests there.

We also have mirrors on [gitlab](https://gitlab.com/kiskadee/kiskadee) and 
[github](https://github.com/LSS-USP/kiskadee).

Kiskadee have a CI environment hosted at this [url](http://143.107.45.126:30130/blue/organizations/jenkins/LSS-USP%2Fkiskadee/activity).
## Documentation

[kiskadee documentation is hosted at pagure.](docs.pagure.org/kiskadee)

To build the documentation just entry in the doc directory, and run

    make html

To access the documentation open the `index.html` file, inside the 
doc/\_build/html.

## License

Copyright (C) 2017 the AUTHORS (see the AUTHORS file)

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
