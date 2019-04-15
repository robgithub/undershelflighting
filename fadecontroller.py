# Fade Controller
#
# Contols the fade (up or down) of the Mote Under Shelf Lighting system.
#
# Rob 2019-04-15

import sys, getopt, pickle, os, colorsys
from mote import Mote

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

def usage():
    print("Usage python fadecontroller --config-filename --colour-filename {FILENAME} --brightness-filename {FILENAME} --increase {INCREASE} --decrease {DECREASE} --poll-interval {POLL}")
    print("INCREASE and DECREASE values are between 0.0 - 1.0")
    print("{POLL} interval is in seconds")
    print("No parameters are mandatory")

try:
  opts, args = getopt.getopt(sys.argv[1:], 'o:c:b:i:d:p:h', ['config-filename=', 'colour-filename=', 'brightness-filename=', 'increase=', 'decrease=', 'poll-interval=', 'help'])
except getopt.GetoptError:
  usage()
  sys.exit(2)
config = { 'colour_filename':"mote.pickle", 'brightness_filename':"data_fadecontrollerbrightness.pickle", 'increase':1.0, 'decrease':0.1, 'poll_interval':10} 
for opt, arg in opts:
  if opt in ('-h', '--help'):
    usage()
    sys.exit(2)
  elif opt in ('-c', '--config-filename'):
    config_filename = arg
  elif opt in ('-c', '--colour-filename'):
    config["colour_filename"] = arg
  elif opt in ('-b', '--brightness-filename'):
    config["brightness_filename"] = arg
  elif opt in ('-i', '--increase'):
    config["increase"] = arg
  elif opt in ('-d', '--decrease'):
    config["decrease"] = arg
  elif opt in ('-p', '--poll-interval'):
    config["poll_interval"] = arg
  else:
    usage()
    sys.exit(2)
print(config_filename)
print(config)
sys.exit(0)

print("Fade Controller Starting")
config = load_config(config_filename)
colour, brightness = load_state(config["colour_filename"], config["brightness_filename"])
init_motes(colour)
print("...starting ping service")
ping_service(colour, brightness, config)
print("terminating")
