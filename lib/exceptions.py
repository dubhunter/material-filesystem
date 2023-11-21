class FilesystemError(Exception):
    pass


class NotFoundError(FilesystemError):
    pass


class DirectoryNotEmptyError(FilesystemError):
    pass


class AlreadyExistsError(FilesystemError):
    pass


class DirectoryAlreadyExistsError(AlreadyExistsError):
    pass


class FileAlreadyExistsError(AlreadyExistsError):
    pass


class NotFileError(FilesystemError):
    pass


class NotDirectoryError(FilesystemError):
    pass


class RootError(FilesystemError):
    pass
