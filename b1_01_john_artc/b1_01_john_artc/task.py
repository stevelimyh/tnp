# ===============================================
# ROS2 Basics Assessment 2025
# STUDENT INFORMATION
# Name       : John Arman Abogado
# Student ID : 1234567890
# School     : Advanced Remanufacturing Technology Centre
# Date       : 17 September 2025
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
    def __init__(self, name):
        super().__init__(name)

        # Given
        self.tag_distance = None
        self.tag_angle = None
        self.current_marker = None
        self.on_service = False
        self.distance_threshold = 0
        self.max_linear_velocity = 0.22
        self.max_angular_velocity = 1.0
        self.scaled_linear_velocity = self.max_linear_velocity 
        self.scaled_angular_velocity = self.max_angular_velocity

        self.parallel_cb = ReentrantCallbackGroup()

        # Implement
        self.cmd_vel_pub = self.create_publisher(Twist, '/cmd_vel', 10)
        self.timer = self.create_timer(0.1, self.drive_callback, callback_group=self.parallel_cb)
        self.tag_callback = self.create_subscription(ArucoMarkers, '/aruco_markers', self.tag_callback, 10, callback_group=self.parallel_cb)
        self.rotate_client = self.create_client(RotateAngle, '/rotate_angle', callback_group=self.parallel_cb)

    # Implement
    def send_rotate_request(self, angle, speed):
        self.on_service = True
        request = RotateAngle.Request()
        request.angle = angle
        request.max_rotation_speed = speed
        future =  self.rotate_client.call_async(request)
        future.add_done_callback(self.rotate_response_callback)


    def tag_callback(self, msg):
        # self.get_logger().info(f"tag_callback")
        if msg.marker_ids:
            self.current_marker = msg.marker_ids[0]
            self.tag_distance = self.get_tag_distance(msg.poses[0].position.z, msg.poses[0].position.x)
            self.tag_angle = self.get_tag_angle(msg.poses[0].position.z, msg.poses[0].position.x)
        else:
            self.tag_distance = None
            self.current_marker = None
            self.tag_angle = None

    def drive_callback(self):
        if self.on_service: # currently turning
            self.get_logger().info("processing rotate_angle service")
            return

        # Implement Here
        if not self.tag_distance or self.current_marker == None or not self.tag_angle: # No aruco tag detected
            return

        self.get_logger().info(f"tag_distance: {self.tag_distance}")
        if self.tag_distance > 0.1: # If far from aruco tag
            self.scaled_linear_velocity  = self.max_linear_velocity * (1 - (self.distance_threshold/self.tag_distance))
            self.scaled_angular_velocity = self.max_angular_velocity * (-self.tag_angle)
            self.move_turtlebot(self.scaled_linear_velocity, self.scaled_angular_velocity)
        else: # Reaches aruco tag
            self.cmd_vel_pub.publish(Twist())
            if self.current_marker == 1:
                self.get_logger().info("sending left request")
                self.send_rotate_request(1.57, 0.7)
                self.cmd_vel_pub.publish(Twist())
            if self.current_marker == 2:
                self.get_logger().info("sending right request")
                self.send_rotate_request(-1.57, 0.7)
                self.cmd_vel_pub.publish(Twist())
            if self.current_marker == 0:
                self.get_logger().info("Navigation Task Finished!")
                self.cmd_vel_pub.publish(Twist())

    # IMPLEMENT
    def move_turtlebot(self, linear_velocity, angular_velocity):
        twist = Twist()
        twist.linear.x = linear_velocity
        twist.angular.z = angular_velocity
        self.cmd_vel_pub.publish(twist)

    # given
    def rotate_response_callback(self, future):
        try:
            result = future.result()
            self.get_logger().info(f"Rotate service completed: {result}")
            self.on_service = False
        except Exception as e:
            self.get_logger().error(f"Rotate service failed: {e}")

    # given
    def get_tag_distance(self, x, y):
        return math.sqrt((x ** 2) + (y ** 2))

    # given
    def get_tag_angle(self, x, y):
        return np.arctan(y/x)

def main(args=None):
    if not rclpy.ok():
        rclpy.init(args=args)
    my_name = 'b1_01_john_artc_task1'
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
