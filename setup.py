import os
from glob import glob
from setuptools import find_packages, setup

package_name = 'museum_guide'

setup(
    name=package_name,
    version="0.0.0",
    packages=find_packages(exclude=["test"]),
    data_files=[
        ("share/ament_index/resource_index/packages", ["resource/" + package_name]),
        ("share/" + package_name, ["package.xml"]),
        (os.path.join("share", package_name, "launch"), glob("launch/*.launch.py")),
        (os.path.join("share", package_name, "config"), glob("config/*.yaml")),
        # ... existing entries ...
        (os.path.join("share", package_name, "worlds"), glob("worlds/*.sdf")),
        # NEW: install the TurtleBot3 model
        # Top-level files (SDF, URDF, model.config)
        (
            os.path.join("share", package_name, "models", "turtlebot3_burger"),
            glob("models/turtlebot3_burger/*.sdf")
            + glob("models/turtlebot3_burger/*.urdf")
            + glob("models/turtlebot3_burger/*.config"),
        ),
        # Mesh files — one entry per subdirectory
        (
            os.path.join(
                "share", package_name, "models", "turtlebot3_burger", "meshes", "bases"
            ),
            glob("models/turtlebot3_burger/meshes/bases/*.stl"),
        ),
        (
            os.path.join(
                "share", package_name, "models", "turtlebot3_burger", "meshes", "wheels"
            ),
            glob("models/turtlebot3_burger/meshes/wheels/*.stl"),
        ),
        (
            os.path.join(
                "share",
                package_name,
                "models",
                "turtlebot3_burger",
                "meshes",
                "sensors",
            ),
            glob("models/turtlebot3_burger/meshes/sensors/*.stl"),
        ),
    ],
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="maithresh",
    maintainer_email="maithreshgokulkumar@gmail.com",
    description="TODO: Package description",
    license="MIT",
    extras_require={
        "test": [
            "pytest",
        ],
    },
    entry_points={
        "console_scripts": [
            "hello = museum_guide.hello_node:main",
            "perception = museum_guide.perception:main",
            "hello_pub = museum_guide.hello_pub:main",
            "planner = museum_guide.planner:main",
            "controller = museum_guide.controller:main",
            "odom_to_tf = museum_guide.odom_to_tf:main",
            "odom_to_path = museum_guide.odom_to_path:main",
        ],
    },
)
