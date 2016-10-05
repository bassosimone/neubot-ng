#
# This file is part of Neubot <https://www.neubot.org/>.
#
# Neubot is free software. See AUTHORS and LICENSE for more
# information on the copying conditions.
#

""" The agent sub-command """

from __future__ import print_function

import getopt
import logging
import sys

from twisted.python import log

from .. import agent

USAGE = """\
usage:
  neubot agent [-v] [-A address] [-p port]
  neubot run --help"""

def subcommand(args):
    """ The agent subcommand """

    try:
        options, arguments = getopt.getopt(args[1:], "A:p:v", ["help"])
    except getopt.error:
        print(USAGE)
        sys.exit(1)
    if arguments:
        print(USAGE)
        sys.exit(1)

    address = "127.0.0.1"
    port = 9774
    verbosity = logging.WARNING
    print_usage = False
    for name, value in options:
        if name == "-A":
            address = value
        elif name == "--help":
            print_usage = True
        elif name == "-p":
            port = int(value)
        elif name == "-v":
            verbosity = logging.DEBUG

    if print_usage:
        print(USAGE)
        sys.exit(0)

    logging.basicConfig(format="%(message)s", level=verbosity)
    log.PythonLoggingObserver().start()

    agent.run(address, port)
