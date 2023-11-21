import unittest

from lib.exceptions import DirectoryAlreadyExistsError, DirectoryNotEmptyError, FileAlreadyExistsError, NotFileError, \
    NotFoundError
from lib.filesystem import Filesystem


class FilesystemTest(unittest.TestCase):

    def setUp(self):
        super().setUp()

        self.fs = Filesystem()

    def testChangeDirectory(self):
        dirname = 'somedir'

        # ensure root PWD
        self.assertEqual(self.fs.pwd(), '/')

        # create & change dir
        self.fs.mkdir(dirname)
        self.fs.cd(dirname)

        # ensure dir PWD
        self.assertEqual(self.fs.pwd(), '/{}'.format(dirname))

        # create & change dir
        self.fs.mkdir(dirname)
        self.fs.cd(dirname)

        # ensure subdir PWD
        self.assertEqual(self.fs.pwd(), '/{}/{}'.format(dirname, dirname))

    def testChangeDirectoryDoesNotExist(self):
        dirname = 'doesnotexist'

        # ensure dir does not exist
        self.assertNotIn(dirname, self.fs.ls())

        # remove dir
        self.assertRaises(NotFoundError, self.fs.cd, dirname)

    def testPrintWorkingDir(self):
        dirname = 'somedir'

        # ensure root PWD
        self.assertEqual(self.fs.pwd(), '/')

        # create & change dir
        self.fs.mkdir(dirname)
        self.fs.cd(dirname)

        # ensure dir PWD
        self.assertEqual(self.fs.pwd(), '/{}'.format(dirname))

        # create & change dir
        self.fs.mkdir(dirname)
        self.fs.cd(dirname)

        # ensure subdir PWD
        self.assertEqual(self.fs.pwd(), '/{}/{}'.format(dirname, dirname))

    def testList(self):
        dirname = 'somedir'
        filename = 'somefile'

        # ensure initial ls is empty
        self.assertListEqual(self.fs.ls(), [])

        # create dir
        self.fs.mkdir(dirname)

        # ensure dir in ls
        self.assertIn(dirname, self.fs.ls())

        # ensure dir is the only thing in the ls
        self.assertListEqual(self.fs.ls(), [dirname])

        # create file
        self.fs.touch(filename)

        # ensure file in ls
        self.assertIn(filename, self.fs.ls())

        # ensure both are in ls
        self.assertListEqual(self.fs.ls(), [dirname, filename])

    def testMakeDir(self):
        dirname = 'somedir'

        # ensure dir does not exist
        self.assertNotIn(dirname, self.fs.ls())

        # create dir
        self.fs.mkdir(dirname)

        # ensure dir exists
        self.assertIn(dirname, self.fs.ls())

    def testMakeDirAlreadyExists(self):
        dirname = 'somedir'
        child = 'child'

        # create dir
        self.fs.mkdir(dirname)

        # ensure dir exists
        self.assertIn(dirname, self.fs.ls())

        # change to directory
        self.fs.cd(dirname)

        # create child dir
        self.fs.mkdir(child)

        # ensure child exists
        self.assertIn(child, self.fs.ls())

        # change to parent directory
        self.fs.cd('..')

        # create dir does not throw error
        self.fs.mkdir(dirname)

        # change dir
        self.fs.cd(dirname)

        # ensure child still exists
        self.assertIn(child, self.fs.ls())

    def testMakeDirFileAlreadyExists(self):
        dirname = 'foobar'
        filename = 'foobar'

        # create file
        self.fs.touch(filename)

        # create dir throws error
        self.assertRaises(FileAlreadyExistsError, self.fs.mkdir, dirname)

    def testRemoveDir(self):
        dirname = 'somedir'

        # create dir
        self.fs.mkdir(dirname)

        # ensure dir exists
        self.assertIn(dirname, self.fs.ls())

        # remove dir
        self.fs.rm(dirname)

        # ensure dir exists
        self.assertNotIn(dirname, self.fs.ls())

    def testRemoveDirNotFound(self):
        dirname = 'doesnotexist'

        # ensure dir does not exist
        self.assertNotIn(dirname, self.fs.ls())

        # remove dir
        self.assertRaises(NotFoundError, self.fs.rm, dirname)

    def testRemoveDirNotEmpty(self):
        dirname = 'notempty'
        child = 'child'

        # create parent directory
        self.fs.mkdir(dirname)

        # ensure parent dir exists
        self.assertIn(dirname, self.fs.ls())

        # change directory
        self.fs.cd(dirname)

        # ensure CWD
        self.assertEqual(self.fs.pwd(), '/{}'.format(dirname))

        # create child dir
        self.fs.mkdir(child)

        # ensure child dir exists
        self.assertIn(child, self.fs.ls())

        # change directory to root
        self.fs.cd('..')

        # ensure CWD
        self.assertEqual(self.fs.pwd(), '/')

        # remove dir
        self.assertRaises(DirectoryNotEmptyError, self.fs.rm, dirname)

    def testRemoveFile(self):
        filename = 'somefile'

        # create file
        self.fs.touch(filename)

        # ensure file exists
        self.assertIn(filename, self.fs.ls())

        # remove file
        self.fs.rm(filename)

        # ensure file exists
        self.assertNotIn(filename, self.fs.ls())

    def testRemoveFileNotFound(self):
        filename = 'doesnotexist'

        # ensure file does not exist
        self.assertNotIn(filename, self.fs.ls())

        # remove file
        self.assertRaises(NotFoundError, self.fs.rm, filename)

    def testRemoveDirNotEmptyForce(self):
        parent = 'notempty'
        child = 'child'

        # create parent directory
        self.fs.mkdir(parent)

        # ensure parent dir exists
        self.assertIn(parent, self.fs.ls())

        # change directory
        self.fs.cd(parent)

        # ensure CWD
        self.assertEqual(self.fs.pwd(), '/{}'.format(parent))

        # create child dir
        self.fs.mkdir(child)

        # ensure child dir exists
        self.assertIn(child, self.fs.ls())

        # change directory to root
        self.fs.cd('..')

        # ensure CWD
        self.assertEqual(self.fs.pwd(), '/')

        # remove parent dir (forced)
        self.fs.rm(parent, True)

        # ensure parent dir does not exist
        self.assertNotIn(parent, self.fs.ls())

    def testCreateFile(self):
        filename = 'empty.txt'

        # create file
        self.fs.touch(filename)

        # ensure file exists
        self.assertIn(filename, self.fs.ls())

    def testCreateFileAlreadyExists(self):
        filename = 'lipsum.txt'
        contents = 'Lorem ipsum dolor sit amet'

        # create file
        self.fs.touch(filename)

        # ensure file exists
        self.assertIn(filename, self.fs.ls())

        # write contents
        self.fs.write(filename, contents)

        # ensure file contents
        self.assertEqual(self.fs.read(filename), contents)

        # create file again
        self.fs.touch(filename)

        # ensure file contents
        self.assertEqual(self.fs.read(filename), contents)

    def testCreateFileDirAlreadyExists(self):
        dirname = 'foobar'
        filename = 'foobar'

        # create dir
        self.fs.mkdir(dirname)

        # ensure exception raised
        self.assertRaises(DirectoryAlreadyExistsError, self.fs.touch, filename)

    def testWriteReadFile(self):
        filename = 'lipsum.txt'
        contents = 'Lorem ipsum dolor sit amet'

        # create file
        self.fs.touch(filename)

        # ensure file exists
        self.assertIn(filename, self.fs.ls())

        # write contents
        self.fs.write(filename, contents)

        # ensure file contents
        self.assertEqual(self.fs.read(filename), contents)

    def testWriteFileNotFound(self):
        filename = 'doesnotexist'

        # ensure file does not exist
        self.assertNotIn(filename, self.fs.ls())

        # ensure exception raised
        self.assertRaises(NotFoundError, self.fs.write, filename, 'stuff')

    def testWriteFileNotFile(self):
        dirname = 'foobar'
        filename = 'foobar'

        # create dir
        self.fs.mkdir(dirname)

        # ensure exception raised
        self.assertRaises(NotFileError, self.fs.write, filename, 'stuff')

    def testReadFileNotFound(self):
        filename = 'doesnotexist'

        # ensure file does not exist
        self.assertNotIn(filename, self.fs.ls())

        # ensure exception raised
        self.assertRaises(NotFoundError, self.fs.read, filename)

    def testReadFileNotFile(self):
        dirname = 'foobar'
        filename = 'foobar'

        # create dir
        self.fs.mkdir(dirname)

        # ensure exception raised
        self.assertRaises(NotFileError, self.fs.read, filename)

    def testMoveDir(self):
        src = 'old'
        dst = 'new'

        # create dir
        self.fs.mkdir(src)

        # ensure dir exists
        self.assertListEqual(self.fs.ls(), [src])

        # move dir
        self.fs.mv(src, dst)

        # ensure ensure new name
        self.assertEqual(self.fs.ls(), [dst])

    def testMoveDirNotFound(self):
        dirname = 'doesnotexist'

        # ensure dir does not exist
        self.assertNotIn(dirname, self.fs.ls())

        # ensure exception raised
        self.assertRaises(NotFoundError, self.fs.mv, dirname, 'new')

    def testFind(self):
        dirs = ['foo', 'bar', 'baz', 'bin']

        # create some dirs
        for d in dirs:
            self.fs.mkdir(d)

        # ensure dirs exist
        self.assertListEqual(self.fs.ls(), dirs)

        # ensure dir found
        self.assertListEqual(self.fs.find('baz'), ['baz'])

    def testFindNotFound(self):
        dirs = ['foo', 'bar', 'baz', 'bin']

        # create some dirs
        for d in dirs:
            self.fs.mkdir(d)

        # ensure dirs exist
        self.assertListEqual(self.fs.ls(), dirs)

        # ensure dir not found
        self.assertListEqual(self.fs.find('zip'), [])

    def testFindFuzzy(self):
        dirs = ['foobar', 'barbaz', 'binzip']

        # create some dirs
        for d in dirs:
            self.fs.mkdir(d)

        # ensure dirs exist
        self.assertListEqual(self.fs.ls(), dirs)

        # ensure dir found
        self.assertListEqual(self.fs.find('bar', True), ['foobar', 'barbaz'])
