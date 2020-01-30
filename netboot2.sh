#!/usr/bin/env bash
# created by xxy1991

CFG_URI='https://cfg.ori.fyi'

# check_py3()
check_py3() {
  PYTHON_VER=$(python3 -V 2>&1 | awk '{print $2}')
  if ! [[ $PYTHON_VER == 3* ]]; then
    apt install -yqq python3
  fi
  PIP_VER=$(pip3 -V 2>&1 | awk '{print $2}')
  if ! [[ $PIP_VER == 9* ]]; then
    apt install -yqq python3-pip
  fi
  pip3 -q install requests invoke
}

# download_script()
download_script() {
  wget -Nq "${CFG_URI}/netboot.py"
}

# exec_script(str agrs)
exec_script() {
  python3 netboot.py "$@"
}

check_py3
download_script
exec_script "$@"
