# App Configuration

## ROS Profiles

This application use custom YAML files called **ROS profiles**. These profiles is used to describe the environment you wants to load, the environment variable to set, the commands to set, etc. For more information on what you can configure through these profiles check the [YAML Reference](../yaml/index.md).

These profiles are files that should have the `.rosprofile` extension (to be sure to not mix them with other YAML files). They should be located in defined directories:

|   System    | Install Path                    | Admin Path                      | User Path                           |
| :---------: | :------------------------------ | :------------------------------ | :---------------------------------- |
| Linux-based | :material-check-circle-outline: | `/opt/ros/ros_switch/`          | `~/.local/share/ros_switch/`        |
|    MacOS    | :material-check-circle-outline: | :material-close-circle-outline: | `~/Library/Preferences/ros_switch/` |

For each of these paths, the directory (what we will call `dir` here) has the following structure:

```
dir/
    profile/  # Where you should put the .rosprofile files
    loader/   # Where the loading script will be generated
    unloader/ # Where the unloading script will be generated
```

!!! info "Custom paths for the profiles location"

    If these paths are not enough for you or if you need a more complex configuration, you can setup custom paths with environment variables:

    - `RSWCH_CUSTOM_ADMIN_PATHS`: for adding paths to the admin level (that use shouldn't modify)
    - `RSWCH_CUSTOM_PATHS`: for adding paths to the user level