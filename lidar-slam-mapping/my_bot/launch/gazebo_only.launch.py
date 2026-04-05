import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource

def generate_launch_description():
    # This file is deprecated - use launch_sim.launch.py instead
    # Kept here for backwards compatibility but returns empty launch description
    return LaunchDescription([
    ])
