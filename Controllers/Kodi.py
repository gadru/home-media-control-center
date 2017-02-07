#!/usr/bin/python
from xbmcjson import XBMC, PLAYER_VIDEO
import socket
import struct
import sys

class Kodi():
    def __init__(self,hostname,mac_address=None,user='xbmc',password='xbmc'):
        self.hostname  = hostname.upper()
        self.mac = mac_address
        self._username = user
        self._password = password
        self.connected = False
        self.kodi = None
        self.Connect()
        
    def ping(self):
        return self.kodi.JSONRPC.Ping()['result']=='pong'

    def isUp(self):
        try:
            res = self.ping()
        except:
            res = False
        self.connected = res
        return res

    def Connect(self):
        address = "http://%s/jsonrpc"%self.hostname 
        self.kodi = XBMC(address,self._username,self._password)
        return self.isUpFast()

    def wakeUp(self):
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

    def toggleSuspend(self):
        if self.isUpFast():
            self.suspend()
            return "off"
        else:
            self.wakeUp()
            return "on"

    def reboot(self):
        if self.connected:
            self.kodi.System.Reboot()

    def playPause(self):
        if self.connected:
            self.kodi.Player.PlayPause([PLAYER_VIDEO])

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
    
    def navLeft(self):
        self.kodi.Input.Left()
    
    def navRight(self):
        self.kodi.Input.Right()
    
    def navUp(self):
        self.kodi.Input.Up()
    
    def navDown(self):
        self.kodi.Input.Up()
    
    def navDown(self):
        self.kodi.Input.Up()
    
    def navBack(self):
        self.kodi.Input.Back()
    
    def navSelect(self):
        self.kodi.Input.Select()                
    
    def navContextMenu(self):
        self.kodi.Input.ContextMenu()
    
    def navInfo(self):
        self.kodi.Input.Info()
    
    def navHome(self):
        self.kodi.Input.Home()
    
    def addon_enable(self,addonid,enable=True):
        data = {"addonid":addonid,'enabled':enable}
        self.kodi.Addons.SetAddonEnabled(data)
    
    def addon_disable(self,addonid):
        self.addon_enable(addonid,False)
    
    def volume_set(self,volume_normalized):
        if not ((type(volume_normalized)=float)and(0<=volume_normalized<=1)):
            raise ValueError("Must be a number between 0 and 1")
        level_percent = round(100*volume_normalized)
        self.kodi.Application.SetVolume({'volume':level_percent})
        