#!/usr/bin/python
"""Links the listeners to their actions."""

from __future__ import print_function
import Resources
import Actions
from Listeners.RpiGPIO import RpiGPIOPushButtonListener,RpiGPIOSwitchListener
            
if __name__ == '__main__':
    print("starting...")
    resources = Resources.Resources()
    resources.add_listener(RpiGPIOPushButtonListener(resources, "sRED", 19))
    resources.add_listener(RpiGPIOPushButtonListener(resources, "bRED", 06))
    resources.add_listener(RpiGPIOPushButtonListener(resources, "trbo", 26))
    resources.add_listener(RpiGPIOPushButtonListener(resources, "rset", 12))
    resources.add_listener(RpiGPIOSwitchListener    (resources, "miSW", 20))
    resources.add_listener(RpiGPIOSwitchListener    (resources, "edSW", 21))
    resources.add_listener(RpiGPIOSwitchListener    (resources, "uTRI", 13))
    resources.add_listener(RpiGPIOSwitchListener    (resources, "dTRI", 16))                                  
    resources.add_action(Actions.kodi_play_pause     , "kodi_play_pause    " , "kodi_play_pause    " , "sRED" )
    resources.add_action(Actions.house_off           , "house_off          " , "house_off          " , "bRED" )
    resources.add_action(Actions.kodi_step_back      , "kodi_step_back     " , "kodi_step_back     " , "trbo" )
    resources.add_action(Actions.kodi_step_forward   , "kodi_step_forward  " , "kodi_step_forward  " , "rset" )
    resources.add_action(Actions.kodi_lifx_ambilight , "kodi_lifx_ambilight" , "kodi_lifx_ambilight" , "miSW" )
    resources.add_action(Actions.lights_control      , "lights_control     " , "lights_control     " , "edSW" )
    resources.add_action(Actions.lights_off          , "lights_off         " , "lights_off         " , "uTRI" )
    resources.add_action(Actions.lights_dark_blue    , "lights_dark_blue   " , "lights_dark_blue   " , "dTRI" )
    resources.listeners_start_all()
    print("started.")
    try:
        while 1:
            pass
    except KeyboardInterrupt:
        resources.listeners_stop_all()
        print("stopped.")