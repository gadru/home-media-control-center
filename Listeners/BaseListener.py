#!/usr/bin/python
""" Base for all listener objects."""
import time
import threading

class BaseEventListener:
    """Base class for listener object. An inheriting class should implement three functions:
    self._event_detect() -> Checks if the event happend:
                            (*) If it happened,
                                (**) If func recieves params,
                                    returns them as tuple, it'll run func(*params)
                                    (***) For one params, return (result)
                                (**) Otherwise, simply Return True
                            (*) Otherwise, the function may wait, return None, or return False.
    self._pre_listen()   -> <Optional> Start listening.
                            Runs before listening start, after listen() is called.
    self._post_listen()  -> <Optional> End listening.
                            Runs after stop() is called.
    """

    def __init__(self, func, min_time_between_hits=0, min_time_between_misses=0):
        self._func = func
        self._min_time_between_hits = min_time_between_hits
        self.min_time_between_misses = min_time_between_misses
        self._running = False
        self._thread = None

    def _listen_thread(self, func=None):
        if func is not None:
            self._func = func
        if self._func is None:
            raise ValueError('No Function given')
        self._running = True
        self._pre_listen()
        while self._running:
            event_result = self._event_detect()
            if event_result not in (False, None):
                if event_result is True:
                    self._func()
                else:
                    self._func(*event_result)
                time.sleep(self._min_time_between_hits)
            else:
                time.sleep(self.min_time_between_misses)
        self._post_listen()

    def listen(self, func=None):
        """Start listening. Run func when event happens."""
        self._thread = threading.Thread(target=self._listen_thread, args=(func, ))
        self._thread.start()

    def stop(self):
        """Stop listening."""
        self._running = False

    def _pre_listen(self):
        """Allow not implementing anything at subclass."""
        pass

    def _post_listen(self):
        """Allow not implementing anything at subclass."""
        pass

    def _event_detect(self):
        raise NotImplementedError("Subclass needs to implement _event_detect()")

if __name__ == '__main__':
    class Listener(BaseEventListener):
        """Example subclass listener"""
        def __init__(self, func, min_time_between_hits):
            BaseEventListener.__init__(self, func, min_time_between_hits)
            self.maxcnt = 3
            self.cnt = 0
        def _pre_listen(self):
            self.cnt = 0
            print("A")
        def _event_detect(self):
            self.cnt += 1
            if self.cnt == self.maxcnt:
                self.cnt = 0
                return (1, 2, 3)
            else:
                return None
        def _post_listen(self):
            self.cnt = 0
            print("B")
    def example():
        """Run example subclass."""
        example_listener = Listener(print, 1)
        example_listener.listen()
        time.sleep(3)
        example_listener.stop()
    example()
