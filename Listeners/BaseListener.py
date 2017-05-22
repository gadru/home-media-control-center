#!/usr/bin/python
""" Base for all listener objects."""
import time
import threading

class BaseEventListener:
    """Base class for listener object. An inheriting class should implement three functions:
    self._listen         -> <Optional> recieves a callback function and registers it.
    self._pre_listen()   -> <Optional> Runs before listening start, when listen() is called.
    self._post_listen()  -> <Optional> Runs when stop() is called.
    self._event_detect() -> <Optional> Checks if the event happend, For polling.:
                             Replaces _listen if defined
                            (*) If it happened,
                                (**) If func recieves params,
                                    returns them as tuple, it'll run func(*params)
                                    (***) For one params, return (result)
                                (**) Otherwise, simply Return True
                            (*) Otherwise, the function may wait, return None, or return False.                            
    """

    def __init__(self, resources, id, display_name, params, classname, min_time_between_hits=0, min_time_between_misses=0):
        self.classname = classname
        self.params = params
        self.id = id
        self.display_name = display_name
        self.resources = resources
        self._min_time_between_hits = min_time_between_hits
        self.min_time_between_misses = min_time_between_misses
        self._running = False
        self._thread = None
    
    def _listen_polling(self):
        self._pre_listen()
        while self._running:
            event_result = self._event_detect()
            if event_result not in (False, None):
                if event_result is True:
                    self.resources.action_execute(self.id)
                else:
                    self.resources.action_execute(self.id,*event_result)
                time.sleep(self._min_time_between_hits)
            else:
                time.sleep(self.min_time_between_misses)
        self._post_listen()

    def _listen_thread(self):
        # TODO: if self._listen is implemented, run it instead.
        self._listen_polling()

    def listen(self):
        """Start listening. Run action when event happens."""
        self._running = True
        self._thread = threading.Thread(target=self._listen_thread)
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

    def get_params(self):
        return self.params.copy()

if __name__ == '__main__':
    class Listener(BaseEventListener):
        """Example subclass listener"""
        def __init__(self, func, min_time_between_hits):
            BaseEventListener.__init__(self, func, min_time_between_hits)
            self.maxcnt = 3
            self.cnt = 0
        def _pre_listen(self):
            self.cnt = 0
        def _event_detect(self):
            self.cnt += 1
            if self.cnt == self.maxcnt:
                self.cnt = 0
                return (1, 2, 3)
            else:
                return None

        def _post_listen(self):
            self.cnt = 0

