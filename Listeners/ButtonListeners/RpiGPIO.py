#!/usr/bin/python

import RPi.GPIO as GPIO
import time

class RpiGPIOPushButtonListener(BaseEventListener):
    def __init__(self,func,min_time_between_presses):
        BaseEventListener.__init__(self,func,min_time_between_presses)
        self.gpio_num = gpio_num
    def _pre_listen(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.gpio_num, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    def _event_detect(self):
            return GPIO.input(self.gpio_num) == False
                

class RpiGPIOSwitchListener(BaseEventListener):
    def __init__(self,func,min_time_between_presses):
        BaseEventListener.__init__(self,func,min_time_between_presses)
        self.gpio_num = gpio_num
        self.old_state = False
    def _pre_listen(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.gpio_num, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        self.old_state = GPIO.input(self.gpio_num)
    def _event_detect(self):
            input_state = GPIO.input(self.gpio_num)
            result = input_state != self.old_state:
            self.old_state = input_state
            return result