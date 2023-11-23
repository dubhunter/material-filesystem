
import unittest

from lib.directory import Directory
from lib.node import Node


class DirectoryTests(unittest.TestCase):

    def setUp(self):
        super().setUp()

        self.d = Directory()

    def testType(self):
        self.assertEqual(self.d.type, Node.TYPE_DIRECTORY)

    def testChildren(self):
        self.assertDictEqual(self.d.children, {})
