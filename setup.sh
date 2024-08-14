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
DIR="$(get_script_dir $0)"
export PATH="$PATH:$DIR/bin"
