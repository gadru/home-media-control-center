#!/usr/bin/python
"""Links the listeners to their actions."""

import time
import flask
import os
import logging

import Resources
from SaveToDisk import SaveToDisk
import ServerFunctions

class HomeServer:
    def __init__(self,config_dir):       
        self.resources = Resources.Resources()
        self.saved  = SaveToDisk(config_dir, self.resources)
        self.saved.load_config()

    def start(self):
        self.resources.listeners.start_all()

    def stop(self):
        self.resources.listeners.stop_all()

    def register(self,listener_id,action_id):
        self.resources.register(listener_id, action_id)

    def unregister(self,listener_id):
        self.resources.unregister(listener_id)

    def get_registrations(self):
        return self.resources.get_registrations()

    def listener_add(self,listener_id,listener_dict):
        self.resources.listener_add(listener_id, listener_dict)

    def listener_remove(self,listener_id):
        self.resources.listener_remove(listener_id)

    def get_listeners(self):
        return self.resources.get_listeners()

    def action_add(self, func_text, action_id, display_name):
        self.resources.action_add(func_text, action_id, display_name)

    def action_remove(self, action_id): 
        self.resources.action_remove(action_id)

    def get_actions(self):
        return self.resources.get_actions()

###################
### Directories ###
###################
    
#Log
logging.basicConfig(filename='home_server.log',level=logging.INFO)
global_logger = logging.getLogger('Global')
global_logger.info("=== Started running ===")
global_logger.info("pid = %d"%os.getpid())

#Globals
ASSETS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Website')
global_logger.info("init flask")
app = flask.Flask(__name__, template_folder=ASSETS_DIR, static_folder=ASSETS_DIR)
global_logger.info("init HomeServer")
hs = HomeServer('conf')
global_logger.info("init functions")

def send_dir(directory,path):
    send_dir = os.path.join("Website", directory)
    return flask.send_from_directory(send_dir, path)

@app.route('/js/<path:path>')
def send_js(path):
    return send_dir('js',path)

@app.route('/css/<path:path>')
def send_css(path):
    return send_dir('css',path)

@app.route("/")
def index():
    return flask.render_template('index.html')

#################################################################################
# registrations schema

@app.route("/registrations_submit",  methods=['POST'])
def set_registrations():
   data = flask.request.get_json()
   ServerFunctions.set_registrations(hs,data)
   return get_registrations_schema()
 
@app.route("/registrations_save",  methods=['POST'])
def save_registrations():
    data = flask.request.get_json()
    ServerFunctions.set_registrations(hs,data)
    hs.saved.save_config()
    return get_registrations_schema()

#################################################################################

# Registration

@app.route("/register",  methods=['POST'])
def register():
    listener_id = flask.request.args.get('listener_id')
    action_id = flask.request.args.get('action_id')
    hs.register(listener_id, listener_id)

@app.route("/unregister",  methods=['POST'])
def unregister(listener_id):
    listener_id = flask.request.args.get('listener_id')
    hs.unregister(listener_id)

# Listeners

@app.route("/listener_add",  methods=['POST'])
def listener_add():
    listener_data = request.args
    listener_id = listener_data.pop('listener_id')
    listener_dict = listener_data
    hs.listener_add(listener_id, listener_dict)

@app.route("/listener_remove",  methods=['POST'])
def listener_remove():
    listener_id = flask.request.args.get('listener_id')
    hs.listener_remove(listener_id)

# Actions

@app.route("/action_add",  methods=['POST'])
def action_add():
    func_text = flask.request.args.get('func_text')
    action_id = flask.request.args.get('action_id')
    hs.action_add(func_text, action_id)

@app.route("/action_remove",  methods=['POST'])
def action_remove(): 
    action_id = flask.request.args.get('action_id')
    hs.action_remove(action_id)

# Get data

@app.route("/get_data")
def get_data():
    return flask.jsonify(ServerFunctions.get_data(hs))


############
### main ###
############
    
def main():
        global_logger.info("Running HomeServer")
        hs.start()
        global_logger.info("started HomeServer.")
        global_logger.info("Running flask")
        app.config['TEMPLATES_AUTO_RELOAD'] = True
        app.run(threaded=True,host="0.0.0.0",port="8080")
        try:
            while 1:
                pass
        except KeyboardInterrupt:
            hs.stop()
            global_logger.info("stopped.")
            raise KeyboardInterrupt

if __name__ == '__main__': 
    try:
        main()
    except:
        global_logger.exception("crashed")