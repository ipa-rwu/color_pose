# Copyright (c) 2023 Ruichao Wu
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from launch import LaunchDescription
from launch.actions import ExecuteProcess
from launch import LaunchDescription
from launch.substitutions import FindExecutable

import yaml
from yaml import SafeLoader

document = """
    header:
      stamp:
        sec: 0
        nanosec: 0
      frame_id: world
    color_poses:
    - header:
        stamp:
          sec: 0
          nanosec: 0
        frame_id: world
      color: red
      element: cube
      pose:
        position:
          x: -0.215
          y: -0.04
          z: 1.065
        orientation:
          x: 0.707
          y: 0.707
          z: 0.0
          w: 0.001
    - header:
        stamp:
          sec: 0
          nanosec: 0
        frame_id: world
      color: red
      element: cube_holder
      pose:
        position:
          x: -0.117
          y: 0.046
          z: 1.065
        orientation:
          x: 0.707
          y: 0.707
          z: 0.0
          w: 0.001
    - header:
        stamp:
          sec: 0
          nanosec: 0
        frame_id: world
      color: blue
      element: cube
      pose:
        position:
          x: -0.216
          y: 0.126
          z: 1.065
        orientation:
          x: 0.707
          y: 0.707
          z: 0.0
          w: 0.001
    - header:
        stamp:
          sec: 0
          nanosec: 0
        frame_id: world
      color: blue
      element: cube_holder
      pose:
        position:
          x: -0.216
          y: -0.04
          z: 1.065
        orientation:
          x: 0.707
          y: 0.707
          z: 0.0
          w: 0.001
    - header:
        stamp:
          sec: 0
          nanosec: 0
        frame_id: world
      color: green
      element: cube
      pose:
        position:
          x: -0.315
          y: 0.046
          z: 1.065
        orientation:
          x: 0.707
          y: 0.707
          z: 0.0
          w: 0.001
    - header:
        stamp:
          sec: 0
          nanosec: 0
        frame_id: world
      color: green
      element: cube_holder
      pose:
        position:
          x: -0.216
          y: 0.126
          z: 1.065
        orientation:
          x: 0.707
          y: 0.707
          z: 0.0
          w: 0.001
    """


def generate_launch_description():
    ld = LaunchDescription()

    req = yaml.load(document, Loader=SafeLoader)

    cmd_str = 'topic pub -r 10 /color_pose_estimation/color_pose_array color_pose_msgs/msg/ColorPoseArray "{}"'.format(
        str(req)
    )

    ld.add_action(
        ExecuteProcess(
            cmd=[[FindExecutable(name="ros2"), " {}".format(cmd_str)]], shell=True
        )
    )
    return ld