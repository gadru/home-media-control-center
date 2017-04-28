from pprint import pprint

def set_registrations(hs,data):
    print("data recieved:")
    print("~~~~~~~~~~~")    
    pprint(data)
    print("~~~~~~~~~~~")
    #for listener_id, action_id in data:
    for listener_id, action_id in hs.resources.registration.get_data().iteritems():
        if data.has_key(listener_id):
            new_action_id = data[listener_id]
            hs.resources.registration.register(listener_id, new_action_id)
        else:
            hs.resources.registration.unregister(listener_id)
            
def registration_schema(resources):
    """Get the json schema to create form for registration."""
    registrations = resources.registration.get_data()
    listeners_data = resources.listeners.get_data()
    available_actions = resources.actions.get_data()
    actions_ids = available_actions.keys()
    available_actions_names = [action_obj.doc for action_obj in available_actions.values()]
    properties = dict()
    for listener_id, listener_obj in listeners_data.iteritems():
        display_name = listener_obj.params["display_name"]
        '''properties[listener_id] = { "title": display_name,
                                    "type": "string",
                                    "enum": actions_ids,
                                    "enum_titles": available_actions_names,
                                    "default": registrations[listener_id]
                                  }'''
        properties[listener_id] = { "title": display_name,
                                    "type": "string",
                                    "enum": actions_ids,
                                    "enum_titles": available_actions_names,
                                    "default": registrations[listener_id]
                                  }

    result= {"schema": {"type": "object",
                    "title": "Regitrations",
                    "properties": properties}}
    pprint(result)                    
    return result
