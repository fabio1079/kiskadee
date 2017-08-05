Kiskadee's configuration file
=============================

Kiskadee uses a configuration file to define several constants used in
execution time. Database configuration, and some fetcher metadata are defined in
the configuration file. When a new fetcher is added to kiskadee, a new entry in
the configuration file is needed. When the new fetcher inherits from
`kiskadee.fetchers.Fetcher`, its configurations are available in its `config`
attribute.

kiskadee looks for the configuration file under `/etc/kiskadee`.

This example shows a simple entry to the example fetcher.

.. code-block:: python

    [example_fetcher]
    target = example
    description = SAMATE Juliet test suite
    analyzers = cppcheck flawfinder
    active = yes

The field `active` tells kiskadee if this fetcher must be loaded when kiskadee
starts. Variables to database conection are also defined in the configuration
file. The field `analyzers` defines which analyzers will be used to run the
analysis on the packages monitored by this fetcher.  Check the list of
:doc:`analyzers </analyzers>` supported by kiskadee.
