#!/usr/bin/python
"""Implements the external actions the system can perform."""
import collections
import Interfaces

class Action:
    def __init__(self,resources,func,id,description,):
        self.id = str(id)
        self.description = str(description)
        self.func = func
    def __call__(self, *args, **kwargs):
        self.func(*args, **kwargs)

class Resources:
    def __init__(self):
        self.interfaces = dict()
        self.interfaces["Lifx"] = Interfaces.Lifx.Lifx()
        self.interfaces["Kodi"] = Interfaces.Kodi.Kodi('jesse')
        self.interfaces["Chromecast"] = Interfaces.Chromecast.Chromecast()
        self.stored_data = collections.defaultdict(dict)
        self.listeners = dict()
        self.available_actions =  dict()
        self.listeners_actions = dict()

    def do_action(self,listener_id,*args,**kwargs):
        """Performs the action registered to the listener, passes *args,**kwargs as arguments."""
        action_id = self.listeners_actions[listener_id]
        action = self.available_actions[action_id]
        action(*args,**kwargs)

    def register_action(self,listener_id,action_id):
        """Set a given action to be triggered by event from given listener."""
        if action_id in self.available_actions:
            self.listeners_actions[listener_id] = action_id

    def add_action(self, func, id, description="",listener_id=None):
        """Add a new action to be available. Add listener_id to also register it."""
        # TODO: verify id is unique. 
        action = Action(func, id, description)
        self.available_actions[id] = action
        if listener_id is not None:
            self.register_action(listener_id,action.id)
    
    def add_listener(self,listener_object):
        #TODO: consider creating the listener inside this function.
        self.listeners[listener_object.id] = listener_object

    def listeners_start_all(self):
        """Start all listeners."""
        for l in self.listeners.values():
            l.listen()

    def listeners_stop_all(self_all_listeners):
        """Start all listeners."""
        for l in self.listeners.values():
            l.stop()