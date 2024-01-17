#!/usr/bin/env python3
import rospy
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist
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

if __name__ =='__main__':
    rospy.init_node("combine_node")
    rospy.loginfo("Node has been started")
    sub=rospy.Subscriber("/turtle1/pose",Pose,callback=pose_call)
    pub=rospy.Publisher("/turtle1/cmd_vel",Twist,queue_size=10)
    rospy.spin()