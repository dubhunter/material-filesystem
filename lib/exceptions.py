class FilesystemError(Exception):
    pass


class NotFoundError(FilesystemError):
    def __init__(self, name):
        super().__init__('"{}" does not exist'.format(name))


class DirectoryNotEmptyError(FilesystemError):
    def __init__(self, name):
        super().__init__('the directory "{}" is not empty'.format(name))


class AlreadyExistsError(FilesystemError):
    def __init__(self, name):
        super().__init__('"{}" already exists'.format(name))


class DirectoryAlreadyExistsError(AlreadyExistsError):
    def __init__(self, name):
        super().__init__('the directory "{}" already exists'.format(name))


class FileAlreadyExistsError(AlreadyExistsError):
    def __init__(self, name):
        super().__init__('the file "{}" already exists'.format(name))


class NotFileError(FilesystemError):
    def __init__(self, name):
        super().__init__('"{}" exists but is not a file'.format(name))


class NotDirectoryError(FilesystemError):
    def __init__(self, name):
        super().__init__('"{}" exists but is not a directory'.format(name))


class RootError(FilesystemError):
    def __init__(self):
        super().__init__('this action cannot be performed on root')
