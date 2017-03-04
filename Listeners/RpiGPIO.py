#!/usr/bin/python
"""Listen for GPIO Button press."""

import RPi.GPIO as GPIO
from Listeners.BaseListener import BaseEventListener

class RpiGPIOPushButtonListener(BaseEventListener):
    """Listen for GPIO pulse push button."""
    def __init__(self, resources, id, gpio_num, min_time_between_presses=0.4):
        BaseEventListener.__init__(self, func, min_time_between_presses)
        self.gpio_num = gpio_num
        self.already_pushed = True
    def _pre_listen(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.gpio_num, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    def _event_detect(self):
        input_state = GPIO.input(self.gpio_num)    
        is_pushed = not input_state
        trigger = is_pushed and (not self.already_pushed)
        self.already_pushed = is_pushed
        return trigger
    def _post_listen(self):
        GPIO.cleanup(self.gpio_num)

class RpiGPIOSwitchListener(BaseEventListener):
    """Listen for GPIO state switch button."""
    def __init__(self, resources, id, gpio_num, min_time_between_presses=0.4):
        BaseEventListener.__init__(self, resources, id, min_time_between_presses)
        self.gpio_num = gpio_num
        self.old_state = False
    def _pre_listen(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.gpio_num, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        self.old_state = GPIO.input(self.gpio_num)
    def _event_detect(self):
        input_state = GPIO.input(self.gpio_num)
        state_changed = input_state != self.old_state
        self.old_state = input_state
        result = False if input_state else True
        if state_changed:
            return [result]
        return False
    def _post_listen(self):
        GPIO.cleanup(self.gpio_num)