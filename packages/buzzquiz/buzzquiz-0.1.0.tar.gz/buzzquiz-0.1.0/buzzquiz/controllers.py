# Python 3.10
# 28/08/2024
"""Controllers handlers for Buzz"""
from __future__ import annotations

from enum import Enum

import hid

from buzzquiz import buzz


class Button(str, Enum):
    """Buzzer buttons"""

    BUZZ = "buzz"
    COLORS = "colors"
    BLUE = "blue"
    ORANGE = "orange"
    GREEN = "green"
    YELLOW = "yellow"

    Z = "buzz"
    B = "blue"
    O = "orange"
    G = "green"
    Y = "yellow"

    def __str__(self) -> str:
        suffix = "\033[0m"
        prefix = ""
        if self == Button.BUZZ:
            prefix = "\033[30;41m"
        elif self == Button.BLUE:
            prefix = "\033[30;44m"
        elif self == Button.ORANGE:
            prefix = "\033[38;2;0;0;0;48;2;255;165;0m"
        elif self == Button.GREEN:
            prefix = "\033[30;42m"
        elif self == Button.YELLOW:
            prefix = "\033[30;43m"
        return f"{prefix}{self.value.upper()}{suffix}"


class Controller:
    """Buzzer controller"""

    def __init__(self, local_id: int, bset: ControllerSet) -> None:
        self.id = bset.id * 4 + local_id
        self.local_id = local_id
        self._bset = bset
        self.light = False

    # lights control

    def on(self) -> None:
        """Turns the Buzz button's light on"""
        buzz.lights.on([self.id])

    def off(self) -> None:
        """Turns the Buzz button's light off"""
        buzz.lights.off([self.id])

    def toggle(self) -> None:
        """Toggles the Buzz button's light"""
        if self.light:
            self.off()
        else:
            self.on()

    # representation

    def __str__(self) -> str:
        style_light = f"\033[30;47mon\033[0m" if self.light else f"\033[2moff\033[0m"
        return f"Controller({self.id}, bset_id={self._bset.id}, light={style_light})"


class ControllerSet:
    """Set of controllers

    Controllers set are 4-controllers groups handled via the same hid port.
    They are hidden from the user.

    Constructor requires the set's ID and the hid device's path, as bytes.

    """

    def __init__(self, id: int, device_path: bytes) -> None:
        self.id = id
        self._path = device_path
        self._device = hid.device()
        self._device.open_path(self._path)
        self._controllers = [Controller(i, self) for i in range(4)]
        self._last_written = [None] * 4

    def __del__(self) -> None:
        self._device.close()

    # interaction with device

    def reopen(self) -> None:
        """Reopens the device"""
        self._device.close()
        self._device.open_path(self._path)

    def read(self, timeout: float) -> list[int] | None:
        """Reads from the device 'timeout' seconds

        If nothing is read, returns None.

        """
        return self._device.read(64, timeout_ms=int(timeout * 1000)) or None

    def write(self) -> None:
        """Writes to the device the lights' status

        It stores the last thing written to the device, to avoid writing the
        same data again. This method is meant to be used internally.

        """
        lights = [0xFF if controller.light else 0x00 for controller in self._controllers]
        if lights == self._last_written:
            return
        self._last_written = lights
        self._device.write([0x00, 0x00, *lights, 0x00, 0x00])

    # representation

    def __str__(self) -> str:
        return f"ControllerSet({self.id})"
