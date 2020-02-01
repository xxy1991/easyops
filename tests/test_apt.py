#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Time    : 2020-02-02 00:02
@Author  : xxy1991
@Email   : xxy1991@gmail.com
"""

import unittest

import json
from easyops.linux import apt2


class TestNetBoot(unittest.TestCase):
    def setUp(self) -> None:
        with open('./sources.json', 'r') as f:
            self.src_list = json.load(f)

    def test_get_source(self) -> None:
        src_cfg = apt2.get_source(self.src_list)
        self.assertEqual('ustc', src_cfg['name'])
        src_cfg = apt2.get_source(self.src_list, name='none')
        self.assertTrue(src_cfg['default'])
        src_cfg = apt2.get_source(self.src_list, name='163')
        self.assertEqual('mirrors.163.com', src_cfg['host'])
        src_cfg = apt2.get_source(self.src_list, os='debian', location='hk')
        self.assertEqual('auto', src_cfg['name'])
