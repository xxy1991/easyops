#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Time    : 2020-01-31 18:36
@Author  : xxy1991
@Email   : xxy1991@gmail.com
"""
from typing import List


class Host(object):
    def __init__(self, config: dict):
        """Constructor"""
        self._data = {}
        fields = ['host', 'domain', 'port', 'os', 'mirror', 'proxy',
                  'username', 'fullname',
                  'features', 'gui', 'files']
        for field in fields:
            if field in config:
                self._data[field] = config[field]
            else:
                self._data[field] = None
        if 'users' in config:
            self._data['users'] = {}
            users = config['users']
            for item in users:
                user = users[item]
                self._data['users'][item] = dict(
                    key=user['key'], password=user['password'])
        if 'network' in config:
            network = config['network']
            self._data['network'] = dict(
                ipv4=network['ipv4'],
                gateway=network['gateway'],
                dns=network['dns']
            )
        if 'postScripts' in config:
            self._data['post_scripts'] = config['postScripts']

    @property
    def data(self):
        return self._data

    @property
    def host(self):
        return self._data['host']

    @property
    def domain(self):
        return self._data['domain']

    @property
    def fqdn(self):
        return '.'.join([self.host, self.domain])

    @property
    def network(self):
        return self._data['network']

    @property
    def port(self):
        return self._data['port']

    @property
    def os(self) -> str:
        return self._data['os']

    @property
    def mirror(self):
        return self._data['mirror']

    @property
    def proxy(self):
        return self._data['proxy']

    @property
    def username(self) -> str:
        return self._data['username']

    @property
    def fullname(self) -> str:
        return self._data['fullname']

    @property
    def users(self):
        return self._data['users']

    @property
    def features(self) -> List[str]:
        return self._data['features']

    @property
    def gui(self):
        return self._data['gui']

    @property
    def files(self):
        return self._data['files']

    @property
    def post_scripts(self) -> List[str]:
        return self._data['post_scripts']
