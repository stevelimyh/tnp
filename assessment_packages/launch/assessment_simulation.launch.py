from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
import os

from ament_index_python.packages import get_package_share_directory

def generate_launch_description():

    aruco = LaunchConfiguration('aruco')
    drive = LaunchConfiguration('drive')

    tb3_gazebo_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                get_package_share_directory('turtlebot3_gazebo'),
                'launch',
                'assessment_world.launch.py'
            )
        )
    )

    aruco_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                get_package_share_directory('ros2_aruco'),
                'launch',
                'aruco_recognition.launch.py'
            )
        ),
        condition=IfCondition(aruco)
    )


    # Optional: DriveDistance node
    drive_distance_node = Node(
        package='assessment_packages',
        executable='drive_distance',
        condition=IfCondition(drive)
    )

    # Optional: RotateAngle node
    rotate_angle_node = Node(
        package='assessment_packages',
        executable='rotate_angle',
        condition=IfCondition(drive)
    )

    return LaunchDescription([

        DeclareLaunchArgument('aruco', default_value='false', description='Launch ArUco detection'),
        DeclareLaunchArgument('drive', default_value='false', description='Launch drive servers'),

        tb3_gazebo_launch,
        aruco_launch,
        drive_distance_node,
        rotate_angle_node
    ])
