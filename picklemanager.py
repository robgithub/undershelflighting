# read and write pickles 

import sys, getopt, pickle, os, colorsys, time, copy
_debug = False

def debug(message):
    if (_debug):
        print(message)

# Pickle loader
def load_pickle(filename, default):
   try:
       obj = pickle.load( open( filename, "rb" ) )
   except IOError:
       obj = default 
   return obj

# Pickle saver 
def save_pickle(filename, obj):
    debug("SAVE {0} {1}".format(filename, obj))
    pickle.dump( obj, open( filename, "wb" ) )

def usage():
    print("Usage python picklemanager --colour-filename {FILENAME} --brightness-filename {FILENAME} --brightness --red --green --blue")

try:
  opts, args = getopt.getopt(sys.argv[1:], 'c:b:i:r:g:b:h', ['colour-filename=', 'brightness-filename=', 'brightness=', 'red=', 'green=', 'blue=', 'help'])
except getopt.GetoptError:
  usage()
  sys.exit(2)
colour_filename = None
brightness_filename = None
brightness = None
r = None
g = None
b = None
for opt, arg in opts:
  if opt in ('-h', '--help'):
    usage()
    sys.exit(2)
  elif opt in ('-c', '--colour-filename'):
    colour_filename = arg
  elif opt in ('-b', '--brightness-filename'):
    brightness_filename = arg
  elif opt in ('-i', '--brightness'):
    brightness = float(arg)
  elif opt in ('-r', '--red'):
    r = int(arg)
  elif opt in ('-g', '--green'):
    g = int(arg)
  elif opt in ('-b', '--blue'):
    b = int(arg)
  else:
    usage()
    sys.exit(2)

if brightness_filename:
    debug("brightness filename {0}".format( brightness_filename))
    debug(load_pickle(brightness_filename, None))
    if brightness != None:
        save_pickle(brightness_filename, brightness)

if colour_filename:
    debug("colour_filename {0}".format(colour_filename))
    state = load_pickle(colour_filename, None)
    original_state = copy.deepcopy(state) 
    debug(state)
    if r != None:
        state[0][0] = r 
        state[1][0] = r 
        state[2][0] = r 
        state[3][0] = r 
    if g != None:
        state[0][1] = g 
        state[1][1] = g 
        state[2][1] = g 
        state[3][1] = g 
    if b != None:
        state[0][2] = b 
        state[1][2] = b 
        state[2][2] = b 
        state[3][2] = b 
    debug("{0}, {1}".format(state, original_state))
    if state != original_state:
        save_pickle(colour_filename, state)
