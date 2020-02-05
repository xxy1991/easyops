#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Time    : 2020-01-26 21：52
@Author  : xxy1991
@Email   : xxy1991@gmail.com
"""
from os import path
import argparse
import json

import requests
from invoke import run, Context

from easyops import Config, SCRIPTS_PATH, Host
from easyops.util import write_text
from easyops.linux import Debian, Ubuntu, apt2

CFG_URI = 'https://cfg.ori.fyi'


class Netboot(object):
    def __init__(self, os, host):
        self.os = os
        self.__host = host
        self.script_path = path.join(SCRIPTS_PATH, 'netboot.sh')

        self.__config = Config(path='invoke.yml')

        uri = CFG_URI + '/sources.json'
        json_text = requests.get(uri).text
        self.src_list = json.loads(json_text)

    @property
    def config(self) -> Config:
        return self.__config

    @config.setter
    def config(self, value) -> None:
        self.__config = value

    @property
    def host(self) -> Host:
        return self.get_config()

    @property
    def executor(self) -> Context:
        return self.config.context

    @property
    def mirror(self) -> dict:
        host = self.host
        if '.' in host.mirror:
            return dict(host=host.mirror)
        else:
            def scheme(src):
                return not ('scheme' in src and 'mirror' in src['scheme'])

            return apt2.get_source(self.src_list, name=host.mirror, os=self.os, scheme=scheme)

    @property
    def mirror_scheme(self) -> []:
        if 'scheme' not in self.mirror:
            return ['http']
        else:
            return self.mirror['scheme']

    @property
    def mirror_uri(self) -> str:
        return self.mirror_scheme[0] + '://' + self.mirror['host']

    def get_config(self):
        if self.__host is not None and self.__host in self.config.hosts:
            return self.config.hosts[self.__host]
        elif self.os in self.config.hosts:
            return self.config.hosts[self.os]

    def download(self, ver_code=None):
        if ver_code is None:
            if self.os == 'debian':
                ver_code = Debian.VERSIONS[9]
            elif self.os == 'ubuntu':
                ver_code = Ubuntu.VERSIONS[18]
        run(' '.join([self.script_path, 'netboot_download', self.mirror_uri, self.os, ver_code]))

    def update_grub(self):
        grub_cfg = None
        if self.os == 'debian':
            grub_cfg = Debian.gen_grub()
        elif self.os == 'ubuntu':
            grub_cfg = Ubuntu.gen_grub()
        if grub_cfg is not None:
            file_path = path.abspath('grub-msdos.cfg')
            write_text(grub_cfg, file_path)
            run(' '.join([self.script_path, 'netboot_grub', file_path]))

    def gen_preseed(self):
        host = self.get_config()
        proxy = host.proxy
        if proxy is None:
            proxy = ''
        values = dict(
            fqdn=host.fqdn,
            root_password=host.users['root']['password'],
            username=host.username, fullname=host.fullname,
            user_password=host.users[host.username]['password'],
            proxy=proxy,
            mirror=self.mirror['host'],
            gui=host.gui,
        )
        preseed_cfg = None
        if self.os == 'debian':
            preseed_cfg = Debian.gen_preseed_conf(values)
        elif self.os == 'ubuntu':
            preseed_cfg = Ubuntu.gen_preseed_conf(values)
        if preseed_cfg is not None:
            file_path = path.abspath('pressed.cfg')
            write_text(preseed_cfg, file_path)
            run(' '.join([self.script_path, 'netboot_preseed', self.os, file_path]))


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
    netboot.update_grub()
    netboot.gen_preseed()
