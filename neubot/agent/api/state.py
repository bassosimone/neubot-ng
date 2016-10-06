#
# This file is part of Neubot <https://www.neubot.org/>.
#
# Neubot is free software. See AUTHORS and LICENSE for more
# information on the copying conditions.
#

""" The /api/state endpoint """

from __future__ import print_function

from twisted.web import server, resource
from twisted.internet import defer, reactor

from ..common import parse_debug

class ApiState(resource.Resource):
    """ Implements the /api/state endpoint """

    director = None  # set to a Director instance during configuration
    state = None  # set to a State instance during configuration
    isLeaf = True

    def render_GET(self, request):
        """ Called on GET /api/state """

        request.setHeader("Content-Type", "application/json; charset=utf-8")
        tsnap = int(request.args.get("t", ["0"])[0])
        indent_level = parse_debug(request)

        if self.state.current_tsnap > tsnap:
            return self.state.serialize()

        deferred = defer.Deferred()
        def finish_response(_):
            """ Finish response when state changes """
            request.write(self.state.serialize(indent_level))
            request.finish()

        def do_timeout():
            """ Timeout the deferred, if needed """
            if not deferred.called:
                deferred.callback(None)

        reactor.callLater(60.0, do_timeout)
        deferred.addCallback(finish_response)
        self.state.register(deferred)

        return server.NOT_DONE_YET
