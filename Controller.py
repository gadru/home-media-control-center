#!/usr/bin/python
"""Links the listeners to their actions."""

from __future__ import print_function
import Model
from Listeners.RpiGPIO import RpiGPIOPushButtonListener,RpiGPIOSwitchListener

class Listeners:
    def __init__(self):
        self._listeners = dict()
        self.model = Model.Model()
        self._listeners["sRED"] = RpiGPIOPushButtonListener(19, self.model.kodi_play_pause)
        self._listeners["bRED"] = RpiGPIOPushButtonListener(06, self.model.house_off)
        self._listeners["trbo"] = RpiGPIOPushButtonListener(26, self.model.kodi_step_back)
        self._listeners["rset"] = RpiGPIOPushButtonListener(12, self.model.kodi_step_forward)
        self._listeners["miSW"] = RpiGPIOSwitchListener(20, self.model.kodi_lifx_ambilight)
        self._listeners["edSW"] = RpiGPIOSwitchListener(21, self.model.lights_control)
        self._listeners["uTRI"] = RpiGPIOSwitchListener(13, self.model.lights_off)
        self._listeners["dTRI"] = RpiGPIOSwitchListener(16, self.model.lights_dark_blue)
    def listen(self):
        for l in self._listeners.values():
            l.listen()
    def stop(self):
        for l in self._listeners.values():
            l.stop()
if __name__ == '__main__':
    print("starting...")
    l = Listeners()
    l.listen()
    print("started.")
    try:
        while 1:
            pass
    except KeyboardInterrupt:
        l.stop()
        print("stopped.")