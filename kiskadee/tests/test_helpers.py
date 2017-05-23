from unittest import TestCase
import unittest
import kiskadee
import kiskadee.helpers
import importlib
import sys
import os
import xml.etree.ElementTree as ET
import shutil
import kiskadee.queue

class TestHelpers(TestCase):

    def test_enqueue_wrapper_pkg(self):

        def my_dict():
            return {'foo': 'bar'}

        enque_my_dict = kiskadee.helpers.enqueue_pkg(my_dict)
        enque_my_dict()
        self.assertTrue(isinstance(kiskadee.queue.dequeue_package(), dict))

    def test_enqueue_wrapper_source(self):

        def my_dict():
            return {'source': '/tmp/tmpafc8yph8/0ad_0.0.21.orig.tar.xz'}

        enque_my_dict = kiskadee.helpers.enqueue_source(my_dict)
        enque_my_dict()
        self.assertTrue(isinstance(kiskadee.queue.dequeue_analysis(), dict))
