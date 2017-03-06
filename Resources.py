#!/usr/bin/python
"""Implements the external actions the system can perform."""
import collections
import Interfaces

class Action:
    def __init__(self, resources, func_text, id, description):
        self.id = str(id)
        self.resources = resources
        self.func_text = func_text
        exec(func_text)
        self.func = execute
        self.description = description if description is not None else execute.__doc__
    def __call__(self, *args, **kwargs):
        try:
            self.func(self.resources, *args, **kwargs)
        except:
            print "Action Failed."

class Resources:
    def __init__(self):
        self.interfaces = dict()
        self.interfaces["Lifx"] = Interfaces.Lifx.Lifx()
        self.interfaces["Kodi"] = Interfaces.Kodi.Kodi('jesse')
        self.interfaces["Chromecast"] = Interfaces.Chromecast.Chromecast()
        self.stored_data = collections.defaultdict(dict) # Data and states for actions.
        self.listeners = dict() # Objects that inherit from BaseListener class.
        self.available_actions =  dict() # All Actions in the system.
        self.listener_id_to_action_id = dict() # Choose what function the listeners activates.
        self._add_action_default() 
        
    def _add_action_default(self):
        """Add a default action to all listeners."""
        not_implemented ="""def execute(*args,**kwargs):\n\traise NotImplementedError"""
        self.add_action(not_implemented, "not_implemented_action", "Action not implemented")

    def register_action(self,listener_id,action_id):
        """Set a given action to be triggered by event from given listener."""
        print "requests to add action %s to listener %s"%(action_id,listener_id)
        if action_id in self.available_actions:
            self.listener_id_to_action_id[listener_id] = action_id
        
    def add_listener(self,listener_object):
        """Add a new listener object"""
        #TODO: consider creating the listener inside this function.
        self.listeners[listener_object.id] = listener_object
        self.register_action(listener_object.id, "not_implemented_action")

    def add_action(self, func_text, id, description=None,listener_id=None):
        """Add a new action to be available. Add listener_id to also register it."""
        # TODO: verify id is unique. 
        print "added action: %s"%str(id)
        action = Action(self, func_text, id, description)
        self.available_actions[id] = action
        if listener_id is not None:
            self.register_action(listener_id,action.id)

    def listeners_start_all(self):
        """Start all listeners."""
        for l in self.listeners.values():
            l.listen()

    def listeners_stop_all(self):
        """Start all listeners."""
        for l in self.listeners.values():
            l.stop()

    def do_action(self,listener_id,*args,**kwargs):
        """Performs the action registered to the listener, passes *args,**kwargs as arguments."""
        print "Triggered %s"%str(listener_id)
        try:
            action_id = self.listener_id_to_action_id[listener_id]
        except KeyError:
            print "Failed to find action for listener_id: %s"%listener_id
        try:
            action = self.available_actions[action_id]
        except:
            print "Failed to find action_id: %s"%action_id
        action(*args,**kwargs)