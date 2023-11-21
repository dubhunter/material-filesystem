from typing import Any, List

from lib.directory import Directory
from lib.exceptions import (
    AlreadyExistsError,
    DirectoryAlreadyExistsError,
    DirectoryNotEmptyError,
    FileAlreadyExistsError,
    FilesystemError, NotFileError,
    NotFoundError, RootError
)
from lib.file import File


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

    def pushdir(self, directory: str):
        if directory not in self._cwd.children:
            raise NotFoundError
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

    def ls(self) -> List:
        return list(self._cwd.children.keys())

    def mkdir(self, path: str, create_intermediate: bool = False):
        if '/' in path:
            # the absolute case
            if path == '/':
                # creating root is a noop
                return
            # ensure there is no trailing slash
            path = path.rstrip('/')
            # save the current stack to reset cwd
            old_stack = self._stack
            try:
                if create_intermediate:
                    # start at root
                    self.cd('/')
                    # recurse for all the parts of the path with a filter for no empty strings
                    for d in filter(None, path.split('/')):
                        self.mkdir(d)
                        self.pushdir(d)
                else:
                    # if we aren't creating intermediates, try to change to parent then create (or error)
                    parent, child = path.rsplit('/', 1)
                    self.cd(parent)
                    self.mkdir(child)
            finally:
                # make sure we put the old stack back
                self._stack = old_stack
        else:
            if path in self._cwd.children:
                node = self._cwd.children[path]
                if node.type == 'File':
                    # error if a file exists with the same name
                    raise FileAlreadyExistsError
                else:
                    # if it's a dir, then  noop
                    return
            self._cwd.children[path] = Directory()

    def rm(self, path: str, force: bool = False):
        try:
            node = self._cwd.children[path]
            # don't allow removing non-empty dirs unless forced (rm -f)
            if not force and node.type == 'Directory' and len(node.children) > 0:
                raise DirectoryNotEmptyError
            del self._cwd.children[path]
        except KeyError:
            raise NotFoundError

    def touch(self, path: str):
        if path in self._cwd.children:
            node = self._cwd.children[path]
            if node.type == 'Directory':
                # error if a dir exists with the same name
                raise DirectoryAlreadyExistsError
            else:
                # if it's a file, then  noop
                return
        self._cwd.children[path] = File()

    def write(self, path: str, contents: str | Any):
        try:
            node = self._cwd.children[path]
            if node.type != 'File':
                # error if the name exists, but is not a file
                raise NotFileError
            node.contents = contents
        except KeyError:
            raise NotFoundError

    def read(self, path: str) -> str | Any:
        try:
            node = self._cwd.children[path]
            if node.type != 'File':
                # error if the name exists, but is not a file
                raise NotFileError
            return node.contents
        except KeyError:
            raise NotFoundError

    def mv(self, src: str, dst: str, force: bool = False):
        if not force and dst in self._cwd.children:
            # don't allow overwriting unless forced
            node = self._cwd.children[dst]
            if node.type == 'File':
                raise FileAlreadyExistsError
            elif node.type == 'Directory':
                raise DirectoryAlreadyExistsError
        try:
            self._cwd.children[dst] = self._cwd.children.pop(src)
        except KeyError:
            raise NotFoundError

    def cp(self, src: str, dst: str, force: bool = False):
        if not force and dst in self._cwd.children:
            # don't allow overwriting unless forced
            node = self._cwd.children[dst]
            if node.type == 'File':
                raise FileAlreadyExistsError
            elif node.type == 'Directory':
                raise DirectoryAlreadyExistsError
        try:
            self._cwd.children[dst] = self._cwd.children[src]
        except KeyError:
            raise NotFoundError

    def find(self, name: str, fuzzy: bool = False) -> List[str]:
        results = []
        if fuzzy:
            for k in self.ls():
                if name in k:
                    results.append(k)
        else:
            # if not fuzzy, hopefully this is more performant than iteration
            if name in self.ls():
                results.append(name)
        return results
