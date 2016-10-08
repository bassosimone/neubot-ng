#
# This file is part of Neubot <https://www.neubot.org/>.
#
# Neubot is free software. See AUTHORS and LICENSE for more
# information on the copying conditions.
#

""" Net test loader """

import logging
import os
import re
import shlex
import sys

def load(spec, params):
    """ Given a specific test name and spec, load command line arguments """

    # TODO: add the possibility of specifying the default value

    for variable_name in spec["params"]:
        if "default_value" not in spec["params"][variable_name]:
            continue
        if variable_name in params:
            continue
        params[variable_name] = spec["params"][variable_name]["default_value"]

    for variable_name in params:
        if variable_name not in spec["params"]:
            logging.warning("No descriptor for: %s", variable_name)
            return
        if "regexp" not in spec["params"][variable_name]:
            logging.warning("No regexp for: %s", variable_name)
            return
        regexp = spec["params"][variable_name]["regexp"]
        if not re.match(regexp, params[variable_name]):
            logging.warning("Regexp does not match for: %s", variable_name)
            return

    params.update({
        "pwd": os.path.abspath("."),
        "python": sys.executable
    })

    command_line = spec["command_line"].format(**params)
    command_line = shlex.split(command_line)
    logging.debug("command line: %s", command_line)

    return command_line
