#!/usr/bin/python
"""Listen for GPIO Button press."""

import RPi.GPIO as GPIO
from .BaseListener import BaseEventListener

class RpiGPIOPushButtonListener(BaseEventListener):
    """Listen for GPIO pulse push button."""
    def __init__(self, gpio_num, func, min_time_between_presses):
        BaseEventListener.__init__(self, func, min_time_between_presses)
        self.gpio_num = gpio_num
        self.already_pushed = False
    def _pre_listen(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.gpio_num, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    def _event_detect(self):
        currently_pushed = GPIO.input(self.gpio_num) is False
        triggered = currently_pushed and (not self.already_pushed)
        self.already_pushed = currently_pushed
        return triggered

class RpiGPIOSwitchListener(BaseEventListener):
    """Listen for GPIO state switch button."""
    def __init__(self, gpio_num, func, min_time_between_presses):
        BaseEventListener.__init__(self, func, min_time_between_presses)
        self.gpio_num = gpio_num
        self.old_state = False
    def _pre_listen(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.gpio_num, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        self.old_state = GPIO.input(self.gpio_num)
    def _event_detect(self):
        input_state = GPIO.input(self.gpio_num)
        result = input_state != self.old_state
        self.old_state = input_state
        return result
