import json
import os

class ConfigHandler:
    def __init__(self,cfg_dir,cfg_filename,save_as_list=False,list_key="id"):
        self.save_as_list = save_as_list
        self.cfg_dir = cfg_dir
        self.cfg_filename = cfg_filename
        self.cfg_path = os.path.join(cfg_dir,cfg_filename)
        self.list_key = list_key
    def _load_from_list(self,data_list):
        result = dict()
        for list_item in data_list:
            dict_value = list_item.copy()
            dict_key = dict_value.pop(self.list_key)
            result[dict_key] = dict_value
        return result 

    def _dump_to_list(self,data):
        result = []
        for dict_key, dict_value in data.iteritems():
            list_item = dict_value.copy()
            list_item[self.list_key] = dict_key
            result.append(list_item)
        return result
        
    def read(self):
        with open(self.cfg_path,'r') as f:
            data = json.load(f)
        if self.save_as_list:
            return self._load_from_list(data)
        return data

    def write(self,data):
        output = data        
        if self.save_as_list:
            output = self._dump_to_list(data)    
        with open(self.cfg_path,'w') as f:
            json.dump(output,f)

class SaveToDisk:
    def __init__(self,cfg_dir,resources):
        self.resources = resources
        self.cfg_listeners = ConfigHandler(cfg_dir,"listeners.json",save_as_list=True)
        self.cfg_registration = ConfigHandler(cfg_dir,"registration.json")
        self.cfg_actions = ConfigHandler(cfg_dir,"actions.json")
        
    def _add_listeneres(self):
        listeners_dict = self.cfg_listeners.read()
        for listener_id,listener_data in listeners_dict.iteritems():
            self.resources.listener_add(listener_id,listener_data)

    def _add_actions(self):
        actions_dict = self.cfg_actions.read()
        actions_dir = actions_dict["dir"]
        file_extension = actions_dict["file_extension"]
        for root, dirs, files in os.walk(actions_dir):
            for name in files:
                os.path.join(root, name)
                if name.lower().endswith(file_extension):
                    path = os.path.join(root, name)
                    action_id = name[:-len(file_extension)]
                    action_display_name = action_id.replace("_"," ")
                    with open(path,'r') as f:
                        action_text = f.read()
                    self.resources.action_add(action_text, action_id, action_display_name)

    def _register_actions(self):
        reg_dict = self.cfg_registration.read()
        for listener_id, action_id in reg_dict.iteritems():
            self.resources.register(listener_id,action_id)

    def load_config(self):
        """Read saved data and fill the resources object with it."""
        self._add_listeneres()
        self._add_actions()
        self._register_actions()

    def save_config(self):
        """Save the current config to file."""
        r = self.resources
        self.cfg_listeners.write(r.listeners.get_data())
        self.cfg_registration.write(r.registration.get_data())
