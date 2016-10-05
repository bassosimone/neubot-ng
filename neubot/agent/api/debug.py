#
# This file is part of Neubot <https://www.neubot.org/>.
#
# Neubot is free software. See AUTHORS and LICENSE for more
# information on the copying conditions.
#

""" The /api/debug endpoint """

from __future__ import print_function

from twisted.web import resource

class ApiDebug(resource.Resource):
    """ Implements the /api/debug endpoint """

    isLeaf = True

    @staticmethod
    def render_GET(request):
        """ Called on GET /api/debug """
        request.setHeader("Content-Type", "application/json; charset=utf-8")
        return "{}"
