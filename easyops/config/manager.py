#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from functools import wraps

from invoke import Config as InvCfg, Context as InvCtx

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


def singleton(cls):
    _instances = {}

    @wraps(cls)
    def _singleton(*args, **kwargs):
        if cls not in _instances:
            _instances[cls] = cls(*args, **kwargs)
        return _instances[cls]

    return _singleton


@singleton
class Config(object):
    def __init__(self, ctx=None, path=None):
        self._hosts = {}
        if ctx is None:
            # cfg = InvCfg(project_location='../configs')
            # cfg.load_project()
            if path is not None:
                cfg = InvCfg(runtime_path=path)
                cfg.load_runtime()
                self._context = InvCtx(cfg)
        else:
            self._context = ctx

        hosts = self.config.Hosts
        default = hosts['default']
        for key in hosts:
            if key == 'default':
                continue
            host = Host(_config_merge(dict(default), dict(hosts[key])))
            self._hosts[key] = host

    @property
    def hosts(self):
        return self._hosts

    @property
    def context(self):
        return self._context

    @property
    def config(self):
        return self.context.config
