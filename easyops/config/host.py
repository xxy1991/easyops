#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class Host(object):
    def __init__(self, config):
        """Constructor"""
        self._data = {}
        fields = ['host', 'domain', 'port', 'os', 'mirror', 'proxy', 'username', 'fullname', 'features', 'gui']
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
                self._data['users'][item] = dict(key=user['key'], password=user['password'])

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
        return self.host + '.' + self.domain

    @property
    def port(self):
        return self._data['port']

    @property
    def os(self):
        return self._data['os']

    @property
    def mirror(self):
        return self._data['mirror']

    @property
    def proxy(self):
        return self._data['proxy']

    @property
    def username(self):
        return self._data['username']

    @property
    def fullname(self):
        return self._data['fullname']

    @property
    def users(self):
        return self._data['users']

    @property
    def features(self):
        return self._data['features']

    @property
    def gui(self):
        return self._data['gui']
