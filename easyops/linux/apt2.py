#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Time    : 2020-02-01 23:59
@Author  : xxy1991
@Email   : xxy1991@gmail.com
"""


# class

def get_by_name(src_list, name, os=None):
    if os is None:
        for os2 in src_list:
            result = get_by_name(src_list, name, os2)
            if result is not None:
                return result
    elif os in src_list:
        for src in src_list[os]:
            if src['name'] == name:
                return src
    else:
        return get_by_name(src_list, 'common', name)


def get_default(src_list, os, location=None, scheme=None):
    if os in src_list:
        for src in src_list[os]:
            if scheme is not None and not scheme(src):
                continue
            if location is not None:
                if 'location' in src and src['location'] != location:
                    continue
                elif 'location-default' in src and src['location-default']:
                    return src
            if os is not None and 'default' in src and src['default']:
                return src
    return get_default(src_list, 'common', location, scheme)


def get_source(src_list, name=None, os=None, location=None, scheme=None):
    # priority level
    # name-os > name >
    # os-location-default > os-default >
    # common-location-default > common-default
    if name is not None:
        for os in src_list:
            for src in src_list[os]:
                if src['name'] == name:
                    return src

    return get_default(src_list, os, location, scheme)
