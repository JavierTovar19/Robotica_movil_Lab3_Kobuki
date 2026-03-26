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
velocidad_w=np.pi/4#radio_muro*velocidad_l/factor_muro
frec=50

X=0
Y=0
yaw=0

def callback(data):
    global X
    global Y
    global yaw
    X = data.pose.pose.position.x
    Y = data.pose.pose.position.y
    quat = data.pose.pose.orientation
    q = [quat.x, quat.y, quat.z, quat.w]
    roll, pitch, yaw = euler_from_quaternion(q)
    yaw=yaw+np.pi
    
def sentido(X,Y,yaw):
    Z2=yaw+np.pi
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
        msg = Twist()
        # Similar to while(ros::ok()) 
        while not rospy.is_shutdown():
            angulo_act=0
            linea_act=0
            while True:
                for i in range(4):
                    while(yaw<1.5+angulo_act):
                        msg.linear.x = 0
                        msg.angular.z =velocidad_w
                        #rospy.loginfo(f'Giro:\n linear= {msg.linear.x}\n angular= {msg.angular.z}')
                        rospy.loginfo(f'Giro{angulo_act}:\nposx: {X}\n posy: {Y}\n angle: {yaw}')
                        pub.publish(msg)
                        rate.sleep()
                    if i==3:
                        angulo_act=0
                    else:
                        angulo_act=yaw
                    for i in range(500):
                        msg.linear.x = velocidad_l
                        msg.angular.z =0
                        #rospy.loginfo(f'Giro:\n linear= {msg.linear.x}\n angular= {msg.angular.z}')
                        rospy.loginfo(f'Giro:\nposx: {X}\n posy: {Y}\n angle: {yaw}')
                        pub.publish(msg)
                        rate.sleep() 


    except rospy.ROSInterruptException:
        pass