# Train-and-Place ROS2 Basics Evaluation 2025: AruCo-Guided Navigation

This repository contains **ROS 2 packages** developed for the **2025 ROS 2 Basics Evaluation**.  
The project focuses on assessing and demonstrating fundamental ROS 2 concepts through a practical navigation scenario.  
Using **ArUco markers** as visual cues, a turtlebot3 with camera decides whether to **turn left, turn right, or stop**.  

The evaluation is designed to assess participants' understanding of: 

- ROS 2 Package Creation
- ROS2 Nodes
- ROS2 Topic Publishers
- ROS2 Topic Subscribers
- Service Clients 
- Launch Files 

## About the Assessment Task

<p align="center">
  <img src="docs/images/sample.gif" alt="ROS2 Basics Evaluation Assessment Demonstration" style="width:100%;"/>
  <br/>
  <strong>ROS2 Basics Evaluation Assessment Demonstration: ArUco-Guided Navigation</strong>
</p>

### Core Concepts Evaluated
- **ROS 2 Nodes & Publishers**  
  - Implement a `TurtlebotNavigation` node that publishes velocity commands (`geometry_msgs/Twist`) to `/cmd_vel`.  
- **ROS 2 Subscribers**  
  - Subscribe to the `/aruco_markers` topic (`ros2_aruco_interfaces/ArucoMarkers`) to detect markers and extract position/angle.  
- **ROS 2 Services**  
  - Use a custom service (`assessment_interfaces/RotateAngle`) to rotate the robot when instructed by marker detection.  
- **Executors & Callback Groups**  
  - Manage concurrent callbacks with `MultiThreadedExecutor` and `ReentrantCallbackGroup`.  

### Navigation Logic
- When **no marker is detected**, the robot should remain idle.  
- When a marker is detected:  
  - **Marker ID 1** → Turn **left** (`+90°`)  
  - **Marker ID 2** → Turn **right** (`-90°`)  
  - **Marker ID 0** → **Stop** (navigation task finished)  
- If the marker is still **far away**, the robot should approach it, scaling linear and angular velocities based on distance and angle.  
- Upon reaching the marker, the robot should stop and execute the corresponding action.  

## Evaluation Criteria


Participants will be evaluated based on the **functionality of their ROS 2 implementation**.  
Each function corresponds to a specific behavior that the TurtleBot3 must demonstrate.

| Function | Description | Pass Condition |
|----------|-------------|----------------|
| **1. Approach and Stop at ArUco** | TurtleBot3 moves toward a detected ArUco marker and stops right in front of it. | Robot consistently stops directly in front of the marker. |
| **2. Idle (No ArUco Detected)** | When no ArUco marker is detected, TurtleBot3 shall remain stopped. | Robot does not move until a marker is detected. |
| **3. Left Turn** | On detecting marker ID `1`, TurtleBot3 stops and rotates left (~90° CCW). | Robot performs a left rotation at marker ID. |
| **4. Right Turn** | On detecting marker ID `2`, TurtleBot3 stops and rotates right (~90° CW). | Robot performs a right rotation at marker ID. |
| **5. Stop Navigation** | On detecting marker ID `0`, TurtleBot3 halts and declares navigation complete. | Robot fully stops and does not resume motion. |
| **6. Launch Integration** | Participant creates a launch file to start both the Rotate Angle server and ArUco navigation node. | A single `ros2 launch` runs both without errors; `/rotate_angle` service and navigation node work correctly. |

## Dependencies

1. Update 
```bash
sudo apt update
```
2. Install Gazebo Classic
```bash
sudo apt install ros-humble-gazebo-*
```
3. Install TF Transformations
```bash
sudo apt install ros-humble-tf-transformations
```

## Environment Configs

1. Add the following environment parameters
```bash
echo -e "\n# ROS 2 Humble\nsource /opt/ros/humble/setup.bash\n\n# Gazebo Classic\nsource /usr/share/gazebo/setup.sh\nsource /usr/share/gazebo/setup.bash\n\n# TurtleBot3\nexport TURTLEBOT3_MODEL=burger_cam" >> ~/.bashrc
```

2. Source the environment parameters
```bash
source ~/.bashrc
```

## Build

1. Go to root of workspace

```bash
colcon build
source install/setup.bash
```

## Run the Demonstration

2. Run the Simulation

```bash
ros2 launch turtlebot3_gazebo turtlebot3_track.launch.py
```

3. Run the RotateAngle Service Server

```bash
ros2 run assessment_packages rotate_angle
```

4. Run the Example Answer

```bash
ros2 run b1_01_john_artc task
```

