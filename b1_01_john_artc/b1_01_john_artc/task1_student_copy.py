# ===============================================
# ROS2 Basics Assessment 2025
# STUDENT INFORMATION
# Name       :
# Student ID :
# School     :
# Date       :
# ===============================================

import rclpy
import numpy as np
from rclpy.node import Node
from geometry_msgs.msg import Twist
from geometry_msgs.msg import PoseArray

def get_tag_distance(z, x):
    return np.sqrt((z ** 2) + (x ** 2))

def get_tag_angle(z, x):
    return np.arctan(x/z)

class Turtlebot3Aruco(Node):

    def __init__(self, name):
        super().__init__(name)

        self.__max_linear_velocity = 0.4
        self.__max_angular_velocity = 0.2
        self.__distance_threshold = 0.5
        self.scaled_linear_velocity = self.__max_linear_velocity 
        self.scaled_angular_velocity = self.__max_angular_velocity

        # ------------------------ #
        # IMPLEMENT YOUR CODE HERE #
        # ------------------------ #
        #
        # 1.) Create a publisher that publish Twist to topic '/cmd_vel'
        # 2.) Create a subscriber that listens to topic '/aruco_poses and expect PoseArray'
        #     Use the aruco_poses_callback as its callback function
        

    def aruco_poses_callback(self, msg):
        
        # ------------------------ #
        # IMPLEMENT YOUR CODE HERE #
        # ------------------------ #
        # 3.) Implement 
        pass

    def move_turtlebot(self, linear_velocity, angular_velocity):
        # ------------------------ #
        # IMPLEMENT YOUR CODE HERE #
        # ------------------------ #
        
        # 4.) Create a Twist Message, assign the following velocity values and publish it to /cmd_vel
        pass

def main(args=None):
    if not rclpy.ok():
        rclpy.init(args=args)
    my_name = 'WRITE_YOUR_NAME_HERE'
    my_node = Turtlebot3Aruco(my_name)
    rclpy.spin(my_node)
    my_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
