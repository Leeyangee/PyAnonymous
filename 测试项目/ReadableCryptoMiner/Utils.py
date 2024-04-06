import time

# from ggminer import *


LEVEL_PROTOCOL = 'protocol'
LEVEL_INFO = 'info'
LEVEL_DEBUG = 'debug'
LEVEL_ERROR = 'error'
DEBUG = False


def log(message, level):
    if not DEBUG and level in [LEVEL_DEBUG, LEVEL_PROTOCOL]:
        return

    print("[%s] %s" % (time.strftime("%Y-%m-%d %H:%M:%S"), message))


def human_readable_hashrate(hr):
    """Returns a human readable representation of hashrate."""

    if hr < 1000:
        return "%2f hashes/s" % hr
    if hr < 10000000:
        return "%2f khashes/s" % (hr / 1000)
    if hr < 10000000000:
        return "%2f Mhashes/s" % (hr / 1000000)
    return "%2f Ghashes/s" % (hr / 1000000000)
