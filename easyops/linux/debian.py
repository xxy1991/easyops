#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Time    : 2020-01-31 18:36
@Author  : xxy1991
@Email   : xxy1991@gmail.com
"""

from .deblike import deblike


@deblike
class Debian(object):

    @staticmethod
    def gen_preseed_conf(values, ver_code=None):
        cfg_dst = Debian.gen_preseed2('debian', values, ver_code)
        return cfg_dst

    @staticmethod
    def gen_apt_src(mirror=None, dir_main='debian', dir_sec='debian-security',
                    version=None, contrib=True, non_free=True,
                    backports=False, src=True, write=False, dst_path=None):
        if mirror is None:
            mirror = Debian.MIRRORS['auto']
        elif '.' not in mirror:
            mirror = Debian.MIRRORS[mirror]
        if version is None:
            version = 10
        repotype = Debian.REPO_TYPES
        if not contrib:
            repotype.remove('contrib')
        if not non_free:
            repotype.remove('non-free')
        values = dict(
            mirror=mirror, dir_main=dir_main, dir_sec=dir_sec,
            version=Debian.VERSIONS[version],
            repotype=' '.join(repotype),
        )
        return Debian.gen_src_list(values, backports, src, write, dst_path)


Debian.VERSIONS = {
    10: 'buster',
    9: 'stretch',
}

Debian.MIRRORS.update({
    'cn': 'ftp.cn.debian.org',
    'hk': 'ftp.hk.debian.org',
    'sg': 'ftp.sg.debian.org',
    'kr': 'ftp.kr.debian.org',
    'jp': 'ftp.jp.debian.org',
    'tw': 'ftp.tw.debian.org',
    'us': 'ftp.us.debian.org',
    'sec': 'security.debian.org',
    'arc': 'archive.debian.org',
    'auto': 'deb.debian.org',
})

Debian.REPO_TYPES = ['main', 'contrib', 'non-free']
