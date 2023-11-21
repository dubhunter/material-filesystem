class NotFoundError(Exception):
    pass


class DirectoryNotEmptyError(Exception):
    pass


class DirectoryAlreadyExistsError(Exception):
    pass


class FileAlreadyExistsError(Exception):
    pass


class NotFileError(Exception):
    pass


class NotDirectoryError(Exception):
    pass
