#
# This file is part of Neubot <https://www.neubot.org/>.
#
# Neubot is free software. See AUTHORS and LICENSE for more
# information on the copying conditions.
#

""" The /api/log endpoint """

from __future__ import print_function

import json
import logging
import time

from twisted.web import resource

from ..common import parse_debug

class ApiLog(resource.Resource):
    """ Implements the /api/log endpoint """

    director = None  # set to a Director instance during configuration
    isLeaf = True

    def render_GET(self, request):
        """ Called on GET /api/log """
        request.setHeader("Content-Type", "application/json; charset=utf-8")
        indent_level = parse_debug(request)
        reverse = int(request.args.get("reversed", [0])[0])

        # XXX: this API should be improved / changed as currently we cannot
        # honour verbosity and provide accurate timestamps

        #verbosity = int(request.args.get("verbosity", [1])[0])  # unused!

        generator = self.director.select_measurements(0, time.time())

        result = []
        for record in generator:
            try:
                with open(record["stderr_path"], "r") as filep:
                    content = filep.read()
            except IOError:
                logging.warning("Cannot open: %s", record["stderr_path"])
                continue
            if not content:
                continue
            result.append({
                "severity": "INFO",
                "timestamp": record["timestamp"],
                "message": content
            })

        if reverse:
            result.reverse()

        return json.dumps(result, indent=indent_level)
