import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import SetEnvironmentVariable

def generate_launch_description():
    # Enable ROS2 debug logging
    return LaunchDescription([
        SetEnvironmentVariable('ROS_LOG_DIR', '/tmp/ros_slam_logs'),
        Node(
            package='slam_toolbox',
            executable='async_slam_toolbox_node',
            name='slam_toolbox',
            output='screen',
            parameters=[{
                'use_sim_time': True,
                'solver_plugin': 'solver_plugins::CeresSolver',
                'ceres_linear_solver_type': 'SPARSE_NORMAL_CHOLESKY',
                'ceres_preconditioner_type': 'SCHUR_JACOBI',
                'ceres_trust_strategy': 'DOGLEG',
                'ceres_dogleg_type': 'TRADITIONAL_DOGLEG',
                'map_update_interval': 1.0,
                'publish_occupancy_grid': True,
            }],
            remappings=[
                ('scan', 'scan'),
                ('tf', 'tf'),
                ('map', 'map'),
                ('odom', 'odom'),
            ]
        ),
    ])
