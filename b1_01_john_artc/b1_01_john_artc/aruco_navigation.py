# ===============================================
# ROS2 Basics Assessment 2025
# STUDENT INFORMATION
# Name       :
# Student ID :
# School     :
# Date       :
# ===============================================

import rclpy
import math
import numpy as np
from rclpy.node import Node
from rclpy.callback_groups import ReentrantCallbackGroup
from rclpy.executors import MultiThreadedExecutor
from assessment_interfaces.srv import RotateAngle
from geometry_msgs.msg import Twist
from ros2_aruco_interfaces.msg import ArucoMarkers

class TurtlebotNavigation(Node):
    # IMPLEMENT
    def __init__(self, name):
        super().__init__(name)

        ############ GIVEN ############
        self.tag_distance = None
        self.tag_angle = None
        self.current_marker = None
        self.rotating = False
        self.distance_threshold = 0
        self.max_linear_velocity = 0.22
        self.max_angular_velocity = 1.0
        self.scaled_linear_velocity = self.max_linear_velocity 
        self.scaled_angular_velocity = self.max_angular_velocity

        self.parallel_cb = ReentrantCallbackGroup()
        ############ GIVEN ############

        # Declare and initialise your ROS2 Publishers, Subscribers, Timers and Client here!

    # IMPLEMENT
    def send_rotate_request(self, angle, speed):
        self.rotating = True

    # IMPLEMENT
    def tag_callback(self, msg):
        if msg.marker_ids: # if an aruco tag is detected
            pass
        else: # if aruco tag is NOT detected
            pass

    # IMPLEMENT
    def drive_callback(self):
        if self.rotating: # currently turning
            self.get_logger().info("processing rotate_angle service")
            return
        
        if self.tag_distance == None or self.current_marker == None or self.tag_angle == None: # No aruco tag detected
            return

        if self.tag_distance > 0.1: # If far from aruco tag
            pass
        else: # Reaches aruco tag
            pass

    # IMPLEMENT
    def move_turtlebot(self, linear_velocity, angular_velocity):
        pass

    # provided, do not modify this function
    def rotate_response_callback(self, future):
        try:
            result = future.result()
            self.get_logger().info(f"Rotate service completed: {result}")
            self.rotating = False
        except Exception as e:
            self.get_logger().error(f"Rotate service failed: {e}")

    # provided, do not modify this function
    def get_tag_distance(self, x, y):
        return math.sqrt((x ** 2) + (y ** 2))

    # provided, do not modify this function
    def get_tag_angle(self, x, y):
        return np.arctan(y/x)

def main(args=None):
    if not rclpy.ok():
        rclpy.init(args=args)
    my_name = 'WRITE_NAME_HERE' # Replace the string with your name
    node = TurtlebotNavigation(my_name)
    executor = MultiThreadedExecutor(num_threads=3)
    executor.add_node(node)
    try:
        executor.spin()
    finally:
        executor.shutdown()
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
