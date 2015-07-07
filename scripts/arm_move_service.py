#!/usr/bin/env python
# coding: utf-8

from arm_move.srv import *
import rospy
import sys

import time
import rsc_u485


#callback arm_move
def handle_arm_move(req):
#    print "This service catched data num=%d, angle=%d motion=%s" %(req.num, req.angle, req.motion)

    servo = rsc_u485.RSC_U485('/dev/ttyUSB0',115200)

    if req.motion == "catch":

        # simultaneously two servo action
        # assumed only #5,3 servo action
        if int(req.num/10) !=0:
            print "dual servo mode start"

            num1 = int(req.num/10)          #servo num1
            num2 = int(req.num%10)          #servo num2

            servo.torque(num1, 1)           #torqe on
            servo.torque(num2, 1)

            print "move angle %d"   %req.angle

            time.sleep(2) # しばし待つ

            servo.move(num1, -req.angle,300)
            servo.move(num2, +req.angle,300)

            time.sleep(2) # しばし待つ

            print 'current angle1:%d' %servo.getAngle(num1)
            print 'current angle2:%d' %servo.getAngle(num2)

            time.sleep(2) # しばし待つ

        #single servo action
        else:
            print'ID%d Torqu on' %req.num
            
            servo.torque(int(req.num), 1)

            print "move angle %d"   %req.angle
            print 'current angle:%d' %servo.getAngle(req.num)

            time.sleep(2)

            servo.move(int(req.num), req.angle,300)
            
            time.sleep(2) # しばし待つ

            print 'current angle:%d' %servo.getAngle(req.num)
          
    elif req.motion == "free":
        for i in range(1,10):
            print "reset servo No. %d"  %i
            time.sleep(1) # しばし待つ
            servo.torque(i, 0)  
        
        print "servo free mode complete"

    print "motion end"

    return ServoResponse(1)

def arm_move_server():
    rospy.init_node('arm_move_server')
    s = rospy.Service('arm_move', Servo, handle_arm_move)
    print 'Ready to arm_move'
    rospy.spin()	

if __name__ == "__main__":
    arm_move_server()


