#
# This file is part of Neubot <https://www.neubot.org/>.
#
# Neubot is free software. See AUTHORS and LICENSE for more
# information on the copying conditions.
#

""" Configuration """

import sqlite3

class Config(object):
    """ Configuration database class """

    def __init__(self, path, variables):
        """
            Initializes the database.

            The `path` argument is the path of the database.

            The `variables` argument contains accepted variables and
            looks like the following:

                {
                    "enabled": {
                        "cast": int,
                        "default_value": 1,
                        "label": "Whether automatic tests are enabled"
                    }
                }
        """
        self._conn = sqlite3.connect(path)
        self._variables = variables
        self._conn.row_factory = sqlite3.Row
        self._conn.execute("""CREATE TABLE IF NOT EXISTS config(
                             name TEXT PRIMARY KEY,
                             value TEXT);""")
        conf = self.select()
        for name in self._variables:
            if name not in conf:
                self._conn.execute("INSERT INTO config VALUES(?, ?);",
                                   (name,
                                    self._variables[name]["default_value"]))
        self._conn.commit()

    def select(self):
        """ Select configuration variables """
        result = {}
        cursor = self._conn.cursor()
        cursor.execute("SELECT name, value FROM config;")
        for name, value in cursor:
            if name in self._variables:
                value = self._variables[name]["cast"](value)
                result[name] = value
        return result

    def select_labels(self):
        """ Select configuration labels """
        return dict(((name, self._variables[name]["label"])
                     for name in self._variables))

    def update(self, dictionary):
        """ Internal function to set config """
        for name in dictionary.keys():
            if name not in self._variables:
                del dictionary[name]
                continue
            # Check whether the type is okay
            # TODO: consider also adding regex for furher robustness
            self._variables[name]["cast"](dictionary[name])
        self._conn.executemany("INSERT OR REPLACE INTO config VALUES(?, ?);",
                               dictionary.items())
        self._conn.commit()
