#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Time    : 2020-01-31 18:49
@Author  : xxy1991
@Email   : xxy1991@gmail.com
"""

from jinja2 import Template

from .. import path_join, path_sep, CONF_APT_PATH, BUILD_TMP_PATH
from ..util import write_text, read_text

import os


def netboot(cls):
    def gen_grub():
        src_path = path_join("templates", "boot", "msdos.grub.j2")
        print(os.getcwd())
        cfg_src = read_text(src_path)

        os_name = cls.__name__.lower()
        cfg_dst = Template(cfg_src).render(os=os_name)
        dst_path = path_join(BUILD_TMP_PATH, "boot", "msdos-debian.cfg")
        # write_text(cfg_dst, dst_path)
        return cfg_dst

    cls.gen_grub = staticmethod(gen_grub)

    return cls
