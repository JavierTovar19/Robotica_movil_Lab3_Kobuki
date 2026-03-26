#!/usr/bin/env python3.8


import rospy 
from geometry_msgs.msg import Twist 
from random import random 
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Pose2D 
import numpy as np

from tf.transformations import euler_from_quaternion


radio_muro=0.01
factor_muro=0.5
limites=[-0.05,0.05]
velocidad_l=0.1
velocidad_w=radio_muro*velocidad_l/factor_muro
frec=60

X=0
Y=0
Z=0

def callback(data):
    global X
    global Y
    global Z
    X = data.pose.pose.position.x
    Y = data.pose.pose.position.y
    quat = data.pose.pose.orientation
    q = [quat.x, quat.y, quat.z, quat.w]
    roll, pitch, Z = euler_from_quaternion(q)
    
def sentido(X,Y,Z):
    Z2=Z+np.pi
    if X>limites[1]-radio_muro:#MURO DERECHO
        if np.pi/2<Z2<=np.pi:
            return -velocidad_w
        elif np.pi<Z2<3*np.pi/2:
            return velocidad_w
        else:
            return 0
    elif X<limites[0]+radio_muro:#MURO IZQUIERDO
        if 3*np.pi/2<Z2<=2*np.pi:
            return -velocidad_w
        elif 0<Z2<np.pi/2:
            return velocidad_w
        else:
            return 0
    elif Y>limites[1]-radio_muro:#MURO SUPERIOR
        if 3*np.pi/2<Z2<2*np.pi:
            return velocidad_w
        elif np.pi<Z2<=3*np.pi/2:
            return -velocidad_w
        else:
            return 0
    elif Y<limites[0]+radio_muro:#MURO INFERIOR
        if 0<Z2<=np.pi/2:
            return -velocidad_w
        elif np.pi/2<Z2<np.pi:
            return velocidad_w
        else:
            return 0
    else:
        return 0


if __name__ == '__main__': 
    try:
    # Create a publisher on topic turtle1/cmd_vel, type geometry_msgs/Twist
        pub = rospy.Publisher('/mobile_base/commands/velocity', Twist, queue_size=1000) 
        rospy.init_node('pypubvel', anonymous=False) 
        sub = rospy.Subscriber("odom", Odometry, callback)
        rate = rospy.Rate(frec)
        # Similar to while(ros::ok()) 
        while not rospy.is_shutdown():
            
        # Create and populate new Twist message 
            if(X>limites[1]-radio_muro or X<limites[0]+radio_muro or Y>limites[1]-radio_muro or Y<limites[0]+radio_muro):
                vw= sentido(X,Y,Z)
                msg = Twist()
                msg.linear.x = velocidad_l
                msg.angular.z =vw
                rospy.loginfo(f'Giro:\n linear= {msg.linear.x}\n angular= {msg.angular.z}')
                rate.sleep() 
            else: 
                msg = Twist()
                msg.linear.x = velocidad_l
                msg.angular.z =0 
                rospy.loginfo(f'Avance:\n linear= {msg.linear.x}\n angular= {msg.angular.z}')
                rate.sleep() 
            rospy.loginfo(f'\nposx: {X} posy: {Y}')
                
            # Similar to ROS_INFO_STREAM macro, log information.

            # Publish the message and wait on rate.
            pub.publish(msg)
            rate.sleep()
    except rospy.ROSInterruptException:
        pass