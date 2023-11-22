import cmd2

from lib.filesystem import Filesystem


class FilesystemApp(cmd2.Cmd):
    """Will Mason's In-Memory Filesystem"""

    def __init__(self) -> None:
        super().__init__()

        # remove a bunch of default commands
        delattr(cmd2.Cmd, 'do_alias')
        delattr(cmd2.Cmd, 'do_edit')
        delattr(cmd2.Cmd, 'do_macro')
        delattr(cmd2.Cmd, 'do_run_pyscript')
        delattr(cmd2.Cmd, 'do_run_script')
        delattr(cmd2.Cmd, 'do_set')
        delattr(cmd2.Cmd, 'do_shell')
        delattr(cmd2.Cmd, 'do_shortcuts')

        self.fs = Filesystem()
        self._update_prompt()

    def _update_prompt(self):
        # set the prompt to the cwd
        self.prompt = cmd2.style('{} $ '.format(self.fs.pwd()), bold=True, dim=True)

    cd_parser = cmd2.Cmd2ArgumentParser()
    cd_parser.add_argument('path', help='path to change to')

    @cmd2.with_argparser(cd_parser)
    def do_cd(self, args):
        """Change directory"""
        self.fs.cd(args.path)
        self._update_prompt()

    def do_pwd(self, _):
        """Print working directory"""
        self.poutput(self.fs.pwd())

    ls_parser = cmd2.Cmd2ArgumentParser()
    ls_parser.add_argument('-l', action='store_true', dest='long',
                           help='show long list with type')
    ls_parser.add_argument('path', nargs='?', help='path to list')

    @cmd2.with_argparser(ls_parser)
    def do_ls(self, args):
        """List current working directory"""
        for item in self.fs.ls(args.path, args.long):
            if args.long:
                # long results give us a tuple, but we only need the first letter of the type
                self.poutput('{} {}'.format(item[0][:1], item[1]))
            else:
                self.poutput(item)

    mkdir_parser = cmd2.Cmd2ArgumentParser()
    mkdir_parser.add_argument('-p', action='store_true', dest='create_intermediate',
                              help='create intermediate directories as required')
    mkdir_parser.add_argument('path', help='path to create')

    @cmd2.with_argparser(mkdir_parser)
    def do_mkdir(self, args):
        """Make a directory"""
        self.fs.mkdir(args.path, args.create_intermediate)

    rm_parser = cmd2.Cmd2ArgumentParser()
    rm_parser.add_argument('-f', action='store_true', dest='force', help='force removal of non-empty items')
    rm_parser.add_argument('path', help='path to remove')

    @cmd2.with_argparser(rm_parser)
    def do_rm(self, args):
        """Remove a file or directory"""
        self.fs.rm(args.path, args.force)

    touch_parser = cmd2.Cmd2ArgumentParser()
    touch_parser.add_argument('path', help='path to file to create')

    @cmd2.with_argparser(touch_parser)
    def do_touch(self, args):
        """Create a file"""
        self.fs.touch(args.path)

    write_parser = cmd2.Cmd2ArgumentParser()
    write_parser.add_argument('path', help='path to file to write to')
    write_parser.add_argument('contents', help='contents to write')

    @cmd2.with_argparser(write_parser)
    def do_write(self, args):
        """Write to a file"""
        self.fs.write(args.path, args.contents)

    read_parser = cmd2.Cmd2ArgumentParser()
    read_parser.add_argument('path', help='path to file to read')

    @cmd2.with_argparser(read_parser)
    def do_read(self, args):
        """Read a file"""
        self.poutput(self.fs.read(args.path))

    mv_parser = cmd2.Cmd2ArgumentParser()
    mv_parser.add_argument('-f', action='store_true', dest='force', help='force overwrite')
    mv_parser.add_argument('src', help='path to source')
    mv_parser.add_argument('dst', help='path to destination')

    @cmd2.with_argparser(mv_parser)
    def do_mv(self, args):
        """Move a file or directory"""
        self.fs.mv(args.src, args.dst, args.force)

    cp_parser = cmd2.Cmd2ArgumentParser()
    cp_parser.add_argument('-f', action='store_true', dest='force', help='force overwrite')
    cp_parser.add_argument('src', help='path to source')
    cp_parser.add_argument('dst', help='path to destination')

    @cmd2.with_argparser(cp_parser)
    def do_cp(self, args):
        """Copy a file or directory"""
        self.fs.cp(args.src, args.dst, args.force)

    find_parser = cmd2.Cmd2ArgumentParser()
    find_parser.add_argument('-x', action='store_true', dest='fuzzy', help='fuzzy search')
    find_parser.add_argument('path', help='path to remove')

    @cmd2.with_argparser(find_parser)
    def do_find(self, args):
        """Find a file or directory"""
        for item in self.fs.find(args.path, args.fuzzy):
            self.poutput(item)


if __name__ == '__main__':
    app = FilesystemApp()
    app.cmdloop()
