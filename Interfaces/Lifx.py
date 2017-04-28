#!/usr/bin/python
"""A lifxlan wrapper to simplify some common actions."""

import lifxlan

class Lifx:
    """A class that allows simple control for Lifx bulbs."""
    def __init__(self,num_lights=None):
        self._no_color = [None, None, None, None]
        self._lifx = lifxlan.LifxLAN(num_lights)
        self._bulbs = self._init_bulbs()
        
    def _init_bulbs(self):
        """Build Dictionary."""
        bulbs_array = self._lifx.get_lights()
        bulbs = {}
        if bulbs_array is None:
            return bulbs, set()
        for bulb in bulbs_array:
            bulbs[bulb.get_label()] = bulb
            bulbs[bulb.get_label()] = bulb
        return bulbs

    @property
    def num_lights(self):
        return set(self._bulbs.keys())

    @property
    def num_of_lights(self):
        return len(self._bulbs)

    def get_bulb_state(self, bulb_label):
        """Get state of single bulb (Right now only supports power)"""
        bulb = self._bulbs[bulb_label]
        result = dict()
        result["power"] = bulb.get_power()!=0
        return result

    def get_state(self):
        """Get the state of all the bulbs"""
        return {"powers": self._lifx.get_power_all_lights(),
            "colors": self._lifx.get_color_all_lights()}

    def set_state(self,state):
        """ Turn all the lights to the state given, formated as lifx.get_state()"""
        if state is None:
            return
        powers = state["powers"]
        colors = state["colors"]
        for light, color in colors:
            light.set_color(color)
        for light, power in powers:
            light.set_power(power)

    def _color_decode(self, color):
        color_temp = color
        if color[0] is not None:
            color_temp[0] = color_temp[0]/360.0
        result = self._no_color
        result[0:3] = [(int((2**16-1)*i) if i is not None else None) for i in color_temp[0:3]]
        result[3] = 9000 if len(color) == 3 else color[3]
        return result

    def _translate_color(self, original_color, hue, saturation,
                         brightness, kelvin, duration, rapid):
        color = [hue, saturation, brightness, kelvin]
        decoded_color = self._color_decode(color)
        new_color = [decoded_color[i] if decoded_color[i] is not None else original_color[i]
                     for i in range(len(decoded_color))]
        duration_ms = duration*1000
        return new_color, duration_ms, rapid

    def set(self, bulb_name, hue=None, saturation=None,
            brightness=None, kelvin=None, power=None, duration=0, rapid=False):
        """Set status of a bulb.\n
        hue [0..360], saturation [0..1], kelvin [2500..9000], duration in seconds."""

        if bulb_name not in self._bulbs:
            return
        bulb = self._bulbs[bulb_name]
        color = self._translate_color(bulb.get_color(), hue, saturation,
                                      brightness, kelvin, duration, rapid)
        bulb.set_color(color[0], color[1], color[2])
        if power is not None:
            bulb.set_power(power)

    def set_multi(self, bulb_names=None, hue=None, saturation=None,
                  brightness=None, kelvin=None, power=None, duration=0, rapid=False):
        """Set status of a list of bulb.\n
        hue [0..360], saturation [0..1], kelvin [2500..9000], duration in seconds."""
        if bulb_names is None:
            bulb_names = self._bulb_names
        for bulb_name in bulb_names:
            self.set(bulb_name, hue, saturation, brightness, kelvin, power, duration, rapid)

    def set_except(self, bulb_names_exluded, hue=None, saturation=None,
                   brightness=None, kelvin=None, power="on", duration=0, rapid=False):
        """Set status of all bulbs except those in bulb_names_exluded.\n
        hue [0..360], saturation [0..1], kelvin [2500..9000], duration in seconds."""
        bulb_names_exluded_set = set(bulb_names_exluded)
        bulb_names = self._bulb_names.difference(bulb_names_exluded_set)
        self.set_multi(bulb_names, hue, saturation, brightness, kelvin, power, duration, rapid)

    def set_all(self, hue, saturation,
                brightness, kelvin=9000, power=None, duration=0, rapid=False):
        """Set status of all bulbs.\n
        hue [0..360], saturation [0..1], kelvin [2500..9000], duration in seconds."""
        if power is not None:
            self._lifx.set_power_all_lights(power)
        color = self._translate_color(self._no_color, hue, saturation,
                                      brightness, kelvin, duration, rapid)
        self._lifx.set_color_all_lights(color[0], color[1], color[2])

    def set_all_power(self, power=True):
        """Control power of all bulbs"""
        power_str = "on" if power else "off"
        if power in ["on", "off"]:
            power_str = power
        self._lifx.set_power_all_lights(power)      
        