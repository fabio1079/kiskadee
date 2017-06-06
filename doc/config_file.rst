Kiskadee's configuration file
=============================

Kiskadee uses a configuration file to define several constants used in
execution time. Database configuration, and some plugin's metadata are
defined in `util/kiskadee.conf`. When a new plugin is added in kiskadee,
a new entry in the configuration file needs to be made. When the new plugin
heritage from `kiskadee.plugins.Plugin`, this configurations is available
with the `config` attribute.

This example shows a simple entry to the example plugin.

.. code-block:: python

    [example_plugin]
    target = example
    description = SAMATE Juliet test suite
    analyzers = cppcheck
    active = yes

Note the field `active`, that tells to kiskadee if this plugin must be
loaded when kiskadee initiates. Variables to database conection also are defined
in `util/kiskadee.conf`. The field `analyzers` define which analyzers 
will be used to run the analysis on the packages monitored by this plugin. 
Check the list of :doc:`analyzers </analyzers>` supported by kiskadee.


