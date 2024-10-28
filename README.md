# ROS Switch

Tools to manage ROS installations on your computer. It works by automatically generating and sourcing loading and unloading script baseds on a YAML configuration. You can describe each of your ROS environment with a config file, and let the program generate the scripts for you to keep a clean terminal while switching between ROS projects.

This project is inspired by the work of [Oliver Kermorgant's ros management tools scripts](https://github.com/oKermorgant/ros_management_tools).

Copyright (c) Meltwin - 2024 

Distributed under the MIT Licence

## Install

This package is composed of Python 3 (>= 3.8) and bash scripts. Thus it does not need any compilation before hand.

To install this, please add this line into your `.bashrc` or `.zshrc` depending of your environment:

```shell
source "<path_to_the_folder_of _the_repo>/setup.sh"
```

This program is compatible with both bash and zsh environments.

## Usage

You can use the `rosswitch` command as follows:

- to load a ROS configuration, simply type `rosswitch <config_name>`
- to list all the available configurations on the path: `rosswitch ls`
- to force the reconfiguration of a config file: `rosswitch gen <config_name>`

<!-- - to make a new ROS configuration (for the actual user), type `rosswitch new <config_name>` -->
<!-- - to extends from an existing ROS configuration, enter `rosswitch extend <parent_config> <child config>` -->

Some aliases are defined in the `setup.sh` script: 

- `rswitch` and `rswtch` are equivalent to `rosswitch`
- `colbuild` is equivalent to `colcon build --symlink-install`

## How to make a profile

The profiles are easy to create. Simply create a file with the format `<preset name>.rosprofile` in one of the application lookup paths. In this file, describe the configuration in YAML (cf. example below):

```YAML
preset:
    metadata:
        author: Meltwin
        date: "10/2024"
        description: "YAML configuration example"
    ros_version: 2
    env_var:
        NEEDED_ENV_VAR: 0
    ros:
        localhost: true
        colorized: true
    pre_load:
        - "echo 'You are loading the basic example configuration'"
    workspaces:
        - "$HOME/Prog/ROS2/my_workspace"
```

### Documentation comming soon !