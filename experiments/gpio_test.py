import RPi.GPIO as GPIO
import time

class PrintGPIO:
    def __init__(self,pins):
        self.pins = pins
        self.setup()

    def setup(self):
        GPIO.cleanup()    
        GPIO.setmode(GPIO.BCM)
        for pin in self.pins:
            GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    def get_all(self):
        states = dict()
        for pin in self.pins:
            states[pin] = (GPIO.input(pin))
        result = '| '
        for pin in self.pins:
            result += str(self.pins[pin]) +' : '+ str(states[pin])+' | '
        return result
    def loop(self):
        state = ''
        try:
            while 1:
                new_state = self.get_all()
                if new_state != state:
                    print new_state
                    state = new_state
                # time.sleep(0.4)
        except KeyboardInterrupt:
            self.done()
    def done(self):
        GPIO.cleanup()
                
if __name__ == '__main__':
    l = [21,26,20,19,16,13,6,12,5]
    d= dict()
    for i in l:
        d[i] = str(i)
    """
    19 : "sRED"
     6 : "lRED"
    26 : "trbo"
    12 : "rset"
    20 : "miSW"
    21 : "edSW"
    13 : "uTRI"
    16 : "dTRI"
    """
    p = PrintGPIO(d)
    p.loop()
    
    
    """ Test results:
        7   Good
        11  Bad
        
    """