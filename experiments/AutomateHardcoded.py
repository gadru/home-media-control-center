from __future__ import print_function

from Listeners.RpiGPIO import RpiGPIOPushButtonListener,RpiGPIOSwitchListener
from Controllers.Lifx import Lifx
import time

def printer(name):
    result = lambda state=True: print(name,state)
    return result
    
def main():
    buttons = dict()
    buttons["sRED"] = RpiGPIOPushButtonListener(19, printer("sRED"), 0.4)
    buttons["lRED"] = RpiGPIOPushButtonListener( 6, printer("lRED"), 0.4)
    buttons["trbo"] = RpiGPIOPushButtonListener(26, printer("trbo"), 0.4)
    buttons["rset"] = RpiGPIOPushButtonListener(12, printer("rset"), 0.4)
    buttons["miSW"] = RpiGPIOSwitchListener    (20, printer("miSW"), 0.4)
    buttons["edSW"] = RpiGPIOSwitchListener    (21, printer("edSW"), 0.4)
    buttons["uTRI"] = RpiGPIOSwitchListener    (13, printer("uTRI"), 0.4)
    buttons["dTRI"] = RpiGPIOSwitchListener    (16, printer("dTRI"), 0.4)
    
    for b in buttons:
        print("stating",b)
        buttons[b].listen()
    print("started.")
    try:
        while 1:
            pass
    except KeyboardInterrupt:
        for b in buttons:
            print("stoping",b)
            buttons[b].stop()
            
if __name__ == '__main__':
    main()