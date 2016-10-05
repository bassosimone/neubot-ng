#
# This file is part of Neubot <https://www.neubot.org/>.
#
# Neubot is free software. See AUTHORS and LICENSE for more
# information on the copying conditions.
#

""" The /api/version endpoint """

from __future__ import print_function

from ...director import VERSION

from twisted.web import resource

class ApiVersion(resource.Resource):
    """ Implements the /api/version endpoint """

    isLeaf = True

    def render_GET(self, request):
        """ Called on GET /api/version """
        request.setHeader("Content-Type", "text/plain; charset=utf-8")
        return VERSION
