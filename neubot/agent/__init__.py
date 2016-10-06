#
# This file is part of Neubot <https://www.neubot.org/>.
#
# Neubot is free software. See AUTHORS and LICENSE for more
# information on the copying conditions.
#

""" Entry point for Neubot's agent """

from __future__ import print_function

import getopt
import logging
import os
import sys

from twisted.internet import reactor, endpoints
from twisted.python import log
from twisted.web import server, resource, static

from .api import Api
from .api.config import ApiConfig
from .api.data import ApiData
from .api.debug import ApiDebug
from .api.exit import ApiExit
from .api.log import ApiLog
from .api.results import ApiResults
from .api.runner import ApiRunner
from .api.state import ApiState
from .api.version import ApiVersion
from ..director import Director
from .state import State

def run(address, port):
    """ Run the agent exposing API at address and port """
    director = Director.make()
    state = State()

    root = static.File(os.path.join("usr", "share", "neubot", "www"))
    api = Api()
    api.putChild("", api)  # this implements the /api/ endpoint
    root.putChild("api", api)

    api_config = ApiConfig()
    api.putChild("config", api_config)
    api_config.director = director
    api_config.state = state

    api_data = ApiData()
    api.putChild("data", api_data)
    api_data.director = director

    api.putChild("debug", ApiDebug())
    api.putChild("exit", ApiExit())

    api_log = ApiLog()
    api.putChild("log", api_log)
    api_log.director = director

    api_results = ApiResults()
    api.putChild("results", api_results)
    api_results.config_file = os.path.join("usr", "share", "neubot", "www",
                                           "config.json")

    api_runner = ApiRunner()
    api.putChild("runner", api_runner)
    api_runner.director = director
    api_runner.state = state

    api_state = ApiState()
    api.putChild("state", api_state)
    api_state.director = director
    api_state.state = state

    api.putChild("version", ApiVersion())

    endpoint = endpoints.TCP4ServerEndpoint(reactor, port, interface=address)
    endpoint.listen(server.Site(root))
    reactor.run()
