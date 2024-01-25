#!/usr/bin/env python3
import rospy
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist
from turtlesim.srv import SetPen
prev_x=0
def call_set_pin(r,g,b,width,off):
    try:
        set=rospy.ServiceProxy("/turtle1/set_pen",SetPen)
        response=set(r,g,b,width,off)

    
    except rospy.ServiceException as e:
        rospy.logwarn(e)

def pose_call(msg:Pose):
    cmd = Twist()
    if msg.x>=10 or msg.x<=1 or msg.y>=10 or msg.y<=1 :
        cmd.linear.x=3
        cmd.angular.z=4
        
       
    else:
        cmd.angular.z=0
        cmd.linear.x=2
    
    #rospy.loginfo("(" + str(msg.x)+","+str(msg.y)+")")
    pub.publish(cmd)
    global prev_x
    if msg.x>=5.5 and prev_x<5.5:
        call_set_pin(200,0,0,3,0)
    elif msg.x<5.5 and prev_x>=5.5:
        call_set_pin(0,200,0,3,0)
    prev_x = msg.x


if __name__ =='__main__':
    rospy.init_node("combine_node")
    rospy.wait_for_service("/turtle1/set_pen")
    
    sub=rospy.Subscriber("/turtle1/pose",Pose,callback=pose_call)
    pub=rospy.Publisher("/turtle1/cmd_vel",Twist,queue_size=10)
    rospy.loginfo("Node has been started")
    rospy.spin()