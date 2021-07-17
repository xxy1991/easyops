#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Time    : 2020-01-31 18:49
@Author  : xxy1991
@Email   : xxy1991@gmail.com
"""

from jinja2 import Template

from .. import path_join, TEMPLATES_PATH
from ..util import read_text


def netboot(cls):
    def gen_grub():
        src_path = path_join(TEMPLATES_PATH, 'boot', 'grub-msdos.cfg.j2')
        cfg_src = read_text(src_path)

        os_name = cls.__name__.lower()
        return Template(cfg_src).render(os=os_name)

    def gen_preseed2(sys, values, ver_code=None):
        src_path = path_join(TEMPLATES_PATH, 'boot')
        if ver_code is None:
            src_path = path_join(src_path, "preseed-" + sys + ".cfg.j2")
        else:
            src_path = path_join(src_path, "preseed-" + sys + '-' + ver_code + ".cfg.j2")
        cfg_src = read_text(src_path)
        cfg_dst = Template(cfg_src).render(values)
        return cfg_dst

    cls.gen_grub = staticmethod(gen_grub)
    cls.gen_preseed2 = staticmethod(gen_preseed2)

    return cls
