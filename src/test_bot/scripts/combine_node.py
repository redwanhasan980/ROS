#!/usr/bin/env python3
import rospy
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist
def pose_call(msg:Pose):
    cmd = Twist()
    if msg.x>=11 or msg.x<=0.5 or msg.y>=11 or msg.y<=0.5 :
        cmd.linear.x=0
        cmd.angular.z=1.5 
        pub.publish(cmd)
        rospy.sleep(2)
        cmd.linear.x=2
        cmd.angular.z=0 
        pub.publish(cmd)
        rospy.sleep(2)
       
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