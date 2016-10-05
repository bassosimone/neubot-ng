#
# This file is part of Neubot <https://www.neubot.org/>.
#
# Neubot is free software. See AUTHORS and LICENSE for more
# information on the copying conditions.
#

""" Measurements results database """

import sqlite3

class Measurements(object):
    """ Measurements results database class """

    def __init__(self, path):
        """ Initialize the results database class. """
        self._conn = sqlite3.connect(path)
        self._conn.row_factory = sqlite3.Row
        self._conn.execute("""CREATE TABLE IF NOT EXISTS measurements(
                             id INTEGER PRIMARY KEY,
                             timestamp NUMBER,
                             test_name TEXT,
                             status TEXT,
                             exitcode NUMBER,
                             test_id TEXT,
                             stderr_path TEXT,
                             stdout_path TEXT,
                             workdir TEXT);""")

    def select(self, since, until, **kwargs):
        """ Select saved data """
        cursor = self._conn.cursor()
        if kwargs.get("test_name"):
            cursor.execute("""SELECT * FROM measurements
                              WHERE timestamp >= ? AND
                                    timestamp < ? AND
                                    test_name = ?;""",
                           (since, until, kwargs["test_name"]))
        else:
            cursor.execute("""SELECT * FROM measurements
                              WHERE timestamp >= ? AND
                                    timestamp < ?;""",
                           (since, until))

        return (dict(e) for e in cursor)

    def insert(self, record, **kwargs):
        """ Insert new result in database """
        self._conn.execute("""INSERT INTO measurements(id, timestamp, test_name,
                             status, exitcode, test_id, stderr_path,
                             stdout_path, workdir) VALUES(NULL, ?, ?, ?, ?, ?,
                             ?, ?, ?);""",
                           (record["timestamp"], record["test_name"],
                            record["status"], record["exitcode"],
                            record["test_id"], record["stderr_path"],
                            record["stdout_path"], record["workdir"]))
        if kwargs.get("commit", True):
            self.commit()

    def commit(self):
        """ Commit changes """
        self._conn.commit()
