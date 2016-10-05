#
# This file is part of Neubot <https://www.neubot.org/>.
#
# Neubot is free software. See AUTHORS and LICENSE for more
# information on the copying conditions.
#

""" Net test loader """

import logging
import re
import shlex
import sys

def load(spec, params):
    """ Given a specific test name and spec, load command line arguments """
    command_line = []
    for elem in shlex.split(spec["command_line"]):
        if not elem.startswith("$"):
            command_line.append(elem)
            continue
        if elem == "$python":
            command_line.append(sys.executable)
            continue
        variable_name = elem[1:]  # Remove the leading `$`
        if variable_name not in params:
            # TODO: add possibility of specifying the default value
            logging.warning("No mapping for: %s", variable_name)
            return
        value = params[variable_name]
        if variable_name not in spec["params"]:
            logging.warning("No descriptor for: %s", variable_name)
            return
        if "regexp" not in spec["params"][variable_name]:
            logging.warning("No regexp for: %s", variable_name)
            return
        regexp = spec["params"][variable_name]["regexp"]
        if not re.match(regexp, value):
            logging.warning("Regexp does not match for: %s", variable_name)
            return
        command_line.append(value)
    return command_line
