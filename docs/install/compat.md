# Compatible systems

This software is made to be compatible with as many system as possible. However, it heavily relies on shell script to source ROS workspace, and so is not made for Windows usage. This may be one future goal, but not in the immediate future.

You can find below the list of known dependencies and the list known compatible systems.

!!! info
    For now, this application only works for shell terminal:

    - bash
    - zsh

## Dependencies

|   Name   | Version  | Description                                   |
| :------: | :------: | :-------------------------------------------- |
|  Python  |  >= 3.8  | Most scripts are in Python3                   |
| colorama | >= 0.4.4 | Python package for putting colors in terminal |
|  PyYAML  | >= 6.0.2 | Python package to read YAML files             |

## Compatible systems

| System  | Version |             Status              |
| :-----: | :-----: | :-----------------------------: |
| Ubuntu  |  22.04  | :material-check-circle-outline: |
|  MacOS  |    -    |            Untested             |
| Windows |    -    | :material-close-circle-outline: |