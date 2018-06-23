import time
from functions import *

tkoffalt = 3.0
leglen = 3 #length of each leg in the mission
stdelay = 5 #starting delay for mission in seconds
wprest  = 2 #rest interval after reaching each waypoint in seconds

def mission_1():
	print "***Please arm drone from the RC***"
	time.sleep(2)

	for i in range(stdelay):
		print "Beginning in ",stdelay-i," seconds"
		time.sleep(1)

	print "***Starting the mission***"

	print "Taking off"
	takeoff(tkoffalt)
	time.sleep(wprest)

	print "On Leg 1"
	setpoint_local_position(leglen,leglen,0,0,tolerance=0.5,relative=True)
	time.sleep(wprest)

	print "On Leg 2"
	setpoint_local_position(leglen,-leglen,0,0,tolerance=0.5,relative=True)
	time.sleep(wprest)

	print "On Leg 3"
	setpoint_local_position(-leglen,-leglen,0,0,tolerance=0.5,relative=True)
	time.sleep(wprest)

	print "On Leg 4"
	setpoint_local_position(-leglen,leglen,0,0,tolerance=0.5,relative=True)
	time.sleep(wprest)

	print "Landing"
	land()

	print "Disarming"
	disarm()

	print "***Mission complete***"
