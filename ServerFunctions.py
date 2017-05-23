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

def get_data(hs):
    data = dict()
    registrations = hs.get_registrations()
    listeners = hs.get_listeners()
    actions = hs.get_actions()
    
    data["registrations"]=dict()
    action_names = dict()
    for action_id in actions:
        action_names[action_id] = actions[action_id]["display_name"]

    data["listeners"]=dict()
    for listener_id, action_id in hs.get_registrations().iteritems():
        listener_display_name = listeners[listener_id]["display_name"]
        action_display_name = actions[action_id]["display_name"]
        data["listeners"][listener_id] = {\
                "listener_display_name" : listener_display_name,
                "action_id" : action_id,
                "action_display_name" : action_display_name,
                "options" : action_names,
                "chosen_option": registrations[listener_id],
                "advanced": listeners[listener_id]
            }
    data["actions"] = actions
        
    return data