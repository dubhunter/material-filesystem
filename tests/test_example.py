import unittest

from lib.filesystem import Filesystem


class ExampleTest(unittest.TestCase):

    def setUp(self):
        super().setUp()

        self.fs = Filesystem()

    def testBase(self):
        # make "school" directory
        self.fs.mkdir('school')
        # change directory to "school"
        self.fs.cd('school')

        # get working directory => "/school"
        self.assertEqual(self.fs.pwd(), '/school')

        # make "homework" directory
        self.fs.mkdir('homework')
        # change directory to "homework"
        self.fs.cd('homework')

        # make "math" directory
        self.fs.mkdir('math')
        # make "lunch" directory
        self.fs.mkdir('lunch')
        # make "history" directory
        self.fs.mkdir('history')
        # make "spanish" directory
        self.fs.mkdir('spanish')

        # delete "lunch" directory
        self.fs.rm('lunch')

        # get working directory contents => ["math", "history", "spanish"]
        self.assertListEqual(self.fs.ls(), ['math', 'history', 'spanish'])

        # get working directory => "/school/homework"
        self.assertEqual(self.fs.pwd(), '/school/homework')

        # change directory to parent
        self.fs.cd('..')

        # make "cheatsheet" directory
        self.fs.mkdir('cheatsheet')

        # get working directory contents => ["homework", "cheatsheet"]
        self.assertListEqual(self.fs.ls(), ['homework', 'cheatsheet'])

        # delete "cheatsheet" directory
        self.fs.rm('cheatsheet')

        # change directory to parent
        self.fs.cd('..')

        # get working directory => "/"
        self.assertEqual(self.fs.pwd(), '/')
