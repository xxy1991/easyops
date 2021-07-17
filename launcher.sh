#!/usr/bin/env bash
# created by xxy1991

CFG_URI='https://cfg.ori.fyi'
PIP_MIRROR='https://mirrors.aliyun.com/pypi/simple'

# check_py3()
check_py3() {
    apt -yqq update
    PYTHON_VER=$(python3 -V 2>&1 | awk '{print $2}')
    if ! [[ $PYTHON_VER == 3* ]]; then
        apt install -yqq python3
    fi
    PIP_VER=$(pip3 -V 2>&1 | awk '{print $2}')
    if ! [[ $PIP_VER == 9* ]]; then
        apt install -yqq python3-pip
    fi
    pip3 install -q -i "$PIP_MIRROR" sortedcontainers requests invoke jinja2
}

# exec_script(str agrs)
exec_script() {
    python3 -m easyops.netboot "$@"
}

check_py3
pip3 install --no-deps --ignore-installed easyops-0.1.0-py2.py3-none-any.whl
exec_script "$@"
