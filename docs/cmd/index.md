# Command line usage

On this page you will find the documentation of the usage of the `rosswitch` command line application.

## Available terminal commands

The application provide several basic commands for managing the profiles:

- `rosswitch load <profile name>` or `rosswitch <profile name>`<br> Load a profile. The profile name can be either the name of the configuration file, or the name with underscore replaced by spaces. It will first check if there's a current preset loaded and will unload it before hand.<br> *E.g. a profile file named `custom_profile.rosprofile` can be loaded by calling either `rosswitch load custom_profile` or `rosswitch load "Custom Profile"`.*
- `rosswitch gen <profile name>` <br> Force a (re-)generation of the load and unload script, for example if you changed it.
- `rosswitch unload` <br> Unload the current profile and clear the paths.

!!! info "Aliases"

    To make it easier, several aliases are defined to the `rosswitch` command:
    
    - `rswitch`
    - `rswtch`
  
    You can of course define your own aliases to make it easier for you by putting the following line in your .bashrc (or .zshrc):

    ```
    alias <your alias here>=rosswitch
    ```

## Available tools

There is also a command `tools` to access several tools (mainly for debug purpose):

- `rosswitch tools colors` <br> Display all the available color scheme that can be used for the preset name display in the terminal. Check the [YAML Reference](../yaml/index.md#block-ros) for the list of all available colors.

## Other aliases

Other aliases are defined to ease ROS development. They are setup in the `setup.sh` file that you source in your .bashrc (.zshrc).

- `colbuild` is an aliase for `colcon build --symlink-install`