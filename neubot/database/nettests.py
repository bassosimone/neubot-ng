#
# This file is part of Neubot <https://www.neubot.org/>.
#
# Neubot is free software. See AUTHORS and LICENSE for more
# information on the copying conditions.
#

""" Network tests """

import json
import logging
import os
import re

class NetTests(object):
    """ Network tests database class """

    def __init__(self, basedir):
        self._basedir = basedir

    def read_one(self, name):
        """ Read single test descriptor """
        if name.startswith("."):
            logging.debug("Skipping test name beginning with dot")
            return
        if not re.match("^[a-z_]+$", name):
            logging.warning("Invalid test name: %s", name)
            return
        # Note: no further checks on whether we exit `basedir` here because
        # we make sure the test name does not contain any `../` above
        descriptor = os.path.join(self._basedir, name)
        if not os.path.isfile(descriptor):
            logging.debug("Skipping non-file test descriptor")
            return
        with open(descriptor, "r") as filep:
            return json.load(filep)

    def read_all(self):
        """ Read all tests descriptors """
        for name in os.listdir(self._basedir):
            value = self.read_one(name)
            if value:
                yield name, value
