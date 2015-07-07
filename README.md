#Summury
The script is handling Kenseiko_mini.

#script
##arm_move_client.py
This script is debug script.
This script send data to ArmPose.srv.

##arm_move_service.py
This scrpt is executable program about servo activation.
From ArmPose.srv, this script get data about servo num, angle.

Since getting the data, this script send data to servo.

##arm_move_tf.py
This script is transform coordinates.

y
|
xtion
|
|
servo1_________________servo2_____________________x
|

From ArmPose.srv, the script get coordinates of point.
Since getting the point, the script change coordinates.

↓library
##rsc_u485.py
##servo_test.py

#SERVICE
##ArmPose.srv
float64 x
float64 y
string motion

int8 result

##Servo.srv
int16 num
int16 angle
string motion

int16 result
