# Python 3.10
# 26/08/2024
"""Buzz input reader interface

Provides a way to read input from all handled controllers, casting them into
statuses and events, and including filtering options.

A Status object represents a static snapshot of the status of the buttons of
each controller at a given time.

An Event object represents a change between two subsequent Status objects.

"""
from __future__ import annotations

import threading
import time
import queue
from copy import deepcopy
from typing import Iterator, Literal

from buzzquiz import buzz
from buzzquiz.controllers import Button, Controller, ControllerSet


DEFAULT_QUEUE_TIMEOUT = 0.1
T_WAIT_PRE_CLEAR = 0.2


# local variables

_stack = queue.Queue()
_stop = threading.Event()
_threads = []
_last_status = None


# status and event


BUZZER_DECODE_MAP = {
    0: [23, 19, 20, 21, 22],
    1: [18, 30, 31, 16, 17],
    2: [29, 25, 26, 27, 28],
    3: [24, 36, 37, 38, 39],
}


class Status:
    """Snapshot of the status of each handled controller at a given time

    It can be used as a dictionary, where the key is the controller's ID and
    the value is another dictionary with every button's status (True if
    pressed, False if not).

    Constructor requires the number of controller sets that will be handled.
    To create a status, the 'new' method must be called, with the raw data
    read, and the ID of the set that read it. It will return a new Status that
    reflects the data read. It also automatically inherits from the current
    generated status the statuses of the sets that were not read.

    Attribute 'time_since_start' is the time since the first status was
    generated, in milliseconds.

    Subtract one status object from another creates an Event object, which
    only contains the buttons that changed their status.

    """

    def __init__(self, n_bsets: int) -> None:
        self._status = {}
        for bset_id in range(n_bsets):
            for controller_id in range(4):
                self._status[bset_id * 4 + controller_id] = {
                    Button.BUZZ: False,
                    Button.BLUE: False,
                    Button.ORANGE: False,
                    Button.GREEN: False,
                    Button.YELLOW: False,
                }
        self._nbsets = n_bsets
        self._ts_start = time.time()
        self.time_since_start = 0

    # dict behavior

    def __getitem__(self, key: int) -> dict[Button, bool]:
        return self._status[key]

    def __iter__(self) -> Iterator[int]:
        return iter(self._status)

    def items(self) -> Iterator[tuple[int, dict[Button, bool]]]:
        return self._status.items()

    # new status and event generation

    def new(self, bset_id: int, raw_data: list[int]) -> Status:
        """Generates a new status from raw data read"""
        # copy
        new = Status(self._nbsets)
        new._status = deepcopy(self._status)
        # update
        raw_data = "".join(f"{item:08b}" for item in raw_data)
        for controller_id, buttons_bit in BUZZER_DECODE_MAP.items():
            new._status[bset_id * 4 + controller_id] = {
                Button.BUZZ: raw_data[buttons_bit[0]] == "1",
                Button.BLUE: raw_data[buttons_bit[1]] == "1",
                Button.ORANGE: raw_data[buttons_bit[2]] == "1",
                Button.GREEN: raw_data[buttons_bit[3]] == "1",
                Button.YELLOW: raw_data[buttons_bit[4]] == "1",
            }
        new._ts_start = self._ts_start
        new.time_since_start = float((time.time() - self._ts_start) * 1000)
        return new

    def __sub__(self, other: Status) -> Event:
        """Subtracts two Status objects to get an Event object"""
        return Event(self, other)

    # representation

    def __str__(self) -> str:
        tokens = []
        for controller_id, status in self.items():
            s_status = []
            for button in status:
                s_status.append("\033[30;47m1\033[0m" if status[button] else "0")
            s_status = s_status[0] + "-" + "".join(s_status[1:])
            tokens.append(f"{controller_id}: {s_status}")
        return f"Status({', '.join(tokens)}, ts={self.time_since_start:.2f}ms)"


class Event:
    """Changes between two subsequent Status objects

    It provides the controller's ID, the button that changed, and the status
    of the change (0 if released, 1 if pressed). Implements a bunch of methods
    to check what changed.

    Constructor requires two subsequent Status objects (prev and current).

    It provides attributes 'trel' and 'tabs', which represent the time between
    the two statuses, and the time since the first status was generated,
    both in milliseconds, respectively.

    Note that an Event will only contain the first change found, so creating
    an Event object from two non-consecutive Status objects will provide
    incomplete information. Also, if no changes are found, it will raise a
    ValueError.

    """

    def __init__(self, prev: Status, current: Status) -> None:
        self.controller_id = None
        self.button = None
        self.action = None
        self.trel = current.time_since_start - prev.time_since_start
        self.tabs = current.time_since_start
        # find change
        for controller_id in current:
            for button in current[controller_id]:
                if current[controller_id][button] != prev[controller_id][button]:
                    self.controller_id = controller_id
                    self.button = button
                    self.action = current[controller_id][button]
                    break
            if self.controller_id:
                break
        # check
        if self.controller_id is None:
            raise ValueError("No changes found")

    def is_buzz(self) -> bool:
        return self.button == Button.BUZZ

    def is_color(self) -> bool:
        return self.button in (Button.BLUE, Button.ORANGE, Button.GREEN, Button.YELLOW)

    def is_press(self) -> bool:
        return self.action == True

    def is_release(self) -> bool:
        return self.action == False

    def pressed(self, button: str | Button) -> bool:
        """Checks whether the specified button has been pressed"""
        return self.is_press() and self.button == button

    def released(self, button: str | Button) -> bool:
        """Checks whether the specified button has been released"""
        return self.is_release() and self.button == button

    def is_button(self, button: str | Button) -> bool:
        """Checks whether the specified button has been pressed or released"""
        if button == Button.COLORS:
            return self.is_color()
        return self.button == button

    def __str__(self) -> str:
        style_action = "pressed" if self.action else "released"
        return f"Event(Controller {self.controller_id}: {self.button} {style_action}, tabs={self.tabs:.2f}ms, trel={self.trel:.2f}ms)"


# public functions


def get(
    n: int | None = None,
    block: bool = True,
    timeout: float | None = None,
    pre_clear: bool = True,
    format: Literal["status", "event"] = "status",
    *,
    trigger: Literal["on_all", "on_press", "on_release"] = "on_all",
    buttons: list[str | Button] | None = None,
    controllers: list[int | Controller] | None = None,
) -> Status | Event | list[Status] | list[Event] | None:
    """Reads 'n' subsequent values from all controllers

    If 'n' is None, it returns the first status captured; if it is any
    integer, returns a list of 'n' subsequent values.

    By default, 'get' will block the execution until it meets the specified
    conditions. If 'block' is set to False, it will return None, or an
    incomplete list, when no more data is available without waiting. Another
    way around is to set 'timeout' to a float, which will stop the waiting
    after the specified time (in seconds). 'block' is ignored if 'timeout' is
    set.

    'pre_clear' clears the stack before starting the reading. By default, it
    is set to True. Note that, if 'block' is set to False, nothing will never
    be captured, as the function won't wait for new data to fill the stack.

    'format' specifies whether the output should be a Status or an Event
    instance. By default, it is set to 'status'.

    If 'format' is set to 'event', 'trigger', 'buttons' and 'controllers' work
    as filters, discarding events that do not meet the specified conditions.

    'trigger' specifies when to trigger an event. By default, it is set to
    'on_all', which triggers an event on any button press or release. If
    set to 'on_press', it triggers an event only on button press; if set to
    'on_release', it triggers an event only on button release.

    'buttons' and 'controllers' are lists of buttons and controllers to filter
    the events. By default, there are no filters.

    """
    global _last_status
    _last_status = _last_status or Status(len(buzz._bsets))

    if pre_clear:
        # sleep is required because devices' readers are a little slow
        time.sleep(T_WAIT_PRE_CLEAR)
        while not _stack.empty():
            bset_id, raw = _stack.get()
            _last_status = _last_status.new(bset_id, raw)

    # set up
    data = []
    n_statuses = n or 1
    tstart = time.time()

    # get statuses from the stack
    while True:
        # check data size
        if len(data) >= n_statuses:
            break
        # check timeout
        if timeout is not None and time.time() - tstart > timeout:
            break
        # get status
        try:
            bset_id, raw = _stack.get(timeout=0.1)
        except queue.Empty:
            # check block
            if timeout is None and not block:
                break
        else:
            # format data and collect
            status = _last_status.new(bset_id, raw)
            if format == "status":
                data.append(status)
            elif format == "event":
                try:
                    event = _last_status - status
                except ValueError:
                    continue
                # filters
                if trigger == "on_press" and not event.is_press():
                    continue
                if trigger == "on_release" and not event.is_release():
                    continue
                if buttons and not any(event.is_button(btn) for btn in buttons):
                    continue
                if controllers and event.controller_id not in controllers:
                    continue
                data.append(event)
            _last_status = status

    # return
    if n is None and not data:
        return None
    return data[0] if n is None else data


def get_status(
    n: int | None = None,
    block: bool = True,
    timeout: float | None = None,
    pre_clear: bool = True,
) -> Status | list[Status] | None:
    """ "Reads 'n' subsequent statuses from all controllers

    If 'n' is None, it returns the first status captured; if it is any
    integer, returns a list of 'n' subsequent statuses.

    By default, it will block the execution until it meets the specified
    conditions. If 'block' is set to False, it will return None, or an
    incomplete list, when no more data is available without waiting. Another
    way around is to set 'timeout' to a float, which will stop the waiting
    after the specified time (in seconds). 'block' is ignored if 'timeout' is
    set.

    'pre_clear' clears the stack before starting the reading. By default, it
    is set to True. Note that, if 'block' is set to False, nothing will never
    be captured, as the function won't wait for new data to fill the stack.

    """
    return get(n=n, block=block, timeout=timeout, pre_clear=pre_clear, format="status")


def get_event(
    n: int | None = None,
    block: bool = True,
    timeout: float | None = None,
    pre_clear: bool = True,
    trigger: str = "on_all",
    buttons: list[str | Button] | None = None,
    controllers: list[int | Controller] | None = None,
) -> Event | list[Event] | None:
    """Reads 'n' subsequent events from all controllers

    If 'n' is None, it returns the first event captured; if it is any
    integer, returns a list of 'n' subsequent events.

    By default, it will block the execution until it meets the specified
    conditions. If 'block' is set to False, it will return None, or an
    incomplete list, when no more data is available without waiting. Another
    way around is to set 'timeout' to a float, which will stop the waiting
    after the specified time (in seconds). 'block' is ignored if 'timeout' is
    set.

    'pre_clear' clears the stack before starting the reading. By default, it
    is set to True. Note that, if 'block' is set to False, nothing will never
    be captured, as the function won't wait for new data to fill the stack.

    'trigger' specifies when to trigger an event. By default, it is set to
    'on_all', which triggers an event on any button press or release. If
    set to 'on_press', it triggers an event only on button press; if set to
    'on_release', it triggers an event only on button release.

    'buttons' and 'controllers' are lists of buttons and controllers to filter
    the events. By default, there are no filters.

    """
    return get(
        n=n,
        block=block,
        timeout=timeout,
        pre_clear=pre_clear,
        format="event",
        trigger=trigger,
        buttons=buttons,
        controllers=controllers,
    )


# background reader per device


def _run(bset: ControllerSet) -> None:
    """Runs the input reader

    Each device is handled by a separate thread, which reads the input data
    and stacks it in a common queue. The data then can be accessed, processed
    and filtered via the 'get' method.

    """
    bset.reopen()
    while not _stop.is_set():
        raw = bset.read(timeout=DEFAULT_QUEUE_TIMEOUT)
        if raw:
            _stack.put((bset.id, raw))


def _start() -> None:
    """Starts the input reader"""
    global _threads
    _threads = [threading.Thread(target=_run, args=(bset,), daemon=True) for bset in buzz._bsets]
    for thread in _threads:
        thread.start()
