#!/usr/bin/python

import lifxlan

class Lifx:
    def __init__(self,):
        self.__NO_COLOR= [None,None,None,None]
        self.lifx = lifxlan.LifxLAN()
        self.bulbs,self.bulb_names = self._init_bulbs()        
        #Keep old values
        self.original_powers = self.lifx.get_power_all_lights()
        self.original_colors = self.lifx.get_color_all_lights()
         
    def _init_bulbs(self):
        #Build Dictionary
        bulbs_array = self.lifx.get_lights()
        bulbs = {}
        for bulb in bulbs_array:
            bulbs[bulb.get_label()] = bulb
        bulb_names = set(bulbs.keys())
        return bulbs,bulb_names
        
    def _color_decode(self,color):
        color_temp = color
        if color[0] is not None:
            color_temp[0] = color_temp[0]/360.0 
        result=self.__NO_COLOR
        result[0:3]= [(int((2**16-1)*i) if i is not None else None) for i in color_temp[0:3]]
        result[3] = 9000 if len(color)==3 else color[3]
        return result
   
    def __translate_color(self,original_color,hue,saturation,brightness,kelvin,duration,rapid):
        color = [hue,saturation,brightness,kelvin]
        decoded_color = self._color_decode(color)
        new_color =[decoded_color[i] if decoded_color[i] is not None else original_color[i] for i in range(len(decoded_color))]
        duration_ms = duration*1000
        return new_color,duration_ms,rapid
        
    def set(self,bulb_name,hue=None,saturation=None,brightness=None,kelvin=None,power=None,duration=0,rapid=False):
        if bulb_name not in self.bulbs:
            return 
        bulb = self.bulbs[bulb_name]
        color = self.__translate_color(bulb.get_color(),hue,saturation,brightness,kelvin,duration,rapid)
        bulb.set_color(color[0],color[1],color[2])
        if power is not None:
            bulb.set_power(power)
    
    def set_multi(self,bulb_names=None,hue=None,saturation=None,brightness=None,kelvin=None,power=None,duration=0,rapid=False):
        if bulb_names is None:
            bulb_names = self.bulb_names
        for bulb_name in bulb_names:
            self.set_state(bulb_name,hue,saturation,brightness,kelvin,power,duration,rapid)
    
    def set_except(self,bulb_names_exluded=None,hue=None,saturation=None,brightness=None,kelvin=None,power="on",duration=0,rapid=False):
        """Set status of all bulbs except those in the list.\new_color
        hue [0..360], saturation [0..1], kelvin [2500..9000], duration in seconds."""
        bulb_names = self.bulb_names
        bulb_names
    
    def set_all(self,hue,saturation,brightness,kelvin=9000,power=None,duration=0,rapid=False):
        """Set status of all bulbs.\new_color
        hue [0..360], saturation [0..1], kelvin [2500..9000], duration in seconds."""
        if power is not None:
            self.lifx.set_power_all_lights(power)
        color = self.__translate_color(self.__NO_COLOR,hue,saturation,brightness,kelvin,duration,rapid)
        self.lifx.set_color_all_lights(color[0],color[1],color[2])
    
    def set_all_power(self,power=True):
        """Control power of all bulbs"""
        if power == True:
            power="on"
        if power in ["on","off"]:
            self.lifx.set_power_all_lights(power)
    
    def restore(self):
        """ Turn all the lights to the state saved on __init__()"""
        for light, color in self.original_colors:
            light.set_color(color)
        for light, power in self.original_powers:
            light.set_power(power)
            
if __name__=='__main__':
    l = LifxInterface(["Bedroom","Kitchen","Living Room","Work Room"])
