# Python 3.10
# 30/08/2024
"""Buzz lights controller interface

Handles basic functions like turning on and off, but also complex ones, like
blinking and walking.

"""

import threading
import time
import queue
from enum import Enum

from buzzquiz import buzz


DEFAULT_QUEUE_TIMEOUT = 0.1

TIMEOUT_CYCLES = 3
TIMEOUT_START_SPEED = 0.4


# local variables

_stack = queue.Queue()
_stop = threading.Event()
_thread = None


# public functions


class Mode(str, Enum):
    """Light modes"""

    ON = "on"
    OFF = "off"
    BLINK = "blink"
    WALK = "walk"
    TIMEOUT = "timeout"


def on(targets: list[int] | None = None) -> None:
    """Turns on the lights"""
    _stack.put((Mode.ON, 1, targets))


def off(targets: list[int] | None = None) -> None:
    """Turns off the lights"""
    _stack.put((Mode.OFF, 1, targets))


def select(targets: int | list[int]) -> None:
    """Turns off all the lights except the ones in 'targets'"""
    targets = [targets] if isinstance(targets, int) else targets
    off()
    on(targets)


def blink(duration: float, targets: list[int] | None = None, clear: bool = False) -> None:
    """Blinks the lights each 'duration' seconds"""
    _stack.put((Mode.BLINK, duration, targets))
    if clear:
        _stack.put((Mode.OFF, duration, [c.id for c in buzz.controllers if c.id not in targets]))


def walk(duration: float, targets: list[int] | None = None, clear: bool = False) -> None:
    """Turns on the lights of 'targets' one by one each 'duration' seconds"""
    _stack.put((Mode.WALK, duration, targets))
    if clear:
        _stack.put((Mode.OFF, duration, [c.id for c in buzz.controllers if c.id not in targets]))


def timeout(duration: float, targets: list[int] | None = None, clear: bool = False) -> None:
    """Blinks the light 'duration' seconds, increasing speed as the time passes

    Note that 'duration' does not refer to the time between blinks, but the
    total time the light will be blinking. After that time, the mode will
    automatically change to 'off'.

    """
    _stack.put((Mode.TIMEOUT, duration, targets))
    if clear:
        _stack.put((Mode.OFF, duration, [c.id for c in buzz.controllers if c.id not in targets]))


def sync() -> None:
    """Synchronizes the lights of all controllers"""
    _stack.put(("sync", 0, None))


# background writing thread


def _run() -> None:
    """Run the lights controller

    The behavior of each controller's light is defined individually, and can be
    changed stacking commands in the queue.

    Each amount of time, lights are updated with the specific action affecting
    each controller.

    """
    # setup
    lights = [
        {
            "mode": Mode.OFF,
            "duration": 0,
            "tstep": 0,
        }
        for _ in buzz.controllers
    ]
    for controller in buzz.controllers:
        controller.light = False

    # main loop
    while not _stop.is_set():
        # check for new commands
        try:
            mode, duration, targets = _stack.get(timeout=DEFAULT_QUEUE_TIMEOUT)
        except queue.Empty:
            pass
        else:
            # sync special command
            if mode == "sync":
                for controller in buzz.controllers:
                    controller.light = False
                    lights[controller.id]["tstep"] = 0
                continue

            # update commands on targeted controllers
            targets = targets or [controller.id for controller in buzz.controllers]
            for controller_id in targets:
                lights[controller_id]["mode"] = mode
                lights[controller_id]["duration"] = duration
                lights[controller_id]["tstep"] = 0

                if mode == Mode.TIMEOUT:
                    lights[controller_id]["cycles"] = iter(
                        [duration * 0.5, duration * 0.3, duration * 0.2]
                    )
                    lights[controller_id]["cycle"] = next(lights[controller_id]["cycles"])
                    lights[controller_id]["tcycle"] = time.time()
                    lights[controller_id]["duration"] = TIMEOUT_START_SPEED

        # update lights depending on the mode
        current_time = time.time()
        walkers = []
        walker_on = None
        for controller in buzz.controllers:
            # only if duration is consumed
            if current_time - lights[controller.id]["tstep"] < lights[controller.id]["duration"]:
                continue

            # on / off
            if lights[controller.id]["mode"] == Mode.ON:
                controller.light = True
            elif lights[controller.id]["mode"] == Mode.OFF:
                controller.light = False

            # blink
            elif lights[controller.id]["mode"] == Mode.BLINK:
                controller.light = not controller.light
                if lights[controller.id]["tstep"] == 0:
                    controller.light = True  # allows sync between controllers

            # timeout (blink with increasing speed)
            elif lights[controller.id]["mode"] == Mode.TIMEOUT:
                controller.light = not controller.light
                if current_time - lights[controller.id]["tcycle"] > lights[controller.id]["cycle"]:
                    lights[controller.id]["tcycle"] = current_time
                    lights[controller.id]["duration"] /= 2
                    lights[controller.id]["cycle"] = next(lights[controller.id]["cycles"], 0)
                    if lights[controller.id]["duration"] < 0.1:
                        # after timeout is reached, turn off
                        lights[controller.id]["mode"] = Mode.OFF
                        lights[controller.id]["duration"] = 1
                        controller.light = False

            # walk
            elif lights[controller.id]["mode"] == Mode.WALK:
                walkers.append(controller)
                if not walker_on and controller.light:
                    walker_on = controller

            # update tstep
            lights[controller.id]["tstep"] = current_time

        # walk logic
        if walkers:
            walker_on = walker_on or walkers[-1]
            walker_on.light = False
            next_walker = walkers[(walkers.index(walker_on) + 1) % len(walkers)]
            next_walker.light = True

        # write lights' status through the device
        for bset in buzz._bsets:
            bset.write()


def _start() -> None:
    """Starts the lights controller"""
    global _thread
    _thread = threading.Thread(target=_run, daemon=True)
    _thread.start()
