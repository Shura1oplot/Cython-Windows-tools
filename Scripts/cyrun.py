#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

import sys
import os
import io
import locale
import time
import shutil

from cypp import run as cypp_run


reload(sys)
sys.setdefaultencoding(locale.getpreferredencoding())


def nt(a, b):
    if os.path.exists(a):
        if os.path.exists(b):
            return os.stat(a).st_mtime > os.stat(b).st_mtime

        return True

    elif os.path.exists(b):
        return False

    else:
        raise ValueError("both files do not exist")


def update_pyx(py_file, pyx_file):
    fpi = io.open(py_file, "r", encoding="utf-8")
    fpo = io.open(pyx_file, "w", encoding="utf-8")

    try:
        cypp_run(fpi, fpo)
    finally:
        fpi.close()
        fpo.close()


def update_pyd(pyx_file):
    from setuptools import setup
    from Cython.Build import cythonize

    argv = sys.argv[:]
    sys.argv[1:] = ["build_ext", "-i"]

    try:
        setup(ext_modules=cythonize(pyx_file))
    except SystemExit as e:
        if e.code != 0:
            raise

    sys.argv[:] = argv


def run_pyd(pyd_file, argv):
    fname, _ = os.path.splitext(os.path.basename(pyd_file))
    sys.path.insert(0, os.path.dirname(pyd_file))
    module = __import__(fname)

    print(">" * 80)

    ts = time.time()
    rv = module.main([pyd_file, ] + argv)
    td = time.time() - ts

    print("<" * 80)
    print("time: {}h {}m {:.2f}s".format(int(td / 60 / 60),
                                         int((td / 60) % 60),
                                         td % 60),
          file=sys.stderr)

    return rv


def clean(pyx_file, pyd_file=None):
    if os.path.isfile(pyx_file):
        os.remove(pyx_file)

    if pyx_file.endswith(".pyx"):
        c_file = pyx_file[:-3] + "c"

        if os.path.isfile(c_file):
            os.remove(c_file)

    if pyd_file and os.path.isfile(pyd_file):
        os.remove(pyd_file)

    if os.path.isdir("build"):
        shutil.rmtree("build")


def main(argv=sys.argv):
    prog = os.path.basename(argv[0])

    try:
        py_file = argv[1]
    except IndexError:
        return 0

    if not os.path.isfile(py_file):
        print("{}: cannot open file: {}".format(prog, py_file))
        return 1

    if py_file.endswith(b".py"):
        pyx_file = b"{}x".format(py_file)
    else:
        pyx_file = b"{}.pyx".format(py_file)

    pyd_file = b"{}d".format(pyx_file[:-1])

    if nt(py_file, pyd_file):
        clean(pyx_file, pyd_file)
        update_pyx(py_file, pyx_file)
        update_pyd(pyx_file)
        clean(pyx_file)

    if os.path.isfile(pyd_file):
        return run_pyd(pyd_file, argv[2:])


if __name__ == "__main__":
    sys.exit(main())
