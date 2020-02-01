#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Time    : 2020-01-31 11:38
@Author  : xxy1991
@Email   : xxy1991@gmail.com
"""

import unittest

import json
from netboot import get_default, get_by_name, get_by_area, get_sources, get_args


class TestNetBoot(unittest.TestCase):
    def setUp(self) -> None:
        with open('./sources.json', 'r') as f:
            self.src_list = json.load(f)

    def test_args(self) -> None:
        args = get_args(['debian', '-H', 'vm-tmp-dstd'])
        self.assertEqual(args.os, 'debian')
        self.assertEqual(args.H, 'vm-tmp-dstd')
        self.assertFalse(args.manual)
        print(args)

    def test_get_default(self) -> None:
        src_cfg = get_default(self.src_list)
        self.assertEqual(src_cfg['addr'], 'mirrors.ustc.edu.cn')

    def test_get_by_name(self) -> None:
        src_cfg = get_by_name(self.src_list, 'none')
        self.assertIsNone(src_cfg)
        src_cfg = get_by_name(self.src_list, '163')
        self.assertEqual(src_cfg['addr'], 'mirrors.163.com')

    def test_get_by_area(self) -> None:
        src_cfg = get_by_area(self.src_list, 'debian', 'hk')
        # self.assertEqual(src_cfg['addr'], 'mirror.xtom.com.hk')

    def test_get_sources(self) -> None:
        get_sources()
        # src_cfg = get_by_area(self.src_list, 'debian', 'hk')
        # self.assertEqual(src_cfg['addr'], 'mirror.xtom.com.hk')
