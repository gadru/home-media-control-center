#!/usr/bin/python
from xbmcjson import XBMC, PLAYER_VIDEO
import socket
import struct
import sys

class Kodi:
    def __init__(self,hostname,mac_address=None,user='xbmc',password='xbmc'):
        self.hostname  = hostname.upper()
        self.mac = mac_address
        self._username = user
        self._password = password
        self.connected = False
        self.kodi = None
        self.connect()
    def _get_info_booleans(self,boolean_name):
        returned = self.kodi.xbmc.GetInfoBooleans(booleans=[boolean_name])
        return returned.get('result',dict()).get(boolean_name)
    def _execute_action(self,action_name):
        returned = self.kodi.Input.ExecuteAction(action=action_name)
        result = returned.get('result')
        return result == u'OK'
    def ping(self):
        return self.kodi.JSONRPC.Ping()['result']=='pong'
    def is_up(self):
        try:
            res = self.ping()
        except:
            res = False
        self.connected = res
        return res
    def connect(self):
        address = "http://%s/jsonrpc"%self.hostname 
        self.kodi = XBMC(address,self._username,self._password)
        return self.is_up()
    def wake_up(self):
        if self.mac is None:
            return None
        macaddress = self.mac
        # Check macaddress format and try to compensate.
        if len(macaddress) == 12:
            pass
        elif len(macaddress) == 12 + 5:
            sep = macaddress[2]
            macaddress = macaddress.replace(sep, '')
        else:
            raise ValueError('Incorrect MAC address format')
        macaddress = macaddress.upper()
        # Pad the synchronization stream.
        data = ''.join(['FFFFFFFFFFFF', macaddress * 20])
        send_data = '' 

        # Split up the hex values and pack.
        for i in range(0, len(data), 2):
            send_data = ''.join([send_data,
                                 struct.pack('B', int(data[i: i + 2], 16))])
        # Broadcast it to the LAN.
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sock.sendto(send_data, ('<broadcast>', 7))
    def suspend(self):
        if self.connected:
            self.kodi.System.Suspend()
    def toggle_suspend(self):
        if self.is_up():
            self.suspend()
            return "off"
        else:
            self.wakeUp()
            return "on"
    def reboot(self):
        if self.connected:
            self.kodi.System.Reboot()
    def play_pause(self):
        if self.connected:
            self.kodi.Player.PlayPause([PLAYER_VIDEO])
    def step_forward(self):
        self._execute_action("stepforward")
    def step_back(self):
        self._execute_action("stepback")
    def big_step_forward(self):
        self._execute_action("bigstepforward")
    def big_step_back(self):
        self._execute_action("bigstepback")
    def small_step_back(self):
        self._execute_action("smallstepback")
    def stop(self):
        if self.connected:
            self.kodi.Player.Stop([PLAYER_VIDEO])
    def mute(self):
        if self.connected:
            self.kodi.Application.SetMute({"mute":True})
    def unmute(self):
        if self.connected:
            self.kodi.Application.SetMute({"mute":False})
    def notify(self,title,message):
        if self.connected:
            self.kodi.GUI.ShowNotification({"title":title, "message":message})
    def nav_left(self):
        self.kodi.Input.Left()
    def nav_right(self):
        self.kodi.Input.Right()
    def nav_up(self):
        self.kodi.Input.Up()
    def nav_down(self):
        self.kodi.Input.Up()
    def nav_down(self):
        self.kodi.Input.Up()
    def nav_back(self):
        self.kodi.Input.Back()
    def nav_select(self):
        self.kodi.Input.Select()                
    def nav_context_menu(self):
        self.kodi.Input.ContextMenu()
    def nav_info(self):
        self.kodi.Input.Info()
    def nav_home(self):
        self.kodi.Input.Home()
    def addon_enable(self,addonid,enable=True):
        data = {"addonid":addonid,'enabled':enable}
        self.kodi.Addons.SetAddonEnabled(data)
    def addon_disable(self,addonid):
        self.addon_enable(addonid,False)
    def volume_set(self,volume_normalized):
        if not ((type(volume_normalized)==float)and(0<=volume_normalized<=1)):
            raise ValueError("Must be a number between 0 and 1")
        level_percent = round(100*volume_normalized)
        self.kodi.Application.SetVolume({'volume':level_percent})
    def play_url(self,url):
        self.kodi.Player.Open(item={"file": url})
    def is_screensaver_on(self):
        return self._get_info_booleans("System.ScreenSaverActive")