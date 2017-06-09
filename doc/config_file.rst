Kiskadee's configuration file
=============================

Kiskadee uses a configuration file to define several constants used in
execution time. Database configuration, and some plugin metadata are defined in
the configuration file. When a new plugin is added to kiskadee, a new entry in
the configuration file is needed. When the new plugin inherits from
`kiskadee.plugins.Plugin`, its configurations are available in its `config`
attribute.

kiskadee looks for the configuration file under `/etc/kiskadee`.

This example shows a simple entry to the example plugin.

.. code-block:: python

    [example_plugin]
    target = example
    description = SAMATE Juliet test suite
    analyzers = cppcheck
    active = yes

The field `active` tells kiskadee if this plugin must be loaded when kiskadee
starts. Variables to database conection are also defined in the configuration
file. The field `analyzers` defines which analyzers will be used to run the
analysis on the packages monitored by this plugin.  Check the list of
:doc:`analyzers </analyzers>` supported by kiskadee.
