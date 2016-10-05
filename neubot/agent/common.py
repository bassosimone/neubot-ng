#
# This file is part of Neubot <https://www.neubot.org/>.
#
# Neubot is free software. See AUTHORS and LICENSE for more
# information on the copying conditions.
#

""" Code shared by the agent implementation """

def parse_debug(request):
    """ Parse the debug option passed to the web api which returns the
        indent level to be passed to simplejson: `None` means do not even
        add newlinws, `0` add newlines but not indent, and so on. """
    indent = None
    dbg = request.args.get("debug", [])
    if dbg:
        indent = int(dbg[0])  # Let the exception propagate on failure
    return indent
