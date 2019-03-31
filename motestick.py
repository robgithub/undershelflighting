#!/usr/bin/env python

# Mote Stick
# sets a single Mote stick to a set colour
#
# Rob on Earth 2019-04-01

import sys, getopt
from mote import Mote

def setstick(s,r,g,b):
    mote = Mote()
    for m in range(1,4+1):
        print(m)
        mote.configure_channel(m, 16, False)
    for p in range(16):
        mote.set_pixel(s, p, r, g, b)
    mote.show()

def usage():
    print("Usage python motestick -s {STICK} -r {RED} -g {GREEN} -b {BLUE}")
    print("Stick values are 1-4")
    print("Colour values are in the 0-255 range ")
    print("no parameters will clear stick 1")
    print("no colours parameters will clear stick")

try:
  opts, args = getopt.getopt(sys.argv[1:], 's:r:g:b:h', ['stick=', 'red=', 'green=', 'blue=', 'help'])
except getopt.GetoptError:
  usage()
  sys.exit(2)
stick=1
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
