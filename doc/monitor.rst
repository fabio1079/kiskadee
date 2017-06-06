Monitor - Module to manage kiskadee analysis
============================================

This class is responsible to dequeue packages from `packages_queue` and
checks if this package needs to be analyzed.

The class defines the following public behaviors:


.. py:class:: Monitor

    .. py:method:: monitor()

        Continuously dequeue packages from `packages_queue` and check if
        this package needs to be analyzed. When a package needs to be analyzed,
        this package is enqueued in the `analyses_queue` queue, in order to
        the runner component trigger a static analysis. All the plugins
        must queue it's packages in the `packages_queue`.

    .. warning::

        If a plugin not enqueue the packages in the packages_queue, the
        analysis will never be done. You can use de decorator
        `@kiskadee.queue.package_enqueuer` to easliy queue a package.

