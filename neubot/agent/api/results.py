#
# This file is part of Neubot <https://www.neubot.org/>.
#
# Neubot is free software. See AUTHORS and LICENSE for more
# information on the copying conditions.
#

""" The /api/results endpoint """

from __future__ import print_function

import json

from twisted.web import resource

from ..common import parse_debug

class ApiResults(resource.Resource):
    """ Implements the /api/results endpoint """

    isLeaf = True
    config_file = None  # To be set to point to proper file at config time

    def render_GET(self, request):
        """ Called on GET /api/results """
        request.setHeader("Content-Type", "application/json; charset=utf-8")
        test_name = request.args["test_name"][0]
        indent_level = parse_debug(request)
        with open(self.config_file, "r") as filep:
            data = json.load(filep)
        result = data.get(test_name, {})
        result.update({
            "available_tests": data.keys(),
        })
        return json.dumps(result, indent=indent_level)
