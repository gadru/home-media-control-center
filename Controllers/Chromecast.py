#!/usr/bin/python
"""A pychromecast wrapper to simplify some common actions."""

import pychromecast

def _filter_type_list(chromecast_list, type_name):
    """Get all chromecasts with cast_type equals to type_name"""
    is_type = lambda cc: cc.device.cast_type == type_name
    return tuple(filter(is_type, chromecast_list))

class Chromecast:
    """A class that creates pychromecast.Chromecast objects.
    Allows easy access to objects and common actions on them"""
    def __init__(self):
        self._friendly_names = dict()
        self.groups = self.audio = self.video = None
        self.register_chromecasts()

    def _register_types(self, chromecast_list):
        self.groups = self.audio = self.video = None
        self.groups = _filter_type_list(chromecast_list, 'group')
        self.audio = _filter_type_list(chromecast_list, 'audio')
        self.video = _filter_type_list(chromecast_list, 'cast')

    def _register_friendly_names(self, chromecast_list):
        self._friendly_names = dict()
        for chromecast in chromecast_list:
            self._friendly_names[chromecast.device.friendly_name] = chromecast

    def register_chromecasts(self):
        """index the Cast devices on local network."""
        chromecast_list = pychromecast.get_chromecasts()
        self._register_types(chromecast_list)
        self._register_friendly_names(chromecast_list)

    def get_chromecast_from_name(self, friendly_name):
        """Return a pychromecast Chromecast object fitting the friendly name.
        Raises exception if not found."""
        chromecast_object = self._friendly_names.get(friendly_name)
        if chromecast_object is None:
            raise ValueError('''Cast device %s not registerd.\n
            Run register_chromecasts(), make sure the device name is correct, 
            and the device is connected.'''%repr(friendly_name))
        chromecast_object.wait()
        return chromecast_object

    def _get_chromecast_object(self, chromecast):
        if isinstance(chromecast, str):
            return self.get_chromecast_from_name(chromecast)
        elif isinstance(chromecast, pychromecast.Chromecast):
            return chromecast
        raise TypeError("""Chromecast input could only be a pychromecast.Chromecast
        or a friendly name string.""")

    def is_active(self, chromecast):
        """Check if a cast app is connected.
        chromecast is either friendly_name or pychromecast.Chromecast."""
        chromecast_object = self._get_chromecast_object(chromecast)
        return chromecast_object.media_controller.is_active

    def is_playing(self, chromecast):
        """Check if chromecast is playing media.
        chromecast is either friendly_name or pychromecast.Chromecast."""
        chromecast_object = self._get_chromecast_object(chromecast)
        return chromecast_object.media_controller.is_playing

    def is_paused(self, chromecast):
        """Check if chromecast is paused.
        chromecast is either friendly_name or pychromecast.Chromecast."""
        chromecast_object = self._get_chromecast_object(chromecast)
        return chromecast_object.media_controller.is_paused

    def is_backdrop(self, chromecast):
        """Return if the chromecast displays the Backdrop (always False for audio).
        chromecast is either friendly_name or pychromecast.Chromecast."""
        chromecast_object = self._get_chromecast_object(chromecast)
        return chromecast_object.status.display_name == 'Backdrop'
