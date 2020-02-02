#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from invoke import Config as InvCfg, Context as InvCtx

from ..util import singleton
from .host import Host


def _config_merge(default, host):
    for key in host:
        if key not in default:
            default[key] = host[key]
        else:
            if isinstance(host[key], str):
                default[key] = host[key]
            else:
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
    def context(self):
        return self.__context

    @property
    def config(self):
        return self.context.config
