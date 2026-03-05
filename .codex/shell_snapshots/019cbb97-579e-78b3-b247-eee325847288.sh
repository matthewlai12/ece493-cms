# Snapshot file
# Unset all aliases to avoid conflicts with functions
# Functions
gawklibpath_append () 
{ 
    [ -z "$AWKLIBPATH" ] && AWKLIBPATH=`gawk 'BEGIN {print ENVIRON["AWKLIBPATH"]}'`;
    export AWKLIBPATH="$AWKLIBPATH:$*"
}
gawklibpath_default () 
{ 
    unset AWKLIBPATH;
    export AWKLIBPATH=`gawk 'BEGIN {print ENVIRON["AWKLIBPATH"]}'`
}
gawklibpath_prepend () 
{ 
    [ -z "$AWKLIBPATH" ] && AWKLIBPATH=`gawk 'BEGIN {print ENVIRON["AWKLIBPATH"]}'`;
    export AWKLIBPATH="$*:$AWKLIBPATH"
}
gawkpath_append () 
{ 
    [ -z "$AWKPATH" ] && AWKPATH=`gawk 'BEGIN {print ENVIRON["AWKPATH"]}'`;
    export AWKPATH="$AWKPATH:$*"
}
gawkpath_default () 
{ 
    unset AWKPATH;
    export AWKPATH=`gawk 'BEGIN {print ENVIRON["AWKPATH"]}'`
}
gawkpath_prepend () 
{ 
    [ -z "$AWKPATH" ] && AWKPATH=`gawk 'BEGIN {print ENVIRON["AWKPATH"]}'`;
    export AWKPATH="$*:$AWKPATH"
}

# setopts 3
set -o braceexpand
set -o hashall
set -o interactive-comments

# aliases 0

# exports 85
declare -x BUNDLED_DEBUGPY_PATH="/home/mlai/.vscode/extensions/ms-python.debugpy-2025.18.0-linux-x64/bundled/libs/debugpy"
declare -x CHROME_DESKTOP="code.desktop"
declare -x CODEX_HOME="/home/mlai/ubuntu-blade/ubuntu/year5/ece493/Lab2/ece493-cms/.codex"
declare -x CODEX_MANAGED_BY_NPM="1"
declare -x COLORTERM="truecolor"
declare -x DBUS_SESSION_BUS_ADDRESS="unix:path=/run/user/1000/bus"
declare -x DEBUGINFOD_URLS="https://debuginfod.ubuntu.com "
declare -x DESKTOP_SESSION="ubuntu-wayland"
declare -x DISPLAY=":1"
declare -x FC_FONTATIONS="1"
declare -x FONTCONFIG_FILE="/etc/fonts/fonts.conf"
declare -x FONTCONFIG_PATH="/etc/fonts"
declare -x GDK_BACKEND="x11"
declare -x GDK_BACKEND_VSCODE_SNAP_ORIG=""
declare -x GDMSESSION="ubuntu-wayland"
declare -x GIO_MODULE_DIR="/home/mlai/snap/code/common/.cache/gio-modules"
declare -x GIO_MODULE_DIR_VSCODE_SNAP_ORIG=""
declare -x GIT_ASKPASS="/snap/code/227/usr/share/code/resources/app/extensions/git/dist/askpass.sh"
declare -x GNOME_DESKTOP_SESSION_ID="this-is-deprecated"
declare -x GNOME_KEYRING_CONTROL="/run/user/1000/keyring"
declare -x GNOME_SETUP_DISPLAY=":2"
declare -x GNOME_SHELL_SESSION_MODE="ubuntu"
declare -x GNOME_TERMINAL_SCREEN="/org/gnome/Terminal/screen/65a28822_f212_4a37_82cf_2c22e1b30680"
declare -x GNOME_TERMINAL_SERVICE=":1.115"
declare -x GSETTINGS_SCHEMA_DIR="/home/mlai/snap/code/227/.local/share/glib-2.0/schemas"
declare -x GSETTINGS_SCHEMA_DIR_VSCODE_SNAP_ORIG=""
declare -x GSM_SKIP_SSH_AGENT_WORKAROUND="true"
declare -x GTK_EXE_PREFIX="/snap/code/227/usr"
declare -x GTK_EXE_PREFIX_VSCODE_SNAP_ORIG=""
declare -x GTK_IM_MODULE_FILE="/home/mlai/snap/code/common/.cache/immodules/immodules.cache"
declare -x GTK_IM_MODULE_FILE_VSCODE_SNAP_ORIG=""
declare -x GTK_MODULES="gail:atk-bridge"
declare -x GTK_PATH="/snap/code/227/usr/lib/x86_64-linux-gnu/gtk-3.0"
declare -x GTK_PATH_VSCODE_SNAP_ORIG=""
declare -x HOME="/home/mlai"
declare -x IM_CONFIG_CHECK_ENV="1"
declare -x IM_CONFIG_PHASE="1"
declare -x LANG="en_US.UTF-8"
declare -x LESSCLOSE="/usr/bin/lesspipe %s %s"
declare -x LESSOPEN="| /usr/bin/lesspipe %s"
declare -x LOCPATH="/snap/code/227/usr/lib/locale"
declare -x LOCPATH_VSCODE_SNAP_ORIG=""
declare -x LOGNAME="mlai"
declare -x LS_COLORS="rs=0:di=01;34:ln=01;36:mh=00:pi=40;33:so=01;35:do=01;35:bd=40;33;01:cd=40;33;01:or=40;31;01:mi=00:su=37;41:sg=30;43:ca=00:tw=30;42:ow=34;42:st=37;44:ex=01;32:*.tar=01;31:*.tgz=01;31:*.arc=01;31:*.arj=01;31:*.taz=01;31:*.lha=01;31:*.lz4=01;31:*.lzh=01;31:*.lzma=01;31:*.tlz=01;31:*.txz=01;31:*.tzo=01;31:*.t7z=01;31:*.zip=01;31:*.z=01;31:*.dz=01;31:*.gz=01;31:*.lrz=01;31:*.lz=01;31:*.lzo=01;31:*.xz=01;31:*.zst=01;31:*.tzst=01;31:*.bz2=01;31:*.bz=01;31:*.tbz=01;31:*.tbz2=01;31:*.tz=01;31:*.deb=01;31:*.rpm=01;31:*.jar=01;31:*.war=01;31:*.ear=01;31:*.sar=01;31:*.rar=01;31:*.alz=01;31:*.ace=01;31:*.zoo=01;31:*.cpio=01;31:*.7z=01;31:*.rz=01;31:*.cab=01;31:*.wim=01;31:*.swm=01;31:*.dwm=01;31:*.esd=01;31:*.avif=01;35:*.jpg=01;35:*.jpeg=01;35:*.mjpg=01;35:*.mjpeg=01;35:*.gif=01;35:*.bmp=01;35:*.pbm=01;35:*.pgm=01;35:*.ppm=01;35:*.tga=01;35:*.xbm=01;35:*.xpm=01;35:*.tif=01;35:*.tiff=01;35:*.png=01;35:*.svg=01;35:*.svgz=01;35:*.mng=01;35:*.pcx=01;35:*.mov=01;35:*.mpg=01;35:*.mpeg=01;35:*.m2v=01;35:*.mkv=01;35:*.webm=01;35:*.webp=01;35:*.ogm=01;35:*.mp4=01;35:*.m4v=01;35:*.mp4v=01;35:*.vob=01;35:*.qt=01;35:*.nuv=01;35:*.wmv=01;35:*.asf=01;35:*.rm=01;35:*.rmvb=01;35:*.flc=01;35:*.avi=01;35:*.fli=01;35:*.flv=01;35:*.gl=01;35:*.dl=01;35:*.xcf=01;35:*.xwd=01;35:*.yuv=01;35:*.cgm=01;35:*.emf=01;35:*.ogv=01;35:*.ogx=01;35:*.aac=00;36:*.au=00;36:*.flac=00;36:*.m4a=00;36:*.mid=00;36:*.midi=00;36:*.mka=00;36:*.mp3=00;36:*.mpc=00;36:*.ogg=00;36:*.ra=00;36:*.wav=00;36:*.oga=00;36:*.opus=00;36:*.spx=00;36:*.xspf=00;36:*~=00;90:*#=00;90:*.bak=00;90:*.crdownload=00;90:*.dpkg-dist=00;90:*.dpkg-new=00;90:*.dpkg-old=00;90:*.dpkg-tmp=00;90:*.old=00;90:*.orig=00;90:*.part=00;90:*.rej=00;90:*.rpmnew=00;90:*.rpmorig=00;90:*.rpmsave=00;90:*.swp=00;90:*.tmp=00;90:*.ucf-dist=00;90:*.ucf-new=00;90:*.ucf-old=00;90:"
declare -x MEMORY_PRESSURE_WATCH="/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/session.slice/org.gnome.SettingsDaemon.MediaKeys.service/memory.pressure"
declare -x MEMORY_PRESSURE_WRITE="c29tZSAyMDAwMDAgMjAwMDAwMAA="
declare -x PATH="/home/mlai/snap/code/227/.local/share/../bin:/home/mlai/.local/bin:/home/mlai/ubuntu-blade/ubuntu/year5/ece493/Lab2/ece493-cms/.codex/tmp/arg0/codex-arg0Eu6exz:/usr/local/lib/node_modules/@openai/codex/node_modules/@openai/codex-linux-x64/vendor/x86_64-unknown-linux-musl/path:/home/mlai/snap/code/227/.local/share/../bin:/home/mlai/.cargo/bin:/home/mlai/.config/Code/User/globalStorage/github.copilot-chat/debugCommand:/home/mlai/.config/Code/User/globalStorage/github.copilot-chat/copilotCli:/home/mlai/.cargo/bin:/home/mlai/.cargo/bin:/home/mlai/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin:/snap/bin:/home/mlai/.vscode/extensions/ms-python.debugpy-2025.18.0-linux-x64/bundled/scripts/noConfigScripts"
declare -x PYDEVD_DISABLE_FILE_VALIDATION="1"
declare -x PYTHONSTARTUP="/home/mlai/.config/Code/User/workspaceStorage/0366cff8267da4a36a2c457d3c78badf/ms-python.python/pythonrc.py"
declare -x PYTHON_BASIC_REPL="1"
declare -x QTWEBENGINE_DICTIONARIES_PATH="/usr/share/hunspell-bdic/"
declare -x QT_ACCESSIBILITY="1"
declare -x QT_IM_MODULE="ibus"
declare -x SESSION_MANAGER="local/mlai-blade:@/tmp/.ICE-unix/2283,unix/mlai-blade:/tmp/.ICE-unix/2283"
declare -x SHELL="/bin/bash"
declare -x SHLVL="3"
declare -x SSH_AUTH_SOCK="/run/user/1000/keyring/ssh"
declare -x SYSTEMD_EXEC_PID="2454"
declare -x TERM="xterm-256color"
declare -x TERM_PROGRAM="vscode"
declare -x TERM_PROGRAM_VERSION="1.110.0"
declare -x USER="mlai"
declare -x USERNAME="mlai"
declare -x VSCODE_DEBUGPY_ADAPTER_ENDPOINTS="/home/mlai/.vscode/extensions/ms-python.debugpy-2025.18.0-linux-x64/.noConfigDebugAdapterEndpoints/endpoint-eabe2cb24d807c3a.txt"
declare -x VSCODE_GIT_ASKPASS_EXTRA_ARGS=""
declare -x VSCODE_GIT_ASKPASS_MAIN="/snap/code/227/usr/share/code/resources/app/extensions/git/dist/askpass-main.js"
declare -x VSCODE_GIT_ASKPASS_NODE="/snap/code/227/usr/share/code/code"
declare -x VSCODE_GIT_IPC_HANDLE="/run/user/1000/vscode-git-7e382ec1f0.sock"
declare -x VSCODE_PYTHON_AUTOACTIVATE_GUARD="1"
declare -x VTE_VERSION="7600"
declare -x WAYLAND_DISPLAY="wayland-0"
declare -x XAUTHORITY="/run/user/1000/.mutter-Xwaylandauth.LHDOL3"
declare -x XDG_CONFIG_DIRS="/etc/xdg/xdg-ubuntu-wayland:/etc/xdg"
declare -x XDG_CONFIG_DIRS_VSCODE_SNAP_ORIG="/etc/xdg/xdg-ubuntu-wayland:/etc/xdg"
declare -x XDG_CURRENT_DESKTOP="ubuntu:GNOME"
declare -x XDG_DATA_DIRS="/home/mlai/snap/code/227/.local/share/flatpak/exports/share:/home/mlai/snap/code/227/.local/share:/home/mlai/snap/code/227:/snap/code/227/usr/share:/usr/share/ubuntu-wayland:/usr/share/gnome:/home/mlai/.local/share/flatpak/exports/share:/var/lib/flatpak/exports/share:/usr/local/share/:/usr/share/:/var/lib/snapd/desktop"
declare -x XDG_DATA_DIRS_VSCODE_SNAP_ORIG="/usr/share/ubuntu-wayland:/usr/share/gnome:/home/mlai/.local/share/flatpak/exports/share:/var/lib/flatpak/exports/share:/usr/local/share/:/usr/share/:/var/lib/snapd/desktop"
declare -x XDG_DATA_HOME="/home/mlai/snap/code/227/.local/share"
declare -x XDG_DATA_HOME_VSCODE_SNAP_ORIG=""
declare -x XDG_MENU_PREFIX="gnome-"
declare -x XDG_RUNTIME_DIR="/run/user/1000"
declare -x XDG_SESSION_CLASS="user"
declare -x XDG_SESSION_DESKTOP="ubuntu-wayland"
declare -x XDG_SESSION_TYPE="wayland"
declare -x XMODIFIERS="@im=ibus"
