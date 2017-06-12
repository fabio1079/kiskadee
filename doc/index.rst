.. kiskadee documentation master file, created by
   sphinx-quickstart on Thu May 25 20:00:01 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

kiskadee documentation
======================

Performing source code static analysis during the software development cycle
may be a difficult task: there are different static analyzers available and
each of them usually performs better in a small set of problems, making it hard
to choose one tool. Combining the analysis of different tools solves this
problem but, then, other problems arise, namely the generated false positives
and the fact that some alarms are more relevant than others.  kiskadee is a
system to support static analysis usage during software development by
providing ranked static analysis reports. First, it runs multiple
security-oriented static analyzers on the source code. Then, using a
classification model, the possible bugs detected by the static analyzers are
ranked based on their importance, where critical flaws are ranked first and
potential false positives are ranked last.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   introduction
   firehose
   monitor
   runner
   analyzers
   plugins
   config_file


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
