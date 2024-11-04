from typing import Any, List

from ..PresetConfig import PresetConfig, ROSVersion
from .ScriptWriter import ScriptWriter, WriterConfig
from colorama import Fore


def is_ip(t: str) -> bool:
    # Look for IPV4
    v = t.split(".")
    if len(v) == 4:
        for ip_block in v:
            if not ip_block.isnumeric():
                return False
        return True
    return False


class ShellScriptWriter(ScriptWriter):
    def __init__(self, file_name: str, config: WriterConfig) -> None:
        super().__init__(
            file_name,
            config.update_from({"eol": "\n", "comment_prefix": "# "}),
        )

    def _format(self, val: Any) -> Any:
        if type(val) is bool:
            return 1 if val else 0
        if type(val) is str:
            s = val.replace('"', r"\"")
            return f'"{s}"'
        return val

    # --------------------------------------------------------
    # Standard export functions
    # --------------------------------------------------------

    def _write_cmd(self, cmd: str) -> None:
        self._write_line(cmd)

    def export_var(self, var: str, val: Any) -> None:
        self._write_line(f"export {var}={self._format(val)}")

    def unset_var(self, var: str) -> None:
        self._write_line(f"unset {var}")

    def _write_load_workspace(self, ws: str) -> None:
        self._write_line(
            f"""
wk_found=0
for sub in $subs
do
    install_path="{ws}${{sub}}local_setup.sh"
    if [[ -f $install_path ]]; then
        source $install_path
        wk_found=1
    fi
done
if [[ $wk_found == 0 ]]; then
    echo -e "{Fore.YELLOW}Workspace {ws} does not seems to be a ROS workspace. No local_setup.sh found!{Fore.RESET}"
fi
    """
        )

    def _write_workspace_list(self, var: str, l: List[str]) -> None:
        self._write_line(f"{var}=(")
        for wk in l:
            self._write_line(f'\t"{wk}"')
        self._write_line(f")")

    def _write_clean_path(self, path, ws) -> None:
        self._write_line(f"export {path}=$(_remove_paths ${path} ${ws})")

    def export_ros_ip(self, env, ip: str | None) -> None:
        if ip is not None and is_ip(ip):
            self.export_var(env, ip)
        else:
            self._write_line(
                f"export {env}=$(_get_interface_ip {'' if ip is None else ip})"
            )

    # --------------------------------------------------------
    # Shell functions to use in the program
    # --------------------------------------------------------

    def _custom_load_dep(self, config: PresetConfig) -> None:
        self._write_line('subs=("/" "/install/" "/devel/")')

        # Look for interface lookup for ROS_IP
        if config.ros_version == ROSVersion.ROS_1 or (
            config.ros.ros_ip.value is not None and not is_ip(config.ros.ros_ip.value)
        ):
            self._write_line(
                r"""
# Function that generate a (name, ip) map of the interfaces of this computer
# Exported as a list of name@ip 
function _get_interfaces() {
    local ips=$(ifconfig)
    local interface_regex="[a-zA-Z0-9]+:$"
    local ip_regex="[0-9.]+"
    
    if [[ $SHELL_TYPE == "zsh" ]]; then
        ips="$(tr '\n' ' ' <<< $ips)"
        read -r -A ips <<< $ips
    fi

    # Iterate over the words to get interfaces names and ip
    local out=("")
    local found_interface=""
    local in_interface=0
    local inet_found=0
    for l in $ips; do
        # echo $l
        # Check for interface name
        if [[ $l =~ $interface_regex ]]; then
            found_interface=$(echo $l | rev | cut -c2- | rev)
            in_interface=1
        elif [[ $in_interface == 1 ]] && [[ $l = *"inet"* ]]; then
            inet_found=1
        elif [[ $inet_found == 1 ]] && [[ $l =~ $ip_regex ]]; then
            # Save interface 
            out="$out $found_interface@$l"
            in_interface=0
            inet_found=0
        fi    
    done
    echo $out
}

# Function that return the ip of the given interface name
# It checks for similar expression as the given argument
# If no argument is provided, default to localhost
function _get_interface_ip() {
    local interfaces=$(_get_interfaces)
    
    if [[ $SHELL_TYPE == "bash" ]]; then
        IFS=' ' read -ra interfaces <<< "$interfaces"
    else
        IFS=' ' read -rA interfaces <<< "$interfaces"
    fi

    local to_find
    if [[ -z $1 ]]; then
        to_find="lo"
    else
        to_find=$1
    fi

    for intf in $interfaces; do
        local intf_name=$(echo $intf | cut -d "@" -f 1)
        local intf_ip=$(echo $intf | cut -d "@" -f 2)
        if [[ $intf_name =~ $to_find ]]; then
            echo $intf_ip
            break
        fi
    done
}
"""
            )

    def _custom_unload_dep(self, config: PresetConfig) -> None:
        self._write_line(
            """
# Function that remove ROS workspaces from a path (eg PATH, PYTHONPATH, ...)
# Made by O. Kermorgan (https://github.com/oKermorgant/) for the ros_management_tools project
function _remove_paths()
{
    if [[ $SHELL_TYPE == "bash" ]]; then
        IFS=':' read -ra PATHES <<< "$1"
    else
        IFS=':' read -rA PATHES <<< "$1"
    fi
    local THISPATH=""
    local ARGS=("$@")
    local N_ARGS="${#ARGS[@]}"
    for fpath in "${PATHES[@]}"; do
        local to_remove=0
        local i=0
        for (( i=2; i <= $N_ARGS; i++ )); do
            if [[ $fpath = *"${ARGS[$i]}"* ]]; then
                to_remove=1
            break
            fi
        done
        if [ $to_remove -eq 0 ]; then
            THISPATH="$THISPATH:$fpath"
        fi
    done
    echo $THISPATH | cut -c2-
}"""
        )
