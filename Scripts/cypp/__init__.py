# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function
import sys
import io
import codecs


__version_info__ = (0, 1, 0)
__version__ = ".".join(str(x) for x in __version_info__)


SWAP_LINES  = "#? "
MODIFY_LINE = "#< "


def run(fpi, fpo):
    skip_next_line = False

    for i, line in enumerate(fpi):
        if i == 0 and line.startswith("#!"):
            if "3" in line:
                fpo.write("# cython: language_level=3\n")
                continue

            else:
                fpo.write("# cython: language_level=2\n")
                continue

        if skip_next_line:
            skip_next_line = False
            continue

        if line.lstrip().startswith(SWAP_LINES):
            line = line.replace(SWAP_LINES, "", 1)
            skip_next_line = True

        elif MODIFY_LINE in line:
            line, prepend = line.split(MODIFY_LINE, 1)
            spaces = len(line) - len(line.lstrip())
            line = line[0:spaces] + prepend.strip() + " " + line[spaces:]

        fpo.write(line.rstrip())
        fpo.write("\n")


def main(argv=sys.argv):
    fpi = io.open(argv[1], "r", encoding="utf-8")

    try:
        fpo = io.open(argv[2], "w", encoding="utf-8")
    except IndexError:
        fpo = codecs.getwriter("utf-8")(sys.stdout)

    return run(fpi, fpo)


if __name__ == "__main__":
    sys.exit(main())
