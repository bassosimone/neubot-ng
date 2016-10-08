#
# This file is part of Neubot <https://www.neubot.org/>.
#
# Neubot is free software. See AUTHORS and LICENSE for more
# information on the copying conditions.
#

""" Neubot's director that coordinates running network tests """

import logging
import os
import uuid

from .database.config import Config
from .database.measurements import Measurements
from .database.nettests import NetTests
from .nettest import loader
from .nettest import runner

VERSION = __version__ = "0.5.0"

_CONF_DIR = os.path.join("etc", "neubot")
_LOCAL_STATE_DIR = os.path.join("var", "lib", "neubot")
MEASUREMENTS_DB = os.path.join(_LOCAL_STATE_DIR, "measurements.sqlite")
NETTESTS_DIR = os.path.join(_LOCAL_STATE_DIR, "nettests")
SETTINGS_DB = os.path.join(_LOCAL_STATE_DIR, "settings.sqlite")
SPECS_DIR = os.path.join(_CONF_DIR, "spec", os.name)

DEFAULT_CONFIG = {
    "enabled": {
        "cast": int,
        "default_value": 1,
        "label": "Whether automatic tests are enabled"
    },
    "uuid": {
        "cast": str,
        "default_value": str(uuid.uuid4()),
        "label": "Random unique indentifier"
    }
}

class Director(object):
    """ Neubot's director class """

    settings_db = SETTINGS_DB
    default_config = DEFAULT_CONFIG
    nettests_dir = NETTESTS_DIR
    measurements_db = MEASUREMENTS_DB
    specs_dir = SPECS_DIR

    def __init__(self):
        self._running = None  # The currently running network test
        self.config = None
        self.measurements = None
        self.nettests = None

    def init(self):
        """ Initialize instance variables with configuration """
        self.config = Config(self.settings_db, self.default_config)
        self.measurements = Measurements(self.measurements_db)
        self.nettests = NetTests(self.specs_dir)
        return self

    @staticmethod
    def make():
        """ Allocates and initialize an instance at once """
        return Director().init()

    def all_nettests(self):
        """ Returns information on all nettests """
        return self.nettests.read_all()

    def read_spec(self, test_name):
        """ Reads the specification of a test """
        spec = self.nettests.read_one(test_name)
        if not spec:
            logging.warning("Cannot load nettest %s", test_name)
        return spec  # which is None on error

    def start_test(self, test_name, params):
        """ Given test name and command line params, starts test """
        if self._running:
            logging.warning("Another test already running")
            return
        spec = self.read_spec(test_name)
        if not spec:
            return  # Error message already printed by read_spec()
        cmd_line = loader.load(spec, params)
        if not cmd_line:
            return
        self._running = \
            runner.run(test_name, cmd_line, workdir=self.nettests_dir)
        return self._running

    def monitor_test(self):
        """ Monitors the status of the currently running test """
        if not self._running:
            logging.warning("No test is currently running")
            return
        try:
            record = next(self._running)
        except StopIteration:
            logging.warning("The test already terminated")
            return  # Happens, for example, if exec() fails
        if record["status"] != "running":
            self._running = None
            self.measurements.insert(record)
            return
        return record

    def get_stdout(self):
        """ Gets the standard output of the current running test """
        record = self.monitor_test()
        if not record:
            return  # Error message already printed by `monitor_test()`
        return open(record["stdout_path"], "r")

    def get_stderr(self):
        """ Gets the standard error of the currently running test """
        record = self.monitor_test()
        if not record:
            return  # Error message already printed by `monitor_test()`
        return open(record["stderr_path"], "r")

    def get_config(self):
        """ Get configuration variables """
        return self.config.select()

    def get_config_labels(self):
        """ Get configuration variables labels """
        return self.config.select_labels()

    def update_config(self, new_conf):
        """ Update configuration variables """
        self.config.update(new_conf)

    def select_measurements(self, since, until, **kwargs):
        """ Select results of a specific test """
        return self.measurements.select(since, until, **kwargs)
