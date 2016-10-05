#
# This file is part of Neubot <https://www.neubot.org/>.
#
# Neubot is free software. See AUTHORS and LICENSE for more
# information on the copying conditions.
#

""" The main() of Neubot """

from __future__ import print_function

import sys

from .director import VERSION

USAGE = """\
usage:
  neubot command [options...]
  neubot --help
  neubot --version
commands:
  agent - runs neubot's api and web user interface
  run - runs a specific network test from the command line"""

def main():
    """ The main() function of Neubot """

    if len(sys.argv) <= 1:
        print(USAGE)
        sys.exit(1)

    if sys.argv[1] == "--version":
        print(VERSION)
        sys.exit(0)

    if sys.argv[1] == "--help":
        print(USAGE)
        sys.exit(0)

    subcommand = sys.argv[1]
    args = sys.argv[1:]

    if subcommand == "agent":
        from .cmdline import agent
        agent.subcommand(args)
        sys.exit(0)

    if subcommand == "run":
        from .cmdline import run
        run.subcommand(args)
        sys.exit(0)

    print(USAGE)
    sys.exit(1)

if __name__ == "__main__":
    main()
