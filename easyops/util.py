#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Time    : 2020-01-31 18:36
@Author  : xxy1991
@Email   : xxy1991@gmail.com
"""

from functools import wraps
from os import makedirs
from os.path import dirname, exists, isfile


def singleton(cls):
    _instances = {}

    @wraps(cls)
    def _singleton(*args, **kwargs):
        key = repr(cls) + repr(frozenset(kwargs.items()))
        if key not in _instances:
            _instances[key] = cls(*args, **kwargs)
        return _instances[key]

    return _singleton


def sudo(ctx, path, command):
    cmd = 'bash -c "cd ' + path + ' && '
    cmd += command
    cmd += '"'
    ctx.sudo(cmd)


def mkdir(path, f=False):
    if not f and exists(path) and isfile(path):
        f = True
    if f:
        path = dirname(path)
    if not exists(path):
        makedirs(path)


def read_text(path):
    with open(path, 'r') as f:
        text = f.read()
    return text


def write_text(text, path):
    mkdir(path, True)
    with open(path, 'w') as f:
        f.write(text)
