from launch import LaunchDescription
from launch_ros.actions import Node
import os
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    pkg_share = get_package_share_directory('my_bot')
    config_file = os.path.join(pkg_share, 'config', 'cartographer.lua')
    
    return LaunchDescription([
        Node(
            package='cartographer_ros',
            executable='cartographer_node',
            name='cartographer_node',
            output='screen',
            arguments=[
                '-configuration_directory', os.path.join(pkg_share, 'config'),
                '-configuration_basename', 'cartographer.lua'
            ],
            parameters=[{
                'use_sim_time': True,
            }],
            remappings=[
                ('/scan', '/scan'),
                ('/imu', '/imu'),
                ('/odom', '/odom'),
            ],
        ),
    ])
