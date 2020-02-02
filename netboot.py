#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Time    : 2020-01-26 21：52
@Author  : xxy1991
@Email   : xxy1991@gmail.com
"""

import sys
import argparse
import json

import requests
from invoke import run

from easyops import Config
from easyops.util import write_text
from easyops.linux import Debian, Ubuntu, apt2

CFG_URI = 'https://cfg.ori.fyi'


class Netboot(object):
    def __init__(self, os, host):
        self.os = os
        self.host = host

        self.config = Config(path='invoke.yml')

        uri = CFG_URI + '/sources.json'
        json_text = requests.get(uri).text
        self.src_list = json.loads(json_text)

    def get_config(self):
        if self.host is not None and self.host in self.config.hosts:
            return self.config.hosts[self.host]
        elif self.os in self.config.hosts:
            return self.config.hosts[self.os]

    def get_mirror(self):
        def scheme(src):
            return not ('scheme' in src and 'mirror' in src['scheme'])

        mirror = apt2.get_source(self.src_list, self.os, scheme=scheme)
        scheme_name = 'http'
        if 'scheme' in mirror:
            scheme_name = mirror['scheme']
        return scheme_name + '://' + mirror['host']

    def download(self, ver_code=None):
        if ver_code is None:
            if self.os == 'debian':
                ver_code = Debian.VERSIONS[9]
            elif self.os == 'ubuntu':
                ver_code = Ubuntu.VERSIONS[18]
        run(' '.join(['./scripts/netboot.sh', 'netboot_download', self.get_mirror(), self.os, ver_code]))


def netboot_grub(os):
    grub_cfg = None
    if os == 'debian':
        grub_cfg = Debian.gen_grub()
    elif os == 'ubuntu':
        grub_cfg = Ubuntu.gen_grub()
    if grub_cfg is not None:
        write_text('grub-msdos.cfg', grub_cfg)
        run('scripts/netboot.sh netboot_grub')


def get_args(args=None):
    parser = argparse.ArgumentParser(description='Linux netboot installer.')
    parser.add_argument('os', choices=['debian', 'ubuntu'], help='os name that install')
    parser.add_argument('-H', help='Hostname')
    parser.add_argument('-m', '--manual', action="store_true", help='manual mode')

    if args is not None:
        return parser.parse_args(args)
    return parser.parse_args()


if __name__ == "__main__":
    options = get_args()
    netboot = Netboot(options.os, options.H)
    netboot.download()
