#!/bin/bash

get_script_dir() {
    SOURCE=$1
    while [ -L "$SOURCE" ]; do # resolve $SOURCE until the file is no longer a symlink
      DIR=$( cd -P "$( dirname "$SOURCE" )" >/dev/null 2>&1 && pwd )
      SOURCE=$(readlink "$SOURCE")
      [[ $SOURCE != /* ]] && SOURCE=$DIR/$SOURCE # if $SOURCE was a relative symlink, we need to resolve it relative to the path where the symlink file was located
    done
    DIR=$( cd -P "$( dirname "$SOURCE" )" >/dev/null 2>&1 && pwd )
    echo $DIR
}

# Get the script directory
export PATH="$PATH:$(get_script_dir $0)/bin"

alias rswitch=rosswitch
alias rswtch=rosswitch
alias colbuild=colcon build --symlink-install