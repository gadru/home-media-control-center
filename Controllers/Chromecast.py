#!/usr/bin/python
import pychromecast
class Chromecast:
    def __init__(self):
        """A pychromecast wrapper to simplify some common actions."""
        self._friendly_names = dict()
        self.groups = self.audio  = self.video  = None
        self.register_chromecasts()        
        
    def _register_types(sel,chromecast_list):
        self.groups = self.audio  = self.video  = None        
        is_type = lambda t :  lambda cc : cc.device.cast_type == t
        self.groups = tuple(filter(is_type('group'),chromecast_list))
        self.audio  = tuple(filter(is_type('audio'),chromecast_list))
        self.video  = tuple(filter(is_type('cast' ),chromecast_list))
        
    def _register_friendly_names(self,chromecast_list):
        self._friendly_names = dict()    
        for cc in chromecast_list:
            self._friendly_names[cc.device.friendly_name] = cc
            
    def register_chromecasts(self):
        """index the Cast devices on local network."""
        chromecast_list = pychromecast.get_chromecasts()
        self._register_types(chromecast_list)
        self._register_friendly_names(chromecast_list)
        
    def get_chromecast(friendly_name):
        """Return a pychromecast Chromecast object fitting the friendly name. Raises exception if not found."""
        cc = self._friendly_names.get(friendly_name)
        if cc is None:
            raise ValueError('''Cast device %s not registerd.\n 
            Run register_chromecasts(), make sure the device name is correct, and the device is connected.'''%repr(friendly_name))
        cc.wait()
        return cc
        
    def is_active(friendly_name):
        """Check if a cast app is connected."""
        cc = self.get_chromecast(friendly_name)
        return cc.media_controller.is_active
        
    def is_playing(friendly_name):
        """Check if chromecast is playing media"""
        cc = self.get_chromecast(friendly_name)
        return cc.media_controller.is_playing
        
    def is_paused(friendly_name):
        """Check if chromecast is paused"""
        cc = self.get_chromecast(friendly_name)
        return cc.media_controller.is_paused
        
    def is_backdrop(friendly_name):
        """Return if the chromecast displays the Backdrop (always False for audio)"""
        cc = self.get_chromecast(friendly_name)
        return cc.status.display_name == 'Backdrop'
    