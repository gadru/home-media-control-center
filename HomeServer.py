#!/usr/bin/python
"""Links the listeners to their actions."""

from __future__ import print_function
import time
print(time.strftime("%H:%M:%S"),"imports")
import Resources
from SaveToDisk import SaveToDisk
import ServerFunctions
import flask
import os

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

from pprint import pprint


class HomeServer:
    def __init__(self,config_dir):       
        self.resources = Resources.Resources()
        self.saved  = SaveToDisk(config_dir,self.resources)
        self.saved.load_config()

    def start(self):
        self.resources.listeners.start_all()

    def stop(self):
        self.resources.listeners.stop_all()

ASSETS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Website')
print(time.strftime("%H:%M:%S"),"init flask")
app = flask.Flask(__name__, template_folder=ASSETS_DIR, static_folder=ASSETS_DIR)
print(time.strftime("%H:%M:%S"), "init functions")

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

@app.route("/registrations_data")
def get_registrations():
    result = ServerFunctions.registration_schema(hs.resources)
    return flask.jsonify(result)
 
@app.route("/registrations_submit",  methods=['POST'])
def set_registrations():
   data = flask.request.get_json()
   ServerFunctions.set_registrations(hs,data)
   return get_registrations()
 
@app.route("/registrations_save",  methods=['POST'])
def save_registrations():
    data = flask.request.get_json()
    ServerFunctions.set_registrations(hs,data)
    hs.saved.save_config()
    return get_registrations()

@app.route("/actions_data")
def get_actions():
    result = ServerFunctions.registration_schema(hs.resources)
    return flask.jsonify(result)
 
@app.route("/actions_submit",  methods=['POST'])
def set_actions():
   data = flask.request.get_json()
   ServerFunctions.set_registrations(hs,data)
   return get_registrations()
 
@app.route("/actions_save",  methods=['POST'])
def save_actions():
    data = flask.request.get_json()
    ServerFunctions.set_registrations(hs,data)
    hs.saved.save_config()
    return get_registrations()

if __name__ == '__main__': 

    print(time.strftime("%H:%M:%S"), "init HomeServer")
    hs = HomeServer('conf')
    print(time.strftime("%H:%M:%S"), "Running HomeServer")
    hs.start()
    print(time.strftime("%H:%M:%S"), "started HomeServer.")
    print(time.strftime("%H:%M:%S"), "Running flask")
    app.run(threaded=True,host="0.0.0.0",port="8080")
    try:
        while 1:
            pass
    except KeyboardInterrupt:
        #hs.stop()
        print("stopped.")
        raise KeyboardInterrupt
