#
# This file is part of Neubot <https://www.neubot.org/>.
#
# Neubot is free software. See AUTHORS and LICENSE for more
# information on the copying conditions.
#

""" The /api/data endpoint """

from __future__ import print_function

import json
import logging
import time

from twisted.web import resource

from ..common import parse_debug

class ApiData(resource.Resource):
    """ Implements the /api/data endpoint """

    director = None  # set to a Director instance during configuration
    isLeaf = True

    def render_GET(self, request):
        """ Called on GET /api/data """
        request.setHeader("Content-Type", "application/json; charset=utf-8")
        test_name = request.args["test"][0]
        since = int(request.args.get("since", [0])[0])
        until = int(request.args.get("until", [time.time()])[0])
        indent_level = parse_debug(request)

        generator = \
            self.director.select_measurements(since, until, test_name=test_name)

        # XXX: this API should be replaced with something better but for now
        # I have implemented whats is already available in 0.4.16.9

        result = []
        for record in generator:
            try:
                with open(record["stdout_path"], "r") as filep:
                    content = filep.read()
            except IOError:
                logging.warning("Cannot open: %s", record["stdout_path"])
                continue
            try:
                document = json.loads(content)
            except ValueError:
                result.append({
                    "test_name": record["test_name"],
                    "timestamp": int(record["timestamp"]),
                    "value": content
                })
                continue
            result.append(document)

        return json.dumps(result, indent=indent_level)
