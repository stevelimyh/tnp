from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='b1_01_john_artc',
            executable='task2',
            name='john_task1'
        ),
        Node(
            package='assessment_packages',
            executable='rotate_angle',
        ),
        Node(
            package='assessment_packages',
            executable='drive_distance',
        )
    ])