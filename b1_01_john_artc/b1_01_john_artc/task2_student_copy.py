# ===============================================
# ROS2 Basics Assessment 2025
# STUDENT INFORMATION
# Name       :
# Student ID :
# School     :
# Date       :
# ===============================================

import rclpy
from rclpy.node import Node
from assessment_interfaces.srv import RotateAngle
from assessment_interfaces.srv import DriveDistance
from std_srvs.srv import Trigger

class TurtlebotNavigation(Node):
    def __init__(self, name):
        super().__init__(name)

        self.client_node = Node("client_node")
        # ------------------------ #
        # IMPLEMENT YOUR CODE HERE #
        # ------------------------ #
        #
        # 1.) Use the self.client node to create a service client to /rotate_angle service with type RotateAngle
        # 2.) Use the self.client node create a service client to /drive_distnace service with type DriveDistance
        # 3.) use TurtlebotNavigation Node to create service server with type Trigger, use self.handle_service as callback


        
    def handle_service(self, request, response):

        # check if serfvice is available
        while not self.rotate_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Waiting for /rotate_angle service...')
        while not self.drive_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Waiting for /drive_straight service...')
        
        # ------------------------ #
        # IMPLEMENT YOUR CODE HERE #
        # ------------------------ #
        #
        # 4.) Implement Logic
        # 5.) return response


    def send_rotate_request(self, angle, speed):
        # ------------------------ #
        # IMPLEMENT YOUR CODE HERE #
        # ------------------------ #
        #
        # 4.) send RotateAngle request

        pass


    def send_drive_request(self, distance, speed):
        # ------------------------ #
        # IMPLEMENT YOUR CODE HERE #
        # ------------------------ #
        #
        # 5.) send DriveDistance request 
        pass

def main(args=None):
    if not rclpy.ok():
        rclpy.init(args=args)
    my_name = 'WRITE_YOUR_NAME_HERE'
    node = TurtlebotNavigation(my_name)
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
