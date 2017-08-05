from unittest import TestCase
import kiskadee.queue


class TestQueue(TestCase):

    def test_enqueue_wrapper_pkg(self):

        def my_dict():
            return {
                    'name': 'bar',
                    'fetcher': kiskadee.fetchers.example.Fetcher(),
                    'version': '1.0.0'
                   }

        enque_my_dict = kiskadee.queue.package_enqueuer(my_dict)
        enque_my_dict()
        self.assertTrue(isinstance(kiskadee.queue.packages_queue.get(), dict))
