#!/usr/bin/env python

# Mote Stick
# set mote brightness (only white)
#
# Rob on Earth 2019-04-06

import sys, getopt, pickle, os
from mote import Mote
 
picklefilename = "mote.pickle"

# set stick
def setstick(s, b, i):
    mote = Mote() # new instance of the Mote class, will do all the USB init
    state = getmotestate()
    if i!=0:
        b = getbrightness(state, s) + i
        if b<0:
            b=0
        elif b>9:
            b=9
    state = setbrightness(state, s, b, i)
    for m in range(1,4+1):
        mote.configure_channel(m, 16, False) # configure for use the Mote sticks
        setpixels(m, state[m-1][0], state[m-1][1], state[m-1][2], mote)
    mote.show()
    setmotestate(state, s, state[s-1][0], state[s-1][1], state[s-1][2])

def setbrightness(state, stick, brightness, increaseby):
    if stick>0:
        state[stick-1][0] = calcbrightness(brightness, increaseby, state[stick-1][0])  
        state[stick-1][1] = calcbrightness(brightness, increaseby, state[stick-1][1])  
        state[stick-1][2] = calcbrightness(brightness, increaseby, state[stick-1][2])  
    else:
        for s in range(4):
            state[s][0] = calcbrightness(brightness, increaseby, state[s][0])  
            state[s][1] = calcbrightness(brightness, increaseby, state[s][1])  
            state[s][2] = calcbrightness(brightness, increaseby, state[s][2])  
    return state

def getbrightness(state, stick):
    b = 0
    if stick==0:
        stick==1 
    b = calcbrightnessrating(state[stick-1][0])
    return b

def calcbrightnessrating(c):
    if c== 255:
        b=9
    elif c>= 220:
        b=8
    elif c>= 190:
        b=7
    elif c>= 160:
        b=6
    elif c>= 130:
        b=5
    elif c>= 100:
        b=4
    elif c>= 70:
        b=3
    elif c>= 40:
        b=2
    elif c>= 10:
        b=1
    else:
        b=0
    return b 


def calcbrightness(b,i,oc):
    if b== 9:
        c=255
    elif b== 8:
        c=220
    elif b== 7:
        c=190
    elif b== 6:
        c=160
    elif b== 5:
        c=130
    elif b== 4:
        c=100
    elif b== 3:
        c=70
    elif b== 2:
        c=40
    elif b== 1:
        c=10
    else:
        c=0
    return c 

# get state from pickle file or defaults
def getmotestate():
    try:
        state = pickle.load( open( picklefilename, "rb" ) )
    except IOError:
        state = [[0]*3 for i in range(4)]  # an array of four arrays of three zeros, representing r,g,b for each for stick
    return state

# update state and pickle to file
def setmotestate(state, s, r, g, b):
    pickle.dump( state, open( picklefilename, "wb" ) )

# set all the pixels to single colour for a given stick 
def setpixels(s, r, g, b, m):
    for p in range(16):
        m.set_pixel(s, p, r, g, b)

def usage():
    print("Usage python motebrightness -s {STICK} -b {BRIGHTNESS} --increase --decrease --help")
    print("Stick values are 1-4")
    print("Brightness values are in the 0-9 range ")
    print("increase and decrease override BRIGHTNESS values")
    print("if {STICK} is not supplied then brightness/increase/decrease will effect all sticks")

try:
  opts, args = getopt.getopt(sys.argv[1:], 's:b:idh', ['stick=', 'brightness=', 'increase', 'decrease', 'help'])
except getopt.GetoptError:
  usage()
  sys.exit(2)
stick=0
brightness=0
increaseby=0
for opt, arg in opts:
  if opt in ('-h', '--help'):
    usage()
    sys.exit(2)
  elif opt in ('-s', '--stick'):
    stick = arg
  elif opt in ('-b', '--brightness'):
    brightness = arg
  elif opt in ('-i', '--increase'):
    increaseby = 1
  elif opt in ('-d', '--decrease'):
    increaseby = -1
  else:
    usage()
    sys.exit(2)
setstick(int(stick), int(brightness), increaseby)
