#
# This file is part of Neubot <https://www.neubot.org/>.
#
# Neubot is free software. See AUTHORS and LICENSE for more
# information on the copying conditions.
#

""" The /api/config endpoint """

from __future__ import print_function

import json

from twisted.web import server, resource
from twisted.internet import reactor

from ..common import parse_debug

class ApiConfig(resource.Resource):
    """ Implements the /api/config endpoint """

    director = None  # set to a Director instance during configuration
    state = None  # set to a State instance during configuration
    isLeaf = True

    def render_GET(self, request):
        """ Called on GET /api/config """
        request.setHeader("Content-Type", "application/json; charset=utf-8")
        indent_level = parse_debug(request)
        labels = int(request.args.get("labels", [0])[0])
        if labels:
            result = self.director.get_config_labels()
        else:
            result = self.director.get_config()
        return json.dumps(result, indent=indent_level)

    def render_POST(self, request):
        """ Called on POST /api/config """
        request.setHeader("Content-Type", "application/json; charset=utf-8")
        new_settings = {}
        for name in request.args:
            new_settings[name] = request.args[name][0]
        self.director.update_config(new_settings)  # Would raise on check error

        # Trigger a `config` event such that the likely waiting comet
        # connection is woken up and receives the update
        self.state.update("config", self.director.get_config())

        return "{}"
