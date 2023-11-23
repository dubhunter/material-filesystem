
import unittest

from lib.file import File
from lib.node import Node


class FileTests(unittest.TestCase):

    def setUp(self):
        super().setUp()

        self.f = File()

    def testType(self):
        self.assertEqual(self.f.type, Node.TYPE_FILE)

    def testContents(self):
        self.assertEqual(self.f.contents, '')
