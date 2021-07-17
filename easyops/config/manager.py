#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Time    : 2020-01-31 18:36
@Author  : xxy1991
@Email   : xxy1991@gmail.com
"""

from invoke import Config as InvCfg, Context as InvCtx
from sortedcontainers import SortedSet

from .host import Host
from ..util import singleton


def _config_merge(default: dict, host: dict) -> dict:
    for key in host:
        if key not in default:
            default[key] = host[key]
        else:
            if isinstance(host[key], str):
                default[key] = host[key]
            elif isinstance(host[key], list):
                default[key] = SortedSet(list(default[key]) + host[key])
            elif isinstance(host[key], dict):
                _config_merge(default[key], host[key])
    return default


@singleton
class Config(object):
    def __init__(self, ctx=None, path=None):
        if ctx is None:
            # cfg = InvCfg(project_location='../configs')
            # cfg.load_project()
            if path is not None:
                cfg = InvCfg(runtime_path=path)
                cfg.load_runtime()
                self.__context = InvCtx(cfg)
            else:
                self.__context = InvCtx()
        else:
            self.__context = ctx

        self.__hosts = {}
        if 'Hosts' in self.config:
            hosts = self.config.Hosts
            default = hosts['default']

            for key in hosts:
                if key == 'default':
                    continue
                host = Host(_config_merge(dict(default), dict(hosts[key])))
                self.__hosts[key] = host

    @property
    def hosts(self):
        return self.__hosts

    @property
    def context(self) -> InvCtx:
        return self.__context

    @property
    def config(self) -> InvCfg:
        return self.context.config
