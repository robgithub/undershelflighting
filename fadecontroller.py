# Fade Controller
#
# Contols the fade (up or down) of the Mote Under Shelf Lighting system.
#
# Rob 2019-04-15

import sys, getopt, pickle, os, colorsys, time
from mote import Mote

config_filename = "data_fadecontroller.pickle"

# Pickle loader
def load_pickle(filename, default):
   try:
       obj = pickle.load( open( filename, "rb" ) )
   except IOError:
       obj = default 
   return obj

# Pickle saver 
def save_pickle(filename, obj):
    print(filename, obj)
    pickle.dump( obj, open( filename, "wb" ) )

# try and read config pickle
def load_config(config_filename):
   return load_pickle(config_filename, { 'colour_filename':"mote.pickle", 'brightness_filename':"data_fadecontrollerbrightness.pickle", 'increase':1.0, 'decrease':0.1, 'poll_interval':4}) 

def load_state(colour_filename, brightness_filename):
   colour = load_colour(colour_filename)
   brightness = load_brightness(brightness_filename)
   return colour, brightness

# try and read colour pickle
def load_colour(filename):
   return load_pickle(filename, [[0]*3 for i in range(4)]) 

# try and read brightness pickle
def load_brightness(filename):
   return load_pickle(filename, 1.0) 

def save_colour(colour, filename):
   # save updated colour
   print("save colour")
   save_pickle(filename, colour)

def save_brightness(brightness, filename):
   # save updated brightness
   print("save brightness")
   save_pickle(filename, brightness)
 
def ping_service(colour, brightness, config):
    print("...starting ping service  CTRL+c to quit")
    try:
        while True:
            print("ping service wakes up")
            # check queue
            is_ping = False
            if is_ping:
                colour, brightness = calculate_colour(colour, brightness, config["increase"])
            else:    
                colour, brightness = calculate_colour(colour, brightness, config["decrease"])
            save_colour(colour, config["colour_filename"])
            save_brightness(brightness, config["brightness_filename"])
            time.sleep(config["poll_interval"])

    except KeyboardInterrupt:
        print("terminating")

def calculate_colour(colour, brightness, change):
   # colour conversion
   return colour, brightness

def init_motes(colour):
   print("initialising Motes")

# Merge objects
# Where any member of obj2 is not None it overwrites the same member of obj1
def merge_objects(obj1, obj2):
    for key in obj1:
        if obj2[key]:
            obj1[key] = obj2[key]
    return obj1

def usage():
    print("Usage python fadecontroller --config-filename --colour-filename {FILENAME} --brightness-filename {FILENAME} --increase {INCREASE} --decrease {DECREASE} --poll-interval {POLL}")
    print("INCREASE and DECREASE values are between 0.0 - 1.0")
    print("{POLL} interval is in seconds and can be fractional")
    print("No parameters are mandatory")

try:
  opts, args = getopt.getopt(sys.argv[1:], 'o:c:b:i:d:p:h', ['config-filename=', 'colour-filename=', 'brightness-filename=', 'increase=', 'decrease=', 'poll-interval=', 'help'])
except getopt.GetoptError:
  usage()
  sys.exit(2)
config_from_args = { 'colour_filename':None, 'brightness_filename':None, 'increase':None, 'decrease':None, 'poll_interval':None} 
for opt, arg in opts:
  if opt in ('-h', '--help'):
    usage()
    sys.exit(2)
  elif opt in ('-c', '--config-filename'):
    config_filename = arg
  elif opt in ('-c', '--colour-filename'):
    config_from_args["colour_filename"] = arg
  elif opt in ('-b', '--brightness-filename'):
    config_from_args["brightness_filename"] = arg
  elif opt in ('-i', '--increase'):
    config_from_args["increase"] = float(arg)
  elif opt in ('-d', '--decrease'):
    config_from_args["decrease"] = float(arg)
  elif opt in ('-p', '--poll-interval'):
    config_from_args["poll_interval"] = float(arg)
  else:
    usage()
    sys.exit(2)
print(config_filename)
config = merge_objects(load_config(config_filename), config_from_args)
print(config)

save_pickle(config_filename, config)
print("Fade Controller Starting")
colour, brightness = load_state(config["colour_filename"], config["brightness_filename"])
print(colour, brightness)

init_motes(colour)

ping_service(colour, brightness, config)
