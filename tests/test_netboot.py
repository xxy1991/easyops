#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Time    : 2020-02-02 00:02
@Author  : xxy1991
@Email   : xxy1991@gmail.com
"""

import unittest
from unittest.mock import patch

import json

from easyops import Config, Host
from easyops.linux import apt2
from netboot import get_args, Netboot


class TestNetBoot(unittest.TestCase):
    def setUp(self) -> None:
        with open('./sources.json', 'r') as f:
            self.src_list = json.load(f)

        self.config = Config(path='tests/invoke.yml')
        self.invoke = self.config.context

    def test_args(self) -> None:
        args = get_args(['debian', '-H', 'vm-tmp-dstd'])
        self.assertEqual('debian', args.os)
        self.assertEqual('vm-tmp-dstd', args.H)
        self.assertFalse(args.manual)
        netboot = Netboot(args.os, args.H)
        # with patch.object(netboot, 'config', self.config), \
        #      patch.object(netboot, 'src_list', self.src_list):
        netboot.config = self.config
        netboot.src_list = self.src_list
        host = netboot.get_config()
        print(host.data)
        mirror = netboot.get_mirror()
        print(mirror)
        # netboot.download()

        print(args)


def test_get_sources(self) -> None:
    # get_sources()
    # src_cfg = get_by_area(self.src_list, 'debian', 'hk')
    # self.assertEqual(src_cfg['addr'], 'mirror.xtom.com.hk')
    pass
