def lights_dark_blue(resources,start):
    if start:
        resources.stored_data["light_state"] = resources.lifx.get_state()
        resources.interfaces["Lifx"].set_all(250, 1, 0.07, kelvin=3000, power=True)
    else:
        resources.interfaces["Lifx"].set_state(resources._light_state)
def lights_off(resources,start):
    if start:
        resources._light_state = resources.interfaces["Lifx"].get_state()
        resources.interfaces["Lifx"].set_all_power(False)
    else:
        resources.interfaces["Lifx"].set_state(resources._light_state)
def lights_control(resources,state):
    power = True if state else False
    resources.interfaces["Lifx"].set_all_power(power)
def kodi_lifx_ambilight(resources,state):
    enabled = True if state else False
    print "kodi_lifx_ambilight:: ",'state:',state,', enabled:',enabled
    resources.interfaces["Kodi"].addon_enable(u'script.kodi.lifx.ambilight',enabled)
def kodi_play_pause(resources):
    resources.interfaces["Kodi"].play_pause()
def kodi_step_forward(resources):
    resources.interfaces["Kodi"].step_forward()
def kodi_step_back(resources):
    resources.interfaces["Kodi"].small_step_back()
def house_off(resources):
    resources.interfaces["Lifx"].set_all_power(False)
    # Turn TV off
    if resources.interfaces["Chromecast"].is_active(resources.interfaces["Chromecast"].get_television()):
        resources.interfaces["Kodi"].navHome()
    resources.interfaces["Chromecast"].quit_all()
    