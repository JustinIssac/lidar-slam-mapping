# Maps

Generated from a full teleoperated mapping session in the Gazebo kitchen/dining room environment using Google Cartographer.

## Files

| File | Description |
|------|-------------|
| `kitchen_slam_final.pgm` | Occupancy grid map image (white=free, black=occupied, grey=unknown) |
| `kitchen_slam_final.yaml` | Map metadata — resolution, origin, thresholds |
| `kitchen_slam_map.pbstream` | Cartographer binary map state — can be used to resume/extend mapping |

## Map Parameters

| Parameter | Value |
|-----------|-------|
| Resolution | 0.05 m/pixel |
| Origin | (-4.1, -7.75, 0.0) |
| Occupied threshold | 0.65 |
| Free threshold | 0.196 |

## Loading the Map

```bash
ros2 run nav2_map_server map_server --ros-args \
  -p yaml_filename:=maps/kitchen_slam_final.yaml \
  -p use_sim_time:=true
```

## Resuming Mapping from pbstream

```bash
ros2 launch my_bot slam.launch.py \
  load_state_filename:=maps/kitchen_slam_map.pbstream
```
