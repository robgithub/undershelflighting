# Fade Controller
#
# Contols the fade (up or down) of the Mote Under Shelf Lighting system.
#
# Rob 2019-04-15

import sys, getopt, pickle, os, colorsys, socket 
import copy
from mote import Mote

_config_filename = "data_fadecontroller.pickle"

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

def save_brightness(brightness, filename):
   # save updated brightness
   print("save brightness")
   save_pickle(filename, brightness)
 
def ping_service(mote, colour, brightness, config):
    print("...starting ping service  CTRL+c to quit")
    colour_original = copy.deepcopy(colour)
    try:
        s = socket.socket(socket.AF_INET,socket.SOCK_RAW,socket.IPPROTO_ICMP)
        s.setsockopt(socket.SOL_IP, socket.IP_HDRINCL, 1)
        s.settimeout(config["poll_interval"])
    except socket.error as err:
        print (err)
        print ("run with sudo")
        sys.exit(2)
    try:
        while True:
            print("ping service wakes up")
            # check queue
            is_ping = False
            try:
                data, addr = s.recvfrom(1508)
                print ("Packet from", addr)
                is_ping = True
            except socket.timeout:
                print ("timeout")
            current_brightness = brightness
            # reload state to make sure it has not changed externally
            colour_original, brightness = load_state(config["colour_filename"], config["brightness_filename"])
            if is_ping:
                colour, brightness = calculate_colour_from_change(colour_original, brightness, config["increase"])
            else:    
                colour, brightness = calculate_colour_from_change(colour_original, brightness, 0.0-config["decrease"])
            if brightness != current_brightness:
                save_brightness(brightness, config["brightness_filename"])
                set_mote_sticks(mote, colour)

    except KeyboardInterrupt:
        print("terminating")

def calculate_colour_from_change(colour_original, brightness, change):
    colour = copy.deepcopy(colour_original)
    #print("current brightness",brightness)
    brightness = brightness + change
    if brightness <0:
        brightness = 0
    if brightness > 1.0:
        brightness = 1.0
    #print("new brightness",brightness)
    # just first stick at the moment
    h,s,v = colorsys.rgb_to_hsv(colour[0][0], colour[0][1], colour[0][2])
    colour[0][0], colour[0][1], colour[0][2] = rgb_to_decimal(colorsys.hsv_to_rgb(h, s, brightness))
    return colour, brightness

def rgb_to_decimal(in_queue):
    out_queue = []
    for i in range(3):
        if in_queue[i] <= 0:
            out_queue.append(0.0)
        else:
            out_queue.append(255 * in_queue[i]) 
    return int(out_queue[0]), int(out_queue[1]), int(out_queue[2]) 

def set_mote_sticks(mote, colour):
    print("set mote to colour", colour)
    for st in range(1,4+1):
        setpixels(st,colour[0][0],colour[0][1],colour[0][2],mote)
    mote.show()

# set all the pixels to single colour for a given stick 
def setpixels(s, r, g, b, m):
    for p in range(16):
        m.set_pixel(s, p, r, g, b)

def init_motes(colour, brightness):
    print("initialising Motes")
    #set
    mote = Mote() # new instance of the Mote class, will do all the USB init
    for m in range(1,4+1):
        mote.configure_channel(m, 16, False) # configure for use the Mote sticks
    #calculate colour for brightness
    # just first stick at the moment
    h,s,v = colorsys.rgb_to_hsv(colour[0][0], colour[0][1], colour[0][2])
    colour_new = [[0]*3 for i in range(4)]
    colour_new[0][0], colour_new[0][1], colour_new[0][2] = rgb_to_decimal(colorsys.hsv_to_rgb(h, s, brightness))
    set_mote_sticks(mote, colour_new)
    return mote

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
    print("Once running ping ICMP messages will be accepted as INCREASE triggers")

def main():
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
  config = merge_objects(load_config(_config_filename), config_from_args)
  #print(config)

  save_pickle(_config_filename, config)
  print("Fade Controller Starting")
  colour, brightness = load_state(config["colour_filename"], config["brightness_filename"])
  print("inital colour and brightness",colour, brightness)
  
  mote_instance = init_motes(colour, brightness)
  ping_service(mote_instance, colour, brightness, config)

main()
