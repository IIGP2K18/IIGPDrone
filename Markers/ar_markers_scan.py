#!/usr/bin/env python

from __future__ import print_function


import cv2
import cv2.aruco as aruco
import numpy as np
import glob

if __name__ == '__main__':
    print('Press "q" to quit')
    capture = cv2.VideoCapture(0)
    landthresh = 30
    font = cv2.FONT_HERSHEY_SIMPLEX
    aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
    parameters = aruco.DetectorParameters_create()

    while True:
        frame_captured, frame = capture.read()
	frame = frame[:,frame.shape[1]/2:,:]
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

	immaxx = frame.shape[1]
	immaxy = frame.shape[0]
        imccx = immaxx/2
	imcry = immaxy/2

	cv2.circle(frame,(imccx,imcry), landthresh, (255,0,0), 2)

	corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)

        if np.all(ids != None):
        	aruco.drawDetectedMarkers(frame, corners) #Draw A square around the markers

		mcx = int((corners[0][0][0][0]+corners[0][0][2][0])/2)
		mcy = int((corners[0][0][0][1]+corners[0][0][2][1])/2)
		dx = mcx-imccx
		dy = mcy-imcry

		cv2.circle(frame,(mcx,mcy), 5, (0,255,0), -1)
		#print("Dx: ",dx,", Dy:",dy)
		frame = cv2.flip(frame, -1)

		if (abs(dx) < landthresh and abs(dy) < landthresh):
			#print("LAND!!")
			cv2.putText(frame,'LAND!!',(10,immaxy-20), font, 2,(0,0,255),3,cv2.LINE_AA)
		frame = cv2.flip(frame, -1)

	frame = cv2.flip(frame, -1)

        cv2.imshow('Test Frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
       	    break

    # When everything done, release the capture
    capture.release()
    cv2.destroyAllWindows()
