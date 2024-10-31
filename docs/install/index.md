# Install from source (Linux)

## Get the sources

You can either download the latest release, or clone the repository to you machine.

### Downloading the latest release

The latest release can be found on this link: [ROS Switch - Release page](https://github.com/Baxterminator/ros_switch/releases).
Now unzip it, and place in the root directory (where the `requirements.txt` and `setup.sh` files are located).

### Cloning from Github

In the directory where you want to place the application, run these command:

```shell
git clone https://github.com/Baxterminator/ros_switch.git
cd ros_switch
```

## Install the application

Go into the folder you downloaded Now, you have to add the setup script to your `.bashrc` or `.zshrc` file (depending on the terminal you use). Just type the following command on your terminal:

=== "Bash"

    ```shell
    python3 -m pip install -r requirements.txt
    echo "source $(readlink -f .)/setup.sh" >> $HOME/.bashrc
    ```

=== "Zsh"

    ```shell
    python3 -m pip install -r requirements.txt
    echo "source $(readlink -f .)/setup.sh" >> $HOME/.zshrc
    ```

Now you can open a new tab and the application should be installed. You can check it by running:

```shell
rosswitch tools colors
```

If there are no problem, you should see several lines of text with colors. Else, if any error occur you might have a problem with you installation or your system. In this case, please fill an issue on [the project GitHub](https://github.com/Baxterminator/ros_switch/issues).