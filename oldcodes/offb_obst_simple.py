#!/usr/bin/env python

# http://wiki.ros.org/mavros/CustomModes for custom modes
# MANUAL
# ACRO
# ALTCTL
# POSCTL
# OFFBOARD
# STABILIZED
# RATTITUDE
# AUTO.MISSION
# AUTO.LOITER
# disable RC failsafe, which can be done by setting NAV_RCL_ACT parameter to 0
# AUTO.RTL
# AUTO.LAND
# AUTO.RTGS
# AUTO.READY
# AUTO.TAKEOFF

import rospy
import thread
import time
import mavros
import time
import RPi.GPIO as GPIO
from geometry_msgs.msg import PoseStamped, Quaternion
from mavros_msgs.msg import State 
from mavros_msgs.srv import CommandBool, SetMode
from std_msgs.msg import String, Float64
from mavros_msgs.srv import *
from math import *
from tf.transformations import quaternion_from_euler
import os
import subprocess
import sys, termios, atexit
from select import select

def kbhit():
    dr,dw,de = select([sys.stdin], [], [], 0)
    return dr <> []

def getch():
    return sys.stdin.read(1)

mavros.set_namespace() # DEFAULT_NAMESPACE = '/mavros'

local_pos_pub = rospy.Publisher(mavros.get_topic('setpoint_position', 'local'), PoseStamped, queue_size=10)

local_pose = PoseStamped()
local_pose.pose.position.x = 0.0
local_pose.pose.position.y = 0.0	
local_pose.pose.position.z = 0.0

def local_pos_fix(topic):
	global local_pose
	local_pose.pose.position.x = topic.pose.position.x
	local_pose.pose.position.y = topic.pose.position.y
	local_pose.pose.position.z = topic.pose.position.z

def ping_update(topic):
	global obj_dist

	obj_dist = topic.data

local_pos_sub = rospy.Subscriber(mavros.get_topic('local_position', 'local'), PoseStamped, local_pos_fix)
ping_sub = rospy.Subscriber('ping_dist', Float64, ping_update)

target_pose = PoseStamped()
# target_pose.header.frame_id = "base_footprint"
# now = rospy.get_rostime()
# target_pose.header.stamp = rospy.Time.now()
target_pose.pose.position.x = 0.0
target_pose.pose.position.y = 0.0	
target_pose.pose.position.z = 0.0

xpos = 0.0
ypos = 0.0
zpos = 0.0

thread_stop_flag = True
posthread = 0
pos_mode = False

# Use board based pin numbering
GPIO.setmode(GPIO.BOARD)
pin = 11 #Board pin , GPIO 17
obj_dist = 0
obj_clear = False###############################################################################################
obst_mode = False
obs_thread = 0

def position_tracking_thread():
	global thread_stop_flag, target_pose, local_pos_pub

	rate = rospy.Rate(10)
	#while not thread_stop_flag:
	while not thread_stop_flag:
		local_pos_pub.publish(target_pose)
		rate.sleep()

def ReadDistance_and_SetFlag():

	global obj_clear, obj_dist

	if obj_dist <= 100.0: 					#Obstacle is Near
		obj_clear = False
		#print ("Obstacle detected")
	else:
		obj_clear = True  				#Obstacle is Far
		#print ("Obstacle free")

def position_control():
	print "begining position control"
	global thread_stop_flag
	global target_pose, local_pose
	global posthread, obs_thread
	global pos_mode,obj_clear
	global xpos, ypos, zpos

	thread_stop_flag = True

	target_pose.pose.position.x = float(xpos)
	target_pose.pose.position.y = float(ypos)
	target_pose.pose.position.z = float(zpos)
	# yaw_degrees = 0  # North
	# yaw = radians(yaw_degrees)
	# quaternion = quaternion_from_euler(0, 0, yaw)
	# target_pose.pose.orientation = Quaternion(*quaternion)
	target_pose.header.frame_id = "base_footprint"
	now = rospy.get_rostime()

	# Update timestamp and publish pose
	target_pose.header.stamp = rospy.Time.now()
	try:
		print "waiting for previous thread to join"
	#	posthread.join()
		time.sleep(1)
		print "thread joined, starting new thread"
		thread_stop_flag = False
		posthread = thread.start_new_thread( position_tracking_thread, ())
		#obs_thread = thread.start_new_thread( ReadDistance_and_SetFlag, ())

	except e:
		print "Error in thready thingy ",e

	print "waiting to start offboard mode"
	time.sleep(1)

	setOffboardMode()

	print "offboard mode enabled"
	print "Press enter to exit position control"

	commanded_pose = target_pose


	while pos_mode:

		ReadDistance_and_SetFlag()

		#get local pos here
		if obj_clear:
			#assign global pos to local pos
			#print "obstacle clear"
			target_pose = commanded_pose
		else:
			#put global pose to commanded pose
			#print "obstacle detected"
			target_pose = local_pose

		if kbhit():
			print "interrupted"
			if getch() == ord('q') or True:
				pos_mode = False
				target_pose = local_pose
				setALTCTLMode()

def setOffboardMode():
	rospy.wait_for_service('/mavros/set_mode')
	try:
		flightModeService = rospy.ServiceProxy('/mavros/set_mode', mavros_msgs.srv.SetMode)
		isModeChanged = flightModeService(custom_mode='OFFBOARD') #return true or false
	except rospy.ServiceException, e:
		print "service set_mode call failed: %s. OFFBOARD Mode could not be set"%e

def setStabilizedMode():
	global pos_mode
	pos_mode = False
	#thread if started, not stopped so that it will keep on publishing to avoid failsafe
	rospy.wait_for_service('/mavros/set_mode')
	try:
		flightModeService = rospy.ServiceProxy('/mavros/set_mode', mavros_msgs.srv.SetMode)
		isModeChanged = flightModeService(custom_mode='STABILIZED') #return true or false
	except rospy.ServiceException, e:
		print "service set_mode call failed: %s. STABILIZED Mode could not be set. Check that GPS is enabled"%e

def setTakeoffMode():
	rospy.wait_for_service('/mavros/cmd/takeoff')
	try:
		takeoffService = rospy.ServiceProxy('/mavros/cmd/takeoff', mavros_msgs.srv.CommandTOL) 
		takeoffService(altitude = 2, latitude = 0, longitude = 0, min_pitch = 0, yaw = 0)
	except rospy.ServiceException, e:
		print "Service takeoff call failed: %s"%e

def setALTCTLMode():
        global pos_mode
        pos_mode = False
        #thread if started, not stopped so that it will keep on publishing to avoid failsafe
        rospy.wait_for_service('/mavros/set_mode')
        try:
                flightModeService = rospy.ServiceProxy('/mavros/set_mode', mavros_msgs.srv.SetMode)
                isModeChanged = flightModeService(custom_mode='ALTCTL') #return true or false
        except rospy.ServiceException, e:
                print "service set_mode call failed: %s. ALTCTL Mode could not be set."%e

def setLandMode():
	global pos_mode
	pos_mode = False
	rospy.wait_for_service('/mavros/cmd/land')
	try:
		landService = rospy.ServiceProxy('/mavros/cmd/land', mavros_msgs.srv.CommandTOL)
		isLanding = landService(altitude = 0, latitude = 0, longitude = 0, min_pitch = 0, yaw = 0)
	except rospy.ServiceException, e:
		print "service land call failed: %s. The vehicle cannot land "%e

def setArm():
	rospy.wait_for_service('/mavros/cmd/arming')
	try:
		armService = rospy.ServiceProxy('/mavros/cmd/arming', mavros_msgs.srv.CommandBool)
		armService(True)
	except rospy.ServiceException, e:
		print "Service arm call failed: %s"%e

def setDisarm():
	rospy.wait_for_service('/mavros/cmd/arming')
	try:
		armService = rospy.ServiceProxy('/mavros/cmd/arming', mavros_msgs.srv.CommandBool)
		armService(False)
	except rospy.ServiceException, e:
		print "Service disarm call failed: %s"%e

def menu():
	print "Press"
	print "1: to set mode to OFFBOARD"
	print "2: to set mode to STABILIZE"
	print "3: to set mode to ARM the drone"
	print "4: to set mode to DISARM the drone"
	print "5: to set mode to TAKEOFF"
	print "6: to set mode to LAND"
	print "7: to set mode to Position Control"
	print "8: to set mode to Altitude Control"

def myLoop():

	global xpos, ypos, zpos
	global pos_mode, thread_stop_flag

	x='1'
	while ((not rospy.is_shutdown())):
		menu()
		x = raw_input("Enter your input: ");

		if (x=='1'):
			setOffboardMode()

		elif(x=='2'):
			print("Tx should be ON")
			pos_mode = False
			setStabilizedMode()

		elif(x=='3'):
			setArm()

		elif(x=='4'):
			setDisarm()

		elif(x=='5'):
			setTakeoffMode()
			time.sleep(2)
			setALTCTLMode()
		elif(x=='6'):
			pos_mode = False
			setLandMode()

		elif(x=='7'):
			xpos = raw_input("Enter x position ")
			ypos = raw_input("Enter y position ")
			zpos = raw_input("Enter z position ")

			pos_mode = True
			position_control()

		elif(x=='8'):
			setALTCTLMode()

		else:
			thread_stop_flag = True
			setStabilizedMode()
			print "Exiting......"
			break

if __name__ == '__main__':
	#subprocess.call("python ping_ros.py", shell=True)

	rospy.init_node('offboard_node', anonymous=True)
	# spin() simply keeps python from exiting until this node is stopped

	#Starting garbage thread
	try:
		time.sleep(1)
		thread_stop_flag = False
		posthread = thread.start_new_thread( position_tracking_thread, ())
	except e:
		print "Error in initial thready thingy ",e

	#setStabilizedMode()
	setOffboardMode()

	try:
		myLoop()

	except KeyboardInterrupt:
		thread_stop_flag = True
	#rospy.spin()
	#include local position estimation
