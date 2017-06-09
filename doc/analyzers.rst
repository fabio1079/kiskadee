List of supported analyzers
===========================

For now, kiskadee only runs cppcheck (http://cppcheck.sourceforge.net/), but it
is ready to run Frama-C and flawfinder, which will be available in the next
release.

Each analyzer in kiskadee runs under docker, so you will have to
properly configure a docker engine in your environment in order to run
the analysis. The output of each analyzer is parsed using the 
Firehose (https://github.com/fedora-static-analysis/firehose) project, 
generating a common XML output. If you intend to add a new analyzer to
kiskadee, keep in mind that this analyzer must be supported by the firehose
project. To enable a new analyzer for some plugin, just add the analyzer name
in the `/etc/kiskadee.conf` (the analyzer must be installed on the environment).


.. automodule:: kiskadee.analyzers
    :members:
