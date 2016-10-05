#
# This file is part of Neubot <https://www.neubot.org/>.
#
# Neubot is free software. See AUTHORS and LICENSE for more
# information on the copying conditions.
#

""" The /api and /api/ endpoints """

from __future__ import print_function

import json

from twisted.web import resource

class Api(resource.Resource):
    """ The /api and /api/ endpoints of the web API """

    def render_GET(self, request):
        request.setHeader("Content-Type", "application/json; charset=utf-8")
        return json.dumps([
            "/api",
            "/api/",
            "/api/config",
            "/api/data",
            "/api/debug",
            "/api/exit",
            "/api/index",
            "/api/log",
            "/api/results",
            "/api/runner",
            "/api/state",
            "/api/version",
        ])
