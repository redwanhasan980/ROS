#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist

def draw_square():
    rospy.init_node('draw_square', anonymous=True)
    pub = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
    rate = rospy.Rate(0.5)  # Set the rate to 0.5 Hz

    for _ in range(4):
        # Move forward
        twist = Twist()
        twist.linear.x = 1.0
        pub.publish(twist)
        rospy.sleep(2.0)

        # Stop
        twist.linear.x = 0.0
        pub.publish(twist)
        rospy.sleep(1.0)

       
        rate.sleep()

if __name__ == '__main__':
    try:
        draw_square()
    except rospy.ROSInterruptException:
        pass
