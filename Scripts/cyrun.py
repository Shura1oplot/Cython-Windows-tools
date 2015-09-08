#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

import sys
import os
import io

from dufilib import with_timer
from cypp import run as cypp_run


def nt(a, b):
    if not os.path.exists(b):
        return True

    return os.stat(a).st_mtime > os.stat(b).st_mtime


def update_pyx(py_file, pyx_file):
    fpi = io.open(py_file, "r", encoding="utf-8")
    fpo = io.open(pyx_file, "w", encoding="utf-8")

    cypp_run(fpi, fpo)

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
        print(e)

    sys.argv[:] = argv


def run_pyd(pyd_file, argv):
    fname, _ = os.path.splitext(os.path.basename(pyd_file))
    sys.path.insert(0, os.path.dirname(pyd_file))
    module = __import__(fname)
    return with_timer(module.main)([pyd_file, ] + argv)


def main(argv=sys.argv):
    try:
        py_file = argv[1]
    except IndexError:
        return 0

    if not os.path.isfile(py_file):
        print("cannot open file: {}".format(py_file))
        return 1

    if py_file.endswith(b".py"):
        pyx_file = b"{}x".format(py_file)
    else:
        pyx_file = b"{}.pyx".format(py_file)

    pyd_file = b"{}d".format(pyx_file[:-1])

    if nt(py_file, pyx_file):
        update_pyx(py_file, pyx_file)

    if nt(pyx_file, pyd_file):
        if os.path.isfile(pyd_file):
            os.remove(pyd_file)

        update_pyd(pyx_file)

    if os.path.isfile(pyd_file):
        return run_pyd(pyd_file, argv[2:])


if __name__ == "__main__":
    sys.exit(main())
