#!/bin/bash

get_shell() {
  script_shell="$(readlink /proc/$$/exe | sed "s/.*\///")"
  echo ${script_shell}
}

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

if [[ "$(get_shell)" == "bash" ]]; then
  sc_source="${BASH_SOURCE[0]}"
  export PS1="$RSWCH_PRESET_COLOR_BASH$RSWCH_PRESET_NAME$RSWCH_SUFFIX_BASH$PS1"
else
  sc_source="$0"
  export PS1="\$RSWCH_PRESET_COLOR\$RSWCH_FPRESET_NAME\$RSWCH_SUFFIX$PS1"
fi

# Get the script directory
# DIR="$(get_script_dir $0)/bin"
DIR="$(get_script_dir $sc_source)/bin"
export PATH="$PATH:$DIR"

alias rosswitch="source $DIR/.rosswitch"
alias rswitch=rosswitch
alias rswtch=rosswitch
alias colbuild="colcon build --symlink-install"