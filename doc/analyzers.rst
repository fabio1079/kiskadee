List of supported analyzers
===========================

For now, kiskadee only suport Cppcheck (http://cppcheck.sourceforge.net/),
but for the next release others analyzers will be supported.

Each analyzer in kiskadee is running using docker, so you will have to
configure a docker engine properly in your environment in order to run
the analysis. The output of each analyzer is parsed using the 
Firehose (https://github.com/fedora-static-analysis/firehose) project, 
generating a common XML output. If you intend to add a new analyzer to
kiskadee, keep in mind that this analyzer must be supported by the firehose
project. To enable a new analyzer for some plugin, just add the analyzer name
in the `util/kiskadee.conf` (the analyzer must be installed on the environment).


.. automodule:: kiskadee.analyzers
    :members:
