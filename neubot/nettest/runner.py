#
# This file is part of Neubot <https://www.neubot.org/>.
#
# Neubot is free software. See AUTHORS and LICENSE for more
# information on the copying conditions.
#

""" Net test runner """

import logging
import subprocess
import tempfile
import time
import uuid

def run(test_name, command_line, **kwargs):
    """ Run a specific test by command line and wait for its completion """
    workdir = kwargs.get("workdir", tempfile.mkdtemp())
    max_runtime = kwargs.get("max_runtime", 60.0)
    begin = time.time()
    test_id = str(uuid.uuid4())
    stdout_prefix = "neubot-" + test_name + "-" + test_id + "-stdout-"
    stdout = tempfile.NamedTemporaryFile(prefix=stdout_prefix, delete=False,
                                         suffix=".txt", dir=workdir)
    stderr_prefix = "neubot-" + test_name + "-" + test_id + "-stderr-"
    stderr = tempfile.NamedTemporaryFile(prefix=stderr_prefix, delete=False,
                                         suffix=".txt", dir=workdir)
    logging.debug("run nettest %s in dir %s", test_name, workdir)
    try:
        proc = subprocess.Popen(command_line, close_fds=True, stdout=stdout,
                                stderr=stderr, cwd=workdir)
    except OSError:
        return  # This will terminate the iterator early
    proc_record = {
        "status": "running",
        "exitcode": 0,
        "test_id": test_id,
        "timestamp": begin,
        "stderr_path": stderr.name,
        "stdout_path": stdout.name,
        "test_name": test_name,
        "workdir": workdir
    }
    while True:
        current_time = time.time()
        exitcode = proc.poll()
        if exitcode is not None:
            logging.debug("nettest %s exited (code %d)", test_name, exitcode)
            proc_record["status"] = "exited"
            proc_record["exitcode"] = exitcode
            yield proc_record
            return  # This stops the generator
        delta = current_time - begin
        if delta > max_runtime:
            logging.warning("force terminating nettest %s", test_name)
            proc.terminate()
            # Note: yes, here we could `continue` assuming that the process
            # is killed and hence we then break out of the loop but, just in
            # case something strange happens, break out as soon as we have
            # deciced to kill the child process rather than looping
            proc_record["status"] = "killed"
            proc_record["exitcode"] = -1
            yield proc_record
            return  # This stops the generator
        logging.debug("nettest %s still running after %f s", test_name, delta)
        yield proc_record
