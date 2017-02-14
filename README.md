# kiskadee

kiskadee is a continuous static analysis tool which writes the analyses
results into a Firehose database.

## Dependencies

In order to install kiskadee dependencies, just run `pip install -e .`

To install docker package, you will need libffi package(in Debian you will
have to install libffi-dev package).

## Architecture

Note: we may substitute fedmsg by rabbitMQ, since it supports queues.

### kiskadee package

#### monitor
  
* load database packages and versions into redis
* loads all plugins watch() functions
* load all repositories package versions with the watch() functions 
* compares repository versions against db versions in redis
* writes differences in fedmsg using the plugin specified message
  * When to update redis information?

#### runner

* loads all plugins callback() function and message string
* listen to fedmsg and compare messages with plugin messages
  * on matches, run plugin callback()
* write callback status on fedmsg (so monitor knows when to update redis)
* when callback() responds: send file to converter

We think kubernetes may be a good idea for each plugin run. Not sure if
possible.

#### converter

* receives file from runner
* checks if is a valid firehose file
  * if not, call plugin.to_firehose()
* loads it in database

### plugins subpackage

kiskadee needs plugins to run static analyzers. Each plugin must define the
following functions and variables:

#### callback()

* Run static analysis on source code based on the message information
* returns (firehose) file

#### to_firehose()

* only needed if callback does not return firehose formated file
* converts file to firehose

#### watch()

* tells monitor how to get package version information from upstream (may be a
distro)

#### message

* fedmsg message format which a plugin understands. MUST include the payload
