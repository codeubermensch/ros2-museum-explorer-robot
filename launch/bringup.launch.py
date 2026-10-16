import os

from launch import LaunchDescription
from launch.actions import ExecuteProcess, IncludeLaunchDescription
from launch.launch_description_sources import (
    PythonLaunchDescriptionSource,
)
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():
    # 1. Resolve the world file
    package_path = get_package_share_directory("museum_guide")

    world_path = os.path.join(
        package_path,
        "worlds",
        "museum_world.sdf",
    )

    # 2. Start Gazebo
    start_gazebo_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                get_package_share_directory("ros_gz_sim"),
                "launch",
                "gz_sim.launch.py",
            )
        ),
        launch_arguments={"gz_args": f"-r {world_path}"}.items(),
    )

    # 3. Start the Gazebo WebSocket bridge (optional)
    gzlaunch_path = os.path.join(
        package_path,
        "launch",
        "websocket.gzlaunch",
    )

    start_gz_websocket_cmd = ExecuteProcess(
        cmd=["gz-launch", gzlaunch_path],
        output="log",
    )

    # 4. Spawn TurtleBot3 in Gazebo
    sdf_path = os.path.join(
        package_path,
        "models",
        "turtlebot3_burger",
        "turtlebot3_burger.sdf",
    )

    spawn_robot_cmd = Node(
        package="ros_gz_sim",
        executable="create",
        arguments=[
            "-world",
            "museum_world",
            "-name",
            "turtlebot3",
            "-x",
            "0",
            "-y",
            "8",
            "-z",
            "0.1",
            "-file",
            sdf_path,
        ],
        output="screen",
    )

    # 5. Bridge Gazebo topics to ROS 2
    start_topic_bridge_cmd = Node(
        package="ros_gz_bridge",
        executable="parameter_bridge",
        arguments=[
            "/scan@sensor_msgs/msg/LaserScan[gz.msgs.LaserScan",
            "/joint_states@sensor_msgs/msg/JointState[gz.msgs.Model",
            "/cmd_vel@geometry_msgs/msg/Twist]gz.msgs.Twist",
            "/odom@nav_msgs/msg/Odometry[gz.msgs.Odometry",
        ],
        output="screen",
    )

    # 6. Run robot_state_publisher
    urdf_path = os.path.join(
        package_path,
        "models",
        "turtlebot3_burger",
        "turtlebot3_burger.urdf",
    )

    with open(urdf_path, "r") as f:
        robot_description = f.read()

    start_robot_state_publisher_cmd = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        parameters=[{"robot_description": robot_description}],
        output="screen",
    )

    # 7. Start RViz2 instead of Foxglove
    start_rviz_cmd = Node(
        package="rviz2",
        executable="rviz2",
        name="rviz2",
        output="screen",
    )

    # 8. Start your robot nodes
    start_nodes_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                package_path,
                "launch",
                "nodes.launch.py",
            )
        ),
    )

    # 9. Assemble the launch description
    ld = LaunchDescription()

    ld.add_action(start_gazebo_cmd)
    ld.add_action(start_gz_websocket_cmd)
    ld.add_action(spawn_robot_cmd)
    ld.add_action(start_topic_bridge_cmd)
    ld.add_action(start_robot_state_publisher_cmd)
    ld.add_action(start_rviz_cmd)
    ld.add_action(start_nodes_cmd)

    return ld
