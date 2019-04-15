Under Shelf Lighting TODO

Take the existing colour setting code and combine it with an external influence.

External influence is a PIR sensor connected to another Raspberry Pi. A ping type message will be sent to the USL(Under Shelf Lighting) controller

Can I use Ping?

On recieving a Ping the USL will increase the Brightness of the Motes. To do this a concept of Brightness will have to be store separately from the colour and the LED settings extrapalated from the HSV or similar calculation.

There will obviously be a MAX brightness and a timer will lower the brightness to 0 as the lack of Pings accumilates.

The increase from Ping will be greater than the timer based decrease. Might opt for 100% increase and then 10% per minute as a decrease. Must be fully configurable.

Steps;
   server will be running listening for Pings.
   this server will have initialised the Mote sticks and set them to the current requested colour as defined in the Pickle. this is the base 100%
   server will then "tick" once an n time period and decrease the brightness percentage based on the configuration.
   if 0 brightness do nothing
   if new ping at any time increase by config setting to no more than 100% total.

Trial a pure mathematical input output sample.
[x] Basic investigation in repl - result import colorsys

