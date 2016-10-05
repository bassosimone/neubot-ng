#
# This file is part of Neubot <https://www.neubot.org/>.
#
# Neubot is free software. See AUTHORS and LICENSE for more
# information on the copying conditions.
#

""" The /api/exit endpoint """

from __future__ import print_function

from twisted.web import server, resource
from twisted.internet import reactor

class ApiExit(resource.Resource):
    """ Implements the /api/exit endpoint """

    isLeaf = True

    @staticmethod
    def render_POST(_):
        """ Called on POST /api/exit """
        reactor.crash()
        return server.NOT_DONE_YET
