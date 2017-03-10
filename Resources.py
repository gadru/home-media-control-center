#!/usr/bin/python
"""Implements the external actions the system can perform."""
import collections
import Interfaces
import Listeners

class Action:
    def __init__(self, resources, func_text, id, display_name=None):
        self.id = str(id)
        self.resources = resources
        self.func_text = func_text
        exec(func_text)
        self.func = execute
        self.display_name = display_name if display_name is not None else execute.__doc__
    def __call__(self, *args, **kwargs):
        self.func(self.resources, *args, **kwargs)
        """try:
            self.func(self.resources, *args, **kwargs)
        except:
            print "Action Failed." """

class RegistrationHandler:
    def __init__(self):
        self.listener_id_to_action_id = dict() # Choose what function the listeners activates.
        self.null_action_id = "null_action"

    def unregister(self,listener_id):
        """The listener will not invoke any action."""
        self.register(listener_id, self.null_action_id)
        
    def register(self,listener_id,action_id):
        """Set a given action to be triggered by event from given listener."""
        self.listener_id_to_action_id[listener_id] = action_id

    def add_listener(self,listener_id):
        """Add a new listener with no action"""
        self.register(listener_id, self.null_action_id)

    def remove_listener(self,listener_id):
        """Delete a listener from existance."""
        self.listener_id_to_action_id.pop(listener_id)

    def remove_action(self,action_id):
        """Disable all listeners registerd to this action"""
        for listener_id, dict_action_id in self.listener_id_to_action_id.iteritems(): 
            if dict_action_id == action_id:
                self.listener_id_to_action_id[listener_id] = self.null_action_id

    def get_action_id(self,listener_id):
        action_id = self.listener_id_to_action_id[listener_id]
        return action_id["action"]
    
    def get_data(self):
        return self.listener_id_to_action_id.copy()

class ListenersHandler:
    def __init__(self, resources, registration):
        self.resources = resources
        self.registration = registration
        self.listeners = dict() # Objects that inherit from BaseListener class.
        
    def add(self,listener_id,listener_data):
        """Add a new listener object. If it already exists, replace it."""
        listener_data_copy = listener_data.copy()
        classname = listener_data_copy.pop("classname")
        listener_class = Listeners.classes[classname]
        listener_object = listener_class(self.resources,listener_id,**listener_data_copy)
        if listener_id not in self.listeners:
            self.registration.add_listener(listener_id)
        self.listeners[listener_id] = listener_object

    def remove(self,listener_id):
        """Delete a listener"""
        self.listeners.pop(listener_id)
        self.registration.remove_listener(listener_id)

    def start(self,listener_id):
        """Start a listener by id."""
        self.listeners[listener_id].listen()

    def stop(self,listener_id):
        """Stop a listener by id."""
        self.listeners[listener_id].stop()
                
    def start_all(self):
        """Start all listeners."""
        for l in self.listeners:
            self.start(l)

    def stop_all(self):
        """Start all listeners."""
        for l in self.listeners:
            self.stop(l)

    def get_data(self):
        return self.listeners.copy()

class ActionsHandler:
    def __init__(self, resources, registration):
        self.resources = resources
        self.registration = registration
        self.available_actions =  dict() # All Actions in the system.
        # Default action.
        
        self._add_default() 

    def _add_default(self):
        """Add a default action to all listeners."""
        null_action ="""def execute(*args,**kwargs):\n\traise NotImplementedError"""
        self.add(null_action, self.registration.null_action_id, "Action not implemented")

    def add(self, func_text, id, description=None):
        """Add a new action to be available. Add listener_id to also register it."""
        action = Action(self.resources, func_text, id, description)
        self.available_actions[id] = action
        self.registration.add_listener(id)

    def remove(self,action_id):
        self.registration.remove_action(action_id)
        self.available_actions.pop(action_id)  

    def execute(self,listener_id,*args,**kwargs):
        """Performs the action registered to the listener, passes *args,**kwargs as arguments."""
        print "Triggered %s"%str(listener_id)
        try:
            action_id = self.registration.get_action_id(listener_id)
        except KeyError:
            print "Failed to find action for listener_id: %s"%listener_id
        try:
            print "action_id = ", repr(action_id)
            action = self.available_actions[action_id]
        except KeyError:
            print "Failed to find action_id: %s"%action_id
        action(*args,**kwargs)


class Resources:
    def __init__(self):
        # Interfaces
        self.interfaces = dict()
        self.interfaces["Lifx"] = Interfaces.Lifx.Lifx()
        self.interfaces["Kodi"] = Interfaces.Kodi.Kodi('jesse')
        self.interfaces["Chromecast"] = Interfaces.Chromecast.Chromecast()
        # Data store
        self.stored_data = collections.defaultdict(dict) # Data and states for actions.
        self.registration = RegistrationHandler()
        self.actions = ActionsHandler(self, self.registration)
        self.listeners = ListenersHandler(self,self.registration)
