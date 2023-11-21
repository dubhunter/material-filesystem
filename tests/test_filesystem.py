import unittest

from lib.exceptions import (
    DirectoryAlreadyExistsError,
    DirectoryNotEmptyError,
    FileAlreadyExistsError,
    NotFileError,
    NotFoundError, RootError
)
from lib.filesystem import Filesystem


class FilesystemTest(unittest.TestCase):

    def setUp(self):
        super().setUp()

        self.fs = Filesystem()

    def testPushDirectory(self):
        dirname = 'somedir'

        # ensure root PWD
        self.assertEqual(self.fs.pwd(), '/')

        # create & change dir
        self.fs.mkdir(dirname)
        self.fs.pushdir(dirname)

        # ensure dir PWD
        self.assertEqual(self.fs.pwd(), '/{}'.format(dirname))

        # create & change dir
        self.fs.mkdir(dirname)
        self.fs.pushdir(dirname)

        # ensure subdir PWD
        self.assertEqual(self.fs.pwd(), '/{}/{}'.format(dirname, dirname))

    def testPushDirectoryDoesNotExist(self):
        dirname = 'doesnotexist'

        # ensure dir does not exist
        self.assertNotIn(dirname, self.fs.ls())

        # remove dir
        self.assertRaises(NotFoundError, self.fs.pushdir, dirname)

    def testPopDirectory(self):
        dirname = 'somedir'

        # ensure root PWD
        self.assertEqual(self.fs.pwd(), '/')

        # create & change dir twice
        self.fs.mkdir(dirname)
        self.fs.pushdir(dirname)
        self.fs.mkdir(dirname)
        self.fs.pushdir(dirname)

        # ensure subdir PWD
        self.assertEqual(self.fs.pwd(), '/{}/{}'.format(dirname, dirname))

        # change up one
        self.fs.popdir()

        # ensure dir PWD
        self.assertEqual(self.fs.pwd(), '/{}'.format(dirname))

        # change up one
        self.fs.popdir()

        # ensure root PWD
        self.assertEqual(self.fs.pwd(), '/')

        # change up one
        self.fs.popdir()

        # ensure still at root PWD
        self.assertEqual(self.fs.pwd(), '/')

    def testChangeDirectoryRelative(self):
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

        # change to current
        self.fs.cd('.')

        # ensure no change PWD
        self.assertEqual(self.fs.pwd(), '/{}/{}'.format(dirname, dirname))

        # change up one
        self.fs.cd('..')

        # ensure dir PWD
        self.assertEqual(self.fs.pwd(), '/{}'.format(dirname))

        # change up one
        self.fs.cd('..')

        # ensure root PWD
        self.assertEqual(self.fs.pwd(), '/')

    def testChangeDirRootParent(self):
        # change up one
        self.fs.cd('..')

        # ensure still at root PWD
        self.assertEqual(self.fs.pwd(), '/')

    def testChangeDirectoryDoesNotExist(self):
        dirname = 'doesnotexist'

        # ensure dir does not exist
        self.assertNotIn(dirname, self.fs.ls())

        # remove dir
        self.assertRaises(NotFoundError, self.fs.cd, dirname)

    def testChangeDirectoryAbsolute(self):
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

        # change to root
        self.fs.cd('/')

        # ensure root PWD
        self.assertEqual(self.fs.pwd(), '/')

        # change two deep
        self.fs.cd('/{}/{}'.format(dirname, dirname))

        # ensure subdir PWD
        self.assertEqual(self.fs.pwd(), '/{}/{}'.format(dirname, dirname))

    def testChangeDirectoryAbsoluteNotFound(self):
        dirname = 'somedir'

        # ensure root PWD
        self.assertEqual(self.fs.pwd(), '/')

        # create & change dirs
        self.fs.mkdir(dirname)
        self.fs.cd(dirname)
        self.fs.mkdir(dirname)
        self.fs.cd(dirname)

        # ensure subdir PWD
        self.assertEqual(self.fs.pwd(), '/{}/{}'.format(dirname, dirname))

        # change to root
        self.fs.popdir()

        # ensure dir PWD
        self.assertEqual(self.fs.pwd(), '/{}'.format(dirname))

        # change two deep (doesn't exist), ensure exception
        self.assertRaises(NotFoundError, self.fs.cd, '/{}/{}'.format(dirname, 'nope'))

        # ensure still dir PWD
        self.assertEqual(self.fs.pwd(), '/{}'.format(dirname))

    def testPrintWorkingDir(self):
        dirname = 'somedir'

        # ensure root PWD
        self.assertEqual(self.fs.pwd(), '/')

        # create & change dir
        self.fs.mkdir(dirname)
        self.fs.pushdir(dirname)

        # ensure dir PWD
        self.assertEqual(self.fs.pwd(), '/{}'.format(dirname))

        # create & change dir
        self.fs.mkdir(dirname)
        self.fs.pushdir(dirname)

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
        self.fs.pushdir(dirname)

        # create child dir
        self.fs.mkdir(child)

        # ensure child exists
        self.assertIn(child, self.fs.ls())

        # change to parent directory
        self.fs.popdir()

        # create dir does not throw error
        self.fs.mkdir(dirname)

        # change dir
        self.fs.pushdir(dirname)

        # ensure child still exists
        self.assertIn(child, self.fs.ls())

    def testMakeDirFileAlreadyExists(self):
        dirname = 'foobar'
        filename = 'foobar'

        # create file
        self.fs.touch(filename)

        # create dir throws error
        self.assertRaises(FileAlreadyExistsError, self.fs.mkdir, dirname)

    def testMakeDirAbsoluteRoot(self):
        # try to create root
        self.fs.mkdir('/')

        # ensure still at root
        self.assertEqual(self.fs.pwd(), '/')

    def testMakeDirAbsolute(self):
        firstdir = 'first'
        seconddir = 'second'

        # ensure dir does not exist
        self.assertNotIn(firstdir, self.fs.ls())

        # create first dir
        self.fs.mkdir(firstdir)

        # ensure dir exists
        self.assertIn(firstdir, self.fs.ls())

        # create second dir absolute without cd
        self.fs.mkdir('/{}/{}'.format(firstdir, seconddir))

        # change into first
        self.fs.pushdir(firstdir)

        # ensure dir exists
        self.assertIn(seconddir, self.fs.ls())

    def testMakeDirAbsoluteIntermediateError(self):
        firstdir = 'first'
        seconddir = 'second'
        thirddir = 'third'

        # create first dir
        self.fs.mkdir(firstdir)

        # ensure second dir does not exist in first
        self.fs.pushdir(firstdir)
        self.assertNotIn(seconddir, self.fs.ls())
        self.fs.popdir()

        # creation of third dir should error
        self.assertRaises(NotFoundError, self.fs.mkdir, '/{}/{}/{}'.format(firstdir, seconddir, thirddir))

        # ensure still at root
        self.assertEqual(self.fs.pwd(), '/')

    def testMakeDirAbsoluteIntermediateCreate(self):
        firstdir = 'first'
        seconddir = 'second'
        thirddir = 'third'

        # create first dir
        self.fs.mkdir(firstdir)

        # ensure second dir does not exist in first
        self.fs.pushdir(firstdir)
        self.assertNotIn(seconddir, self.fs.ls())
        self.fs.popdir()

        # create third dir absolute without cd
        self.fs.mkdir('/{}/{}/{}'.format(firstdir, seconddir, thirddir), True)

        # ensure still at root
        self.assertEqual(self.fs.pwd(), '/')

        # change into second
        self.fs.cd('/{}/{}'.format(firstdir, seconddir))

        # ensure dir exists
        self.assertIn(thirddir, self.fs.ls())

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
        self.fs.pushdir(dirname)

        # ensure cwd
        self.assertEqual(self.fs.pwd(), '/{}'.format(dirname))

        # create child dir
        self.fs.mkdir(child)

        # ensure child dir exists
        self.assertIn(child, self.fs.ls())

        # change directory to root
        self.fs.popdir()

        # ensure cwd
        self.assertEqual(self.fs.pwd(), '/')

        # remove dir
        self.assertRaises(DirectoryNotEmptyError, self.fs.rm, dirname)

    def testRemoveDirNotEmptyForce(self):
        parent = 'notempty'
        child = 'child'

        # create parent directory
        self.fs.mkdir(parent)

        # ensure parent dir exists
        self.assertIn(parent, self.fs.ls())

        # change directory
        self.fs.pushdir(parent)

        # ensure cwd
        self.assertEqual(self.fs.pwd(), '/{}'.format(parent))

        # create child dir
        self.fs.mkdir(child)

        # ensure child dir exists
        self.assertIn(child, self.fs.ls())

        # change directory to root
        self.fs.popdir()

        # ensure cwd
        self.assertEqual(self.fs.pwd(), '/')

        # remove parent dir (forced)
        self.fs.rm(parent, True)

        # ensure parent dir does not exist
        self.assertNotIn(parent, self.fs.ls())

    def testRemoveDirAbsoluteRoot(self):
        # ensure error
        self.assertRaises(RootError, self.fs.rm, '/')

    def testRemoveDirAbsolute(self):
        firstdir = 'first'
        seconddir = 'second'

        # create dirs
        self.fs.mkdir('/{}/{}'.format(firstdir, seconddir), True)

        # change into first and ensure second
        self.fs.pushdir(firstdir)
        self.assertIn(seconddir, self.fs.ls())
        self.fs.popdir()

        # remove second dir abosule
        self.fs.rm('/{}/{}'.format(firstdir, seconddir))

        # ensure back to root
        self.assertEqual(self.fs.pwd(), '/')

        # change into first and ensure cwd
        self.fs.pushdir(firstdir)
        self.assertEqual(self.fs.pwd(), '/{}'.format(firstdir))

        # ensure second dir does not exist
        self.assertNotIn(seconddir, self.fs.ls())

    def testRemoveDirAbsoluteError(self):
        dirname = 'doesnotexist'

        # ensure dir does not exist
        self.assertNotIn(dirname, self.fs.ls())

        # remove dir
        self.assertRaises(NotFoundError, self.fs.rm, '/{}'.format(dirname))

        # ensure still at root
        self.assertEqual(self.fs.pwd(), '/')

    def testRemoveDirAbsoluteNotEmptyForce(self):
        dirname = 'notempty'
        child = 'child'

        # create parent directory
        self.fs.mkdir('/{}/{}'.format(dirname, dirname), True)

        # change directory
        self.fs.cd('/{}/{}'.format(dirname, dirname))

        # ensure cwd
        self.assertEqual(self.fs.pwd(), '/{}/{}'.format(dirname, dirname))

        # create child dir
        self.fs.mkdir(child)

        # ensure child dir exists
        self.assertIn(child, self.fs.ls())

        # change directory to root
        self.fs.cd('/')

        # ensure cwd
        self.assertEqual(self.fs.pwd(), '/')

        # remove parent dir (forced)
        self.fs.rm('/{}/{}'.format(dirname, dirname), True)

        # change into first dir
        self.fs.pushdir(dirname)

        # ensure cwd
        self.assertEqual(self.fs.pwd(), '/{}'.format(dirname))

        # ensure parent dir does not exist
        self.assertNotIn(dirname, self.fs.ls())

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

    def testMoveDirCollision(self):
        src = 'old'
        dst = 'new'

        # create dirs
        self.fs.mkdir(src)
        self.fs.mkdir(dst)

        # ensure dir exists
        self.assertListEqual(self.fs.ls(), [src, dst])

        # ensure exception raised
        self.assertRaises(DirectoryAlreadyExistsError, self.fs.mv, src, dst)

    def testMoveDirCollisionOverwrite(self):
        src = 'old'
        dst = 'new'
        filename = 'sentinel'

        # create dirs
        self.fs.mkdir(src)
        self.fs.mkdir(dst)

        # ensure dirs exists
        self.assertListEqual(self.fs.ls(), [src, dst])

        # create a file in src to check for later
        self.fs.pushdir(src)
        self.fs.touch(filename)
        self.assertIn(filename, self.fs.ls())
        self.fs.popdir()

        # move dir
        self.fs.mv(src, dst, True)

        # ensure dirs exist
        self.assertListEqual(self.fs.ls(), [dst])

        # change into new name and check for sentinel file
        self.fs.pushdir(dst)
        self.assertIn(filename, self.fs.ls())

    def testMoveFile(self):
        src = 'old'
        dst = 'new'

        # create file
        self.fs.touch(src)

        # ensure file exists
        self.assertListEqual(self.fs.ls(), [src])

        # move file
        self.fs.mv(src, dst)

        # ensure ensure new name
        self.assertEqual(self.fs.ls(), [dst])

    def testMoveFileNotFound(self):
        filename = 'doesnotexist'

        # ensure file does not exist
        self.assertNotIn(filename, self.fs.ls())

        # ensure exception raised
        self.assertRaises(NotFoundError, self.fs.mv, filename, 'new')

    def testMoveFileCollision(self):
        src = 'old'
        dst = 'new'

        # create files
        self.fs.touch(src)
        self.fs.touch(dst)

        # ensure file exists
        self.assertListEqual(self.fs.ls(), [src, dst])

        # ensure exception raised
        self.assertRaises(FileAlreadyExistsError, self.fs.mv, src, dst)

    def testMoveFileCollisionOverwrite(self):
        src = 'old'
        dst = 'new'
        contents = 'sentinel'

        # create files
        self.fs.touch(src)
        self.fs.touch(dst)

        # ensure files exist
        self.assertListEqual(self.fs.ls(), [src, dst])

        # add contents to src to check for later
        self.fs.write(src, contents)
        self.assertEqual(self.fs.read(src), contents)

        # move file
        self.fs.mv(src, dst, True)

        # ensure files exists
        self.assertListEqual(self.fs.ls(), [dst])

        # read new name and check for sentinel value
        self.assertEqual(self.fs.read(dst), contents)

    def testCopyDir(self):
        src = 'old'
        dst = 'new'

        # create dir
        self.fs.mkdir(src)

        # ensure dir exists
        self.assertListEqual(self.fs.ls(), [src])

        # move dir
        self.fs.cp(src, dst)

        # ensure ensure new name
        self.assertEqual(self.fs.ls(), [src, dst])

    def testCopyDirNotFound(self):
        dirname = 'doesnotexist'

        # ensure dir does not exist
        self.assertNotIn(dirname, self.fs.ls())

        # ensure exception raised
        self.assertRaises(NotFoundError, self.fs.cp, dirname, 'new')

    def testCopyDirCollision(self):
        src = 'old'
        dst = 'new'

        # create dirs
        self.fs.mkdir(src)
        self.fs.mkdir(dst)

        # ensure dir exists
        self.assertListEqual(self.fs.ls(), [src, dst])

        # ensure exception raised
        self.assertRaises(DirectoryAlreadyExistsError, self.fs.cp, src, dst)

    def testCopyDirCollisionOverwrite(self):
        src = 'old'
        dst = 'new'
        filename = 'sentinel'

        # create dirs
        self.fs.mkdir(src)
        self.fs.mkdir(dst)

        # ensure dirs exists
        self.assertListEqual(self.fs.ls(), [src, dst])

        # create a file in src to check for later
        self.fs.pushdir(src)
        self.fs.touch(filename)
        self.assertIn(filename, self.fs.ls())
        self.fs.popdir()

        # move dir
        self.fs.cp(src, dst, True)

        # ensure dirs exist
        self.assertListEqual(self.fs.ls(), [src, dst])

        # change into old name and check for sentinel file
        self.fs.pushdir(src)
        self.assertIn(filename, self.fs.ls())
        self.fs.popdir()

        # change into new name and check for sentinel file
        self.fs.pushdir(dst)
        self.assertIn(filename, self.fs.ls())

    def testCopyFile(self):
        src = 'old'
        dst = 'new'

        # create file
        self.fs.touch(src)

        # ensure file exists
        self.assertListEqual(self.fs.ls(), [src])

        # move file
        self.fs.cp(src, dst)

        # ensure ensure new name
        self.assertEqual(self.fs.ls(), [src, dst])

    def testCopyFileNotFound(self):
        filename = 'doesnotexist'

        # ensure file does not exist
        self.assertNotIn(filename, self.fs.ls())

        # ensure exception raised
        self.assertRaises(NotFoundError, self.fs.cp, filename, 'new')

    def testCopyFileCollision(self):
        src = 'old'
        dst = 'new'

        # create files
        self.fs.touch(src)
        self.fs.touch(dst)

        # ensure file exists
        self.assertListEqual(self.fs.ls(), [src, dst])

        # ensure exception raised
        self.assertRaises(FileAlreadyExistsError, self.fs.cp, src, dst)

    def testCopyFileCollisionOverwrite(self):
        src = 'old'
        dst = 'new'
        contents = 'sentinel'

        # create files
        self.fs.touch(src)
        self.fs.touch(dst)

        # ensure files exist
        self.assertListEqual(self.fs.ls(), [src, dst])

        # add contents to src to check for later
        self.fs.write(src, contents)
        self.assertEqual(self.fs.read(src), contents)

        # move file
        self.fs.cp(src, dst, True)

        # ensure files exists
        self.assertListEqual(self.fs.ls(), [src, dst])

        # read old name and check for sentinel value
        self.assertEqual(self.fs.read(src), contents)

        # read new name and check for sentinel value
        self.assertEqual(self.fs.read(dst), contents)

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
