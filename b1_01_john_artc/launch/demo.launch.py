import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node


def generate_launch_description():

    # 1) Track simulation: gazebo server/client + robot_state_publisher +
    #    spawn_turtlebot3 + aruco_recognition (publishes /aruco_markers)
    track_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                get_package_share_directory('turtlebot3_gazebo'),
                'launch',
                'turtlebot3_track.launch.py'
            )
        )
    )

    # 2) RotateAngle service server -> provides /rotate_angle
    rotate_angle_node = Node(
        package='assessment_packages',
        executable='rotate_angle',
        output='screen'
    )

    # 3) The navigation node (the solution)
    task_node = Node(
        package='b1_01_john_artc',
        executable='task',
        output='screen'
    )

    # Give Gazebo, the ArUco detector and the service server time to come up
    # before starting the navigation node (it calls /rotate_angle without
    # waiting for the service, so starting too early can leave it stuck).
    delayed_task_node = TimerAction(period=10.0, actions=[task_node])

    return LaunchDescription([
        track_launch,
        rotate_angle_node,
        delayed_task_node,
    ])
