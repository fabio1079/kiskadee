List of supported analyzers
===========================

For now, kiskadee supports cppcheck (http://cppcheck.sourceforge.net/),
flawfinder (https://www.dwheeler.com/flawfinder/), Frama-C, and the clang
static analyzer (scan-build). While there's full support for cppcheck and
flawfinder, Frama-C and scan-build support is still in early stages, since
these tools run more sophisticated analysis and require some tunning for each
software analyzed, which makes it harder to come up with a general approach.

Each analyzer in kiskadee runs under docker, so you will have to
properly configure a docker engine in your environment in order to run
the analysis. The output of each analyzer is parsed using the 
Firehose (https://github.com/fedora-static-analysis/firehose) project, 
generating a common XML output. If you intend to add a new analyzer to
kiskadee, keep in mind that this analyzer must be supported by the firehose
project. To enable a new analyzer for some fetcher, just add the analyzer name
in the `/etc/kiskadee.conf` (the analyzer must be installed on the environment).


.. automodule:: kiskadee.analyzers
    :members:
