#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

"""
This file originates from the 'jupyter-packaging' package, and
contains a set of useful utilities for including npm packages
within a Python package.
"""
from os.path import join as pjoin
import io
import os
import fnmatch
import functools
import pipes
import shlex
import subprocess
import sys


# BEFORE importing distutils, remove MANIFEST. distutils doesn't properly
# update it when the contents of directories change.
if os.path.exists('MANIFEST'): os.remove('MANIFEST')


from distutils.core import setup
from distutils.cmd import Command
from distutils.command.build_py import build_py
from distutils.command.sdist import sdist
from distutils import log

try:
    from wheel.bdist_wheel import bdist_wheel
except ImportError:
    bdist_wheel = None

if sys.platform == 'win32':
    from subprocess import list2cmdline
else:
    def list2cmdline(cmd_list):
        return ' '.join(map(pipes.quote, cmd_list))


__version__ = '0.2.0'

# ---------------------------------------------------------------------------
# Top Level Variables
# ---------------------------------------------------------------------------

here = os.path.abspath(os.path.dirname(__file__))
is_repo = os.path.exists(pjoin(here, '.git'))
node_modules = pjoin(here, 'node_modules')

npm_path = ':'.join([
    pjoin(here, 'node_modules', '.bin'),
    os.environ.get('PATH', os.defpath),
])

if "--skip-npm" in sys.argv:
    print("Skipping npm install as requested.")
    skip_npm = True
    sys.argv.remove("--skip-npm")
else:
    skip_npm = False


# For some commands, use setuptools.  Note that we do NOT list install here!
if 'develop' in sys.argv or any(a.startswith('bdist') for a in sys.argv):
    import setuptools


# ---------------------------------------------------------------------------
# Public Functions
# ---------------------------------------------------------------------------


def get_data_files(file_patterns):
    """Expand file patterns to a list of `data_files` paths.

    Parameters
    -----------
    file_patterns: list or str
        A list of glob patterns for the data file locations.
        The globs can be recursive if they include a `**`.
        They should be relative paths from the root directory or
        absolute paths.
    """
    if not isinstance(file_patterns, (list, tuple)):
        file_patterns = [file_patterns]
    files = []
    for pattern in file_patterns:
        pattern = os.path.relpath(pattern, here)
        pattern = pjoin(here, pattern)
        matches = find_files(here, pattern)
        files.extend([os.path.relpath(f, here) for f in matches])
    return files


def get_package_data(root, file_patterns=None):
    """Expand file patterns to a list of `package_data` paths.

    Parameters
    -----------
    root: str
        The relative path to the package root from `here`.
    file_patterns: list or str, optional
        A list of glob patterns for the data file locations.
        The globs can be recursive if they include a `**`.
        They should be relative paths from the root or
        absolute paths.  If not given, all files will be used.
    """
    if file_patterns is None:
        file_patterns = ['*']
    if not isinstance(file_patterns, (list, tuple)):
        file_patterns = [file_patterns]
    files = get_data_files([pjoin(root, f) for f in file_patterns])
    return [os.path.relpath(root, f) for f in files]


def get_version(file, name='__version__'):
    """Get the version of the package from the given file by
    executing it and extracting the given `name`.
    """
    path = os.path.realpath(file)
    version_ns = {}
    with io.open(path, encoding="utf8") as f:
        exec(f.read(), {}, version_ns)
    return version_ns[name]


def ensure_python(specs):
    """Given a list of range specifiers for python, ensure compatibility.
    """
    if not isinstance(specs, (list, tuple)):
        specs = [specs]
    v = sys.version_info
    part = '%s.%s' % (v.major, v.minor)
    for spec in specs:
        if part == spec:
            return
        try:
            if eval(part + spec):
                return
        except SyntaxError:
            pass
    raise ValueError('Python version %s unsupported' % part)


def find_packages(top=here):
    """
    Find all of the packages.
    """
    packages = []
    for d, dirs, _ in os.walk(top, followlinks=True):
        if os.path.exists(pjoin(d, '__init__.py')):
            packages.append(os.path.relpath(d, top).replace(os.path.sep, '.'))
        elif d != top:
            # Do not look for packages in subfolders if current is not a package
            dirs[:] = []
    return packages


def update_package_data(distribution):
    """update build_py options to get package_data changes"""
    build_py = distribution.get_command_obj('build_py')
    build_py.finalize_options()


def create_cmdclass(prerelease_cmds=None):
    """Create a command class with the given optional prerelease class.

    Parameters
    ----------
    prerelease_cmds: list, optional
        The list of command names to run before releasing.
    """
    wrapper = functools.partial(wrap_command, prerelease_cmds or [])
    cmdclass = dict(
        build_py=wrapper(build_py, strict=is_repo),
        sdist=wrapper(sdist, strict=True),
    )
    if bdist_wheel:
        cmdclass['bdist_wheel'] = wrapper(bdist_wheel, strict=True)
    return cmdclass


def command_for_func(func):
    """Create a command that calls the given function."""

    class FuncCommand(BaseCommand):

        def run(self):
            func()
            update_package_data(self.distribution)

    return FuncCommand


def run(cmd, **kwargs):
    """Echo a command before running it.  Defaults to repo as cwd"""
    log.info('> ' + list2cmdline(cmd))
    kwargs.setdefault('cwd', here)
    kwargs.setdefault('shell', os.name == 'nt')
    kwargs['stdout'] = subprocess.PIPE
    kwargs['stderr'] = subprocess.STDOUT
    if not isinstance(cmd, (list, tuple)) and os.name != 'nt':
        cmd = shlex.split(cmd)
    proc = None
    try:
        proc = subprocess.Popen(cmd, **kwargs)
        while proc.poll() is None:
            log.info(proc.stdout.readline().decode('utf-8'))
    except subprocess.CalledProcessError as e:
        print(e.output.decode('utf-8'))
        raise e
    finally:
        if proc:
            proc.wait()


def is_stale(target, source):
    """Test whether the target file/directory is stale based on the source
       file/directory.
    """
    if not os.path.exists(target):
        return True
    target_mtime = recursive_mtime(target) or 0
    return compare_recursive_mtime(source, cutoff=target_mtime)


class BaseCommand(Command):
    """Empty command because Command needs subclasses to override too much"""
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def get_inputs(self):
        return []

    def get_outputs(self):
        return []


def combine_commands(*commands):
    """Return a Command that combines several commands."""

    class CombinedCommand(Command):

        def initialize_options(self):
            self.commands = []
            for C in commands:
                self.commands.append(C(self.distribution))
            for c in self.commands:
                c.initialize_options()

        def finalize_options(self):
            for c in self.commands:
                c.finalize_options()

        def run(self):
            for c in self.commands:
                c.run()
    return CombinedCommand


def compare_recursive_mtime(path, cutoff, newest=True):
    """Compare the newest/oldest mtime for all files in a directory.

    Cutoff should be another mtime to be compared against. If an mtime that is
    newer/older than the cutoff is found it will return True.
    E.g. if newest=True, and a file in path is newer than the cutoff, it will
    return True.
    """
    if os.path.isfile(path):
        mt = mtime(path)
        if newest:
            if mt > cutoff:
                return True
        elif mt < cutoff:
            return True
    for dirname, _, filenames in os.walk(path, topdown=False):
        for filename in filenames:
            mt = mtime(pjoin(dirname, filename))
            if newest:  # Put outside of loop?
                if mt > cutoff:
                    return True
            elif mt < cutoff:
                return True
    return False


def recursive_mtime(path, newest=True):
    """Gets the newest/oldest mtime for all files in a directory."""
    if os.path.isfile(path):
        return mtime(path)
    current_extreme = None
    for dirname, _, filenames in os.walk(path, topdown=False):
        for filename in filenames:
            mt = mtime(pjoin(dirname, filename))
            if newest:  # Put outside of loop?
                if mt >= (current_extreme or mt):
                    current_extreme = mt
            elif mt <= (current_extreme or mt):
                current_extreme = mt
    return current_extreme


def mtime(path):
    """shorthand for mtime"""
    return os.stat(path).st_mtime


def install_npm(path=None, build_dir=None, source_dir=None, build_cmd='build', force=False):
    """Return a Command for managing an npm installation.

    Note: The command is skipped if the `--skip-npm` flag is used.

    Parameters
    ----------
    path: str, optional
        The base path of the node package.  Defaults to the repo root.
    build_dir: str, optional
        The target build directory.  If this and source_dir are given,
        the JavaScript will only be build if necessary.
    source_dir: str, optional
        The source code directory.
    build_cmd: str, optional
        The npm command to build assets to the build_dir.
    """

    class NPM(BaseCommand):
        description = 'install package.json dependencies using npm'

        def run(self):
            if skip_npm:
                log.info('Skipping npm-installation')
                return
            node_package = path or here
            node_modules = pjoin(node_package, 'node_modules')

            if not which("npm"):
                log.error("`npm` unavailable.  If you're running this command "
                          "using sudo, make sure `npm` is availble to sudo")
                return
            if force or is_stale(node_modules, pjoin(node_package, 'package.json')):
                log.info('Installing build dependencies with npm.  This may '
                         'take a while...')
                run(['npm', 'install'], cwd=node_package)
            if build_dir and source_dir and not force:
                should_build = is_stale(build_dir, source_dir)
            else:
                should_build = True
            if should_build:
                run(['npm', 'run', build_cmd], cwd=node_package)

    return NPM


def ensure_targets(targets):
    """Return a Command that checks that certain files exist.

    Raises a ValueError if any of the files are missing.

    Note: The check is skipped if the `--skip-npm` flag is used.
    """

    class TargetsCheck(BaseCommand):
        def run(self):
            if skip_npm:
                log.info('Skipping target checks')
                return
            missing = [t for t in targets if not os.path.exists(t)]
            if missing:
                raise ValueError(('missing files: %s' % missing))

    return TargetsCheck


# `shutils.which` function copied verbatim from the Python-3.3 source.
def which(cmd, mode=os.F_OK | os.X_OK, path=None):
    """Given a command, mode, and a PATH string, return the path which
    conforms to the given mode on the PATH, or None if there is no such
    file.
    `mode` defaults to os.F_OK | os.X_OK. `path` defaults to the result
    of os.environ.get("PATH"), or can be overridden with a custom search
    path.
    """

    # Check that a given file can be accessed with the correct mode.
    # Additionally check that `file` is not a directory, as on Windows
    # directories pass the os.access check.
    def _access_check(fn, mode):
        return (os.path.exists(fn) and os.access(fn, mode) and
                not os.path.isdir(fn))

    # Short circuit. If we're given a full path which matches the mode
    # and it exists, we're done here.
    if _access_check(cmd, mode):
        return cmd

    path = (path or os.environ.get("PATH", os.defpath)).split(os.pathsep)

    if sys.platform == "win32":
        # The current directory takes precedence on Windows.
        if os.curdir not in path:
            path.insert(0, os.curdir)

        # PATHEXT is necessary to check on Windows.
        pathext = os.environ.get("PATHEXT", "").split(os.pathsep)
        # See if the given file matches any of the expected path extensions.
        # This will allow us to short circuit when given "python.exe".
        matches = [cmd for ext in pathext if cmd.lower().endswith(ext.lower())]
        # If it does match, only test that one, otherwise we have to try
        # others.
        files = [cmd] if matches else [cmd + ext.lower() for ext in pathext]
    else:
        # On other platforms you don't have things like PATHEXT to tell you
        # what file suffixes are executable, so just pass on cmd as-is.
        files = [cmd]

    seen = set()
    for dir in path:
        dir = os.path.normcase(dir)
        if dir not in seen:
            seen.add(dir)
            for thefile in files:
                name = os.path.join(dir, thefile)
                if _access_check(name, mode):
                    return name
    return None


# ---------------------------------------------------------------------------
# Private Functions
# ---------------------------------------------------------------------------


def wrap_command(cmds, cls, strict=True):
    """Wrap a setup command

    Parameters
    ----------
    cmds: list(str)
        The names of the other commands to run prior to the command.
    strict: boolean, optional
        Wether to raise errors when a pre-command fails.
    """
    class WrappedCommand(cls):

        def run(self):
            if not getattr(self, 'uninstall', None):
                try:
                    [self.run_command(cmd) for cmd in cmds]
                except Exception:
                    if strict:
                        raise
                    else:
                        pass

            result = cls.run(self)
            # update package data
            update_package_data(self.distribution)
            return result
    return WrappedCommand


def find_files(directory, pattern='*'):
    """Find files in a directory matching a pattern, recursive.

    Adapted from https://stackoverflow.com/a/29270022.
    """
    if not os.path.exists(directory):
        raise ValueError("Directory not found {}".format(directory))

    matches = []
    for root, dirnames, filenames in os.walk(directory):
        if 'node_modules' in dirnames:
            dirnames.remove('node_modules')
        for filename in filenames:
            full_path = os.path.join(root, filename)
            if fnmatch.filter([full_path], pattern):
                matches.append(pjoin(root, filename).replace(os.sep, '/'))
    return matches
