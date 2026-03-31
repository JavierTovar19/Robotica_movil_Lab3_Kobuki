#!/usr/bin/env python3.8

import rospy 
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Pose2D
import numpy as np
from tf.transformations import euler_from_quaternion

class bot:
    def __init__(self, rate=10):
        rospy.init_node('pypubvel', anonymous=False) 
        self.pose = rospy.Subscriber("/odom", Odometry, self.callback_pose)
        self.pub = rospy.Publisher("/mobile_base/commands/velocity", Twist, queue_size=10)
        self.x = 0
        self.y=0
        self.yaw=0
        self.rate=rospy.Rate(rate)
        self.distancia=0
        self.angulo_objetivo=0
        self.tolerancia=0.01
        self.kp_dist = 1.0
        self.kp_ang = 1.0

    def callback(self,data):
        self.x=data.pose.pose.position.x
        self.y=data.pose.pose.position.y
        quat = data.pose.pose.orientation
        q = [quat.x, quat.y, quat.z, quat.w]
        roll, pitch, self.yaw = euler_from_quaternion(q)
    

    def move(self,linear,angular):
        msg = Twist()
        msg.linear.x = linear
        msg.angular.z = angular
        self.pub.publish(msg)

    def goto(self, x_o, y_o, dx, dt):
        
        self.distancia = np.sqrt((x_o - self.x)**2 + (y_o - self.y)**2)
        self.angulo_objetivo = np.arctan2(y_o - self.y, x_o - self.x)
        error_ang = np.arctan2(np.sin(self.angulo_objetivo - self.yaw),
                            np.cos(self.angulo_objetivo - self.yaw))
        
        if np.abs(error_ang) < self.tolerancia and self.distancia < self.tolerancia:
            self.move(0, 0)
            return True
        
        vel_lineal = self.kp_dist * self.distancia
        if np.abs(error_ang) > self.tolerancia:
            vel_lineal = 0
        vel_lineal=np.clip(vel_lineal,0,dx)
        vel_angular = self.kp_ang * error_ang
        vel_angular = np.clip(vel_angular, -dt,dt)
        
        self.move(vel_lineal, vel_angular)
        return False


if __name__ == '__main__': 
    try:
        objetivos=[[5,5],[7,5],[7.5,7],[6,8],[4.5,7]]
        obj_act=objetivos[0]
        kobuki = bot()
        kobuki.tolerancia=0.1
        kobuki.rate= rospy.Rate(10)
        max_vel_lin=1
        max_vel_w=1
        while not rospy.is_shutdown():
            rospy.loginfo(f'Giro:\n x= {kobuki.x}\n y= {kobuki.y}\n yaw= {kobuki.yaw}')
            if kobuki.goto(obj_act[0],obj_act[1], max_vel_lin,max_vel_w):
                objetivos.pop(0)
                objetivos.append(obj_act)
                obj_act=objetivos[0]

            rospy.loginfo(f'Giro:\n angulo_actual= {kobuki.yaw}\n angulo_deseado= {kobuki.angulo_objetivo}, diferencia= {np.abs(kobuki.angulo_objetivo-kobuki.yaw)}')
            kobuki.rate.sleep()
    except rospy.ROSInterruptException:
        pass