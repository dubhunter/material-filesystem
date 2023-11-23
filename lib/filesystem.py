import copy
import os
from contextlib import contextmanager
from typing import Any, List

from lib.directory import Directory
from lib.exceptions import (
    DirectoryAlreadyExistsError,
    DirectoryNotEmptyError,
    FileAlreadyExistsError,
    FilesystemError,
    NotDirectoryError,
    NotFileError,
    NotFoundError,
    RootError
)
from lib.file import File
from lib.node import Node


class Filesystem:
    def __init__(self):
        self._root = Directory()
        self._stack = []

    @property
    # get the current working directory by walking the stack
    def _cwd(self) -> Directory:
        d = self._root
        # this is the one part about the stack I don't love...the iteration here
        for name in self._stack:
            d = d.children[name]
        return d

    @contextmanager
    def _resetting_stack(self):
        # save the current stack to reset cwd
        old_stack = self._stack.copy()
        try:
            yield
        finally:
            # make sure we put the old stack back
            self._stack = old_stack

    def _absolute_child_action(self, path: str, action: callable, *args) -> Any:
        if path == '/':
            # you cannot action on root
            raise RootError
        # ensure there is no trailing slash
        path = path.rstrip('/')
        with self._resetting_stack():
            # try to change to parent then act (or error)
            parent, child = path.rsplit('/', 1)
            self.cd(parent if parent else '/')
            return action(child, *args)

    def pushdir(self, directory: str):
        if directory not in self._cwd.children:
            raise NotFoundError(directory)
        if self._cwd.children[directory].type != Node.TYPE_DIRECTORY:
            raise NotDirectoryError(directory)
        self._stack.append(directory)

    def popdir(self):
        if len(self._stack):
            self._stack.pop()

    def cd(self, path: str):
        if path == '.':
            # change to current dir is a noop
            return
        if path == '..':
            # shortcut for popdir
            self.popdir()
        elif '/' not in path:
            self.pushdir(path)
        else:
            # the absolute case
            # save the current stack in case we hit an exception
            old_stack = self._stack
            self._stack = []
            try:
                # push all the parts of the path with a filter for no empty strings
                for d in filter(None, path.split('/')):
                    self.pushdir(d)
            except FilesystemError as e:
                # if we hit an exception we want to put the old stack back
                self._stack = old_stack
                raise e

    def pwd(self) -> str:
        return '/{}'.format('/'.join(self._stack))

    def ls(self, path: str = None, long: bool = False) -> List:
        if path and '/' in path:
            # the absolute case
            with self._resetting_stack():
                self.cd(path)
                return self.ls(long=long)
        else:
            if long:
                # return a tuple with the type
                return [(v.type, k) for k, v in self._cwd.children.items()]
            else:
                # just return the keys
                return list(self._cwd.children.keys())

    def mkdir(self, path: str, create_intermediate: bool = False):
        if '/' in path:
            # the absolute case
            if path == '/':
                # creating root is a noop
                return
            with self._resetting_stack():
                if create_intermediate:  # TODO: because of this case, we cannot use self._absolute_child_action()
                    # start at root
                    self.cd('/')
                    # recurse for all the parts of the path with a filter for no empty strings
                    for d in filter(None, path.split('/')):
                        self.mkdir(d)
                        self.pushdir(d)
                else:
                    # if we aren't creating intermediates, try to change to parent then create (or error)
                    parent, child = path.rsplit('/', 1)
                    self.cd(parent if parent else '/')
                    self.mkdir(child)
        else:
            if path in self._cwd.children:
                node = self._cwd.children[path]
                if node.type == Node.TYPE_FILE:
                    # error if a file exists with the same name
                    raise FileAlreadyExistsError(path)
                else:
                    # if it's a dir, then  noop
                    return
            self._cwd.children[path] = Directory()

    def rm(self, path: str, force: bool = False):
        if '/' in path:
            self._absolute_child_action(path, self.rm, force)
        else:
            try:
                node = self._cwd.children[path]
                # don't allow removing non-empty dirs unless forced (rm -f)
                if not force and node.type == Node.TYPE_DIRECTORY and len(node.children) > 0:
                    raise DirectoryNotEmptyError(path)
                del self._cwd.children[path]
            except KeyError:
                raise NotFoundError(path)

    def touch(self, path: str):
        if '/' in path:
            self._absolute_child_action(path, self.touch)
        else:
            if path in self._cwd.children:
                node = self._cwd.children[path]
                if node.type == Node.TYPE_DIRECTORY:
                    # error if a dir exists with the same name
                    raise DirectoryAlreadyExistsError(path)
                else:
                    # if it's a file, then  noop
                    return
            self._cwd.children[path] = File()

    def write(self, path: str, contents: str | Any):
        if '/' in path:
            self._absolute_child_action(path, self.write, contents)
        else:
            try:
                node = self._cwd.children[path]
                if node.type != Node.TYPE_FILE:
                    # error if the name exists, but is not a file
                    raise NotFileError(path)
                node.contents = contents
            except KeyError:
                raise NotFoundError(path)

    def read(self, path: str) -> str | Any:
        if '/' in path:
            return self._absolute_child_action(path, self.read)
        else:
            try:
                node = self._cwd.children[path]
                if node.type != Node.TYPE_FILE:
                    # error if the name exists, but is not a file
                    raise NotFileError(path)
                return node.contents
            except KeyError:
                raise NotFoundError(path)

    def mv(self, src: str, dst: str, force: bool = False):  # TODO: Support absolute paths
        if not force and dst in self._cwd.children:
    def mv(self, src: str, dst: str, force_overwrite: bool = False):  # TODO: Support absolute paths
        if not force_overwrite and dst in self._cwd.children:
            # don't allow overwriting unless forced
            node = self._cwd.children[dst]
            if node.type == Node.TYPE_FILE:
                raise FileAlreadyExistsError(dst)
            elif node.type == Node.TYPE_DIRECTORY:
                raise DirectoryAlreadyExistsError(dst)
        try:
            self._cwd.children[dst] = self._cwd.children.pop(src)
        except KeyError:
            raise NotFoundError(src)

    def cp(self, src: str, dst: str, force_overwrite: bool = False):  # TODO: Support absolute paths
        if not force_overwrite and dst in self._cwd.children:
            # don't allow overwriting unless forced
            node = self._cwd.children[dst]
            if node.type == Node.TYPE_FILE:
                raise FileAlreadyExistsError(dst)
            elif node.type == Node.TYPE_DIRECTORY:
                raise DirectoryAlreadyExistsError(dst)
        try:
            self._cwd.children[dst] = copy.deepcopy(self._cwd.children[src])
        except KeyError:
            raise NotFoundError(src)

    def find(self, name: str, fuzzy: bool = False, recursive: bool = False) -> List[str]:
        results = []
        for k, v in self._cwd.children.items():
            if (fuzzy and name in k) or name == k:
                results.append('{}/{}'.format(self.pwd().rstrip('/'), k))
            if recursive and v.type == Node.TYPE_DIRECTORY:
                with self._resetting_stack():
                    self.pushdir(k)
                    results.extend(self.find(name, fuzzy, recursive))
        # sort alphabetically with deeper paths later
        return sorted(sorted(results), key=lambda p: (p.count(os.path.sep), p))
