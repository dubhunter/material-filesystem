class NotFoundError(Exception):
    pass


class DirectoryNotEmptyError(Exception):
    pass


class AlreadyExistsError(Exception):
    pass


class DirectoryAlreadyExistsError(AlreadyExistsError):
    pass


class FileAlreadyExistsError(AlreadyExistsError):
    pass


class NotFileError(Exception):
    pass


class NotDirectoryError(Exception):
    pass
