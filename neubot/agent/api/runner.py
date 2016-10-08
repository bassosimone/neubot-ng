#
# This file is part of Neubot <https://www.neubot.org/>.
#
# Neubot is free software. See AUTHORS and LICENSE for more
# information on the copying conditions.
#

""" The /api/runner endpoint """

from __future__ import print_function

import json
import logging

from twisted.web import server, resource
from twisted.internet import reactor

class ApiRunner(resource.Resource):
    """ Implements the /api/runner endpoint """

    director = None  # set to a Director instance during configuration
    state = None  # set to a State instance during configuration
    isLeaf = True

    # XXX The v0.4.16.9 web-ui uses GET but POST would be more proper
    def render_GET(self, request):
        """ Called on GET /api/runner """
        return self.render_POST(request)

    def render_POST(self, request):
        """ Called on POST /api/runner """

        request.setHeader("Content-Type", "application/json; charset=utf-8")
        test_name = request.args["test"][0]
        streaming = int(request.args.get("streaming", [0])[0])

        # Note: the request body is an extension of the specification
        test_params = {}
        request_body = request.content.read()
        if request_body:
            test_params = json.loads(request_body)

        record = self.director.start_test(test_name, test_params)
        if not record:
            request.setResponseCode(500)
            return "{}"

        def monitor_test():
            """ Monitor test until it is complete """
            logging.debug("checking whether %s is still running", test_name)
            if not self.director.monitor_test():
                logging.debug("nettest terminated %s", test_name)
                self.state.update("idle")
                return
            logging.debug("scheduling next check for %s", test_name)
            reactor.callLater(1.0, monitor_test)

        self.state.update("test", {})
        reactor.callLater(1.0, monitor_test)

        if not streaming:
            return "{}"

        # Here we handle the streaming case

        def read_stdio():
            """ Reads the test's stdio """
            stderr_fp = self.director.get_stderr()
            if not stderr_fp:
                request.finish()
                return
            stdout_fp = self.director.get_stdout()
            if not stdout_fp:
                request.finish()
                return
            request.write(stderr_fp.read())
            request.write(stdout_fp.read())
            reactor.callLater(0.5, read_stdio)

        reactor.callLater(0.5, read_stdio)

        return server.NOT_DONE_YET
