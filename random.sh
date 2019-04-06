#/bin/sh

# sets random stick to random colour
S=$(( ( RANDOM % 4 )  + 1 )) 
python motestick.py -s $S -r $(( ( RANDOM % 255 )  + 1 )) -g $(( ( RANDOM % 255 )  + 1 )) -b $(( ( RANDOM % 255 )  + 1 )) 
#python motebrightness.py -s $S -b $(( ( RANDOM % 9 )  + 1 )) 
