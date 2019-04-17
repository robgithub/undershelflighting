# read and write pickles 

import sys, getopt, pickle, os, colorsys, time

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
    print("brightness filename", brightness_filename)
    print(load_pickle(brightness_filename, None))
    if brightness != None:
        save_pickle(brightness_filename, brightness)

if colour_filename:
    print("colour_filename", colour_filename)
    state = load_pickle(colour_filename, None)
    original_state = state 
    print(state)
    if r != None:
        state[0][0] = r 
    if g != None:
        state[0][1] = g 
    if b != None:
        state[0][2] = b 
    if state != original_state:
        save_pickle(colour_filename, state)
