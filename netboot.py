#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Time    : 2020-01-26 21：52
@Author  : xxy1991
@Email   : xxy1991@gmail.com
"""

import sys
import json

import requests
from invoke import run

CFG_URI = 'https://cfg.ori.fyi'


def get_sources2(os=None, name=None, area=None):
    uri = CFG_URI + '/sources.json'
    json_text = requests.get(uri).text
    json2 = json.loads(json_text)
    print(json2)

    os = name.split('.')[0]
    name = name.split('.')[1]
    json2 = json2[os]


def get_default(src_list):
    for src in src_list['common']:
        if 'default' in src and src['default']:
            return src


def get_by_name(src_list, name):
    for os in src_list:
        for src in src_list[os]:
            if src['name'] == name:
                return src


def get_by_area(src_list, os, area):
    if os in src_list:
        for src in src_list[os]:
            if src['area'] == area and \
                    ('area-default' in src and src['area-default']):
                return src
    else:
        return get_by_area(src_list, 'common', area)


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


def main():
    print('arg num : ', len(sys.argv))
    print('args : ', sys.argv)
    print('script name : ', sys.argv[0])

    for i in range(len(sys.argv)):
        print("arg[{0}] = {1}".format(i, sys.argv[i]))

    get_sources()


if __name__ == "__main__":
    main()
