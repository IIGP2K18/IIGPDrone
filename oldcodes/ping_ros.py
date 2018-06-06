#!/usr/bin/python
import time
import RPi.GPIO as GPIO
import rospy
from std_msgs.msg import Float64


# Use board based pin numbering
GPIO.setmode(GPIO.BOARD)


def ReadDistance(pin):
   GPIO.setup(pin, GPIO.OUT)
   GPIO.output(pin, 0)

   time.sleep(0.000002)


   #send trigger signal
   GPIO.output(pin, 1)


   time.sleep(0.000005)


   GPIO.output(pin, 0)


   GPIO.setup(pin, GPIO.IN)


   while GPIO.input(pin)==0:
      starttime=time.time()


   while GPIO.input(pin)==1:
      endtime=time.time()
      
   duration=endtime-starttime
   # Distance is defined as time/2 (there and back) * speed of sound 34000 cm/s 
   distance=duration*34000/2
   return distance


if __name__ == '__main__':
    pub = rospy.Publisher('ping_dist', Float64, queue_size=10)
    rospy.init_node('ping_node', anonymous=True)
    rate = rospy.Rate(20) # 10hz
    while not rospy.is_shutdown():
        distance = ReadDistance(11)
        #rospy.loginfo(distance)
        pub.publish(distance)
        rate.sleep()
