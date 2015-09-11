# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

import sys
import io
import codecs

from . import run


def main(argv=sys.argv):
    fpi = io.open(argv[1], "r", encoding="utf-8")

    try:
        fpo = io.open(argv[2], "w", encoding="utf-8")
    except IndexError:
        fpo = codecs.getwriter("utf-8")(sys.stdout)

    return run(fpi, fpo)


if __name__ == "__main__":
    sys.exit(main())
