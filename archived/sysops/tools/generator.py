#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from subprocess import call as call

from jinja2 import Template as Template

from sysops.config import Config
from sysops.config import path_join, CFG_WEB_PATH, CONF_PATH, SH_PATH, CONF_PRESEED_PATH, BUILD_TMP_PATH
from sysops.config.linux import Debian, Ubuntu
from sysops.config.util import read_text, write_text, sudo
from sysops.tools.docker import Docker


# def gen_apt(key):
#     config = Config()
#     host = config.Hosts[key]
#     if host.os is not None and host.mirror is not None:
#         if host.os == 'debian':
#             Debian.gen_apt_src(mirror=host.mirror, write=True, dst_path=key)
#         if host.os == 'ubuntu':
#             Ubuntu.gen_apt_src(mirror=host.mirror, write=True, dst_path=key)


def gen_apt():
    config = Config()
    for key in config.hosts:
        host = config.hosts[key]
        if host.os is not None and host.mirror is not None:
            if host.os == 'debian':
                Debian.gen_apt_src(mirror=host.mirror, write=True, dst_path=key)
            if host.os == 'ubuntu':
                Ubuntu.gen_apt_src(mirror=host.mirror, write=True, dst_path=key)
    ctx = Config().context
    base_path = path_join(BUILD_TMP_PATH, 'apt')
    with ctx.cd(base_path):
        ctx.run('cp sources.list.dsstd sources.list.debian')
        ctx.run('cp sources.list.ubstd sources.list.ubuntu')


def gen_preseed():
    config = Config()
    for key in config.hosts:
        host = config.hosts[key]
        if host.os is not None:
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
            if host.os == 'debian':
                if '.' not in host.mirror:
                    mirror = Debian.MIRRORS[host.mirror]
                values['mirror'] = mirror
                Debian.gen_preseed_conf(values, write=True, dst_path=key)
            if host.os == 'ubuntu':
                if '.' not in host.mirror:
                    mirror = Ubuntu.MIRRORS[host.mirror]
                values['mirror'] = mirror
                Ubuntu.gen_preseed_conf(values, write=True, dst_path=key)
    ctx = Config().context
    base_path = path_join(BUILD_TMP_PATH, 'boot')
    with ctx.cd(base_path):
        ctx.run('cp preseed-dsstd.cfg preseed-debian.cfg')
        ctx.run('cp preseed-ubstd.cfg preseed-ubuntu.cfg')


def gen_grub():
    src_path = path_join(CONF_PRESEED_PATH, "grub-msdos.cfg.j2")
    cfg_src = read_text(src_path)

    cfg_dst = Template(cfg_src).render(os="debian")
    dst_path = path_join(BUILD_TMP_PATH, "boot", "msdos-debian.cfg")
    write_text(cfg_dst, dst_path)

    cfg_dst = Template(cfg_src).render(os="ubuntu")
    dst_path = path_join(BUILD_TMP_PATH, "boot", "msdos-ubuntu.cfg")
    write_text(cfg_dst, dst_path)


def shell(*args):
    call(*args, shell=True)


if __name__ == '__main__':
    invoke = Config().context
    invoke.run('rm -fR ' + BUILD_TMP_PATH)
    invoke.run('mkdir -p ' + BUILD_TMP_PATH)

    gen_apt()
    gen_preseed()
    gen_grub()

    call(['mkdir', '-p', path_join(BUILD_TMP_PATH, 'keys')])
    invoke.run('cp ' + path_join(CONF_PATH, 'keys', '*.pub ' + path_join(BUILD_TMP_PATH, 'keys')))
    call(['mkdir', '-p', path_join(BUILD_TMP_PATH, 'scripts')])
    invoke.run('cp ' + path_join(SH_PATH, '*.sh ' + path_join(BUILD_TMP_PATH, 'scripts')))
    invoke.run('cp ' + path_join(SH_PATH, '*.py ' + path_join(BUILD_TMP_PATH, 'scripts')))
    invoke.run('cp ' + path_join(SH_PATH, '*.json ' + path_join(BUILD_TMP_PATH, 'scripts')))
    call(['mkdir', '-p', path_join(BUILD_TMP_PATH, 'rancher')])
    invoke.run('cp ' + path_join(CONF_PATH, 'rancher', '*.yml ' + path_join(BUILD_TMP_PATH, 'rancher')))

    invoke.run('rm -fR ' + CFG_WEB_PATH)
    invoke.run('mkdir -p ' + path_join(CFG_WEB_PATH, 'web'))

    invoke.run('cp -r ' + BUILD_TMP_PATH + '/apt ' + path_join(CFG_WEB_PATH, 'web'))
    invoke.run('cp -r ' + BUILD_TMP_PATH + '/boot ' + path_join(CFG_WEB_PATH, 'web'))
    invoke.run('cp -r ' + BUILD_TMP_PATH + '/keys ' + path_join(CFG_WEB_PATH, 'web'))
    invoke.run('cp -r ' + BUILD_TMP_PATH + '/scripts/* ' + path_join(CFG_WEB_PATH, 'web'))
    invoke.run('cp -r ' + BUILD_TMP_PATH + '/rancher ' + path_join(CFG_WEB_PATH, 'web'))

    cert_path = path_join(CFG_WEB_PATH, 'cert')
    cert_live_path = '../docker/certbot/config/live'
    invoke.run('mkdir -p ' + cert_path)
    invoke.run('cp ' + cert_live_path + '/cfg.ori.fyi/fullchain.pem ' + cert_path + '/cfg-ori-fyi.crt')
    invoke.run('cp ' + cert_live_path + '/cfg.ori.fyi/privkey.pem ' + cert_path + '/cfg-ori-fyi.key')
    invoke.run('cp ../docker/sysops/nginx/cfg-ori-fyi-ssl.conf ' + CFG_WEB_PATH)
    invoke.run('cp ../docker/sysops/nginx/nginx.Dockerfile ' + CFG_WEB_PATH)
