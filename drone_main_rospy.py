import time
#from functions import *

tkoffalt = 3.0
leglen = 3.0
stdelay = 5

print "Please arm drone from the RC"

for i in range(stdelay):
	print "Beginning in ",stdelay-i," seconds"
	time.sleep(1)

print "Starting the mission"

print "Taking off"
takeoff(tkoffalt)
time.sleep(1)

print "On Leg 1"
setpoint_local_position(leglen,leglen,0,0,tolerance=0.5,relative=True)
time.sleep(1)

print "On Leg 2"
setpoint_local_position(leglen,-leglen,0,0,tolerance=0.5,relative=True)
time.sleep(1)

print "On Leg 3"
setpoint_local_position(-leglen,-leglen,0,0,tolerance=0.5,relative=True)
time.sleep(1)

print "On Leg 4"
setpoint_local_position(-leglen,leglen,0,0,tolerance=0.5,relative=True)
time.sleep(1)

print "Landing"
land()

print "Disarming"
disarm()
