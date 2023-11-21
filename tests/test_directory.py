
import unittest

from lib.directory import Directory


class DirectoryTests(unittest.TestCase):

    def setUp(self):
        super().setUp()

        self.d = Directory()

    def testType(self):
        self.assertEqual(self.d.type, 'Directory')

    def testChildren(self):
        self.assertDictEqual(self.d.children, {})
