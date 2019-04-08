#!/usr/bin/env python

# Mote Stick
# sets a single Mote stick to a set colour
#
# Rob on Earth 2019-04-01

import sys, getopt, pickle, os
from mote import Mote
 
picklefilename = "mote.pickle"

# set stick
def setstick(s,r,g,b):
    mote = Mote() # new instance of the Mote class, will do all the USB init
    state = getmotestate()
    for m in range(1,4+1):
        mote.configure_channel(m, 16, False) # configure for use the Mote sticks
        setpixels(m, state[m-1][0], state[m-1][1], state[m-1][2], mote)
    if s==0:
        for st in range(1,4+1):
            setpixels(st,r,g,b,mote)
            setmotestate(state, st, r, g, b)
    else:
        setpixels(s,r,g,b,mote)
        setmotestate(state, s, r, g, b)
    mote.show()


# get state from pickle file or defaults
def getmotestate():
    try:
        state = pickle.load( open( picklefilename, "rb" ) )
    except IOError:
        state = [[0]*3 for i in range(4)]  # an array of four arrays of three zeros, representing r,g,b for each for stick
    return state

# update state and pickle to file
def setmotestate(state, s, r, g, b):
    state[s-1][0] = r
    state[s-1][1] = g
    state[s-1][2] = b
    pickle.dump( state, open( picklefilename, "wb" ) )

# set all the pixels to single colour for a given stick 
def setpixels(s, r, g, b, m):
    for p in range(16):
        m.set_pixel(s, p, r, g, b)

def usage():
    print("Usage python motestick -s {STICK} -r {RED} -g {GREEN} -b {BLUE}")
    print("Stick values are 1-4")
    print("Colour values are in the 0-255 range ")
    print("no parameters will clear all")
    print("no colours parameters will clear stick")

try:
  opts, args = getopt.getopt(sys.argv[1:], 's:r:g:b:h', ['stick=', 'red=', 'green=', 'blue=', 'help'])
except getopt.GetoptError:
  usage()
  sys.exit(2)
stick=0
red=0
green=0
blue=0
for opt, arg in opts:
  if opt in ('-h', '--help'):
    usage()
    sys.exit(2)
  elif opt in ('-s', '--stick'):
    stick = arg
  elif opt in ('-r', '--red'):
    red = arg
  elif opt in ('-g', '--green'):
    green = arg
  elif opt in ('-b', '--blue'):
    blue = arg
  else:
    usage()
    sys.exit(2)

setstick(int(stick), int(red), int(green), int(blue))
