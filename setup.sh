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
  export PS1="\$(echo \${RSWCH_PRESET_COLOR}) \$RSWCH_PRESET_NAME \$RSWCH_SUFFIX$PS1"
fi

# Get the script directory
# DIR="$(get_script_dir $0)/bin"
DIR="$(get_script_dir $sc_source)/bin"
export PATH="$PATH:$DIR"

alias rosswitch="source $DIR/.rosswitch"
alias rswitch=rosswitch
alias rswtch=rosswitch
alias colbuild="colcon build --symlink-install"

# printf "\e[0;30mBlack\n"
# printf "\e[0;31mRed\n"
# printf "\e[0;32mGreen\n"
# printf "\e[0;33mYellow\n"
# printf "\e[0;34mBlue\n"
# printf "\e[0;35mPurple\n"
# printf "\e[0;36mCyan\n"
# printf "\e[0;37mWhite\n"

# printf "\e[1;30mbold Black\n"
# printf "\e[1;31mbold Red\n"
# printf "\e[1;32mbold Green\n"
# printf "\e[1;33mbold Yellow\n"
# printf "\e[1;34mbold Blue\n"
# printf "\e[1;35mbold Purple\n"
# printf "\e[1;36mbold Cyan\n"
# printf "\e[1;37mbold White\n"

# printf "\e[0;90mhigh intensity Black\n"
# printf "\e[0;91mhigh intensity Red\n"
# printf "\e[0;92mhigh intensity Green\n"
# printf "\e[0;93mhigh intensity Yellow\n"
# printf "\e[0;94mhigh intensity Blue\n"
# printf "\e[0;95mhigh intensity Purple\n"
# printf "\e[0;96mhigh intensity Cyan\n"
# printf "\e[0;97mhigh intensity White\n"