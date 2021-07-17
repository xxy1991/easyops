#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Time    : 2020-02-02 00:02
@Author  : xxy1991
@Email   : xxy1991@gmail.com
"""

import json
import unittest
from typing import List

from easyops.linux.apt2 import SourceConfigSet, SourceConfigItem


class TestApt(unittest.TestCase):
    def setUp(self) -> None:
        with open('./sources.json', 'r') as f:
            self.src_list = json.load(f)

        self.configSet = SourceConfigSet(self.src_list)

    def test_config_set(self) -> None:
        config = self.configSet.get_mirror()
        self.assertEqual('aly', config.name)
        config = self.configSet.get_mirror(name='163')
        config = self.configSet.get_by_name(os='common', name='163')
        self.assertEqual('mirrors.163.com', config.host)
        config = self.configSet.get_mirror(os='debian', location='hk')
        self.assertEqual('auto', config.name)
        self.assertEqual('debian', config.os)

        def scheme(schemes: List[str]):
            return 'mirror' not in schemes

        config = self.configSet.get_mirror(os='ubuntu', scheme=scheme)
        self.assertEqual('aly', config.name)
        self.assertTrue(scheme(config.scheme))
