from unittest import TestCase
import kiskadee
import kiskadee.queue


class TestQueue(TestCase):

    def test_enqueue_wrapper_pkg(self):

        def my_dict():
            return {'foo': 'bar'}

        enque_my_dict = kiskadee.queue.package_enqueuer(my_dict)
        enque_my_dict()
        self.assertTrue(isinstance(kiskadee.queue.dequeue_package(), dict))

    def test_enqueue_wrapper_source(self):

        def my_dict():
            return {'source': '/tmp/tmpafc8yph8/0ad_0.0.21.orig.tar.xz'}

        enque_my_dict = kiskadee.queue.source_enqueuer(my_dict)
        enque_my_dict()
        self.assertTrue(isinstance(kiskadee.queue.dequeue_analysis(), dict))
