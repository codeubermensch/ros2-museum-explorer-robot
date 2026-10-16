# Museum Explorer Robot 🤖

A ROS 2-based simulated mobile robot that explores a museum environment using LiDAR-based obstacle avoidance and reactive navigation.

Built using ROS 2 Jazzy, Gazebo Harmonic, Python, and the TurtleBot3 Burger platform, this project demonstrates a modular robotics pipeline from sensor perception to motion control, with real-time visualization in RViz2.

## Overview

Museum Explorer is designed to roam through a simulated museum environment while reacting to nearby obstacles.

The robot processes LiDAR measurements, estimates obstacle distances in four directions, selects a movement decision, and converts that decision into velocity commands.

The system is organized into separate ROS 2 nodes to make its perception, planning, and control components easier to understand, test, and extend.

## Features

- **LiDAR-based perception:** Processes LaserScan data to estimate obstacle distances in front of, behind, and to either side of the robot.
- **Reactive obstacle avoidance:** Selects forward movement, left turns, right turns, or stopping based on obstacle distances.
- **Velocity control:** Converts navigation decisions into linear and angular velocity commands.
- **RViz2 visualization:** Publishes markers representing perception regions and the planner's intended movement.
- **Configurable behavior:** Provides YAML parameter profiles for different operating conditions.
- **Odometry visualization:** Includes ROS 2 nodes for odometry-to-TF conversion and path visualization.
- **Gazebo simulation:** Uses a TurtleBot3 Burger model in a custom museum world.
- **Modular architecture:** Separates perception, planning, and control into independent ROS 2 nodes.

## Technology Stack

| Technology | Purpose |
|---|---|
| ROS 2 Jazzy | Robotics middleware and node communication |
| Gazebo Harmonic | Robot and environment simulation |
| Python | Perception, planning, and control logic |
| TurtleBot3 Burger | Simulated mobile robot platform |
| LiDAR / LaserScan | Obstacle-distance estimation |
| RViz2 | Robot state and decision visualization |
| ROS 2 Launch | Simulation and node orchestration |
| YAML | Runtime parameter configuration |

## System Architecture

'
             Gazebo Museum World
                     |
                     v
              TurtleBot3 Burger
                     |
                     v
                LiDAR /scan
                     |
                     v
           +-------------------+
           | Perception Node   |
           |                   |
           | Front distance    |
           | Left distance     |
           | Right distance    |
           | Rear distance     |
           +-------------------+
                     |
                     v
           +-------------------+
           | Planner Node      |
           |                   |
           | GO_FORWARD        |
           | TURN_LEFT         |
           | TURN_RIGHT        |
           | STOP              |
           +-------------------+
                     |
                 /drive_cmd
                     |
                     v
           +-------------------+
           | Controller Node   |
           +-------------------+
                     |
                  /cmd_vel
                     |
                     v
              TurtleBot3 Burger

       Perception and planner markers
                     |
                     v
                   RViz2


## Project Structure

museum_guide/
├── config/
│   ├── standard_guide.yaml
│   ├── cautious_tour.yaml
│   ├── agile_demo.yaml
│   ├── crowded_gallery.yaml
│   └── after_hours.yaml
├── launch/
│   ├── bringup.launch.py
│   └── nodes.launch.py
├── models/
│   └── turtlebot3_burger/
│       ├── meshes/
│       ├── turtlebot3_burger.sdf
│       └── turtlebot3_burger.urdf
├── museum_guide/
│   ├── controller.py
│   ├── hello_node.py
│   ├── hello_pub.py
│   ├── odom_to_path.py
│   ├── odom_to_tf.py
│   ├── perception.py
│   └── planner.py
├── resource/
├── test/
├── worlds/
│   └── museum_world.sdf
├── LICENSE
├── package.xml
├── setup.cfg
├── setup.py
└── README.md

## Installation
# Prerequisites

The project is developed for:
- Ubuntu 24.04
- ROS 2 Jazzy
- Gazebo Harmonic
- RViz2
- ros_gz_sim and ros_gz_bridge

Install ROS 2 and Gazebo dependencies according to their official installation documentation before proceeding.

1. Create a ROS 2 workspace
mkdir -p ~/ros2_ws/src
cd ~/ros2_ws/src

2. Clone the repository
git clone https://github.com/codeubermensch/ros2-museum-explorer-robot.git museum_guide

3. Install dependencies
cd ~/ros2_ws
source /opt/ros/jazzy/setup.bash
rosdep install --from-paths src --ignore-src -r -y

4. Build the package
colcon build --packages-select museum_guide
source install/setup.bash

Running the Simulation
Launch the complete simulation:
ros2 launch museum_guide bringup.launch.py

The launch system starts the Gazebo simulation, spawns the robot, establishes the configured Gazebo-to-ROS bridges, starts robot state publishing, opens RViz2, and launches the perception, planning, control, and odometry nodes.
The robot reacts to obstacle distances using its configured reactive navigation logic.
ROS 2 Topics
Topic	Message type	Purpose
/scan	sensor_msgs/msg/LaserScan	LiDAR measurements
/front_distance	std_msgs/msg/Float32	Closest valid obstacle distance in the front sector
/left_distance	std_msgs/msg/Float32	Closest valid obstacle distance in the left sector
/right_distance	std_msgs/msg/Float32	Closest valid obstacle distance in the right sector
/back_distance	std_msgs/msg/Float32	Closest valid obstacle distance in the rear sector
/drive_cmd	std_msgs/msg/String	Planner decision
/cmd_vel	geometry_msgs/msg/Twist	Robot velocity commands
/perception/markers	visualization_msgs/msg/MarkerArray	Perception-window visualization
/planner/markers	visualization_msgs/msg/MarkerArray	Planner-decision visualization
/odom	nav_msgs/msg/Odometry	Robot odometry


Navigation Logic
The perception node divides the LiDAR scan into four directional sectors and calculates the minimum valid distance in each sector.
The planner uses the front distance and the left/right distances to choose an action:
- GO_FORWARD: The front distance is at least the configured stopping distance.
- TURN_LEFT: The front is obstructed and the left side has more clearance than the right.
- TURN_RIGHT: The front is obstructed and the right side has more clearance than the left.
- STOP: The front is obstructed and both sides are below the stopping threshold.

The controller translates these decisions into linear and angular velocity commands.
This is a reactive obstacle-avoidance approach. It does not, by itself, provide global path planning or guarantee collision-free navigation.


Configurable Operating Profiles
The config/ directory contains five YAML parameter profiles:
- standard_guide.yaml
- cautious_tour.yaml
- agile_demo.yaml
- crowded_gallery.yaml
- after_hours.yaml

These profiles are intended to configure the robot's behavior through ROS 2 parameters, such as stopping distance and movement speeds.
The nodes.launch.py file accepts a params_file argument. To select a profile when launching the nodes:
ros2 launch museum_guide nodes.launch.py \
  params_file:=/absolute/path/to/config/cautious_tour.yaml

Replace the path with the location of the desired YAML file.
Current Limitations
- Navigation is based on local obstacle distances rather than a global map or planned route.
- The planner uses a small set of discrete movement decisions.
- There is no visitor interaction or destination-based tour guidance.
- Navigation performance depends on sensor measurements, parameter choices, and the simulated environment.
Future Improvements
- Add waypoint-based navigation.
- Integrate SLAM and map-based navigation.
- Improve obstacle avoidance using more advanced local planning.
- Add a visitor-facing interface for selecting destinations.
- Evaluate navigation performance using repeatable simulation scenarios.
- Add automated tests and demonstration videos.
License
This project is licensed under the MIT License. See LICENSE for details.
EOF


You should see the project title and overview.
