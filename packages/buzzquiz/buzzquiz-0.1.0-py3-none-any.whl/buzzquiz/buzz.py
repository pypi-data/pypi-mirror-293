# Python 3.10
# 31/08/2024
"""Buzz! buzzers handler

Main module acts as a facade for Buzz! controllers and interfaces.

Must be initialized via 'init' function, which registers all connected Buzz!
controllers. If none are found, BuzzError exception is raised.

"""

import atexit

import hid

from buzzquiz import lights, reader
from buzzquiz.controllers import Button, Controller, ControllerSet


class BuzzError(Exception):
    """Custon exception for Buzz! controllers errors"""


__initialized = False
_bsets = []
controllers = []


def init(n_controllers: int = 0) -> None:
    """Initializes Buzz! controllers

    If 'n_controllers' is set to a positive integer, only the amount of
    specified controllers will be used. If the number is higher than the
    available, it will raise a BuzzError exception.

    """
    global __initialized
    if __initialized:
        return
    __initialized = True

    # find all buzz controllers
    bset_id = 0
    for port in hid.enumerate():
        if "BUZZ" in port["product_string"].upper():
            _bsets.append(ControllerSet(bset_id, port["path"]))
            bset_id += 1

    # generate controllers
    global controllers
    controllers = [controller for bset in _bsets for controller in bset._controllers]
    if len(controllers) == 0:
        raise BuzzError("No Buzz! controllers found")
    n_controllers = n_controllers or len(controllers)
    if len(controllers) < n_controllers:
        raise BuzzError("Not enough Buzz! controllers found")
    controllers = controllers[:n_controllers]

    # start threads
    reader._start()
    lights._start()


get_status = reader.get_status
get_event = reader.get_event


# at exit stops all threads


def _exit() -> None:
    """Exit function"""
    # lights off
    lights.off()
    lights._stop.set()
    lights._thread.join()
    # reader stop
    reader._stop.set()
    for thread in reader._threads:
        thread.join()


atexit.register(_exit)
