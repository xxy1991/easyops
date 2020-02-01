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

from easyops.util import write_text
from easyops.linux import Debian, Ubuntu

CFG_URI = 'https://cfg.ori.fyi'


def get_sources2(os=None, name=None, area=None):
    uri = CFG_URI + '/sources.json'
    json_text = requests.get(uri).text
    json2 = json.loads(json_text)
    print(json2)

    os = name.split('.')[0]
    name = name.split('.')[1]
    json2 = json2[os]


def get_sources(os=None, name=None, area=None):
    uri = CFG_URI + '/sources.json'
    src_list = json.loads(requests.get(uri).text)

    run('sh ./scripts/netboot.sh test')

    # os = name.split('.')[0]
    # name = name.split('.')[1]
    # json2 = json2[os]


def netboot_download(os, ver_code):
    file_name = 'netboot.tar.gz'
    cmd = 'wget -Nq "' + CFG_URI + '/' + os + '/dists/' + ver_code \
          + '/main/installer-amd64/current/images/netboot/' + file_name + '"'
    run(cmd)
    run('tar -zxf ' + file_name)


def netboot_grub(os):
    grub_cfg = None
    if os == 'debian':
        grub_cfg = Debian.gen_grub()
    elif os == 'ubuntu':
        grub_cfg = Ubuntu.gen_grub()
    if grub_cfg is not None:
        write_text('grub-msdos.cfg', grub_cfg)
        run('scripts/netboot.sh netboot_grub')


def get_config(config, os, host=None):
    if host is not None and host in config.hosts:
        return config.hosts[host]
    elif os in config.hosts:
        return config.hosts[os]


def get_args(args):
    parser = argparse.ArgumentParser(description='Linux netboot installer.')
    parser.add_argument('os', choices=['debian', 'ubuntu'], help='os name that install')
    parser.add_argument('-H', help='Hostname')
    parser.add_argument('-m', '--manual', action="store_true", help='manual mode')

    return parser.parse_args(args)


def main():
    get_sources()


if __name__ == "__main__":
    main()
