from typing import Any, List
from .ScriptWriter import ScriptWriter, WriterConfig
from colorama import Fore


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

    def _custom_load_dep(self) -> None:
        self._write_line(
            """
subs=(\"/\" \"/install/\" \"/devel/\")
"""
        )

    def _custom_unload_dep(self) -> None:
        self._write_line(
            """_remove_paths()
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
