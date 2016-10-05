#
# This file is part of Neubot <https://www.neubot.org/>.
#
# Neubot is free software. See AUTHORS and LICENSE for more
# information on the copying conditions.
#

""" State of the agent """

import json
import logging
import os
import time

class State(object):
    """ Class representing agent's state """

    # Implementation note: with respect to v0.4.16.9, here we use a counter
    # rather than the current time to keep track of progress. The counter is
    # good because it's robust to time jumps, but the JavaScript code is to
    # changed to reset its state if the server seems coming from the past.

    def __init__(self):
        self._current = "idle"
        self._events = {
            "pid": os.getpid(),
            "since": int(time.time())
        }
        self._tsnap = 1  # so we update client starting from zero
        self._deferreds = []

    @property
    def current_tsnap(self):
        """ Return current state """
        return self._tsnap

    def serialize(self, indent_level=None):
        """ Serialize the state """
        return json.dumps({
            "events": self._events,
            "current": self._current,
            "t": self._tsnap
        }, indent=indent_level)

    def update(self, name, event=None):
        """ Update the current state """
        self._current = name
        self._events[name] = event
        self._tsnap += 1
        logging.debug("emit %s event", name)
        xyz, self._deferreds = self._deferreds, []
        for deferred in xyz:
            if not deferred.called:
                deferred.callback(self)

    def register(self, deferred):
        """ Register deferred to notify of next event """
        self._deferreds.append(deferred)
