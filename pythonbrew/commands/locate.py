
import os
import sys

from pythonbrew.basecommand import Command
from pythonbrew.define import PATH_PYTHONS, PATH_VENVS
from pythonbrew.util import Package, is_installed, get_using_python_pkgname
from pythonbrew.log import logger


class LocateCommand(Command):
    name = "locate"
    usage = "%prog [OPTIONS] [SCRIPT]"
    summary = "Locate the given version of python/specified binary"

    def __init__(self):
        super(LocateCommand, self).__init__()
        self.parser.add_option(
            "-p", "--python",
            dest="python",
            default=None,
            help="Use the specified python version.",
            metavar='VERSION'
        )
        self.parser.add_option(
            "-v", "--venv",
            dest="venv",
            default=None,
            help="Use the virtual environment python."
        )

    def run_command(self, options, args):
        if args:
            bin_ = args[0]
        else:
            bin_ = 'python'

        # target python interpreter
        if options.python:
            pkgname = Package(options.python).name
            if not is_installed(pkgname):
                logger.error('%s is not installed.' % pkgname)
                sys.exit(1)
        else:
            pkgname = get_using_python_pkgname()

        if options.venv:
            venv_pkgdir = os.path.join(PATH_VENVS, pkgname)
            venv_dir = os.path.join(venv_pkgdir, options.venv)
            if not os.path.isdir(venv_dir):
                logger.error("`%s` environment was not found in %s." % (options.venv, venv_pkgdir))
                sys.exit(1)

            bindir = os.path.join(venv_dir, 'bin')

        else:
            bindir = os.path.join(PATH_PYTHONS, pkgname, 'bin')

        if not os.path.isdir(bindir):
            logger.error("`%s` is not installed." % pkgname)
            sys.exit(1)

        path = os.path.join(bindir, bin_)

        logger.log(path)

LocateCommand()

