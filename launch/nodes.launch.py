import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():
    # Launch configuration variables
    params_file = LaunchConfiguration("params_file")

    # Argument declarations
    declare_params_file_cmd = DeclareLaunchArgument(
        "params_file",
        default_value=os.path.join(
            get_package_share_directory("museum_guide"), "config", "standard_guide.yaml"
        ),
        description="Full path to the YAML params file for all museum_guide nodes",
    )

    # Node actions
    perception_node = Node(
        package="museum_guide",
        executable="perception",
        name="perception",
        parameters=[params_file],
    )
    planner_node = Node(
        package="museum_guide",
        executable="planner",
        name="planner",
        parameters=[params_file],
    )
    controller_node = Node(
        package="museum_guide",
        executable="controller",
        name="controller",
        parameters=[params_file],
    )
    odom_to_tf_node = Node(
        package="museum_guide",
        executable="odom_to_tf",
        name="odom_to_tf",
        parameters=[params_file],
    )
    odom_to_path_node = Node(
        package="museum_guide",
        executable="odom_to_path",
        name="odom_to_path",
        parameters=[params_file],
    )

    # Assemble the LaunchDescription
    ld = LaunchDescription()

    # Declare the launch options
    ld.add_action(declare_params_file_cmd)

    # Add the actions to launch the nodes
    ld.add_action(perception_node)
    ld.add_action(planner_node)
    ld.add_action(controller_node)
    ld.add_action(odom_to_tf_node)
    ld.add_action(odom_to_path_node)

    return ld
