#!/usr/bin/env python
# coding: utf-8

import sys
import rospy
import math

from arm_move_pkg.srv import *

# from x,y transform servo's num & angle

def usadge():
    return "%s [num angle]" %sys.argv[0]

def arm_move_client(num,angle,motion):
    rospy.wait_for_service('arm_move')
    try:
        arm_move = rospy.ServiceProxy('arm_move',Servo)
        resp1 = arm_move(num, angle ,motion)
        return resp1.result
    except rospy.ServiceException, e:
        print "Service call failed: %s"%e

#callback
def handle_arm_pose(req):
#	print "Requesting pose.x=%f pose.y=%f motion=%s" %(req.x, req.y, req.motion)
	motion = req.motion
##########################################################
###		E S P E C I A R Y   M O T I O N
##########################################################
	if motion == "open":
		#hand open
		num = 9
		angle = 200

		if arm_move_client(num, angle,motion)==1:
			print "service process clear"
		else:
			print "service process out"
			sys.exit(1)
	elif motion == "free":

	# Move to Fast Position
		num = 9
		angle = 200
		motion = "catch"

		if arm_move_client(num, angle,motion)==1:
			print "service process clear"
		else:
			print "service process out"
			sys.exit(1)

		num = 7
		angle = 900
		motion = "catch"

		if arm_move_client(num, angle,motion)==1:
			print "service process clear"
		else:
			print "service process out"
			sys.exit(1)

		num = 53
		angle = -900
		motion = "catch"

		if arm_move_client(num, angle,motion)==1:
			print "service process clear"
		else:
			print "service process out"
			sys.exit(1)

	# END Moving Fast position

	# All Servo motor changed free mode
		num = 999
		angle = 999
		motion = "free"

		if arm_move_client(num, angle,motion)==1:
			print "service process clear"
		else:
			print "service process out"
			sys.exit(1)


##########################################################
###		N O M A L  C A T C H M O D E
##########################################################
	x = req.x
	y = req.y
	length = math.pow( x*x+y*y ,0.5)

	if length < 350:
		print "too near from fast joint"
		sys.exit(1)

	if length > 530:
		print "too far from fast joint"
		sys.exit(1)
	
	l1 =390			#fast link length
	l2 =50			#second link length

	theta1=0
	theta2=0

	if motion == "catch":
		if y > 0:		
			theta1 += math.atan2(y,x-l2)*180/math.pi
			theta2 += -1*theta1
		else:
			y=y*-1
			theta1 += math.atan2(y,x-l2)*-1*180/math.pi+10
			theta2 += -1*theta1
		
		num = 53
		angle = theta1*10

		#check return 
		if arm_move_client(num, angle,motion)==1:
			print "service process clear"
		else:
			print "service process out"
			sys.exit(1)

		num = 7
		angle = theta2*10

		if arm_move_client(num, angle,motion)==1:
			print "service process clear"
		else:
			print "service process out"	
			sys.exit(1)

	#hand close
		num = 9
		angle = -200

		if arm_move_client(num, angle,motion)==1:
			print "service process clear"
		else:
			print "service process out"
			sys.exit(1)

def arm_move_server():
    rospy.init_node('arm_pose_server')
    s = rospy.Service('arm_pose', ArmPose, handle_arm_pose)
    print 'Ready to arm_pose'
    rospy.spin()	


if __name__ == "__main__":
	arm_move_server()