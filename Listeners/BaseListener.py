#!/usr/bin/python

import time
import threading

class BaseEventListener:
    def __init__(self,func,min_time_between_hits=0,min_time_between_misses=0):        
        """Base class for listener object. An inheriting class should implement three functions:
        self._event_detect() -> Checks if the event happend:
                                (*) If it happened, 
                                    (**) If func recieves params, returns them as tuple, it'll run func(*params)
                                        (***) For one params, return (result)
                                    (**) Otherwise, simply Return True
                                (*) Otherwise, the function may wait, return None, or return False.
        self._pre_listen()   -> <Optional> Start listening. Runs before listening start, after listen() is called.        
        self._post_listen()  -> <Optional> End listening. Runs after stop() is called.
        """
        
        self._func = func
        self._min_time_between_hits  = min_time_between_hits
        self.min_time_between_misses = min_time_between_misses
        self._running = False
        self._thread = None
    def _listen_thread(self,func=None):
        if func is not None:
            self._func = func
        if self._func is None:
            raise ValueError('No Function given')
        self.running = True
        self._pre_listen()
        while self.running:
            event_result = self._event_detect()
            if (event_result not in (False,None)):
                if event_result == True:
                    self._func()
                else:
                    self._func(*event_result)
                time.sleep(self._min_time_between_hits)
            else:
                time.sleep(self.min_time_between_misses)            
        self._post_listen()
    def listen(self,func=None):
        self._thread = threading.Thread(target=self._listen_thread,args=(func,))
        self._thread.start()
    def stop(self):
        self.running=False
    def _pre_listen(self):
        pass
    def _post_listen(self):
        pass

if __name__=='__main__':
    class Listener(BaseEventListener):
        def __init__(self,func,min_time_between_hits):
            BaseEventListener.__init__(self,func,min_time_between_hits)
            self.maxcnt = 3
            self.cnt = 0
        def _pre_listen(self):
            self.cnt = 0
            print("A")
        def _event_detect(self):
            self.cnt += 1
            if self.cnt == self.maxcnt:
                self.cnt = 0
                return (1,2,3)
            else:
                return None
        def _post_listen(self):
            self.cnt = 0
            print("B")
    l = Listener(print,1)
    l.listen()
    time.sleep(3)
    l.stop()