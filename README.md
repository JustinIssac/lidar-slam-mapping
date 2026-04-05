# 🤖 2D SLAM Room Mapping — ROS2 + Google Cartographer

**Autonomous 2D Map Generation using LIDAR/IMU Sensor Fusion in Gazebo**  
EE5108 Digital Twins | University of Galway | January 2026

> **Base package:** [EE5108-DigitalTwins/my_bot](https://github.com/EE5108-DigitalTwins/my_bot) by Prof. Brian Deegan.  
> This repo extends the base with Google Cartographer SLAM integration, IMU fusion configuration, and a completed kitchen mapping session.

---

## Overview

A ROS2 package implementing 2D Simultaneous Localisation and Mapping (SLAM) using Google Cartographer with LIDAR/IMU sensor fusion. A custom differential drive robot is simulated in Gazebo inside a kitchen/dining room environment. The robot is teleoperated to explore the space while Cartographer builds an occupancy grid map in real time.

**Nav2 autonomous navigation was not completed** due to dependency installation issues with `nav2` on ROS2 Humble. The config file (`nav2_params.yaml`) is included for reference.

---

## Result — Generated Map

The final occupancy grid map of the Gazebo kitchen environment:

![Kitchen SLAM Map](maps/kitchen_slam_final.pgm)

| Parameter | Value |
|-----------|-------|
| Resolution | 0.05 m/pixel |
| Map origin | (-4.1, -7.75, 0.0) |
| Occupied threshold | 0.65 |
| Free threshold | 0.196 |
| Map format | PGM (occupancy grid) + pbstream (Cartographer internal) |

---

## System Architecture

```
Gazebo Simulation
       │
       ├── Simulated LIDAR  ──→  /scan   (360°, 10 Hz, 0.3–30m)
       └── Simulated IMU    ──→  /imu    (50 Hz)
                                   │
                          cartographer_node
                          (slam.launch.py + cartographer.lua)
                                   │
                          2D Occupancy Grid Map
                          (/map topic → map_saver → .pgm + .yaml)
```

### Cartographer Configuration (cartographer.lua)

| Parameter | Value | Notes |
|-----------|-------|-------|
| Mode | 2D | `MAP_BUILDER.use_trajectory_builder_2d = true` |
| IMU fusion | Enabled | `TRAJECTORY_BUILDER_2D.use_imu_data = true` |
| Odometry | Enabled | Differential drive wheel encoders |
| Motion filter — time | 5 s | Suppresses redundant poses |
| Motion filter — distance | 0.2 m | |
| Motion filter — angle | 5° | |
| Voxel filter size | 0.025 m | Point cloud downsampling |

---

## Repository Structure

```
lidar-slam-mapping/
├── README.md
├── .gitignore
│
├── my_bot/                          # ROS2 package (colcon workspace src/)
│   ├── package.xml
│   ├── CMakeLists.txt
│   ├── config/
│   │   ├── cartographer.lua         # Cartographer SLAM configuration ← key file
│   │   ├── sensors.yaml             # LIDAR + IMU simulation parameters
│   │   ├── gazebo_params.yaml       # Gazebo plugin parameters
│   │   ├── my_controllers.yaml      # Differential drive controllers
│   │   ├── slam_toolbox.yaml        # slam_toolbox config (alternative, unused)
│   │   ├── twist_mux.yaml           # Velocity input multiplexer
│   │   └── nav2_params.yaml         # Nav2 config (incomplete — see notes)
│   ├── description/
│   │   ├── robot.urdf.xacro         # Top-level URDF entry point
│   │   ├── robot_core.xacro         # Chassis, wheels, LIDAR + IMU links
│   │   ├── inertial_macros.xacro    # Inertia helper macros
│   │   ├── gazebo_control.xacro     # Gazebo diff drive + sensor plugins
│   │   └── models/kitchen_dining/   # Gazebo kitchen world mesh + SDF
│   ├── launch/
│   │   ├── slam.launch.py           # ✅ Launch Cartographer SLAM (use this)
│   │   ├── launch_sim.launch.py     # Launch full Gazebo simulation
│   │   ├── rsp.launch.py            # Robot State Publisher
│   │   ├── launch_robot.launch.py   # Real robot launch (hardware)
│   │   ├── nav2.launch.py           # Nav2 (incomplete)
│   │   ├── gazebo_only.launch.py    # Gazebo only (no robot)
│   │   └── cartographer.launch.py   # ⚠️ Incomplete — missing config args
│   └── worlds/
│       └── empty_world.world
│
└── maps/
    ├── kitchen_slam_final.pgm       # Generated occupancy grid map
    ├── kitchen_slam_final.yaml      # Map metadata
    └── kitchen_slam_map.pbstream    # Cartographer binary map state
```

---

## Setup & Usage

### Prerequisites

- ROS2 Humble (Ubuntu 22.04)
- Gazebo Classic
- Google Cartographer ROS

```bash
sudo apt install ros-humble-cartographer ros-humble-cartographer-ros \
                 ros-humble-gazebo-ros-pkgs ros-humble-twist-mux \
                 ros-humble-teleop-twist-keyboard
```

### Build

```bash
mkdir -p ~/ros2_ws/src
cd ~/ros2_ws/src
git clone https://github.com/YOUR_USERNAME/lidar-slam-mapping.git
cd ~/ros2_ws
colcon build --packages-select my_bot
source install/setup.bash
```

### Run SLAM Mapping

**Terminal 1 — Launch Gazebo simulation:**
```bash
ros2 launch my_bot launch_sim.launch.py
```

**Terminal 2 — Launch Cartographer SLAM:**
```bash
ros2 launch my_bot slam.launch.py
```

**Terminal 3 — Teleop to drive the robot:**
```bash
ros2 run teleop_twist_keyboard teleop_twist_keyboard
```

**Terminal 4 — Save the map when done:**
```bash
ros2 run nav2_map_server map_saver_cli -f ~/my_map
```

### Load a Saved Map

```bash
ros2 run nav2_map_server map_server --ros-args \
  -p yaml_filename:=maps/kitchen_slam_final.yaml \
  -p use_sim_time:=true
```

---

## Sensor Configuration

### LIDAR (Simulated, Gazebo ray plugin)
| Parameter | Value |
|-----------|-------|
| Scan rate | 10 Hz |
| Angular range | 360° |
| Min range | 0.3 m |
| Max range | 30 m |
| Resolution | 0.02 rad |
| Samples/scan | 360 |

### IMU (Simulated, Gazebo imu plugin)
| Parameter | Value |
|-----------|-------|
| Update rate | 50 Hz |
| Topic | `/imu` |
| Frame | `imu_link` (child of `base_link`) |

---

## Known Issues / Incomplete Work

- **Nav2 autonomous navigation** — `nav2_params.yaml` is configured but the `nav2` stack was not successfully launched due to dependency issues on ROS2 Humble in the VMware environment. This is a logical next step.
- **slam_toolbox** — a `slam_toolbox.yaml` config is included as an alternative SLAM backend but was not evaluated against Cartographer.

---

## Credits

Base robot package built on: [EE5108-DigitalTwins/my_bot](https://github.com/EE5108-DigitalTwins/my_bot) — Prof. Liam Kilmartin, University of Galway.

Cartographer configuration, IMU fusion tuning, sensor parameter setup, and kitchen mapping session by Justin Issac.

---

## License

Apache License 2.0 — see original base package.

---

## Contact

**Justin Issac** — MSc Intelligent Robotics, University of Galway  
[GitHub](https://github.com/YOUR_USERNAME)
