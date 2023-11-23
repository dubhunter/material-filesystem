# material-filesystem
In memory filesystem coding challenge.

## Features/Extensions
* Basic requirements
* Absolute/deep path operations
* Move/copy files & directories
* Find supports recursive search
* CLI App

## Wishes
I took a stab at soft/hard links, and while hard links seem easy, my design makes soft links much harder.
This is largely due to the nodes not having any visibility into the rest of the filesystem.
I have started a branch for links for discussion. 

## Library
```python
from lib.filesystem import Filesystem

fs = Filesystem()
```

### Methods
| Name    | Description                |
|---------|----------------------------|
| cd      | Change directory           |
| pushdir | Change to child directory  |
| popdir  | Change to parent directory |
| pwd     | Print working directory    |
| ls      | List directory contents    |
| mkdir   | Create a directory         |
| rm      | Remove a directory/file    |
| touch   | Create a file              |
| write   | Write to a file            |
| read    | Read from a file           |
| mv      | Move a directory/file      |
| cp      | Copy a directory/file      |
| find    | Find a directory/file      |

## CLI App
Included is a command line app to interact with the filesystem.

### Running
Run the app with:
```shell
> make run
```

### Help
List available commands with: 
```shell
/ $ help -v

Documented commands (use 'help -v' for verbose/'help <topic>' for details):
======================================================================================================
cd                    Change directory
cp                    Copy a file or directory
find                  Find a file or directory
help                  List available commands or provide detailed help for a specific command
history               View, run, edit, save, or clear previously entered commands
ls                    List current working directory
mkdir                 Make a directory
mv                    Move a file or directory
pwd                   Print working directory
quit                  Exit this application
read                  Read a file
rm                    Remove a file or directory
touch                 Create a file
write                 Write to a file
```

## Tests
The test suite can be run with:
```shell
> make test
venv/bin/python3 -m unittest discover -s tests
..............................................................................
----------------------------------------------------------------------
Ran 78 tests in 0.002s

OK
```

## Coverage
The tests can also be run with a coverage report:
```shell
> make coverage
venv/bin/coverage run -m unittest discover -s tests
..............................................................................
----------------------------------------------------------------------
Ran 78 tests in 0.005s

OK
venv/bin/coverage report
Name                       Stmts   Miss  Cover
----------------------------------------------
lib/__init__.py                0      0   100%
lib/directory.py               4      0   100%
lib/exceptions.py             25      0   100%
lib/file.py                    4      0   100%
lib/filesystem.py            168      0   100%
lib/node.py                    6      0   100%
tests/test_directory.py       11      0   100%
tests/test_example.py         25      0   100%
tests/test_file.py            11      0   100%
tests/test_filesystem.py     577      0   100%
----------------------------------------------
TOTAL                        831      0   100%
```


