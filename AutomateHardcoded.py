from Listeners.RpiGPIO import RpiGPIOPushButtonListener,RpiGPIOSwitchListener
from Controllers.Lifx import Lifx
import time

def switch(state):
    lifx.set("Living Room",power=state)
    print "New state", state
    
def main():
    lifx = Lifx()
    switch = RpiGPIOSwitchListener(7,switch,0.4)
    switch.listen()     
    print "started."
    try:
        while 1:
            pass
    except KeyboardInterrupt:
        switch.stop()

if __name__ == '__main__':
    main()