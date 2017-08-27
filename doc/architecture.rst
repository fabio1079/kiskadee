Architecture
=====================

kiskadee architecture aims to decouple source code analysis from release
monitoring.  To accomplish that, we have separated the component responsible to
fetch package versions and source code, and the component responsible to run
the analyses. The communication between them is made through queues, as shown
in the Figure below.

For the current architecture, we use three queues. The *packages_queue* is used
by the fetchers to enqueue the packages that should be analyzed. This queue is
consumed by the monitor component, to check if the enqueued package was not
analyzed. The second queue, called *analysis_queue*, is consumed by the runner
component, in order to receive packages that must be analyzed from the monitor.
If a dequeued package does not exist in the database, the monitor component
will send it for analysis using the *analysis_queue*. When an analysis is
performed, the runner component sends the analysis report to the monitor
component, using the *results_queue*. The package (and the analysis) are saved
in the database by the monitor component.  Currently, kiskadee only generates
analysis for projects written in C/C++. This was a scope decision made by the
kiskadee authors.

.. figure:: _static/kiskadee_atualizado2.png
        :align: center

..

*Figure One: kiskadee architecture.*
