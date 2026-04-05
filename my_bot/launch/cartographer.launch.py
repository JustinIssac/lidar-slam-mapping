# NOTE: This launch file is incomplete — missing -configuration_directory and -configuration_basename arguments.
# Use slam.launch.py instead for correct Cartographer launch.

import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='cartographer_ros',
            executable='cartographer_node',
            name='cartographer_node',
            output='screen',
            parameters=[{
                'use_sim_time': True,
                'use_pose_extrapolator': True,
            }],
            remappings=[
                ('scan', '/scan'),
                ('imu', '/imu'),
            ],
        ),
    ])
