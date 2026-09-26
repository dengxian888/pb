from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os
def generate_launch_description(): 
  pkg_path=get_package_share_directory('turtle_eight')
  param_file=os.path.join(pkg_path,'config','turtle_params.yaml')
  executable_path='/home/ljx/ros2_ws/install/turtle_eight/lib/turtle_eight/eight_control'
  
  return LaunchDescription([
    Node(
      package='turtlesim',
      executable='turtlesim_node',
      name='turtlesim',
      output='screen'
    ),
    Node(
      executable=executable_path,
      name='turtle_eight_node',
      output='screen',
      parameters=[param_file]
    )
  ])
