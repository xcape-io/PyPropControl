#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Singleton.py

https://github.com/pycontribs/tendo/blob/master/tendo/singleton.py
"""

import sys
import os
import tempfile


class SingletonException(BaseException):
    pass


class Singleton:
    """
	If you want to prevent your script from running in parallel just instantiate Singleton() class. If is there another instance already running it will throw a `SingletonException`.

	This option is very useful if you have scripts executed by crontab at small amounts of time.
	Remember that this works by creating a lock file with a filename based on the full path to the script file.
	Providing a flavor_id will augment the filename with the provided flavor_id, allowing you to create multiple singleton instances from the same file. This is particularly useful if you want specific functions to have their own singleton instances.
	"""

    def __init__(self, flavor_id=""):
        self._initialized = False
        basename = os.path.splitext(os.path.abspath(sys.argv[0]))[0].replace(
            "/", "-").replace(":", "").replace("\\", "-") + '-%s' % flavor_id + '.lock'
        # os.path.splitext(os.path.abspath(sys.modules['__main__'].__file__))[0].replace("/", "-").replace(":", "").replace("\\", "-") + '-%s' % flavor_id + '.lock'
        self.lockfile = os.path.normpath(
            tempfile.gettempdir() + '/' + basename)

        if sys.platform == 'win32':
            try:
                # file already exists, we try to remove (in case previous
                # execution was interrupted)
                if os.path.exists(self.lockfile):
                    os.unlink(self.lockfile)
                self.fd = os.open(
                    self.lockfile, os.O_CREAT | os.O_EXCL | os.O_RDWR)
            except BaseException as e:
                type, e, tb = sys.exc_info()
                if e.errno == 13:
                    print("Another instance is already running, quitting.")
                    raise SingletonException()
                print(e.errno)
                raise
        else:  # non Windows
            import fcntl
            self.fp = open(self.lockfile, 'w')
            self.fp.flush()
            try:
                fcntl.lockf(self.fp, fcntl.LOCK_EX | fcntl.LOCK_NB)
            except IOError:
                print("Another instance is already running, quitting.")
                raise SingletonException()
        self._initialized = True

    def __del__(self):
        if not self._initialized:
            return
        try:
            if sys.platform == 'win32':
                if hasattr(self, 'fd'):
                    os.close(self.fd)
                    os.unlink(self.lockfile)
            else:
                import fcntl
                fcntl.lockf(self.fp, fcntl.LOCK_UN)
                # os.close(self.fp)
                if os.path.isfile(self.lockfile):
                    os.unlink(self.lockfile)
        except Exception as e:
            print("Unloggable error: %s" % e)
            sys.exit(-1)
