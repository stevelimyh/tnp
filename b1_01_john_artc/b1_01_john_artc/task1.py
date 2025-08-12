# ===============================================
# ROS2 Basics Assessment 2025
# STUDENT INFORMATION
# Name       : John Arman Abogado
# Student ID : 1234567890
# School     : Advanced Remanufacturing Technology Centre
# Date       : 17 September 2025
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

        self.cmd_vel_publisher = self.create_publisher(Twist, 'cmd_vel', 10)
        self.aruco_sub = self.create_subscription(PoseArray, 'aruco_poses', self.aruco_poses_callback, 10)

    def aruco_poses_callback(self, msg):
        
        distance = get_tag_distance(msg.poses[0].position.z, msg.poses[0].position.x)
        theta = get_tag_angle(msg.poses[0].position.z, msg.poses[0].position.x)

        self.get_logger().info(f"Aruco Position - d: {distance:.3f}, theta: {theta:.3f}")

        self.scaled_linear_velocity  = self.__max_linear_velocity * (1 - (self.__distance_threshold/distance))

        self.scaled_angular_velocity = self.__max_angular_velocity * (-theta)

        self.move_turtlebot(self.scaled_linear_velocity, self.scaled_angular_velocity)

    def move_turtlebot(self, linear_velocity, angular_velocity):
        twist = Twist()
        twist.linear.x = linear_velocity
        twist.angular.z = angular_velocity
        self.cmd_vel_publisher.publish(twist)

def main(args=None):
    if not rclpy.ok():
        rclpy.init(args=args)
    my_name = 'b1_01_john_artc_task1'
    my_node = Turtlebot3Aruco(my_name)
    rclpy.spin(my_node)
    my_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
