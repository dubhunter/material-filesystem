
import unittest

from lib.file import File


class FileTests(unittest.TestCase):

    def setUp(self):
        super().setUp()

        self.f = File()

    def testType(self):
        self.assertEqual(self.f.type, 'File')

    def testContents(self):
        self.assertEqual(self.f.contents, '')
