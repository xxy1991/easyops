#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Time    : 2020-01-31 18:36
@Author  : xxy1991
@Email   : xxy1991@gmail.com
"""

from jinja2 import Template

from .apt import apt_gen
from .netboot import netboot
from .. import path_join, path_sep, CONF_PRESEED_PATH, BUILD_TMP_PATH
from ..util import write_text, read_text


def deblike(cls):
    cls = apt_gen(cls)
    cls = netboot(cls)

    def gen_preseed(sys, values, write=False, dst_path=None):
        src_path = path_join(CONF_PRESEED_PATH, "preseed-" + sys + ".cfg.j2")
        cfg_src = read_text(src_path)
        cfg_dst = Template(cfg_src).render(values)
        if write:
            base_path = path_join(BUILD_TMP_PATH, "boot", "preseed-")
            if dst_path is None:
                dst_path = path_join(base_path + sys + '.cfg')
            elif path_sep not in dst_path:
                dst_path = path_join(base_path + dst_path + '.cfg')
            write_text(cfg_dst, dst_path)
        return cfg_dst

    cls.VERSIONS = {}
    cls.gen_preseed = staticmethod(gen_preseed)

    return cls
