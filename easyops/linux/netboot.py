#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Time    : 2020-01-31 18:49
@Author  : xxy1991
@Email   : xxy1991@gmail.com
"""

from jinja2 import Template

from .. import path_join
from ..util import read_text


def netboot(cls):
    def gen_grub():
        src_path = path_join("templates", "boot", "grub-msdos.cfg.j2")
        cfg_src = read_text(src_path)

        os_name = cls.__name__.lower()
        return Template(cfg_src).render(os=os_name)

    cls.gen_grub = staticmethod(gen_grub)

    return cls
