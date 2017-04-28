#!/usr/bin/python
"""Implements the external actions the system can perform."""
import collections
import Interfaces
import Listeners
import time
import sys

class Action:
    def __init__(self, resources=None, func_text=None, id=None):
        """Create an action. if one of the inputs is None, creates null action"""
        self.resources = resources
        if None not in (resources, func_text, id):
            self.func_text = func_text
            self.id = id
        else: #Null action
            self.func_text ="""def execute(*args,**kwargs):\n\t"Does nothing."\n\tprint 'no action'"""
            self.id = "null_action"
        exec(self.func_text)
        self.func = execute
        self.doc = str(execute.__doc__)
        
        
    def __call__(self, *args, **kwargs):
        self.func(self.resources, *args, **kwargs)

class RegistrationHandler:
    def __init__(self):
        self.listener_id_to_action_id = dict() # Choose what function the listeners activates.
        self.null_action_id = Action().id
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
        return self.listener_id_to_action_id[listener_id]
    
    def get_data(self):
        return self.listener_id_to_action_id.copy()

class ListenersHandler:
    def __init__(self, resources, registration):
        self.resources = resources
        self.registration = registration
        self.listeners = dict() # Objects that inherit from BaseListener class.
        
    def add(self,listener_id,listener_data):
        """Add a new listener object. If it already exists, replace it."""
        saved_params = listener_data.copy()
        sent_params = listener_data.copy()
        classname = sent_params.pop("classname")
        listener_class = Listeners.classes[classname]
        listener_object = listener_class(self.resources,listener_id,saved_params,**sent_params)
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

        self._add_default() 

    def _add_obj(self,action):
        self.available_actions[action.id] = action

    def _add_default(self):
        """Add a default action to all listeners."""
        null_action = Action()
        self._add_obj(null_action)
        
    def add(self, func_text, data):
        """Add a new action to be available. Add listener_id to also register it."""
        action = Action(self.resources, func_text, data)
        self._add_obj(action)
        
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
            print("Failed to find action_id: %s"%action_id)
        except:
            print "Unexpected error:", sys.exc_info()[0]
            
        action(*args,**kwargs)

    def get_data(self):
        return self.available_actions.copy()

class Resources:
    def __init__(self):
        # Interfaces
        self.interfaces = dict()
        print time.strftime("%H:%M:%S"), "Interface - Lifx"
        self.interfaces["Lifx"] = Interfaces.Lifx.Lifx()
        print time.strftime("%H:%M:%S"), "Interface - Kodi"
        self.interfaces["Kodi"] = Interfaces.Kodi.Kodi('jesse')
        print time.strftime("%H:%M:%S"), "Interface - Chromecast"
        self.interfaces["Chromecast"] = Interfaces.Chromecast.Chromecast()
        # Data store
        print time.strftime("%H:%M:%S"), "stored_data"
        self.stored_data = collections.defaultdict(dict) # Data and states for actions.
        print time.strftime("%H:%M:%S"), "registration"
        self.registration = RegistrationHandler()
        print time.strftime("%H:%M:%S"), "actions"
        self.actions = ActionsHandler(self, self.registration)
        print time.strftime("%H:%M:%S"), "listeners"
        self.listeners = ListenersHandler(self,self.registration)
