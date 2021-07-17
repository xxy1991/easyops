#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Time    : 2020-01-26 21：52
@Author  : xxy1991
@Email   : xxy1991@gmail.com
"""
import logging
import argparse
import json
from os import path
from functools import reduce
from typing import List

import requests
from invoke import run, Context

from easyops import Config, SCRIPTS_PATH, Host
from easyops.linux import Debian, Ubuntu
from easyops.linux.apt2 import SourceConfigSet, SourceConfigItem
from easyops.util import write_text

CFG_URI = 'https://develop.xxy.fyi'


class Netboot(object):
    def __init__(self, os: str, host: str):
        self.os = os
        self.__host = host
        self.script_path = path.join(SCRIPTS_PATH, 'netboot.sh')

        self.__config = Config(path='invoke.yml')
        if self.os is None:
            if self.get_config().os is not None:
                self.os = self.get_config().os
            else:
                raise Exception('OS must be specified!')

        uri = CFG_URI + '/sources.json'
        json_text = requests.get(uri).text
        self.__mirror_set = SourceConfigSet(json.loads(json_text))

    @property
    def config(self) -> Config:
        return self.__config

    @config.setter
    def config(self, value: Config) -> None:
        self.__config = value

    @property
    def mirror_set(self) -> SourceConfigSet:
        return self.__mirror_set

    @mirror_set.setter
    def mirror_set(self, value: SourceConfigSet) -> None:
        self.__mirror_set = value

    @property
    def host(self) -> Host:
        return self.get_config()

    @property
    def executor(self) -> Context:
        return self.config.context

    @property
    def mirror(self) -> SourceConfigItem:
        host = self.host
        if '.' in host.mirror:
            return SourceConfigItem(self.os, dict(host=host.mirror))
        else:
            def scheme(schemes: List[str]):
                return 'mirror' not in schemes

            return self.mirror_set.get_mirror(os=self.os, name=host.mirror, scheme=scheme)

    @property
    def mirror_uri(self) -> str:
        return self.mirror.scheme[0] + '://' + self.mirror.host

    def get_config(self) -> Host:
        if self.__host is not None and self.__host in self.config.hosts:
            return self.config.hosts[self.__host]
        elif self.os in self.config.hosts:
            return self.config.hosts[self.os]

    def download(self, ver_code=None):
        if ver_code is None:
            if self.os == 'debian':
                ver_code = Debian.VERSIONS[10]
            elif self.os == 'ubuntu':
                ver_code = Ubuntu.VERSIONS[20]
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

    def get_preseed_cfg(self, hostname: str):
        host = self.get_config()
        proxy = host.proxy
        if proxy is None:
            proxy = ''
        values = dict(
            fqdn=host.fqdn,
            root_password=host.users['root']['password'],
            root_key=host.users['root']['key'],
            username=host.username, fullname=host.fullname,
            user_password=host.users[host.username]['password'],
            user_key=host.users[host.username]['key'],
            proxy=proxy,
            mirror=self.mirror.host,
            gui=host.gui,
            features=host.features,
        )
        if 'network' in host.data:
            values['network_ipv4'] = host.network['ipv4']
            values['network_gateway'] = host.network['gateway']
            values['network_dns'] = host.network['dns']
        if 'post_scripts' in host.data:
            values['post_scripts'] = host.post_scripts
        if hostname:
            values['fqdn'] = '.'.join([hostname, host.domain])
        preseed_cfg = None
        if self.os == 'debian':
            preseed_cfg = Debian.gen_preseed_conf(values)
        elif self.os == 'ubuntu':
            preseed_cfg = Ubuntu.gen_preseed_conf(values)
        return preseed_cfg

    def gen_preseed(self, hostname: str = None):
        preseed_cfg = self.get_preseed_cfg(hostname)
        if preseed_cfg is not None:
            file_path = path.abspath('pressed.cfg')
            write_text(preseed_cfg, file_path)
            run(' '.join([self.script_path, 'netboot_preseed', self.os, file_path]))

    def attach_data(self):
        if self.host.files is None:
            return
        files = self.host.files
        for file in files:
            if path.exists(file):
                run(' '.join([self.script_path,
                              'netboot_attach',
                              self.os,
                              path.relpath(file),
                              path.abspath(path.curdir)]))
            else:
                logging.warning("File: " + path.abspath(file) + " is not found!")


def get_args(args=None):
    parser = argparse.ArgumentParser(description='Linux netboot installer.')
    parser.add_argument('--os', choices=['debian', 'ubuntu'], help="the distribution's name")
    parser.add_argument('-V', '--version', action='version',
                        version='%(prog)s 0.1.0',
                        help="the distribution's major version")
    parser.add_argument('-T', '--target', help='target name')
    parser.add_argument('-H', help='hostname')
    parser.add_argument('-M', '--manual', action="store_true", help='manual mode')

    if args is not None:
        return parser.parse_args(args)
    return parser.parse_args()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    options = get_args()
    if not options.target and not options.os:
        raise Exception('Target or OS is required!')
    netboot = Netboot(options.os, options.target)

    logging.info("Start download netboot files...")
    netboot.download()
    logging.info("Netboot files had downloaded.")

    logging.info("Start download netboot files...")
    netboot.update_grub()
    logging.info("Grub config had updated.")

    if not options.manual:
        netboot.gen_preseed(options.H)
        netboot.attach_data()
