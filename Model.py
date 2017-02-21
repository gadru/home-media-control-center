#!/usr/bin/python
"""Implements the external actions the system can perform."""

from Interfaces import Kodi,Lifx,Chromecast

class Model:
    def __init__(self):
        self.lifx = Lifx.Lifx()
        self.kodi = Kodi.Kodi('jesse')
        self.chromecast = Chromecast.Chromecast()
        self._light_state = None
    def lights_dark_blue(self,start):
        if start:
            self._light_state = self.lifx.get_state()
            self.lifx.set_all(250, 1, 0.07, kelvin=3000, power=True)
        else:
            self.lifx.set_state(self._light_state)
    def lights_off(self,start):
        if start:
            self._light_state = self.lifx.get_state()
            self.lifx.set_all_power(False)
        else:
            self.lifx.set_state(self._light_state)
    def lights_control(self,state):
        power = True if state else False
        self.lifx.set_all_power(power)
    def kodi_lifx_ambilight(self,state):
        enabled = True if state else False
        print "kodi_lifx_ambilight:: ",'state:',state,', enabled:',enabled
        self.kodi.addon_enable(u'script.kodi.lifx.ambilight',enabled)
    def kodi_play_pause(self):
        self.kodi.play_pause()
    def kodi_step_forward(self):
        self.kodi.step_forward()
    def kodi_step_back(self):
        self.kodi.small_step_back()
    def house_off(self):
        self.lifx.set_all_power(False)
        # Turn TV off
        if self.chromecast.is_active(self.chromecast.get_television()):
            self.kodi.navHome()
        self.chromecast.quit_all()