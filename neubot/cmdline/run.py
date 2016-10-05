#
# This file is part of Neubot <https://www.neubot.org/>.
#
# Neubot is free software. See AUTHORS and LICENSE for more
# information on the copying conditions.
#

""" The run sub-command """

from __future__ import print_function

import getopt
import json
import logging
import sys
import time

from ..director import Director

USAGE = """\
usage:
  neubot run nettest [--help] [-v] [-D key=value]
  neubot run --help"""

def _do_run(director, test_name, params):
    """ Run network test and monitor its standard error """
    started = director.start_test(test_name, params)
    if not started:
        sys.exit(1)  # Error message already printed by start_test()
    stdout_fp = director.get_stdout()
    if not stdout_fp:
        logging.warning("cannot open nettest's standard output")
        sys.exit(1)
    stderr_fp = director.get_stderr()
    if not stderr_fp:
        logging.warning("cannot open nettest's standard error")
        sys.exit(1)
    while True:
        sys.stdout.write(stdout_fp.read())
        sys.stderr.write(stderr_fp.read())
        if not director.monitor_test():
            break
        time.sleep(0.5)

def subcommand(args):
    """ The run subcommand """

    if len(args) <= 1:
        print(USAGE)
        sys.exit(0)

    director = Director.make()

    if args[1] == "--help":
        print(USAGE)
        print("available tests:")
        for name, _ in director.all_nettests():
            print("  " + name)
        sys.exit(0)

    test_name = args[1]
    try:
        options, arguments = getopt.getopt(args[2:], "D:v", ["help"])
    except getopt.error:
        print(USAGE)
        sys.exit(1)
    if arguments:
        print(USAGE)
        sys.exit(1)

    params = {}
    verbosity = logging.WARNING
    print_usage = False
    for name, value in options:
        if name == "-D":
            oname, ovalue = value.split("=", 1)
            params[oname] = ovalue
        elif name == "--help":
            print_usage = True
        elif name == "-v":
            verbosity = logging.DEBUG

    logging.basicConfig(format="%(message)s", level=verbosity)

    if print_usage:
        spec = director.read_spec(test_name)
        if not spec:
            sys.exit(1)  # Error message already printed by read_spec()
        print(json.dumps(spec, indent=4))
        sys.exit(0)

    _do_run(director, test_name, params)
