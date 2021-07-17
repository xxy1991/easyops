#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Time    : 2020-01-31 18:35
@Author  : xxy1991
@Email   : xxy1991@gmail.com
"""
import json
import unittest

from easyops import Config
from easyops.linux import Ubuntu
from easyops.linux.apt2 import SourceConfigSet


class TestUbuntu(unittest.TestCase):
    def setUp(self) -> None:
        self.config = Config(path='tests/invoke.yml')
        self.invoke = self.config.context

        with open('./sources.json', 'r') as f:
            self.mirror_set = SourceConfigSet(json.load(f))

    def test_gen_grub(self) -> None:
        config = Ubuntu.gen_grub()
        with open('tests/ubuntu/grub-msdos.cfg', 'r') as f:
            example = f.read()
        self.assertEqual(example, config)

    def test_gen_preseed(self) -> None:
        host = self.config.hosts['ubuntu']
        mirror = None
        proxy = ''
        if host.proxy is not None:
            proxy = host.proxy
        values = dict(
            fqdn=host.fqdn,
            root_password=host.users['root']['password'],
            username=host.username, fullname=host.fullname,
            user_password=host.users[host.username]['password'],
            proxy=proxy,
            gui=host.gui,
        )
        if '.' not in host.mirror:
            mirror = Ubuntu.MIRRORS[host.mirror]
        values['mirror'] = mirror
        config = Ubuntu.gen_preseed_conf(values)
        with open('tests/ubuntu/preseed-std-18.cfg', 'r') as f:
            example = f.read()
        self.assertEqual(example, config)
