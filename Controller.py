#!/usr/bin/python
"""Links the listeners to their actions."""

from __future__ import print_function
import Resources
import Listeners
import os
import json

def add_actions(resources):
    for root, dirs, files in os.walk("Actions"):
        for name in files:
            os.path.join(root, name)
            if name.lower().endswith('.action'):
                path = os.path.join(root, name)
                action_name = name[:-len('.action')]
                with open(path,'r') as f:
                    action_text = f.read()
                    resources.add_action(action_text,action_name)

def register_actions(resources, actions_dict):
    for listener_id in actions_dict:
        resources.register_action(listener_id,actions_dict[listener_id])

def add_listeneres(resources,listeners_list):
    for listener_tuple in listeners_list:
        listener_class = Listeners.classes[listener_tuple[0]]
        params = listener_tuple[1:]
        listener = listener_class(resources,*params)
        resources.add_listener(listener)

if __name__ == '__main__':
    d = {"registration":    {   "sRED": "kodi_play_pause"    ,
                                "bRED": "house_off"          ,
                                "trbo": "kodi_step_back"     ,
                                "rset": "kodi_step_forward"  ,
                                "miSW": "kodi_lifx_ambilight",
                                "edSW": "lifx_power"         ,
                                "uTRI": "lifx_off"           ,
                                "dTRI": "lifx_darkblue"      
                            },
        "listeners":    { "sRED" : {"classname": "RpiGPIOPushButtonListener", "displayname":"Small red button" , "gpio_num" : 19},
                          "bRED" : {"classname": "RpiGPIOPushButtonListener", "displayname":"Big red button"   , "gpio_num" : 06},
                          "trbo" : {"classname": "RpiGPIOPushButtonListener", "displayname":"Turbo button"     , "gpio_num" : 26},
                          "rset" : {"classname": "RpiGPIOPushButtonListener", "displayname":"Reset button"     , "gpio_num" : 12},
                          "miSW" : {"classname": "RpiGPIOSwitchListener"    , "displayname":"Middle switch"    , "gpio_num" : 20},
                          "edSW" : {"classname": "RpiGPIOSwitchListener"    , "displayname":"Edge switch"      , "gpio_num" : 21},
                          "uTRI" : {"classname": "RpiGPIOSwitchListener"    , "displayname":"TriState up"      , "gpio_num" : 13},
                          "dTRI" : {"classname": "RpiGPIOSwitchListener"    , "displayname":"TriState down"    , "gpio_num" : 16}
                        }
        }
    with open("config.json",'w') as f:
        json.dump(d,f)
    print("starting...")
    resources = Resources.Resources()
    add_listeneres(resources,listeners)
    add_actions(resources)
    register_actions(resources, registration)
    resources.listeners_start_all()

    from pprint import pprint
    pprint(resources.available_actions)
    pprint(resources.listener_id_to_action_id)

    print("started.")
    try:
        while 1:
            pass
    except KeyboardInterrupt:
        resources.listeners_stop_all()
        print("stopped.")