class Node:
    TYPE_DIRECTORY = 'Directory'
    TYPE_FILE = 'File'

    @property
    def type(self):
        return self.__class__.__name__
