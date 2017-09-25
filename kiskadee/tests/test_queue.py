import unittest
import kiskadee.queue
import kiskadee.fetchers.example


class QueueTestCase(unittest.TestCase):

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


if __name__ == '__main__':
    unittest.main()
