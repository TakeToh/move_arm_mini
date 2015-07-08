#!/usr/bin/env python
# coding: utf-8

#debug program 

import sys
import rospy

from arm_move_pkg.srv import *

def arm_move_client(num,angle,moiton):
    rospy.wait_for_service('arm_move')
    try:
        arm_move = rospy.ServiceProxy('arm_move',Servo)
        resp1 = arm_move(num,angle,motion)
        return resp1.result
    except rospy.ServiceException, e:
        print "Service call failed: %s"%e

def usage():
    return "%s [num angle]"%sys.argv[0]

if __name__ == "__main__":
    if len(sys.argv) == 4:
        num = int(sys.argv[1])
        angle = int(sys.argv[2])
        motion = str(sys.argv[3])
    else:
        print usage()

    print "Requesting num=%d angle=%d motion=%s" %(num, angle,motion)

    if motion == "free":
        num = 7
        angle = 900
        motion = "catch"

        if arm_move_client(num, angle,motion) == 1:
            print "service process clear"
        else:
            print "service process out"

        num = 999
        angle = 999
        motion = "free"

        if arm_move_client(num, angle,motion) == 1:
            print "service process clear"
        else:
            print "service process out"

    elif arm_move_client(num, angle,motion) == 1:
        print "service process clear"
    else:
        print "service process out"