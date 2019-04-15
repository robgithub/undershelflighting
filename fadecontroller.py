# Fade Controller
#
# Contols the fade (up or down) of the Mote Under Shelf Lighting system.
#
# Rob 2019-04-15

import colorsys

config_filename = "data_fadecontroller.pickle"

def load_config(config_filename):
   #try and read config pickle
   config = { 'colour_filename':"mote.pickle", 'brightness_filename':"data_fadecontrollerbrightness.pickle", 'increase':1.0, 'decrease':0.1} 
   return config

def load_state(colour_filename, brightness_filename):
   colour = load_colour(colour_filename)
   brightness = load_brightness(brightness_filename)
   return colour, brightness

def load_colour(filename):
   #try and read colour pickle
   colour = None
   return colour

def load_brightness(filename):
   #try and read brightness pickle
   brightness = None
   return brightness

def save_colour(colour, colour_filename):
   # save updated colour
   print("save colour")

def save_brightness(brightness, brightness_filename):
   # save updated brightness
   print("save brightness")
 
def ping_service(colour, brightness, config):
   # listen for pings
   colour = calculate_colour(colour, brightness, config["increase"])
   colour = calculate_colour(colour, brightness, config["decrease"])
   save_colour(colour, config["colour_filename"])
   save_brightness(brightness, config["brightness_filename"])

def calculate_colour(colour, brightness, change):
   # colour conversion
   return colour

def init_motes(colour):
   print("initialising Motes")

print("Fade Controller Starting")
config = load_config(config_filename)
colour, brightness = load_state(config["colour_filename"], config["brightness_filename"])
init_motes(colour)
print("...starting ping service")
ping_service(colour, brightness, config)
print("terminating")
