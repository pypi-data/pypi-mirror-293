# -*- coding: utf-8 -*-

try:
    import syslog
    syslog.openlog("Percol")
except ImportError:
    pass
    # probably windows
    # https://github.com/mooz/percol/issues/86 why is this debugging by default?


def log(name, s = ""):
    syslog.syslog(syslog.LOG_ALERT, str(name) + ": " + str(s))

def dump(obj):
    import pprint
    pp = pprint.PrettyPrinter(indent=2)
    syslog.syslog(syslog.LOG_ALERT, str(name) + ": " + pp.pformat(obj))
    return obj
