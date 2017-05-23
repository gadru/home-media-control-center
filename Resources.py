#!/usr/bin/python
"""Implements the external actions the system can perform."""
import collections
import time
import sys
import logging 
import threading

import Interfaces
import Listeners

class Action:
    def __init__(self, resources=None, func_text=None, id=None, display_name=None):
        """Create an action. if one of the inputs is None, creates null action"""
        self.resources = resources
        if None not in (resources, func_text, id):
            self.func_text = func_text
            self.id = id
            self.display_name = display_name
        else: #Null action
            self.func_text ="""def execute(*args,**kwargs):\n\t"Does nothing."\n\tprint 'no action'"""
            self.id = "null_action"
            self.display_name = "-"
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
        
    def get_data_dict(self):
        return self.listener_id_to_action_id.copy()

class ListenersHandler:
    def __init__(self, resources, registration):
        self.resources = resources
        self.registration = registration
        self.listeners = dict() # Objects that inherit from BaseListener class.

    def __create_object(self, listener_id, listener_dict):
        params = listener_dict.copy()
        classname = params.pop("classname")
        display_name = params.pop("display_name")
        listener_class = Listeners.classes[classname]
        listener_object = listener_class(self.resources, listener_id, display_name, params, classname)
        return listener_object

    def add(self,listener_id,listener_dict):
        """Add a new listener object. If it already exists, replace it."""
        listener_object = self.__create_object(listener_id, listener_dict)
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

    def get_data_dict(self):
        result = dict()
        for listener_id, listener_obj in self.listeners.iteritems():
            data = dict()
            data["display_name"] = listener_obj.display_name
            data["params"] = listener_obj.get_params()
            data["classname"] = listener_obj.classname
            result[listener_id] = data
        return result

class ActionsHandler:
    def __init__(self, resources, registration):
        self.resources = resources
        self.registration = registration
        self.available_actions =  dict() # All Actions in the system.
        self._add_default() 
        self.log = logging.getLogger("Actions")

    def _add_obj(self,action):
        self.available_actions[action.id] = action

    def _add_default(self):
        """Add a default action to all listeners."""
        null_action = Action()
        self._add_obj(null_action)

    def add(self, func_text, action_id, display_name):
        """Add a new action to be available. Add listener_id to also register it."""
        action = Action(self.resources, func_text, action_id, display_name)
        self._add_obj(action)

    def remove(self,action_id):
        self.registration.remove_action(action_id)
        self.available_actions.pop(action_id)  

    def _run_action(self, action, *args, **kwargs):
        action(*args,**kwargs)

    def execute(self,listener_id,*args,**kwargs):
        """Performs the action registered to the listener, passes *args,**kwargs as arguments."""
        self.log.info("Triggered %s"%str(listener_id))
        try:
            action_id = self.registration.get_action_id(listener_id)
        except KeyError:
            self.log.info("Failed to find action for listener_id: %s"%str(listener_id))
            return 

        try:
            self.log.info("action_id = %s"%repr(action_id))
            action = self.available_actions[action_id]
        except KeyError:
            self.log.info("Failed to find action_id: %s"%str(action_id))
        except:
            self.log.info("Unexpected error: %s" %str(sys.exc_info()[0]))

        self.log.info("Running action: %s"%str(action_id))
        self._run_action(action,*args,**kwargs)
        self.log.info("Done action %s"%str(action_id))

    def get_data(self):
        return self.available_actions.copy()

    def get_data_dict(self):
        result = dict()
        
        for action_id, action_obj in self.available_actions.iteritems():
            data = dict()
            data["display_name"] = action_obj.display_name
            data["func_text"] = action_obj.func_text
            result[action_id] = data.copy()
        return result

class Resources:
    def __init__(self):
        self.log = logging.getLogger("Resources")
        # Interfaces
        self.interfaces = dict()
        self.log.info("Interface - Lifx")
        self.interfaces["Lifx"] = Interfaces.Lifx.Lifx()
        self.log.info("Interface - Kodi")
        self.interfaces["Kodi"] = Interfaces.Kodi.Kodi('jesse')
        self.log.info("Interface - Chromecast")
        self.interfaces["Chromecast"] = Interfaces.Chromecast.Chromecast()
        # Data store
        self.log.info("stored_data")
        self.stored_data = collections.defaultdict(dict) # Data and states for actions.
        self.log.info("registration")
        self.registration = RegistrationHandler()
        self.log.info("actions")
        self.actions = ActionsHandler(self, self.registration)
        self.log.info("listeners")
        self.listeners = ListenersHandler(self,self.registration)
        self.lock = threading.Lock()
    def register(self,listener_id,action_id):
        with self.lock:
            self.registration.register(listener_id,action_id)

    def unregister(self,listener_id):
        with self.lock:
            self.registration.unregister(listener_id)

    def get_registrations(self):
        with self.lock:
            return self.registration.get_data()

    def listener_add(self,listener_id,listener_dict):
        with self.lock:
            self.listeners.add(listener_id,listener_dict)

    def listener_remove(self,listener_id):
        with self.lock:
            self.listeners.add(listener_id)

    def get_listeners(self):
        with self.lock:
            return self.listeners.get_data_dict()

    def action_add(self, func_text, action_id, display_name):
        with self.lock:
            self.actions.add(func_text, action_id, display_name)

    def action_remove(self, action_id): 
        with self.lock:
            self.actions.remove(action_id)

    def action_execute(self, *args,**kwargs):
        with self.lock:
            self.actions.execute(*args,**kwargs)

    def get_actions(self):
        with self.lock:
            return self.actions.get_data_dict()