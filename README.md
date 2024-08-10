# ROS Switch

Tools to manage ROS installations on your computer.

This project is inspired of the work of [Oliver Kermorgant's ros management tools](https://github.com/oKermorgant/ros_management_tools).

Copyright (c) Meltwin - 2024 

Distributed under the MIT Licence

## Usage

You can use the `rosswitch` command as follows:

- to load a ROS configuration, simply type `rosswitch <config_name>`
- to make a new ROS configuration (for the actual user), type `rosswitch new <config_name>`
- to extends from an existing ROS configuration, enter `rosswitch extend <parent_config> <child config>`
- to force the reconfiguration of a config file: `rosswitch gen <config_name>`

## How to configure

These scripts are based on Python 3. 