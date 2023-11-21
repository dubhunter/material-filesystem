from typing import Any, List

from lib.directory import Directory
from lib.exceptions import DirectoryAlreadyExistsError, DirectoryNotEmptyError, FileAlreadyExistsError, NotFileError, \
    NotFoundError
from lib.file import File


class Filesystem:
    def __init__(self):
        self._root = Directory()
        self._stack = []

    @property
    def _cwd(self) -> Directory:
        d = self._root
        for name in self._stack:
            d = d.children[name]
        return d

    def cd(self, path: str):
        if path == '.':
            return
        if path == '..':
            self._stack.pop()
        else:
            if path not in self._cwd.children:
                raise NotFoundError
            self._stack.append(path)

    def pwd(self) -> str:
        return '/{}'.format('/'.join(self._stack))

    def ls(self) -> List:
        return list(self._cwd.children.keys())

    def mkdir(self, path: str, create_intermediate: bool = False):
        if path in self._cwd.children:
            node = self._cwd.children[path]
            if node.type == 'File':
                raise FileAlreadyExistsError
            else:
                return
        self._cwd.children[path] = Directory()

    def rm(self, path: str, force: bool = False):
        try:
            node = self._cwd.children[path]
            if not force and node.type == 'Directory' and len(node.children) > 0:
                raise DirectoryNotEmptyError
            del self._cwd.children[path]
        except KeyError:
            raise NotFoundError

    def touch(self, path: str):
        if path in self._cwd.children:
            node = self._cwd.children[path]
            if node.type == 'Directory':
                raise DirectoryAlreadyExistsError
            else:
                return
        self._cwd.children[path] = File()

    def write(self, path: str, contents: str | Any):
        try:
            node = self._cwd.children[path]
            if node.type != 'File':
                raise NotFileError
            node.contents = contents
        except KeyError:
            raise NotFoundError

    def read(self, path: str) -> str | Any:
        try:
            node = self._cwd.children[path]
            if node.type != 'File':
                raise NotFileError
            return node.contents
        except KeyError:
            raise NotFoundError

    def mv(self, src: str, dst: str):
        try:
            self._cwd.children[dst] = self._cwd.children.pop(src)
        except KeyError:
            raise NotFoundError

    def find(self, name: str, fuzzy: bool = False) -> List:
        results = []
        if fuzzy:
            for k in self.ls():
                if name in k:
                    results.append(k)
        else:
            if name in self.ls():
                results.append(name)
        return results
