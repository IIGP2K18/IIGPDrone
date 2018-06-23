import time
from functions import *

while True:
	
	print ""
	print "****************"
	print "1. Takeoff"
	print "2. Setpoint hold"
	print "3. Hold position (risky)"
	print "4. Land"
	print "5. Disarm"
	print "6. Exit"
	print "****************"
	print ""

	choice = raw_input("Your selection: ")

	if (choice == '1'):
		takeoff(3.0)

	elif (choice == '2'):
		set_x = input("Enter relative setpoint x: ")
		set_y = input("Enter relative setpoint y: ")
		set_z = input("Enter relative setpoint z: ")
		set_yaw = input("Enter relative setpoint yaw: ")
		
		setpoint_local_position(set_x, set_y, set_z, set_yaw, tolerance=1.0, relative=True)

	elif (choice == '3'):
		position_hold()

	elif (choice == '4'):
		land()

	elif (choice == '5'):
		disarm()

	elif (choice == '6'):
		exit()

	else:
		print "Invalid choice"
